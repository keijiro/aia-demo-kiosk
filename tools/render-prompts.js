// Build-time prompt-log pre-renderer (run with JavaScriptCore, no Node needed):
//
//   osascript -l JavaScript tools/render-prompts.js DriftMayhem/Prompts
//
// For the given prompts directory it converts every *.md to a pre-rendered
// *.html fragment (with the local Path / Task ID metadata stripped) using the
// vendored marked, then writes index.json listing the *.html filenames.
// At view time shared/prompt-log.js just fetches the .html — no client-side
// markdown parsing. Re-run this whenever the source logs change.
ObjC.import('Foundation');

function read(p) {
  return $.NSString.stringWithContentsOfFileEncodingError($(p), $.NSUTF8StringEncoding, null).js;
}
function write(p, s) {
  $(s).writeToFileAtomicallyEncodingError($(p), true, $.NSUTF8StringEncoding, null);
}
function listMd(dir) {
  var arr = $.NSFileManager.defaultManager.contentsOfDirectoryAtPathError($(dir), null);
  var out = [];
  for (var i = 0; i < arr.count; i++) {
    var f = arr.objectAtIndex(i).js;
    if (f.slice(-3) === '.md') out.push(f);
  }
  return out;
}

function stripMeta(md) {
  return md.replace(/^- \*\*(Path|Task ID):\*\*.*\n?/gm, '');
}

function run(argv) {
  var dir = argv[0];
  if (!dir) { console.log('usage: render-prompts.js <promptsDir>'); return; }
  dir = dir.replace(/\/$/, '');

  (0, eval)(read('tools/marked.min.js'));
  var marked = globalThis.marked;
  if (!marked || typeof marked.parse !== 'function') { console.log('ERROR: marked not loaded'); return; }

  var files = listMd(dir).sort();
  var htmlNames = [];
  files.forEach(function (f) {
    var html = marked.parse(stripMeta(read(dir + '/' + f)));
    var out = f.replace(/\.md$/, '.html');
    write(dir + '/' + out, html);
    htmlNames.push(out);
    console.log('rendered ' + out);
  });
  write(dir + '/index.json', JSON.stringify(htmlNames, null, 2));
  console.log('wrote index.json (' + htmlNames.length + ' entries) in ' + dir);
}
