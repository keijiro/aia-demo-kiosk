# Listing Current Implementation TIPS Contents

- **Date:** 2026-05-01 22:12
- **Task ID:** `5dcde7de-e0e6-40f0-8932-1ab34080acd9`
- **Messages:** 2

---

## 🧑 User

Please list the contents currently displayed as TIPS in the implementation.

## 🤖 Assistant

The following is the content currently defined in the `TIPS` array in `Assets/Scripts/CombatManager.cs`.

1.  **"Ska" (?) blocks cannot be matched. Shatter or Blast them.**
2.  **Shattering an elemental block drops a "Ska" block from above.**
3.  **Shattering or Blasting a "Ska" block drops an elemental block from above.**
4.  **If stuck, focus on shattering "Ska" blocks to find new matches.**
5.  **Match Shields to block incoming physical attacks.**
6.  **Magic matches hit the entire enemy party.**
7.  **Shields cannot exceed your Max HP.**
8.  **Shields cannot block enemy magic attacks.**
9.  **A Key is needed for chests, but you can only carry one.**
10. **Match Gems to gain EXP.**
11. **Matching Heal blocks at full HP grants EXP.**
12. **Matching Keys while holding one grants EXP.**
13. **Enemies in the back row attack more slowly.**
14. **Blasting "Ska" blocks near your matches slightly increases their power.**
<details>
<summary>🔧 Tool: Unity.Grep (CoreAgent)</summary>

**引数**

```json
{
  "args": "-i \"Tips\""
}
```

**結果**

```
Assets/Scripts/CombatManager.cs
94:    private static readonly string[] TIPS = new string[]
795:        if (nextTipIndex >= TIPS.Length) yield break;
798:        string currentTip = TIPS[nextTipIndex];

```

</details>

<details>
<summary>🔧 Tool: Unity.GetFileContent (CoreAgent)</summary>

**引数**

```json
{
  "endLine": 110,
  "filePath": "Assets/Scripts/CombatManager.cs",
  "startLine": 90
}
```

**結果**

```
90:     private VisualElement tipIcon;
91:     private VisualElement dialogueBox;
92:     private Label treasureMessage;
93: 
94:     private static readonly string[] TIPS = new string[]
95:     {
96:         "\"Ska\" (?) blocks cannot be matched. Shatter or Blast them.",
97:         "Shattering an elemental block drops a \"Ska\" block from above.",
98:         "Shattering or Blasting a \"Ska\" block drops an elemental block from above.",
99:         "If stuck, focus on shattering \"Ska\" blocks to find new matches.",
100:         "Match Shields to block incoming physical attacks.",
101:         "Magic matches hit the entire enemy party.",
102:         "Shields cannot exceed your Max HP.",
103:         "Shields cannot block enemy magic attacks.",
104:         "A Key is needed for chests, but you can only carry one.",
105:         "Match Gems to gain EXP.",
106:         "Matching Heal blocks at full HP grants EXP.",
107:         "Matching Keys while holding one grants EXP.",
108:         "Enemies in the back row attack more slowly.",
109:         "Blasting \"Ska\" blocks near your matches slightly increases their power."
110:     };

```

</details>