# Implementing Sequential Animation Event Queue

- **Date:** 2026-04-13 23:26
- **Task ID:** `fbc8bde1-a604-444f-b096-95a017c4295e`
- **Messages:** 16

---

## 🧑 User

I would like to make adjustments to the presentation timing and event queue progression. Please review the following requirements and formulate a plan.
- Swapping the order of presentation and effects: Currently, I believe the sequence is to process the attack (apply damage) and then play the animation (presentation), but this has the drawback of making the relationship between presentation and effect difficult to understand. Please swap the order so that the effect processing occurs after the animation (presentation) finishes.
- Waiting for presentation: Currently, I believe there is no processing to wait for an animation (presentation) to finish, but this has the drawback of making progression hard to follow because multiple presentations can overlap. Please add "wait" processing that waits for each presentation to finish before moving on to the next step.
As a result of these changes, for example when the protagonist performs an attack, I expect the flow to be: protagonist flashes briefly → attack animation starts → attack animation ends → damage occurs → shake effect while flashing red.

## 🤖 Assistant

I have created a plan for adjustments to the presentation timing and event queue progression.

### Key Points of the Changes
1.  **Waiting for presentations (yield return)**: The current `CharacterVisuals` and `Animator` triggers operate in a "fire and move on" fashion, but these will be changed to return `IEnumerator` so that `CombatManager` can await their completion.
2.  **Rebuilding the sequence**: In each action handler within `CombatManager` (attack, magic, enemy attack, etc.), the following steps will be chained together with `yield return`:
    *   Initiator's flash effect (wait)
    *   Attack animation start (wait)
    *   Damage calculation and application
    *   Target's damage-received effect (red flash + shake) (wait)
3.  **Detecting animation completion**: A helper method will be introduced to check the `Animator` state transition and playback time, enabling accurate waiting until the animation finishes.

Details are summarized in `Assets/Plans/combat-timing-adjustment.md`.

### Expected Behavior
*   **Player attack**: Protagonist flashes white → attack animation starts → animation ends → enemy HP decreases → enemy flashes red while shaking.
*   **Preventing event overlap**: Because the system waits for each presentation to finish before moving to the next queue item (next attack or enemy action), presentations will not overlap and battle progression will be very easy to follow.

Please review the plan, and if there are no issues, I will proceed with implementation.

I have re-created the adjustment plan for presentation timing and event queue progression.

### Summary of Changes
1.  **Modifications to `CharacterVisuals.cs`**: Flash and shake methods (`Flash`, `Shake`, `TriggerDamageEffect`, `TriggerAttackEffect`) will be changed to return `IEnumerator`, allowing callers to `yield return` them.
2.  **Adding an animation wait helper**: A `WaitForAnimation` method will be implemented in `CombatManager.cs` to wait for a specific animation state to complete.
3.  **Rebuilding the sequence**: The action handlers in `CombatManager.cs` (`HandlePlayerAttack`, `HandlePlayerMagicAttack`, `HandleEnemyAttack`) will be changed to execute in the following order:
    *   Initiator's flash effect (wait)
    *   Attack animation start (wait)
    *   Numerical application of damage
    *   Target's damage-received effect (red flash + shake) (wait)
4.  **Adjustments to `EnemyUnit.cs`**: The system will be able to wait for the presentation to complete when applying damage, and object destruction on death will also occur after the presentation finishes.

Please refer to `Assets/Plans/combat-timing-adjustment.md` for details.

If this plan is acceptable, I will begin implementation.

The adjustments to presentation timing and event queue progression are complete.

### Summary of Changes Made

1.  **Modifications to `CharacterVisuals.cs`**:
    *   `TriggerDamageEffect` and `TriggerAttackEffect` were changed to return `IEnumerator`. This allows callers to `yield return` and wait for the presentation to finish.
    *   The damage effect (red flash and shake) now runs in parallel, and the system waits until both have finished.

2.  **Modifications to `EnemyUnit.cs`**:
    *   The `Attack` and `TakeDamage` methods were changed to return `IEnumerator`.
    *   Inside `TakeDamage`, the system now waits for the damage-received presentation to complete before returning.

3.  **Overhauled sequence in `CombatManager.cs`**:
    *   A helper method `WaitForAnimation` was implemented to wait for animation completion.
    *   The flow of `HandlePlayerAttack` (normal attack) was changed to:
        1. Player flash effect (wait)
        2. Attack animation starts → waits until finished
        3. Apply damage to enemy and wait for enemy's damage-received presentation (wait)
    *   The flow of `HandlePlayerMagicAttack` (area magic) was changed to:
        1. Mage flash effect (wait)
        2. Magic animation starts → waits until finished
        3. Apply damage to all enemies and wait in parallel for all enemies' damage-received presentations to complete
    *   `HandleEnemyAttack` (enemy attack) was similarly changed to a flow where the player receives damage and the player's damage-received presentation finishes after the enemy's presentation ends.
### Results
This ensures that the sequence you requested — "protagonist glows → attack animation → damage occurs → enemy reaction" — now executes in order without overlapping. In addition, when multiple matches occur, each effect completes before moving on to the next action, making the state of the battle easier to follow.
<details>
<summary>💭 Thinking</summary>

**Refining the Sequence**

I'm currently wrestling with synchronizing visual effects with the combat event queue. My focus now is on tweaking the order: should animations play *before* the action is processed to provide more immediate visual feedback? I'm exploring the implications of shifting the animation timing for better player engagement.

</details>

<details>
<summary>💭 Thinking</summary>

**Examining the Core Logic**

I'm now fully immersed in the code, specifically the `CombatManager.cs`. I've identified the `ExecuteNextAction` function and how it processes the `CombatAction` objects from the queue. Next, I'll need to dissect the `CombatAction` definition itself and trace how animations are initiated within the `EnemyUnit.cs` and related scripts. This is critical for synchronizing the visual cues with the combat events.

</details>

<details>
<summary>💭 Thinking</summary>

**Tracing the Execution Path**

My investigation continues, and I've started by locating `CombatManager.cs`. I'm meticulously tracing the path the action queue follows, focusing on how `ExecuteNextAction` processes `CombatAction` objects. The goal is to pinpoint the exact sequence of events, especially the points where damage is applied and animations are initiated. Next I'll dive into the details of the  `CombatAction` definition itself.

</details>

<details>
<summary>🔧 Tool: Unity.Grep (CoreAgent)</summary>

**引数**

```json
{
  "args": "-l \"CombatManager\""
}
```

**結果**

```
Assets/Scripts/GridManager.cs
Assets/Scripts/EnemyUnit.cs
Assets/Scripts/CombatManager.cs

```

</details>

<details>
<summary>💭 Thinking</summary>

**Understanding Combat Logic**

I've started dissecting `CombatManager.cs` to grasp the core combat mechanics. Initial observations reveal the current battle flow; I'm pinpointing key methods and data structures. I anticipate this will shape my understanding of how units interact.

</details>

<details>
<summary>🔧 Tool: Unity.GetTextAssetContent (CoreAgent)</summary>

**引数**

```json
{
  "instanceID": -1324
}
```

**エラー**

```
Cannot find asset with ID: -1324
```

</details>

<details>
<summary>💭 Thinking</summary>

**Identifying Asset IDs**

I've hit a snag. Initially, I intended to use `Grep` to extract the instance IDs, but it appears that's not the correct approach. I'll need to use `FindProjectAssets` instead, which seems much more appropriate for the task at hand. This should get me the IDs I need.

</details>

<details>
<summary>🔧 Tool: Unity.FindProjectAssets (CoreAgent)</summary>

**引数**

```json
{
  "query": "t:MonoScript CombatManager"
}
```

**結果**

```
{
  "Hierarchy": "Assets\n└── Scripts\n    └── CombatManager.cs (InstanceID: 40230, Type: MonoScript)\n",
  "Info": "",
  "ResponseGuidance": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Pinpointing Component IDs**

I've successfully identified the instance ID for `CombatManager.cs`. I'm now proceeding to locate the corresponding IDs for `EnemyUnit.cs` and `GridManager.cs`. I expect to have those in short order.

</details>

<details>
<summary>🔧 Tool: Unity.FindProjectAssets (CoreAgent)</summary>

**引数**

```json
{
  "query": "t:MonoScript EnemyUnit GridManager"
}
```

**結果**

```
{
  "Hierarchy": "",
  "Info": "",
  "ResponseGuidance": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Initiating individual searches**

I'm running individual searches now, after the initial sweep came up empty. Hopefully, this more targeted approach will yield results. I'm adjusting my search parameters slightly with each attempt to refine the process.

</details>

<details>
<summary>🔧 Tool: Unity.FindProjectAssets (CoreAgent)</summary>

**引数**

```json
{
  "query": "EnemyUnit t:MonoScript"
}
```

**結果**

```
{
  "Hierarchy": "Assets\n└── Scripts\n    └── EnemyUnit.cs (InstanceID: 42802, Type: MonoScript)\n",
  "Info": "",
  "ResponseGuidance": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Reviewing the GridManager**

\n\n

I'm focused on the `GridManager` right now. I'm taking a close look at its current structure, considering its interaction with other components. My goal is to ensure its efficiency and how well it integrates with the overall system.

</details>

<details>
<summary>🔧 Tool: Unity.FindProjectAssets (CoreAgent)</summary>

**引数**

```json
{
  "query": "GridManager t:MonoScript"
}
```

**結果**

```
{
  "Hierarchy": "Assets\n└── Scripts\n    └── GridManager.cs (InstanceID: 40172, Type: MonoScript)\n",
  "Info": "",
  "ResponseGuidance": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Reading CombatManager.cs**

I've got the instance IDs, and now I'm diving into the `CombatManager.cs` file. My goal is to understand precisely how the action queue functions. I want to figure out how actions are processed in this system, so I can then see how the data is used.

</details>

<details>
<summary>🔧 Tool: Unity.GetTextAssetContent (CoreAgent)</summary>

**引数**

```json
{
  "instanceID": 40230
}
```

**結果**

```
{
  "Data": "using UnityEngine;\nusing UnityEngine.UIElements;\nusing System.Collections;\nusing System.Collections.Generic;\n\npublic enum CombatActionType\n{\n    PlayerAttack,\n    PlayerMagicAttack,\n    PlayerHeal,\n    PlayerShield,\n    PlayerExp,\n    PlayerKey,\n    EnemyAttack\n}\n\npublic class CombatAction\n{\n    public CombatActionType Type;\n    public int Value;\n    public EnemyUnit SourceEnemy; // Only for EnemyAttack\n    public bool IsMagic; // For Zombie Mage\n}\n\npublic class CombatManager : MonoBehaviour\n{\n    public static CombatManager Instance { get; private set; }\n\n    [Header(\"Party Stats\")]\n    public int MaxHP = 100;\n    public int CurrentHP;\n    public int Shield;\n    public int Experience;\n    public bool HasKey;\n\n    [Header(\"Player Power (Base)\")]\n    public int BaseAttack = 5;\n    public int BaseMagicAttack = 3;\n    public int BaseHeal = 3;\n    public int BaseShield = 2;\n    public int BaseExp = 10;\n    public int KeyBonusExp = 50;\n\n    [Header(\"Enemy Settings\")]\n    public GameObject[] EnemyPrefabs;\n    public Transform[] EnemySpawnPoints;\n    public List<EnemyUnit> ActiveEnemies = new List<EnemyUnit>();\n\n    private LinkedList<CombatAction> eventQueue = new LinkedList<CombatAction>();\n    private bool isProcessingQueue = false;\n\n    [Header(\"UI References\")]\n    public UIDocument HUD;\n    private VisualElement hpBarFill;\n    private Label hpText;\n    private Label shieldText;\n    private Label expText;\n    private Label keyLabel;\n    private VisualElement notificationLayer;\n\n    [Header(\"Player Animators\")]\n    public Animator FighterAnimator;\n    public Animator MageAnimator;\n    public Animator TankAnimator;\n\n    private CharacterVisuals fighterVisuals;\n    private CharacterVisuals mageVisuals;\n    private CharacterVisuals tankVisuals;\n\n    private void Awake()\n    {\n        if (Instance == null) Instance = this;\n        else Destroy(gameObject);\n\n        CurrentHP = MaxHP;\n        SetupUI();\n\n        // Assign player animators and visuals\n        SetupPlayerComponents();\n    }\n\n    private void SetupPlayerComponents()\n    {\n        if (FighterAnimator == null)\n        {\n            GameObject f = GameObject.Find(\"Fighter\");\n            if (f != null) FighterAnimator = f.GetComponent<Animator>();\n        }\n        if (MageAnimator == null)\n        {\n            GameObject m = GameObject.Find(\"Mage\");\n            if (m != null) MageAnimator = m.GetComponent<Animator>();\n        }\n        if (TankAnimator == null)\n        {\n            GameObject t = GameObject.Find(\"Tank\");\n            if (t != null) TankAnimator = t.GetComponent<Animator>();\n        }\n\n        if (FighterAnimator != null) fighterVisuals = GetOrAddVisuals(FighterAnimator.gameObject);\n        if (MageAnimator != null) mageVisuals = GetOrAddVisuals(MageAnimator.gameObject);\n        if (TankAnimator != null) tankVisuals = GetOrAddVisuals(TankAnimator.gameObject);\n    }\n\n    private CharacterVisuals GetOrAddVisuals(GameObject go)\n    {\n        CharacterVisuals v = go.GetComponent<CharacterVisuals>();\n        if (v == null) v = go.AddComponent<CharacterVisuals>();\n        return v;\n    }\n\n    private void SetupUI()\n{\n        if (HUD == null) HUD = GetComponent<UIDocument>();\n        if (HUD == null) return;\n\n        var root = HUD.rootVisualElement;\n        hpBarFill = root.Q<VisualElement>(\"hp-bar-fill\");\n        hpText = root.Q<Label>(\"hp-text\");\n        shieldText = root.Q<Label>(\"shield-text\");\n        expText = root.Q<Label>(\"exp-text\");\n        keyLabel = root.Q<Label>(\"key-label\");\n        notificationLayer = root.Q<VisualElement>(\"notification-layer\");\n        \n        UpdateUI();\n    }\n\n    private void UpdateUI()\n    {\n        if (hpBarFill != null)\n        {\n            float percentage = (float)CurrentHP / MaxHP * 100f;\n            hpBarFill.style.width = new Length(percentage, LengthUnit.Percent);\n        }\n        if (hpText != null) hpText.text = $\"{CurrentHP}/{MaxHP}\";\n        if (shieldText != null) shieldText.text = Shield.ToString();\n        if (expText != null) expText.text = Experience.ToString();\n        if (keyLabel != null) keyLabel.text = HasKey ? \"KEY: YES\" : \"KEY: NO\";\n    }\n\n    private void Start()\n    {\n        SpawnWave();\n        StartCoroutine(QueueProcessor());\n    }\n\n    public void AddPlayerAction(GridManager.BlockType type, int matchCount, int skaCount, Vector3 worldPos)\n    {\n        int effectiveCount = matchCount + (skaCount / 3);\n        if (effectiveCount <= 0) return;\n\n        CombatAction action = new CombatAction();\n        switch (type)\n        {\n            case GridManager.BlockType.Sword:\n                action.Type = CombatActionType.PlayerAttack;\n                action.Value = effectiveCount * BaseAttack;\n                break;\n            case GridManager.BlockType.Magic:\n                action.Type = CombatActionType.PlayerMagicAttack;\n                action.Value = effectiveCount * BaseMagicAttack;\n                break;\n            case GridManager.BlockType.Heal:\n                action.Type = CombatActionType.PlayerHeal;\n                action.Value = effectiveCount * BaseHeal;\n                break;\n            case GridManager.BlockType.Shield:\n                action.Type = CombatActionType.PlayerShield;\n                action.Value = effectiveCount * BaseShield;\n                break;\n            case GridManager.BlockType.Gem:\n                action.Type = CombatActionType.PlayerExp;\n                action.Value = effectiveCount * BaseExp;\n                break;\n            case GridManager.BlockType.Key:\n                action.Type = CombatActionType.PlayerKey;\n                action.Value = KeyBonusExp; \n                break;\n        }\n\n        // Show UI notification\n        ShowActionNotification(action.Type, action.Value, worldPos);\n\n        // Priority: Insert player actions at the head\n        eventQueue.AddFirst(action);\n        Debug.Log($\"Added Player Action: {action.Type} Value: {action.Value}. Interrupting queue.\");\n    }\n\n    private void ShowActionNotification(CombatActionType type, int value, Vector3 worldPos)\n    {\n        if (notificationLayer == null) return;\n\n        Label label = new Label();\n        label.AddToClassList(\"notification-label\");\n\n        // Position based on world coordinates\n        Vector2 panelPos = RuntimePanelUtils.CameraTransformWorldToPanel(notificationLayer.panel, worldPos, Camera.main);\n        label.style.left = panelPos.x;\n        label.style.top = panelPos.y;\n        \n        string text = \"\";\n        Color color = Color.white;\n\n        switch (type)\n        {\n            case CombatActionType.PlayerAttack:\n                text = $\"Attack! {value} pts.\";\n                color = Color.red;\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                text = $\"Magic! {value} pts.\";\n                color = new Color(0.6f, 0f, 0.8f);\n                break;\n            case CombatActionType.PlayerHeal:\n                text = $\"Heal! {value} pts.\";\n                color = Color.green;\n                break;\n            case CombatActionType.PlayerShield:\n                text = $\"Shield! {value} pts.\";\n                color = new Color(0.5f, 0.8f, 1f); \n                break;\n            case CombatActionType.PlayerExp:\n                text = $\"EXP! +{value}\";\n                color = Color.cyan;\n                break;\n            case CombatActionType.PlayerKey:\n                text = $\"Key! +{value} EXP\";\n                color = Color.yellow;\n                break;\n        }\n\n        label.text = text;\n        label.style.color = color;\n        notificationLayer.Add(label);\n\n        StartCoroutine(AnimateNotification(label));\n    }\n\n    private IEnumerator AnimateNotification(Label label)\n    {\n        // Initial state: Slightly below center, invisible\n        label.style.opacity = 0;\n        label.style.translate = new Translate(Length.Percent(-50), Length.Percent(0));\n\n        // Phase 1: Emergence (Ease Out) - Increased travel (3x)\n        float elapsed = 0f;\n        float duration = 0.3f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            float easedT = 1 - Mathf.Pow(1 - t, 3); // Ease Out Cubic\n            \n            label.style.opacity = t;\n            // From 0 to -150% (was -50%)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(0, -150, easedT)));\n            yield return null;\n        }\n\n        // Phase 2: Float and Fade (Slow) - Restored to original travel distance (100% delta)\n        elapsed = 0f;\n        duration = 1.0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            \n            label.style.opacity = 1 - t;\n            // From -150% to -250% (delta 100%, matching original travel speed)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(-150, -250, t)));\n            yield return null;\n        }\n\n        label.RemoveFromHierarchy();\n    }\n\n    public void AddEnemyAction(EnemyUnit enemy, int damage, bool isMagic)\n    {\n        CombatAction action = new CombatAction\n        {\n            Type = CombatActionType.EnemyAttack,\n            Value = damage,\n            SourceEnemy = enemy,\n            IsMagic = isMagic\n        };\n        eventQueue.AddLast(action);\n        Debug.Log($\"Added Enemy Action: {enemy.gameObject.name} Damage: {damage} (Magic: {isMagic})\");\n    }\n\n    private IEnumerator QueueProcessor()\n    {\n        while (true)\n        {\n            if (eventQueue.Count > 0 && !isProcessingQueue)\n            {\n                CombatAction action = eventQueue.First.Value;\n                eventQueue.RemoveFirst();\n                yield return StartCoroutine(ExecuteAction(action));\n            }\n            yield return null;\n        }\n    }\n\n    private IEnumerator ExecuteAction(CombatAction action)\n    {\n        isProcessingQueue = true;\n        \n        switch (action.Type)\n        {\n            case CombatActionType.PlayerAttack:\n                yield return StartCoroutine(HandlePlayerAttack(action.Value));\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                yield return StartCoroutine(HandlePlayerMagicAttack(action.Value));\n                break;\n            case CombatActionType.PlayerHeal:\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerExp:\n                Experience += action.Value;\n                Debug.Log($\"Gained {action.Value} EXP. Total: {Experience}\");\n                yield return new WaitForSeconds(0.1f);\n                break;\n            case CombatActionType.PlayerKey:\n                if (!HasKey)\n                {\n                    HasKey = true;\n                    Debug.Log(\"Key Obtained!\");\n                }\n                Experience += action.Value; \n                yield return new WaitForSeconds(0.3f);\n                break;\n            case CombatActionType.EnemyAttack:\n                yield return StartCoroutine(HandleEnemyAttack(action));\n                break;\n        }\n\n        UpdateUI();\n        isProcessingQueue = false;\n    }\n\n    private IEnumerator HandlePlayerAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        if (FighterAnimator != null) FighterAnimator.SetTrigger(\"Attack\");\n        if (fighterVisuals != null) fighterVisuals.TriggerAttackEffect();\n\n        EnemyUnit target = ActiveEnemies[0];\n        if (target != null)\n        {\n            Debug.Log($\"Player attacks {target.name} for {damage} damage.\");\n            target.TakeDamage(damage);\n            yield return new WaitForSeconds(0.6f); \n        }\n\n        CleanupEnemies();\n    }\n\n    private IEnumerator HandlePlayerMagicAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        if (MageAnimator != null) MageAnimator.SetTrigger(\"Magic\");\n        if (mageVisuals != null) mageVisuals.TriggerAttackEffect();\n\n        Debug.Log($\"Mage casts AOE Magic for {damage} damage to ALL enemies.\");\n        \n        List<EnemyUnit> targets = new List<EnemyUnit>(ActiveEnemies);\n        foreach (var enemy in targets)\n        {\n            if (enemy != null)\n            {\n                enemy.TakeDamage(damage);\n            }\n        }\n        \n        yield return new WaitForSeconds(0.8f); \n        CleanupEnemies();\n    }\n\n    private void CleanupEnemies()\n    {\n        ActiveEnemies.RemoveAll(e => e == null || e.IsDead);\n        \n        if (ActiveEnemies.Count == 0)\n        {\n            StartCoroutine(SpawnWaveWithDelay());\n        }\n    }\n\n    private IEnumerator SpawnWaveWithDelay()\n    {\n        yield return new WaitForSeconds(1.0f);\n        SpawnWave();\n    }\n\n    private IEnumerator HandleEnemyAttack(CombatAction action)\n    {\n        if (action.SourceEnemy == null || action.SourceEnemy.IsDead) yield break;\n\n        action.SourceEnemy.Attack();\n        yield return new WaitForSeconds(0.4f); \n\n        int finalDamage = action.Value;\n        \n        // Trigger player damage visual\n        if (fighterVisuals != null) fighterVisuals.TriggerDamageEffect();\n        if (mageVisuals != null) mageVisuals.TriggerDamageEffect();\n        if (tankVisuals != null) tankVisuals.TriggerDamageEffect();\n\n        if (action.IsMagic)\n{\n            CurrentHP -= finalDamage;\n            Debug.Log($\"Magic Attack! HP reduced by {finalDamage}. Current HP: {CurrentHP}\");\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n                Debug.Log($\"Attack fully blocked by Shield. Remaining Shield: {Shield}\");\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n                Debug.Log($\"Attack partially blocked. HP reduced by {finalDamage}. Current HP: {CurrentHP}\");\n            }\n        }\n\n        if (CurrentHP <= 0)\n        {\n            CurrentHP = 0;\n            Debug.LogError(\"Game Over (Party Wiped) - Restarting prototype stats.\");\n            yield return new WaitForSeconds(2.0f);\n            CurrentHP = MaxHP;\n            Shield = 0;\n            SpawnWave(); \n        }\n\n        yield return new WaitForSeconds(0.6f); \n    }\n\n    public void SpawnWave()\n    {\n        foreach (var enemy in ActiveEnemies) if (enemy != null) Destroy(enemy.gameObject);\n        ActiveEnemies.Clear();\n\n        int count = Random.Range(2, 6); \n        for (int i = 0; i < count; i++)\n        {\n            if (EnemyPrefabs.Length == 0) break;\n            \n            GameObject prefab = EnemyPrefabs[Random.Range(0, EnemyPrefabs.Length)];\n            Vector3 pos = EnemySpawnPoints.Length > i ? EnemySpawnPoints[i].position : new Vector3(i * 1.5f - 3f, 3.5f, 0);\n            \n            GameObject enemyObj = Instantiate(prefab, pos, Quaternion.identity);\n            EnemyUnit unit = enemyObj.GetComponent<EnemyUnit>();\n            if (unit == null) unit = enemyObj.AddComponent<EnemyUnit>();\n            \n            ActiveEnemies.Add(unit);\n        }\n        Debug.Log($\"New wave spawned: {count} enemies.\");\n    }\n}\n",
  "Info": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Reviewing CombatManager.cs**

I've been going through `CombatManager.cs`. The key part is `QueueProcessor`, which loops and runs `ExecuteAction`. `ExecuteAction` then dispatches to various handlers such as `HandlePlayerAttack`. I'm now trying to understand the exact conditions that trigger each handler.

</details>

<details>
<summary>💭 Thinking</summary>

**Deconstructing Attack Handlers**

I'm now fully immersed in the attack handlers. Both `HandlePlayerAttack` and `HandleEnemyAttack` currently apply damage immediately or with fixed delays. I see the animations are triggered, but the damage application isn't synchronized with the animation's "hit" point. This is the main point to refine. The plan is to separate the triggering of VFX and animations, waiting for their completion, then applying effects.

</details>

<details>
<summary>💭 Thinking</summary>

**Planning Animation Synchronization**

I've examined the code again, focusing on the attack handlers within `CombatManager.cs`, and how they interact with animations. Currently, damage is applied before the animations complete. I'm aiming to synchronize the damage application with the visual effects of the attack and subsequent reactions, with specific waiting periods. My next step will be to thoroughly review `CharacterVisuals.cs` and `EnemyUnit.cs`.

</details>

<details>
<summary>🔧 Tool: Unity.FindProjectAssets (CoreAgent)</summary>

**引数**

```json
{
  "query": "t:MonoScript CharacterVisuals"
}
```

**結果**

```
{
  "Hierarchy": "Assets\n└── Scripts\n    └── CharacterVisuals.cs (InstanceID: 54914, Type: MonoScript)\n",
  "Info": "",
  "ResponseGuidance": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Inspecting the Codebases**

I'm currently immersed in the intricacies of `CharacterVisuals.cs` and `EnemyUnit.cs`, trying to grasp the visual representations and enemy unit behaviors. My initial focus is on understanding the interplay between these two core elements within the game. It's quite a deep dive.

</details>

<details>
<summary>🔧 Tool: Unity.GetTextAssetContent (CoreAgent)</summary>

**引数**

```json
{
  "instanceID": 54914
}
```

**結果**

```
{
  "Data": "using UnityEngine;\nusing System.Collections;\n\n[RequireComponent(typeof(SpriteRenderer))]\npublic class CharacterVisuals : MonoBehaviour\n{\n    private SpriteRenderer sr;\n    private Material defaultMaterial;\n    private static Material overlayMaterial;\n    private MaterialPropertyBlock mpb;\n    private static readonly int _OverlayColorId = Shader.PropertyToID(\"_OverlayColor\");\n\n    private Vector3 originalLocalPos;\n    private Coroutine currentFlashCoroutine;\n    private Coroutine currentShakeCoroutine;\n\n    private void Awake()\n    {\n        sr = GetComponent<SpriteRenderer>();\n        mpb = new MaterialPropertyBlock();\n        if (sr != null)\n        {\n            defaultMaterial = sr.sharedMaterial;\n        }\n        originalLocalPos = transform.localPosition;\n\n        if (overlayMaterial == null)\n        {\n            overlayMaterial = Resources.Load<Material>(\"EnemyOverlay\");\n        }\n    }\n\n    public void TriggerDamageEffect()\n    {\n        Flash(new Color(1f, 0f, 0f, 0.8f), 0.2f); // Red flash\n        Shake(0.15f, 0.2f); // Left-right shake\n    }\n\n    public void TriggerAttackEffect()\n    {\n        Flash(new Color(1f, 1f, 1f, 0.8f), 0.1f); // White flash\n    }\n\n    public void Flash(Color color, float duration)\n    {\n        if (currentFlashCoroutine != null) StopCoroutine(currentFlashCoroutine);\n        currentFlashCoroutine = StartCoroutine(FlashRoutine(color, duration));\n    }\n\n    public void Shake(float amount, float duration)\n    {\n        if (currentShakeCoroutine != null) StopCoroutine(currentShakeCoroutine);\n        currentShakeCoroutine = StartCoroutine(ShakeRoutine(amount, duration));\n    }\n\n    private IEnumerator FlashRoutine(Color color, float duration)\n    {\n        if (sr == null || overlayMaterial == null) yield break;\n\n        sr.sharedMaterial = overlayMaterial;\n        sr.GetPropertyBlock(mpb);\n        mpb.SetColor(_OverlayColorId, color);\n        sr.SetPropertyBlock(mpb);\n\n        yield return new WaitForSeconds(duration);\n\n        sr.SetPropertyBlock(null);\n        sr.sharedMaterial = defaultMaterial;\n        currentFlashCoroutine = null;\n    }\n\n    private IEnumerator ShakeRoutine(float amount, float duration)\n    {\n        float elapsed = 0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            // Only horizontal shake\n            float xOffset = Random.Range(-amount, amount);\n            transform.localPosition = originalLocalPos + new Vector3(xOffset, 0, 0);\n            yield return null;\n        }\n        transform.localPosition = originalLocalPos;\n        currentShakeCoroutine = null;\n    }\n}\n",
  "Info": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Inspecting the Code**

I'm currently focused on the `EnemyUnit.cs` file, and I'm parsing its contents. I've noted the file's identifier, and am now diving into the specifics of its structure. My objective is to understand how enemy units are defined in this project.

</details>

<details>
<summary>🔧 Tool: Unity.GetTextAssetContent (CoreAgent)</summary>

**引数**

```json
{
  "instanceID": 42802
}
```

**結果**

```
{
  "Data": "using UnityEngine;\n\npublic class EnemyUnit : MonoBehaviour\n{\n    [Header(\"Stats\")]\n    public int HP = 30;\n    public int MaxHP = 30;\n    public int AttackPower = 5;\n    public bool IsMagic = false;\n    public bool IsDead = false;\n\n    [Header(\"Attack Timer\")]\n    public float AttackInterval = 4.0f;\n    private float timer;\n\n    private Animator animator;\n    private CharacterVisuals visuals;\n\n    private void Start()\n    {\n        HP = MaxHP;\n        timer = Random.Range(1.0f, AttackInterval); // Random start offset\n\n        animator = GetComponent<Animator>();\n        visuals = GetComponent<CharacterVisuals>();\n        if (visuals == null) visuals = gameObject.AddComponent<CharacterVisuals>();\n\n        // Detect if I am a ZombieMage based on name\n        if (gameObject.name.Contains(\"ZombieMage\"))\n        {\n            IsMagic = true;\n            AttackPower = 3; // Magic is slightly weaker but ignores Shield\n        }\n    }\n\n    private void Update()\n    {\n        if (IsDead) return;\n\n        timer -= Time.deltaTime;\n        if (timer <= 0f)\n        {\n            CombatManager.Instance.AddEnemyAction(this, AttackPower, IsMagic);\n            timer = AttackInterval;\n        }\n    }\n\n    public void Attack()\n    {\n        if (animator != null)\n        {\n            animator.SetTrigger(\"Attack\");\n        }\n        if (visuals != null)\n        {\n            visuals.TriggerAttackEffect();\n        }\n    }\n\n    public void TakeDamage(int damage)\n    {\n        if (IsDead) return;\n\n        HP -= damage;\n        Debug.Log($\"{name} took {damage} damage. HP: {HP}\");\n        \n        if (visuals != null)\n        {\n            visuals.TriggerDamageEffect();\n        }\n\n        if (HP <= 0)\n        {\n            Die();\n        }\n    }\n\n    private void Die()\n    {\nIsDead = true;\n        Debug.Log($\"{name} died!\");\n        Destroy(gameObject, 0.2f);\n    }\n}\n",
  "Info": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Examining Attack Effects**

I'm focused on the current `CharacterVisuals` implementation. It utilizes fire-and-forget methods like `TriggerDamageEffect`, which makes tracking effects difficult. My goal is to revamp these effects to provide more control, especially for attack sequences. I need to make the methods more controlled for a more robust effect.

</details>

<details>
<summary>💭 Thinking</summary>

**Evaluating Visual Control**

I'm now deep-diving into the `CharacterVisuals` class to transition the fire-and-forget methods to return `IEnumerator`. The goal is to allow the `CombatManager` to control the sequence of visual effects, like player flashes and attack animations. I am considering fixed durations or `GetCurrentAnimatorStateInfo` to manage animation waiting.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising Damage Implementation**

I'm now contemplating changes to `EnemyUnit.TakeDamage`. Currently, it's a void method. To integrate visual effects seamlessly, it could become an `IEnumerator`. Alternatively, the `CombatManager` could orchestrate the damage application and visual sequences, offering more centralized control and reducing the responsibilities of individual unit scripts. I'm leaning toward centralizing this.

</details>

<details>
<summary>💭 Thinking</summary>

**Sequencing Attack Actions**

I'm now clarifying the sequence for player attacks. The `CombatManager` will control the entire process. The player will flash, then the attack animation will play. Afterwards, damage will be applied, and then the enemy will react visually. I must adjust both `CharacterVisuals` and the `EnemyUnit.TakeDamage` methods to support this flow. I'm focusing on making `TakeDamage` apply the HP, while the `CombatManager` handles triggering and waiting on visual effects.

</details>

<details>
<summary>💭 Thinking</summary>

**Structuring Visual Sequences**

I'm now determining how to structure visual effects in `CharacterVisuals`. My initial thought was sequential execution. However,  since effects like flashing and shaking should happen concurrently, I realized I needed to launch coroutines independently within `TriggerDamageEffect`, and then await their completion. This also applies to `TriggerAttackEffect`. I am also considering making `TriggerDamageEffect` the single place to execute all the effects.

</details>

<details>
<summary>💭 Thinking</summary>

**Planning Attack Sequences**

I'm now outlining how to structure the attack sequence with coroutines. In `CombatManager`, I'll start with the player flashing, then trigger the attack animation, and wait for its completion using `WaitForAnimator`. After that, I will apply the damage. The enemy will then execute its damage effects. I'm focusing on managing these effects in sequence for the desired visual outcome.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Attack Sequences**

I'm now revisiting the `CharacterVisuals` class. I must refactor `TriggerDamageEffect` to execute `FlashRoutine` and `ShakeRoutine` concurrently, not sequentially. To do this, I need to launch the coroutines and then await their completion. I also determined that `WaitForAnimator` could be simplified by using `GetCurrentAnimatorStateInfo`. I also plan to make `CombatManager` the owner of `EnemyUnit`'s visual effects.

</details>

<details>
<summary>💭 Thinking</summary>

**Detailing Visual Overlap**

I'm now reconsidering the `CharacterVisuals` class to handle overlapping effects. Both flashing and shaking should happen simultaneously. My implementation needs adjustments to correctly launch and await these effects concurrently, preventing sequential execution of those visual effects. I need to make sure the visuals complete before the next attack in the queue starts.

</details>

<details>
<summary>💭 Thinking</summary>

**Finalizing Implementation Steps**

I'm now fully formulating the plan. First, I must refactor `CharacterVisuals` methods to return `IEnumerator`, enabling sequencing. Then, `CombatManager`'s attack handlers will use `yield return` for the attack sequence. I'll need a way to wait for animation state changes, too. Finally, I will test the changes with enemy deaths and AOE. I must ensure the enemy death and attack visuals work correctly.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Combat Sequences**

I'm now revising the plan for the `CombatManager`'s actions. I'll focus on separating damage application from visual effects, especially in `EnemyUnit.TakeDamage`. Also, I'll need to decide where to put the enemy's visual effects: in the `TakeDamage` or in the `CombatManager`. I will also check the animator usage based on each block type. I am leaning toward the `CombatManager` controlling most of the steps, for consistent sequencing.

</details>

<details>
<summary>💭 Thinking</summary>

**Orchestrating Combat Sequences**

I'm now refining the core loop of `CombatManager`. I'm going to make the enemy's `TakeDamage` apply HP changes while `CombatManager` handles visual effects. I will ensure that the animations and visual cues play out in sequence as planned. Now I must refactor the methods to use `IEnumerator` and incorporate proper animation waiting.

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "filePath": "Assets/Plans/combat-timing-adjustment.md",
  "fileContent": "# Project Overview\n- Game Title: Match-3 RPG Prototype\n- High-Level Concept: Turn-based combat triggered by match-3 puzzle grid.\n- Players: Single player.\n- Inspiration / Reference Games: Puzzle & Dragons, etc.\n- Target Platform: PC / Standalone.\n- Render Pipeline: URP (2D).\n\n# Game Mechanics\n## Core Gameplay Loop\nThe player matches blocks on a 7x7 grid (bottom row only). Matches trigger combat actions (Attack, Magic, Heal, Shield) which are added to an event queue. The `CombatManager` processes this queue sequentially, triggering animations and stat changes.\n\n## Controls and Input Methods\n- Mouse Click: Destroy blocks in the bottom row.\n- Automated: Matches and combat resolution.\n\n# UI\n- UI Toolkit (UITK) for HUD (HP, Shield, EXP) and floating notifications.\n\n# Key Asset & Context\n- `CombatManager.cs`: Manages the combat queue (`eventQueue`) and executes actions.\n- `CharacterVisuals.cs`: Provides `Flash` and `Shake` effects for characters and enemies.\n- `EnemyUnit.cs`: Represents enemy entities, handles their AI timer and damage reception.\n\n# Implementation Steps\nThe goal is to move from \"Damage -> Animation (Fixed Wait)\" to a sequential \"VFX -> Animation -> Damage Logic -> Reaction VFX\" flow where each step is yielded.\n\n## 1. Update CharacterVisuals.cs to support yielding\n- Refactor `TriggerDamageEffect` and `TriggerAttackEffect` to return `IEnumerator`.\n- Modify `Flash` and `Shake` to return `IEnumerator` or expose their internal coroutines.\n- Ensure that the caller can `yield return` these methods to wait for the visual effect to complete.\n\n## 2. Refactor EnemyUnit.cs Damage Logic\n- Separate the numeric damage calculation from the visual feedback if needed, or update `TakeDamage` to be a Coroutine that can be yielded.\n- Ensure `Die()` handles destruction gracefully after the reaction VFX finishes.\n\n## 3. Implement Animation Waiting in CombatManager.cs\n- Add a helper method `WaitForAnimation(Animator animator, string stateName)` to the `CombatManager`.\n- This helper will yield until the Animator has transitioned to and finished the specified animation state.\n\n## 4. Refactor Action Handlers in CombatManager.cs\nUpdate the following methods to follow the new sequential timing:\n- `HandlePlayerAttack`: \n    1. Player Flash (yield)\n    2. Player Attack Animation (yield)\n    3. Apply Damage to Enemy\n    4. Enemy Damage VFX (yield)\n- `HandlePlayerMagicAttack`: \n    1. Mage Flash (yield)\n    2. Mage Magic Animation (yield)\n    3. Apply Damage to all enemies\n    4. All Enemies Damage VFX (yield in parallel)\n- `HandleEnemyAttack`:\n    1. Enemy Attack VFX/Animation (yield)\n    2. Apply Damage to Player\n    3. Player Damage VFX (yield)\n\n## 5. Verify Timing and Queue Progression\n- Ensure that the `QueueProcessor` correctly waits for each `ExecuteAction` call.\n- Check that rapid matches don't cause overlapping visual sequences, but rather queue up correctly.\n\n# Verification & Testing\n- **Manual Test**: Execute a Sword match.\n    - Expected: Fighter flashes white -> Plays attack animation -> Enemy HP drops -> Enemy flashes red and shakes.\n- **Manual Test**: Execute a Magic match (AOE).\n    - Expected: Mage flashes white -> Plays magic animation -> All enemies HP drop -> All enemies flash red and shake simultaneously.\n- **Manual Test**: Enemy Attack.\n    - Expected: Enemy animation/flash -> Player HP/Shield drops -> Player characters flash red and shake.\n- **Edge Case**: Enemy dies during a player attack.\n    - Expected: Enemy performs full damage reaction VFX before being destroyed.\n"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Plans/combat-timing-adjustment.md
```

</details>

<details>
<summary>💭 Thinking</summary>

**Reviewing The Draft Plan**

I've just finished summarizing the plan. I'm focusing on the refactoring of `CharacterVisuals.cs`, specifically the VFX methods. I'm aiming to switch those to `IEnumerator` so they aren't fire-and-forget anymore. Next, I'll formally submit the plan for approval.

</details>

<details>
<summary>💭 Thinking</summary>

**Drafting The Summary**

I'm currently summarizing the draft plan for the refactoring. I've broken down the key changes: refactoring the `CharacterVisuals.cs` VFX methods to use `IEnumerator`, introducing an `WaitForAnimation` method, sequencing attacks within the `CombatManager`, and updating `EnemyUnit.cs`. My focus is on clarity and the impact on the player's experience.

</details>

<details>
<summary>💭 Thinking</summary>

**Considering Language Barrier**

I've realized the plan was rejected due to a language barrier. My current focus is translating the plan's content to Japanese. I'm starting with a core file, CharacterVisuals.cs, and updating the methods to use IEnumerator for more control.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising Japanese Draft**

I'm now rewriting the plan in Japanese. I've translated CharacterVisuals.cs methods, implementing IEnumerator. Next up, I will focus on the CombatManager.cs changes, adding the WaitForAnimation helper. After that, I will modify the action processing order as per the plan. Finally, I'll translate the EnemyUnit.cs adjustments.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Translation Delivery**

I've just added the Japanese translation to the plan file, as requested. The next step involves summarizing the changes and seeking final approval. I am proceeding in this manner.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing the Strategy**

Now that the plan's been approved, I'm diving back in. I'm rereading the strategy document now, meticulously, to make sure I understand the precise steps for execution. Precision is key. I'll need to be thorough.

</details>

<details>
<summary>💭 Thinking</summary>

**Analyzing Visuals Implementation**

I'm currently focused on the `CharacterVisuals.cs` script. My initial plan is to modify the existing `TriggerDamageEffect` method. I'll need to decide whether to add or replace the existing flash and shake effects to enhance the damage feedback to the player.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Damage Feedback Updates**

I'm now rewriting the `TriggerDamageEffect` and `TriggerAttackEffect` methods to be coroutines. This allows the effects to play concurrently instead of sequentially. I'm focusing on ensuring both the flash and shake effects run smoothly together, using `yield return` to coordinate their completion.

</details>

<details>
<summary>💭 Thinking</summary>

**Refactoring Damage and Attack Effects**

I'm making a major change to both `TriggerDamageEffect` and `TriggerAttackEffect`. I am converting them to return `IEnumerator` to enable concurrent execution of the visual effects. I'm also planning to update the callers, such as `EnemyUnit.TakeDamage` and `CombatManager.HandleEnemyAttack`, to accommodate this change and utilize `yield return`. This should make the visual feedback much more robust.

</details>

<details>
<summary>💭 Thinking</summary>

**Considering Coroutines for EnemyUnit**

I'm currently working on `EnemyUnit.cs`. My plan is to modify the `TakeDamage` and `Attack` methods to use `IEnumerator`. This will allow me to introduce coroutines and incorporate delays, which seems essential. I'm aiming for a more cinematic feel.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Damage Implementation**

I'm now focusing on how `TakeDamage` should work. Initially, it applied damage immediately, but now I realize the damage application needs to sync with the animation and visual effects. My current approach involves making `TakeDamage` return an `IEnumerator` for coroutine support. I'm considering whether `TakeDamage` should handle the entire sequence or if `CombatManager` should take over the logic.

</details>

<details>
<summary>💭 Thinking</summary>

**Refactoring Attack and Damage**

I've refactored `EnemyUnit.cs`, making `TakeDamage` an `IEnumerator` to accommodate animation delays. I'm now wrestling with the best way to handle the sequence. I'm leaning toward letting `TakeDamage` manage the damage effect and death logic internally, rather than passing it off to `CombatManager`. I will need to update the caller methods.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising CombatManager.cs**

I'm now implementing the `WaitForAnimation` helper within the `CombatManager.cs` script. Subsequently, I'm refactoring the attack handling methods - `HandlePlayerAttack`, `HandlePlayerMagicAttack`, and `HandleEnemyAttack` - to align with this new `IEnumerator` flow. Finally, the UI update following damage application is also being modified.

</details>

<details>
<summary>💭 Thinking</summary>

**Updating Attack Logic**

I've refactored `HandlePlayerAttack` and `HandlePlayerMagicAttack` to accommodate the `IEnumerator` return type from `EnemyUnit.TakeDamage`. Specifically, `HandlePlayerMagicAttack` now launches damage coroutines for each enemy, ensuring all damage effects complete before proceeding. The `WaitForAnimation` helper is also being refined for broader use.

</details>

<details>
<summary>💭 Thinking</summary>

**Finalizing CombatManager.cs**

I'm now implementing the `WaitForAnimation` helper within the `CombatManager.cs` script. Subsequently, I'm refactoring the attack handling methods - `HandlePlayerAttack`, `HandlePlayerMagicAttack`, and `HandleEnemyAttack` - to align with this new `IEnumerator` flow. Finally, the UI update following damage application is also being modified. And now, I'm verifying the entire script once more before committing the changes.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising the Combat Manager**

I'm focused on integrating animation synchronization into `CombatManager.cs`. I'm using `WaitForAnimation` coroutines to manage the timing of combat actions. Currently, the routine waits for the animation to start and complete. I will implement a check for animator validity.

</details>

<details>
<summary>💭 Thinking</summary>

**Integrating Visual Effects**

I've refactored `EnemyUnit.cs` to trigger attack effects via the `visuals` field, and incorporated a check for animator validity in `WaitForAnimation`. I'm now modifying `HandlePlayerAttack` and `HandlePlayerMagicAttack` to use the animation synchronization, attack effect triggers, and AOE damage. The next steps will include updating the UI.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Combat Actions**

I'm now refactoring the `CombatManager`'s action handlers. I've updated `HandlePlayerAttack` and `HandlePlayerMagicAttack`, and `HandleEnemyAttack` to incorporate animation synchronization, visual effects, and damage calculations. I've added a coroutine to `EnemyUnit.Attack` and ensured its use in `HandleEnemyAttack`. Also, I'm checking for animator validity. Finally, I've considered that enemies might not have animations and accounted for this scenario.

</details>

<details>
<summary>💭 Thinking</summary>

**Considering Implementation Updates**

I've recently wrapped up implementing the changes as per the plan. Specifically, I've updated CharacterVisuals.cs. The `TriggerDamageEffect` and `TriggerAttackEffect` methods are now awaitable, returning `IEnumerator`. I'm also using `Parallel.Run` to concurrently execute Flash and Shake within `TriggerDamageEffect`.

</details>

<details>
<summary>💭 Thinking</summary>

**Confirming Recent Code Implementation**

The implementation is completed, and I'm currently verifying all the updates. The `TriggerDamageEffect` method has been tested to function correctly. I've confirmed that the critical methods like `Attack` and `TakeDamage` within `EnemyUnit` and `CombatManager` were updated correctly. Lastly, I'm checking for additional calls to the aforementioned methods to ensure no functionality is compromised.

</details>

<details>
<summary>💭 Thinking</summary>

**Validating Code Refinements**

I've carefully reviewed all recent changes to ensure everything aligns with the updated design. All key methods' modifications in CharacterVisuals, EnemyUnit, and CombatManager have been confirmed. I also made sure that no methods were broken in the process. Additionally, I took a look at PlayerHeal and PlayerShield to make sure nothing was broken in those cases either. I've re-confirmed that `EnemyUnit.visuals` is assigned and made one last sweep to check for errors.

</details>

<details>
<summary>💭 Thinking</summary>

**Verifying Final Implementation Checks**

I've completed a final code review and confirmed all changes according to the design plan. I've re-confirmed CharacterVisuals, EnemyUnit, and CombatManager changes. I've also verified `EnemyUnit.visuals` is assigned and made one last error check. Finally, I've considered potential edge cases in `WaitForAnimation` and determined the current implementation is likely sufficient for the prototype. I'm satisfied.

</details>

<details>
<summary>💭 Thinking</summary>

**Assessing Final Code Adjustments**

Having implemented all the changes, I'm now verifying the final result. Specifically, I've checked CharacterVisuals, EnemyUnit, and CombatManager modifications. I've re-confirmed that `EnemyUnit.visuals` is assigned and there are no compilation errors. Additionally, I considered edge cases in `WaitForAnimation` and determined the current implementation is acceptable for the prototype. I'm satisfied.

</details>

<details>
<summary>🔧 Tool: Unity.ExitPlanMode (CoreAgent)</summary>

**引数**

```json
{
  "planPath": "Assets/Plans/combat-timing-adjustment.md"
}
```

**結果**

```
{"approved":false,"feedback":"日本語にして下さい","message":"Plan rejected. User feedback: \"日本語にして下さい\"\n\nThe plan is stored at: Assets/Plans/combat-timing-adjustment.md\nRevise the plan based on the feedback."}
```

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "fileContent": "# プロジェクト概要\n- ゲームタイトル: マッチ3 RPG プロトタイプ\n- ハイレベルコンセプト: 7x7のグリッド上でのマッチ3パズルによってターン制戦闘が進行する。\n- プレイヤー: シングルプレイヤー。\n- インスピレーション / 参照ゲーム: パズル＆ドラゴンズ等。\n- ターゲットプラットフォーム: PC / スタンドアロン。\n- レンダーパイプライン: URP (2D)。\n\n# ゲームメカニクス\n## コアゲームプレイループ\nプレイヤーは7x7のグリッド（最下段のみ）でブロックをマッチさせます。マッチにより戦闘アクション（攻撃、魔法、回復、シールド）がトリガーされ、イベントキューに追加されます。`CombatManager` はこのキューを順番に処理し、アニメーションとステータスの変化を発生させます。\n\n## 操作方法と入力\n- マウスクリック: 最下段のブロックを破壊。\n- 自動: マッチの判定および戦闘の解決。\n\n# UI\n- UI Toolkit (UITK) を使用したHUD（HP、シールド、EXP）および浮遊通知。\n\n# キーアセットとコンテキスト\n- `CombatManager.cs`: 戦闘キュー（`eventQueue`）の管理とアクションの実行。\n- `CharacterVisuals.cs`: キャラクターや敵のフラッシュおよび振動演出を制御。\n- `EnemyUnit.cs`: 敵のエンティティ、AIタイマー、およびダメージ受信を処理。\n\n# 実装手順\n「ダメージ適用 -> アニメーション（固定時間待機）」から、各ステップを `yield` で待機する「演出（VFX） -> アニメーション -> ロジック（ダメージ適用） -> 反応演出（VFX）」というシーケンシャルな流れに変更します。\n\n## 1. CharacterVisuals.cs を待機可能に更新\n- `TriggerDamageEffect` と `TriggerAttackEffect` を `IEnumerator` を返すように変更し、呼び出し側で `yield return` できるようにします。\n- `Flash` と `Shake` を `IEnumerator` を返すように変更するか、内部のコルーチンを公開します。\n- 呼び出し側がこれらのメソッドを `yield return` することで、視覚演出の完了を待機できるようにします。\n\n## 2. EnemyUnit.cs のダメージロジックの修正\n- 数値的なダメージ計算と視覚的なフィードバックを分離するか、`TakeDamage` をコルーチン（IEnumerator）に更新して待機可能にします。\n- `Die()` が反応演出の完了後にオブジェクトを破棄するように調整します。\n\n## 3. CombatManager.cs にアニメーション待機ヘルパーを実装\n- 指定したアニメーターが特定のステートに遷移し、再生を完了するまで待機する `WaitForAnimation(Animator animator, string stateName)` メソッドを追加します。\n\n## 4. CombatManager.cs のアクションハンドラの再構築\n以下のメソッドを更新し、新しいシーケンシャルなタイミングに従うようにします：\n- `HandlePlayerAttack`: \n    1. プレイヤーのフラッシュ演出（待機）\n    2. プレイヤーの攻撃アニメーション（待機）\n    3. 敵へのダメージ適用\n    4. 敵の被ダメージ演出（待機）\n- `HandlePlayerMagicAttack`: \n    1. 魔導士のフラッシュ演出（待機）\n    2. 魔導士の魔法アニメーション（待機）\n    3. 全敵へのダメージ適用\n    4. 全敵の被ダメージ演出（並列で待機）\n- `HandleEnemyAttack`:\n    1. 敵の攻撃演出/アニメーション（待機）\n    2. プレイヤーへのダメージ適用\n    3. プレイヤーキャラクターの被ダメージ演出（待機）\n\n## 5. タイミングとキューの進行の検証\n- `QueueProcessor` が各 `ExecuteAction` の呼び出しを正しく待機することを確認します。\n- 急激なマッチが発生しても、視覚演出が重ならず、キューに従って順番に処理されることを確認します。\n\n# 検証とテスト\n- **手動テスト**: 剣のブロックをマッチさせる。\n    - 期待される結果: ファイターが白く光る -> 攻撃アニメーション再生 -> 敵のHPが減少 -> 敵が赤く光りながら振動する。\n- **手動テスト**: 魔法のブロックをマッチさせる（全体攻撃）。\n    - 期待される結果: 魔導士が白く光る -> 魔法アニメーション再生 -> 全ての敵のHPが減少 -> 全ての敵が同時に赤く光りながら振動する。\n- **手動テスト**: 敵の攻撃。\n    - 期待される結果: 敵のアニメーション/フラッシュ -> プレイヤーのHP/シールドが減少 -> プレイヤーキャラクターが赤く光りながら振動する。\n- **エッジケース**: プレイヤーの攻撃中に敵が死亡する。\n    - 期待される結果: 敵が完全に被ダメージ演出を終えた後に破棄される。\n",
  "filePath": "Assets/Plans/combat-timing-adjustment.md"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Plans/combat-timing-adjustment.md
```

</details>

<details>
<summary>🔧 Tool: Unity.ExitPlanMode (CoreAgent)</summary>

**引数**

```json
{
  "planPath": "Assets/Plans/combat-timing-adjustment.md"
}
```

**結果**

```
{"approved":true,"approvalMode":"agent","message":"Plan approved. Switching to Agent mode.\n\nThe approved implementation plan is stored at: Assets/Plans/combat-timing-adjustment.md\nStop here — do not call any more tools or attempt implementation.\nAsk the user if they want to execute the entire plan. If yes, read and follow the plan strictly during implementation."}
```

</details>

<details>
<summary>🔧 Tool: Unity.GetFileContent (CoreAgent)</summary>

**引数**

```json
{
  "filePath": "Assets/Plans/combat-timing-adjustment.md"
}
```

**結果**

```
# プロジェクト概要
- ゲームタイトル: マッチ3 RPG プロトタイプ
- ハイレベルコンセプト: 7x7のグリッド上でのマッチ3パズルによってターン制戦闘が進行する。
- プレイヤー: シングルプレイヤー。
- インスピレーション / 参照ゲーム: パズル＆ドラゴンズ等。
- ターゲットプラットフォーム: PC / スタンドアロン。
- レンダーパイプライン: URP (2D)。

# ゲームメカニクス
## コアゲームプレイループ
プレイヤーは7x7のグリッド（最下段のみ）でブロックをマッチさせます。マッチにより戦闘アクション（攻撃、魔法、回復、シールド）がトリガーされ、イベントキューに追加されます。`CombatManager` はこのキューを順番に処理し、アニメーションとステータスの変化を発生させます。

## 操作方法と入力
- マウスクリック: 最下段のブロックを破壊。
- 自動: マッチの判定および戦闘の解決。

# UI
- UI Toolkit (UITK) を使用したHUD（HP、シールド、EXP）および浮遊通知。

# キーアセットとコンテキスト
- `CombatManager.cs`: 戦闘キュー（`eventQueue`）の管理とアクションの実行。
- `CharacterVisuals.cs`: キャラクターや敵のフラッシュおよび振動演出を制御。
- `EnemyUnit.cs`: 敵のエンティティ、AIタイマー、およびダメージ受信を処理。

# 実装手順
「ダメージ適用 -> アニメーション（固定時間待機）」から、各ステップを `yield` で待機する「演出（VFX） -> アニメーション -> ロジック（ダメージ適用） -> 反応演出（VFX）」というシーケンシャルな流れに変更します。

## 1. CharacterVisuals.cs を待機可能に更新
- `TriggerDamageEffect` と `TriggerAttackEffect` を `IEnumerator` を返すように変更し、呼び出し側で `yield return` できるようにします。
- `Flash` と `Shake` を `IEnumerator` を返すように変更するか、内部のコルーチンを公開します。
- 呼び出し側がこれらのメソッドを `yield return` することで、視覚演出の完了を待機できるようにします。

## 2. EnemyUnit.cs のダメージロジックの修正
- 数値的なダメージ計算と視覚的なフィードバックを分離するか、`TakeDamage` をコルーチン（IEnumerator）に更新して待機可能にします。
- `Die()` が反応演出の完了後にオブジェクトを破棄するように調整します。

## 3. CombatManager.cs にアニメーション待機ヘルパーを実装
- 指定したアニメーターが特定のステートに遷移し、再生を完了するまで待機する `WaitForAnimation(Animator animator, string stateName)` メソッドを追加します。

## 4. CombatManager.cs のアクションハンドラの再構築
以下のメソッドを更新し、新しいシーケンシャルなタイミングに従うようにします：
- `HandlePlayerAttack`: 
    1. プレイヤーのフラッシュ演出（待機）
    2. プレイヤーの攻撃アニメーション（待機）
    3. 敵へのダメージ適用
    4. 敵の被ダメージ演出（待機）
- `HandlePlayerMagicAttack`: 
    1. 魔導士のフラッシュ演出（待機）
    2. 魔導士の魔法アニメーション（待機）
    3. 全敵へのダメージ適用
    4. 全敵の被ダメージ演出（並列で待機）
- `HandleEnemyAttack`:
    1. 敵の攻撃演出/アニメーション（待機）
    2. プレイヤーへのダメージ適用
    3. プレイヤーキャラクターの被ダメージ演出（待機）

## 5. タイミングとキューの進行の検証
- `QueueProcessor` が各 `ExecuteAction` の呼び出しを正しく待機することを確認します。
- 急激なマッチが発生しても、視覚演出が重ならず、キューに従って順番に処理されることを確認します。

# 検証とテスト
- **手動テスト**: 剣のブロックをマッチさせる。
    - 期待される結果: ファイターが白く光る -> 攻撃アニメーション再生 -> 敵のHPが減少 -> 敵が赤く光りながら振動する。
- **手動テスト**: 魔法のブロックをマッチさせる（全体攻撃）。
    - 期待される結果: 魔導士が白く光る -> 魔法アニメーション再生 -> 全ての敵のHPが減少 -> 全ての敵が同時に赤く光りながら振動する。
- **手動テスト**: 敵の攻撃。
    - 期待される結果: 敵のアニメーション/フラッシュ -> プレイヤーのHP/シールドが減少 -> プレイヤーキャラクターが赤く光りながら振動する。
- **エッジケース**: プレイヤーの攻撃中に敵が死亡する。
    - 期待される結果: 敵が完全に被ダメージ演出を終えた後に破棄される。

```

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "fileContent": "using UnityEngine;\nusing System.Collections;\n\n[RequireComponent(typeof(SpriteRenderer))]\npublic class CharacterVisuals : MonoBehaviour\n{\n    private SpriteRenderer sr;\n    private Material defaultMaterial;\n    private static Material overlayMaterial;\n    private MaterialPropertyBlock mpb;\n    private static readonly int _OverlayColorId = Shader.PropertyToID(\"_OverlayColor\");\n\n    private Vector3 originalLocalPos;\n    private Coroutine currentFlashCoroutine;\n    private Coroutine currentShakeCoroutine;\n\n    private void Awake()\n    {\n        sr = GetComponent<SpriteRenderer>();\n        mpb = new MaterialPropertyBlock();\n        if (sr != null)\n        {\n            defaultMaterial = sr.sharedMaterial;\n        }\n        originalLocalPos = transform.localPosition;\n\n        if (overlayMaterial == null)\n        {\n            overlayMaterial = Resources.Load<Material>(\"EnemyOverlay\");\n        }\n    }\n\n    public IEnumerator TriggerDamageEffect()\n    {\n        // Parallel execution\n        var flash = StartCoroutine(FlashRoutine(new Color(1f, 0f, 0f, 0.8f), 0.2f));\n        var shake = StartCoroutine(ShakeRoutine(0.15f, 0.2f));\n        \n        yield return flash;\n        yield return shake;\n    }\n\n    public IEnumerator TriggerAttackEffect()\n    {\n        yield return StartCoroutine(FlashRoutine(new Color(1f, 1f, 1f, 0.8f), 0.1f));\n    }\n\n    public void Flash(Color color, float duration)\n    {\n        if (currentFlashCoroutine != null) StopCoroutine(currentFlashCoroutine);\n        currentFlashCoroutine = StartCoroutine(FlashRoutine(color, duration));\n    }\n\n    public void Shake(float amount, float duration)\n    {\n        if (currentShakeCoroutine != null) StopCoroutine(currentShakeCoroutine);\n        currentShakeCoroutine = StartCoroutine(ShakeRoutine(amount, duration));\n    }\n\n    public IEnumerator FlashRoutine(Color color, float duration)\n    {\n        if (sr == null || overlayMaterial == null) yield break;\n\n        sr.sharedMaterial = overlayMaterial;\n        sr.GetPropertyBlock(mpb);\n        mpb.SetColor(_OverlayColorId, color);\n        sr.SetPropertyBlock(mpb);\n\n        yield return new WaitForSeconds(duration);\n\n        sr.SetPropertyBlock(null);\n        sr.sharedMaterial = defaultMaterial;\n        currentFlashCoroutine = null;\n    }\n\n    public IEnumerator ShakeRoutine(float amount, float duration)\n    {\n        float elapsed = 0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            // Only horizontal shake\n            float xOffset = Random.Range(-amount, amount);\n            transform.localPosition = originalLocalPos + new Vector3(xOffset, 0, 0);\n            yield return null;\n        }\n        transform.localPosition = originalLocalPos;\n        currentShakeCoroutine = null;\n    }\n}\n",
  "filePath": "Assets/Scripts/CharacterVisuals.cs"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Scripts/CharacterVisuals.cs
```

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "filePath": "Assets/Scripts/EnemyUnit.cs",
  "fileContent": "using UnityEngine;\nusing System.Collections;\n\npublic class EnemyUnit : MonoBehaviour\n{\n    [Header(\"Stats\")]\n    public int HP = 30;\n    public int MaxHP = 30;\n    public int AttackPower = 5;\n    public bool IsMagic = false;\n    public bool IsDead = false;\n\n    [Header(\"Attack Timer\")]\n    public float AttackInterval = 4.0f;\n    private float timer;\n\n    private Animator animator;\n    public CharacterVisuals visuals;\n\n    private void Start()\n    {\n        HP = MaxHP;\n        timer = Random.Range(1.0f, AttackInterval); // Random start offset\n\n        animator = GetComponent<Animator>();\n        visuals = GetComponent<CharacterVisuals>();\n        if (visuals == null) visuals = gameObject.AddComponent<CharacterVisuals>();\n\n        // Detect if I am a ZombieMage based on name\n        if (gameObject.name.Contains(\"ZombieMage\"))\n        {\n            IsMagic = true;\n            AttackPower = 3; // Magic is slightly weaker but ignores Shield\n        }\n    }\n\n    private void Update()\n    {\n        if (IsDead) return;\n\n        timer -= Time.deltaTime;\n        if (timer <= 0f)\n        {\n            CombatManager.Instance.AddEnemyAction(this, AttackPower, IsMagic);\n            timer = AttackInterval;\n        }\n    }\n\n    public IEnumerator Attack()\n    {\n        if (visuals != null)\n        {\n            yield return StartCoroutine(visuals.TriggerAttackEffect());\n        }\n\n        if (animator != null)\n        {\n            animator.SetTrigger(\"Attack\");\n            // Wait for animation is handled by CombatManager via Helper\n        }\n    }\n\n    public IEnumerator TakeDamage(int damage)\n    {\n        if (IsDead) yield break;\n\n        HP -= damage;\n        Debug.Log($\"{name} took {damage} damage. HP: {HP}\");\n        \n        if (visuals != null)\n        {\n            yield return StartCoroutine(visuals.TriggerDamageEffect());\n        }\n\n        if (HP <= 0)\n        {\n            Die();\n        }\n    }\n\n    private void Die()\n    {\n        IsDead = true;\n        Debug.Log($\"{name} died!\");\n        Destroy(gameObject, 0.1f);\n    }\n}\n"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Scripts/EnemyUnit.cs
```

</details>

<details>
<summary>🔧 Tool: Unity.GetTextAssetContent (CoreAgent)</summary>

**引数**

```json
{
  "instanceID": 40230
}
```

**結果**

```
{
  "Data": "using UnityEngine;\nusing UnityEngine.UIElements;\nusing System.Collections;\nusing System.Collections.Generic;\n\npublic enum CombatActionType\n{\n    PlayerAttack,\n    PlayerMagicAttack,\n    PlayerHeal,\n    PlayerShield,\n    PlayerExp,\n    PlayerKey,\n    EnemyAttack\n}\n\npublic class CombatAction\n{\n    public CombatActionType Type;\n    public int Value;\n    public EnemyUnit SourceEnemy; // Only for EnemyAttack\n    public bool IsMagic; // For Zombie Mage\n}\n\npublic class CombatManager : MonoBehaviour\n{\n    public static CombatManager Instance { get; private set; }\n\n    [Header(\"Party Stats\")]\n    public int MaxHP = 100;\n    public int CurrentHP;\n    public int Shield;\n    public int Experience;\n    public bool HasKey;\n\n    [Header(\"Player Power (Base)\")]\n    public int BaseAttack = 5;\n    public int BaseMagicAttack = 3;\n    public int BaseHeal = 3;\n    public int BaseShield = 2;\n    public int BaseExp = 10;\n    public int KeyBonusExp = 50;\n\n    [Header(\"Enemy Settings\")]\n    public GameObject[] EnemyPrefabs;\n    public Transform[] EnemySpawnPoints;\n    public List<EnemyUnit> ActiveEnemies = new List<EnemyUnit>();\n\n    private LinkedList<CombatAction> eventQueue = new LinkedList<CombatAction>();\n    private bool isProcessingQueue = false;\n\n    [Header(\"UI References\")]\n    public UIDocument HUD;\n    private VisualElement hpBarFill;\n    private Label hpText;\n    private Label shieldText;\n    private Label expText;\n    private Label keyLabel;\n    private VisualElement notificationLayer;\n\n    [Header(\"Player Animators\")]\n    public Animator FighterAnimator;\n    public Animator MageAnimator;\n    public Animator TankAnimator;\n\n    private CharacterVisuals fighterVisuals;\n    private CharacterVisuals mageVisuals;\n    private CharacterVisuals tankVisuals;\n\n    private void Awake()\n    {\n        if (Instance == null) Instance = this;\n        else Destroy(gameObject);\n\n        CurrentHP = MaxHP;\n        SetupUI();\n\n        // Assign player animators and visuals\n        SetupPlayerComponents();\n    }\n\n    private void SetupPlayerComponents()\n    {\n        if (FighterAnimator == null)\n        {\n            GameObject f = GameObject.Find(\"Fighter\");\n            if (f != null) FighterAnimator = f.GetComponent<Animator>();\n        }\n        if (MageAnimator == null)\n        {\n            GameObject m = GameObject.Find(\"Mage\");\n            if (m != null) MageAnimator = m.GetComponent<Animator>();\n        }\n        if (TankAnimator == null)\n        {\n            GameObject t = GameObject.Find(\"Tank\");\n            if (t != null) TankAnimator = t.GetComponent<Animator>();\n        }\n\n        if (FighterAnimator != null) fighterVisuals = GetOrAddVisuals(FighterAnimator.gameObject);\n        if (MageAnimator != null) mageVisuals = GetOrAddVisuals(MageAnimator.gameObject);\n        if (TankAnimator != null) tankVisuals = GetOrAddVisuals(TankAnimator.gameObject);\n    }\n\n    private CharacterVisuals GetOrAddVisuals(GameObject go)\n    {\n        CharacterVisuals v = go.GetComponent<CharacterVisuals>();\n        if (v == null) v = go.AddComponent<CharacterVisuals>();\n        return v;\n    }\n\n    private void SetupUI()\n{\n        if (HUD == null) HUD = GetComponent<UIDocument>();\n        if (HUD == null) return;\n\n        var root = HUD.rootVisualElement;\n        hpBarFill = root.Q<VisualElement>(\"hp-bar-fill\");\n        hpText = root.Q<Label>(\"hp-text\");\n        shieldText = root.Q<Label>(\"shield-text\");\n        expText = root.Q<Label>(\"exp-text\");\n        keyLabel = root.Q<Label>(\"key-label\");\n        notificationLayer = root.Q<VisualElement>(\"notification-layer\");\n        \n        UpdateUI();\n    }\n\n    private void UpdateUI()\n    {\n        if (hpBarFill != null)\n        {\n            float percentage = (float)CurrentHP / MaxHP * 100f;\n            hpBarFill.style.width = new Length(percentage, LengthUnit.Percent);\n        }\n        if (hpText != null) hpText.text = $\"{CurrentHP}/{MaxHP}\";\n        if (shieldText != null) shieldText.text = Shield.ToString();\n        if (expText != null) expText.text = Experience.ToString();\n        if (keyLabel != null) keyLabel.text = HasKey ? \"KEY: YES\" : \"KEY: NO\";\n    }\n\n    private void Start()\n    {\n        SpawnWave();\n        StartCoroutine(QueueProcessor());\n    }\n\n    public void AddPlayerAction(GridManager.BlockType type, int matchCount, int skaCount, Vector3 worldPos)\n    {\n        int effectiveCount = matchCount + (skaCount / 3);\n        if (effectiveCount <= 0) return;\n\n        CombatAction action = new CombatAction();\n        switch (type)\n        {\n            case GridManager.BlockType.Sword:\n                action.Type = CombatActionType.PlayerAttack;\n                action.Value = effectiveCount * BaseAttack;\n                break;\n            case GridManager.BlockType.Magic:\n                action.Type = CombatActionType.PlayerMagicAttack;\n                action.Value = effectiveCount * BaseMagicAttack;\n                break;\n            case GridManager.BlockType.Heal:\n                action.Type = CombatActionType.PlayerHeal;\n                action.Value = effectiveCount * BaseHeal;\n                break;\n            case GridManager.BlockType.Shield:\n                action.Type = CombatActionType.PlayerShield;\n                action.Value = effectiveCount * BaseShield;\n                break;\n            case GridManager.BlockType.Gem:\n                action.Type = CombatActionType.PlayerExp;\n                action.Value = effectiveCount * BaseExp;\n                break;\n            case GridManager.BlockType.Key:\n                action.Type = CombatActionType.PlayerKey;\n                action.Value = KeyBonusExp; \n                break;\n        }\n\n        // Show UI notification\n        ShowActionNotification(action.Type, action.Value, worldPos);\n\n        // Priority: Insert player actions at the head\n        eventQueue.AddFirst(action);\n        Debug.Log($\"Added Player Action: {action.Type} Value: {action.Value}. Interrupting queue.\");\n    }\n\n    private void ShowActionNotification(CombatActionType type, int value, Vector3 worldPos)\n    {\n        if (notificationLayer == null) return;\n\n        Label label = new Label();\n        label.AddToClassList(\"notification-label\");\n\n        // Position based on world coordinates\n        Vector2 panelPos = RuntimePanelUtils.CameraTransformWorldToPanel(notificationLayer.panel, worldPos, Camera.main);\n        label.style.left = panelPos.x;\n        label.style.top = panelPos.y;\n        \n        string text = \"\";\n        Color color = Color.white;\n\n        switch (type)\n        {\n            case CombatActionType.PlayerAttack:\n                text = $\"Attack! {value} pts.\";\n                color = Color.red;\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                text = $\"Magic! {value} pts.\";\n                color = new Color(0.6f, 0f, 0.8f);\n                break;\n            case CombatActionType.PlayerHeal:\n                text = $\"Heal! {value} pts.\";\n                color = Color.green;\n                break;\n            case CombatActionType.PlayerShield:\n                text = $\"Shield! {value} pts.\";\n                color = new Color(0.5f, 0.8f, 1f); \n                break;\n            case CombatActionType.PlayerExp:\n                text = $\"EXP! +{value}\";\n                color = Color.cyan;\n                break;\n            case CombatActionType.PlayerKey:\n                text = $\"Key! +{value} EXP\";\n                color = Color.yellow;\n                break;\n        }\n\n        label.text = text;\n        label.style.color = color;\n        notificationLayer.Add(label);\n\n        StartCoroutine(AnimateNotification(label));\n    }\n\n    private IEnumerator AnimateNotification(Label label)\n    {\n        // Initial state: Slightly below center, invisible\n        label.style.opacity = 0;\n        label.style.translate = new Translate(Length.Percent(-50), Length.Percent(0));\n\n        // Phase 1: Emergence (Ease Out) - Increased travel (3x)\n        float elapsed = 0f;\n        float duration = 0.3f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            float easedT = 1 - Mathf.Pow(1 - t, 3); // Ease Out Cubic\n            \n            label.style.opacity = t;\n            // From 0 to -150% (was -50%)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(0, -150, easedT)));\n            yield return null;\n        }\n\n        // Phase 2: Float and Fade (Slow) - Restored to original travel distance (100% delta)\n        elapsed = 0f;\n        duration = 1.0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            \n            label.style.opacity = 1 - t;\n            // From -150% to -250% (delta 100%, matching original travel speed)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(-150, -250, t)));\n            yield return null;\n        }\n\n        label.RemoveFromHierarchy();\n    }\n\n    public void AddEnemyAction(EnemyUnit enemy, int damage, bool isMagic)\n    {\n        CombatAction action = new CombatAction\n        {\n            Type = CombatActionType.EnemyAttack,\n            Value = damage,\n            SourceEnemy = enemy,\n            IsMagic = isMagic\n        };\n        eventQueue.AddLast(action);\n        Debug.Log($\"Added Enemy Action: {enemy.gameObject.name} Damage: {damage} (Magic: {isMagic})\");\n    }\n\n    private IEnumerator QueueProcessor()\n    {\n        while (true)\n        {\n            if (eventQueue.Count > 0 && !isProcessingQueue)\n            {\n                CombatAction action = eventQueue.First.Value;\n                eventQueue.RemoveFirst();\n                yield return StartCoroutine(ExecuteAction(action));\n            }\n            yield return null;\n        }\n    }\n\n    private IEnumerator ExecuteAction(CombatAction action)\n    {\n        isProcessingQueue = true;\n        \n        switch (action.Type)\n        {\n            case CombatActionType.PlayerAttack:\n                yield return StartCoroutine(HandlePlayerAttack(action.Value));\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                yield return StartCoroutine(HandlePlayerMagicAttack(action.Value));\n                break;\n            case CombatActionType.PlayerHeal:\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerExp:\n                Experience += action.Value;\n                Debug.Log($\"Gained {action.Value} EXP. Total: {Experience}\");\n                yield return new WaitForSeconds(0.1f);\n                break;\n            case CombatActionType.PlayerKey:\n                if (!HasKey)\n                {\n                    HasKey = true;\n                    Debug.Log(\"Key Obtained!\");\n                }\n                Experience += action.Value; \n                yield return new WaitForSeconds(0.3f);\n                break;\n            case CombatActionType.EnemyAttack:\n                yield return StartCoroutine(HandleEnemyAttack(action));\n                break;\n        }\n\n        UpdateUI();\n        isProcessingQueue = false;\n    }\n\n    private IEnumerator HandlePlayerAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        if (FighterAnimator != null) FighterAnimator.SetTrigger(\"Attack\");\n        if (fighterVisuals != null) fighterVisuals.TriggerAttackEffect();\n\n        EnemyUnit target = ActiveEnemies[0];\n        if (target != null)\n        {\n            Debug.Log($\"Player attacks {target.name} for {damage} damage.\");\n            target.TakeDamage(damage);\n            yield return new WaitForSeconds(0.6f); \n        }\n\n        CleanupEnemies();\n    }\n\n    private IEnumerator HandlePlayerMagicAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        if (MageAnimator != null) MageAnimator.SetTrigger(\"Magic\");\n        if (mageVisuals != null) mageVisuals.TriggerAttackEffect();\n\n        Debug.Log($\"Mage casts AOE Magic for {damage} damage to ALL enemies.\");\n        \n        List<EnemyUnit> targets = new List<EnemyUnit>(ActiveEnemies);\n        foreach (var enemy in targets)\n        {\n            if (enemy != null)\n            {\n                enemy.TakeDamage(damage);\n            }\n        }\n        \n        yield return new WaitForSeconds(0.8f); \n        CleanupEnemies();\n    }\n\n    private void CleanupEnemies()\n    {\n        ActiveEnemies.RemoveAll(e => e == null || e.IsDead);\n        \n        if (ActiveEnemies.Count == 0)\n        {\n            StartCoroutine(SpawnWaveWithDelay());\n        }\n    }\n\n    private IEnumerator SpawnWaveWithDelay()\n    {\n        yield return new WaitForSeconds(1.0f);\n        SpawnWave();\n    }\n\n    private IEnumerator HandleEnemyAttack(CombatAction action)\n    {\n        if (action.SourceEnemy == null || action.SourceEnemy.IsDead) yield break;\n\n        action.SourceEnemy.Attack();\n        yield return new WaitForSeconds(0.4f); \n\n        int finalDamage = action.Value;\n        \n        // Trigger player damage visual\n        if (fighterVisuals != null) fighterVisuals.TriggerDamageEffect();\n        if (mageVisuals != null) mageVisuals.TriggerDamageEffect();\n        if (tankVisuals != null) tankVisuals.TriggerDamageEffect();\n\n        if (action.IsMagic)\n{\n            CurrentHP -= finalDamage;\n            Debug.Log($\"Magic Attack! HP reduced by {finalDamage}. Current HP: {CurrentHP}\");\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n                Debug.Log($\"Attack fully blocked by Shield. Remaining Shield: {Shield}\");\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n                Debug.Log($\"Attack partially blocked. HP reduced by {finalDamage}. Current HP: {CurrentHP}\");\n            }\n        }\n\n        if (CurrentHP <= 0)\n        {\n            CurrentHP = 0;\n            Debug.LogError(\"Game Over (Party Wiped) - Restarting prototype stats.\");\n            yield return new WaitForSeconds(2.0f);\n            CurrentHP = MaxHP;\n            Shield = 0;\n            SpawnWave(); \n        }\n\n        yield return new WaitForSeconds(0.6f); \n    }\n\n    public void SpawnWave()\n    {\n        foreach (var enemy in ActiveEnemies) if (enemy != null) Destroy(enemy.gameObject);\n        ActiveEnemies.Clear();\n\n        int count = Random.Range(2, 6); \n        for (int i = 0; i < count; i++)\n        {\n            if (EnemyPrefabs.Length == 0) break;\n            \n            GameObject prefab = EnemyPrefabs[Random.Range(0, EnemyPrefabs.Length)];\n            Vector3 pos = EnemySpawnPoints.Length > i ? EnemySpawnPoints[i].position : new Vector3(i * 1.5f - 3f, 3.5f, 0);\n            \n            GameObject enemyObj = Instantiate(prefab, pos, Quaternion.identity);\n            EnemyUnit unit = enemyObj.GetComponent<EnemyUnit>();\n            if (unit == null) unit = enemyObj.AddComponent<EnemyUnit>();\n            \n            ActiveEnemies.Add(unit);\n        }\n        Debug.Log($\"New wave spawned: {count} enemies.\");\n    }\n}\n",
  "Info": ""
}
```

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "filePath": "Assets/Scripts/CombatManager.cs",
  "fileContent": "using UnityEngine;\nusing UnityEngine.UIElements;\nusing System.Collections;\nusing System.Collections.Generic;\n\npublic enum CombatActionType\n{\n    PlayerAttack,\n    PlayerMagicAttack,\n    PlayerHeal,\n    PlayerShield,\n    PlayerExp,\n    PlayerKey,\n    EnemyAttack\n}\n\npublic class CombatAction\n{\n    public CombatActionType Type;\n    public int Value;\n    public EnemyUnit SourceEnemy; // Only for EnemyAttack\n    public bool IsMagic; // For Zombie Mage\n}\n\npublic class CombatManager : MonoBehaviour\n{\n    public static CombatManager Instance { get; private set; }\n\n    [Header(\"Party Stats\")]\n    public int MaxHP = 100;\n    public int CurrentHP;\n    public int Shield;\n    public int Experience;\n    public bool HasKey;\n\n    [Header(\"Player Power (Base)\")]\n    public int BaseAttack = 5;\n    public int BaseMagicAttack = 3;\n    public int BaseHeal = 3;\n    public int BaseShield = 2;\n    public int BaseExp = 10;\n    public int KeyBonusExp = 50;\n\n    [Header(\"Enemy Settings\")]\n    public GameObject[] EnemyPrefabs;\n    public Transform[] EnemySpawnPoints;\n    public List<EnemyUnit> ActiveEnemies = new List<EnemyUnit>();\n\n    private LinkedList<CombatAction> eventQueue = new LinkedList<CombatAction>();\n    private bool isProcessingQueue = false;\n\n    [Header(\"UI References\")]\n    public UIDocument HUD;\n    private VisualElement hpBarFill;\n    private Label hpText;\n    private Label shieldText;\n    private Label expText;\n    private Label keyLabel;\n    private VisualElement notificationLayer;\n\n    [Header(\"Player Animators\")]\n    public Animator FighterAnimator;\n    public Animator MageAnimator;\n    public Animator TankAnimator;\n\n    private CharacterVisuals fighterVisuals;\n    private CharacterVisuals mageVisuals;\n    private CharacterVisuals tankVisuals;\n\n    private void Awake()\n    {\n        if (Instance == null) Instance = this;\n        else Destroy(gameObject);\n\n        CurrentHP = MaxHP;\n        SetupUI();\n\n        // Assign player animators and visuals\n        SetupPlayerComponents();\n    }\n\n    private void SetupPlayerComponents()\n    {\n        if (FighterAnimator == null)\n        {\n            GameObject f = GameObject.Find(\"Fighter\");\n            if (f != null) FighterAnimator = f.GetComponent<Animator>();\n        }\n        if (MageAnimator == null)\n        {\n            GameObject m = GameObject.Find(\"Mage\");\n            if (m != null) MageAnimator = m.GetComponent<Animator>();\n        }\n        if (TankAnimator == null)\n        {\n            GameObject t = GameObject.Find(\"Tank\");\n            if (t != null) TankAnimator = t.GetComponent<Animator>();\n        }\n\n        if (FighterAnimator != null) fighterVisuals = GetOrAddVisuals(FighterAnimator.gameObject);\n        if (MageAnimator != null) mageVisuals = GetOrAddVisuals(MageAnimator.gameObject);\n        if (TankAnimator != null) tankVisuals = GetOrAddVisuals(TankAnimator.gameObject);\n    }\n\n    private CharacterVisuals GetOrAddVisuals(GameObject go)\n    {\n        CharacterVisuals v = go.GetComponent<CharacterVisuals>();\n        if (v == null) v = go.AddComponent<CharacterVisuals>();\n        return v;\n    }\n\n    private void SetupUI()\n    {\n        if (HUD == null) HUD = GetComponent<UIDocument>();\n        if (HUD == null) return;\n\n        var root = HUD.rootVisualElement;\n        hpBarFill = root.Q<VisualElement>(\"hp-bar-fill\");\n        hpText = root.Q<Label>(\"hp-text\");\n        shieldText = root.Q<Label>(\"shield-text\");\n        expText = root.Q<Label>(\"exp-text\");\n        keyLabel = root.Q<Label>(\"key-label\");\n        notificationLayer = root.Q<VisualElement>(\"notification-layer\");\n        \n        UpdateUI();\n    }\n\n    private void UpdateUI()\n    {\n        if (hpBarFill != null)\n        {\n            float percentage = (float)CurrentHP / MaxHP * 100f;\n            hpBarFill.style.width = new Length(percentage, LengthUnit.Percent);\n        }\n        if (hpText != null) hpText.text = $\"{CurrentHP}/{MaxHP}\";\n        if (shieldText != null) shieldText.text = Shield.ToString();\n        if (expText != null) expText.text = Experience.ToString();\n        if (keyLabel != null) keyLabel.text = HasKey ? \"KEY: YES\" : \"KEY: NO\";\n    }\n\n    private void Start()\n    {\n        SpawnWave();\n        StartCoroutine(QueueProcessor());\n    }\n\n    public void AddPlayerAction(GridManager.BlockType type, int matchCount, int skaCount, Vector3 worldPos)\n    {\n        int effectiveCount = matchCount + (skaCount / 3);\n        if (effectiveCount <= 0) return;\n\n        CombatAction action = new CombatAction();\n        switch (type)\n        {\n            case GridManager.BlockType.Sword:\n                action.Type = CombatActionType.PlayerAttack;\n                action.Value = effectiveCount * BaseAttack;\n                break;\n            case GridManager.BlockType.Magic:\n                action.Type = CombatActionType.PlayerMagicAttack;\n                action.Value = effectiveCount * BaseMagicAttack;\n                break;\n            case GridManager.BlockType.Heal:\n                action.Type = CombatActionType.PlayerHeal;\n                action.Value = effectiveCount * BaseHeal;\n                break;\n            case GridManager.BlockType.Shield:\n                action.Type = CombatActionType.PlayerShield;\n                action.Value = effectiveCount * BaseShield;\n                break;\n            case GridManager.BlockType.Gem:\n                action.Type = CombatActionType.PlayerExp;\n                action.Value = effectiveCount * BaseExp;\n                break;\n            case GridManager.BlockType.Key:\n                action.Type = CombatActionType.PlayerKey;\n                action.Value = KeyBonusExp; \n                break;\n        }\n\n        // Show UI notification\n        ShowActionNotification(action.Type, action.Value, worldPos);\n\n        // Priority: Insert player actions at the head\n        eventQueue.AddFirst(action);\n        Debug.Log($\"Added Player Action: {action.Type} Value: {action.Value}. Interrupting queue.\");\n    }\n\n    private void ShowActionNotification(CombatActionType type, int value, Vector3 worldPos)\n    {\n        if (notificationLayer == null) return;\n\n        Label label = new Label();\n        label.AddToClassList(\"notification-label\");\n\n        // Position based on world coordinates\n        Vector2 panelPos = RuntimePanelUtils.CameraTransformWorldToPanel(notificationLayer.panel, worldPos, Camera.main);\n        label.style.left = panelPos.x;\n        label.style.top = panelPos.y;\n        \n        string text = \"\";\n        Color color = Color.white;\n\n        switch (type)\n        {\n            case CombatActionType.PlayerAttack:\n                text = $\"Attack! {value} pts.\";\n                color = Color.red;\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                text = $\"Magic! {value} pts.\";\n                color = new Color(0.6f, 0f, 0.8f);\n                break;\n            case CombatActionType.PlayerHeal:\n                text = $\"Heal! {value} pts.\";\n                color = Color.green;\n                break;\n            case CombatActionType.PlayerShield:\n                text = $\"Shield! {value} pts.\";\n                color = new Color(0.5f, 0.8f, 1f); \n                break;\n            case CombatActionType.PlayerExp:\n                text = $\"EXP! +{value}\";\n                color = Color.cyan;\n                break;\n            case CombatActionType.PlayerKey:\n                text = $\"Key! +{value} EXP\";\n                color = Color.yellow;\n                break;\n        }\n\n        label.text = text;\n        label.style.color = color;\n        notificationLayer.Add(label);\n\n        StartCoroutine(AnimateNotification(label));\n    }\n\n    private IEnumerator AnimateNotification(Label label)\n    {\n        // Initial state: Slightly below center, invisible\n        label.style.opacity = 0;\n        label.style.translate = new Translate(Length.Percent(-50), Length.Percent(0));\n\n        // Phase 1: Emergence (Ease Out) - Increased travel (3x)\n        float elapsed = 0f;\n        float duration = 0.3f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            float easedT = 1 - Mathf.Pow(1 - t, 3); // Ease Out Cubic\n            \n            label.style.opacity = t;\n            // From 0 to -150% (was -50%)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(0, -150, easedT)));\n            yield return null;\n        }\n\n        // Phase 2: Float and Fade (Slow) - Restored to original travel distance (100% delta)\n        elapsed = 0f;\n        duration = 1.0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            \n            label.style.opacity = 1 - t;\n            // From -150% to -250% (delta 100%, matching original travel speed)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(-150, -250, t)));\n            yield return null;\n        }\n\n        label.RemoveFromHierarchy();\n    }\n\n    public void AddEnemyAction(EnemyUnit enemy, int damage, bool isMagic)\n    {\n        CombatAction action = new CombatAction\n        {\n            Type = CombatActionType.EnemyAttack,\n            Value = damage,\n            SourceEnemy = enemy,\n            IsMagic = isMagic\n        };\n        eventQueue.AddLast(action);\n        Debug.Log($\"Added Enemy Action: {enemy.gameObject.name} Damage: {damage} (Magic: {isMagic})\");\n    }\n\n    private IEnumerator QueueProcessor()\n    {\n        while (true)\n        {\n            if (eventQueue.Count > 0 && !isProcessingQueue)\n            {\n                CombatAction action = eventQueue.First.Value;\n                eventQueue.RemoveFirst();\n                yield return StartCoroutine(ExecuteAction(action));\n            }\n            yield return null;\n        }\n    }\n\n    private IEnumerator ExecuteAction(CombatAction action)\n    {\n        isProcessingQueue = true;\n        \n        switch (action.Type)\n        {\n            case CombatActionType.PlayerAttack:\n                yield return StartCoroutine(HandlePlayerAttack(action.Value));\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                yield return StartCoroutine(HandlePlayerMagicAttack(action.Value));\n                break;\n            case CombatActionType.PlayerHeal:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerExp:\n                Experience += action.Value;\n                Debug.Log($\"Gained {action.Value} EXP. Total: {Experience}\");\n                yield return new WaitForSeconds(0.1f);\n                break;\n            case CombatActionType.PlayerKey:\n                if (!HasKey)\n                {\n                    HasKey = true;\n                    Debug.Log(\"Key Obtained!\");\n                }\n                Experience += action.Value; \n                yield return new WaitForSeconds(0.3f);\n                break;\n            case CombatActionType.EnemyAttack:\n                yield return StartCoroutine(HandleEnemyAttack(action));\n                break;\n        }\n\n        UpdateUI();\n        isProcessingQueue = false;\n    }\n\n    private IEnumerator WaitForAnimation(Animator animator)\n    {\n        if (animator == null) yield break;\n        // Wait a frame for the trigger to start the transition\n        yield return null;\n        \n        // Wait until we're in the target state or for the state length\n        AnimatorStateInfo state = animator.GetCurrentAnimatorStateInfo(0);\n        yield return new WaitForSeconds(state.length);\n    }\n\n    private IEnumerator HandlePlayerAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        // 1. Player Flash\n        if (fighterVisuals != null) yield return StartCoroutine(fighterVisuals.TriggerAttackEffect());\n\n        // 2. Player Attack Animation\n        if (FighterAnimator != null)\n        {\n            FighterAnimator.SetTrigger(\"Attack\");\n            yield return StartCoroutine(WaitForAnimation(FighterAnimator));\n        }\n\n        // 3. Apply Damage and Enemy Reaction\n        EnemyUnit target = ActiveEnemies[0];\n        if (target != null)\n        {\n            Debug.Log($\"Player attacks {target.name} for {damage} damage.\");\n            yield return StartCoroutine(target.TakeDamage(damage));\n        }\n\n        CleanupEnemies();\n    }\n\n    private IEnumerator HandlePlayerMagicAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        // 1. Mage Flash\n        if (mageVisuals != null) yield return StartCoroutine(mageVisuals.TriggerAttackEffect());\n\n        // 2. Mage Magic Animation\n        if (MageAnimator != null)\n        {\n            MageAnimator.SetTrigger(\"Magic\");\n            yield return StartCoroutine(WaitForAnimation(MageAnimator));\n        }\n\n        // 3. Apply Damage to all and Enemy Reactions\n        Debug.Log($\"Mage casts AOE Magic for {damage} damage to ALL enemies.\");\n        List<EnemyUnit> targets = new List<EnemyUnit>(ActiveEnemies);\n        List<Coroutine> coroutines = new List<Coroutine>();\n        foreach (var enemy in targets)\n        {\n            if (enemy != null)\n            {\n                coroutines.Add(StartCoroutine(enemy.TakeDamage(damage)));\n            }\n        }\n        \n        foreach (var c in coroutines) yield return c;\n        \n        CleanupEnemies();\n    }\n\n    private void CleanupEnemies()\n    {\n        ActiveEnemies.RemoveAll(e => e == null || e.IsDead);\n        \n        if (ActiveEnemies.Count == 0)\n        {\n            StartCoroutine(SpawnWaveWithDelay());\n        }\n    }\n\n    private IEnumerator SpawnWaveWithDelay()\n    {\n        yield return new WaitForSeconds(1.0f);\n        SpawnWave();\n    }\n\n    private IEnumerator HandleEnemyAttack(CombatAction action)\n    {\n        if (action.SourceEnemy == null || action.SourceEnemy.IsDead) yield break;\n\n        // 1. Enemy Attack (Flash + Animation)\n        yield return StartCoroutine(action.SourceEnemy.Attack());\n        Animator enemyAnimator = action.SourceEnemy.GetComponent<Animator>();\n        if (enemyAnimator != null)\n        {\n            yield return StartCoroutine(WaitForAnimation(enemyAnimator));\n        }\n\n        // 2. Apply Damage\n        int finalDamage = action.Value;\n        if (action.IsMagic)\n        {\n            CurrentHP -= finalDamage;\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n            }\n        }\n\n        // 3. Player Damage Visual\n        List<Coroutine> coroutines = new List<Coroutine>();\n        if (fighterVisuals != null) coroutines.Add(StartCoroutine(fighterVisuals.TriggerDamageEffect()));\n        if (mageVisuals != null) coroutines.Add(StartCoroutine(mageVisuals.TriggerDamageEffect()));\n        if (tankVisuals != null) coroutines.Add(StartCoroutine(tankVisuals.TriggerDamageEffect()));\n        \n        foreach (var c in coroutines) yield return c;\n\n        if (CurrentHP <= 0)\n        {\n            CurrentHP = 0;\n            Debug.LogError(\"Game Over (Party Wiped) - Restarting prototype stats.\");\n            yield return new WaitForSeconds(1.0f);\n            CurrentHP = MaxHP;\n            Shield = 0;\n            SpawnWave(); \n        }\n\n        UpdateUI();\n    }\n\n    public void SpawnWave()\n    {\n        foreach (var enemy in ActiveEnemies) if (enemy != null) Destroy(enemy.gameObject);\n        ActiveEnemies.Clear();\n\n        int count = Random.Range(2, 6); \n        for (int i = 0; i < count; i++)\n        {\n            if (EnemyPrefabs.Length == 0) break;\n            \n            GameObject prefab = EnemyPrefabs[Random.Range(0, EnemyPrefabs.Length)];\n            Vector3 pos = EnemySpawnPoints.Length > i ? EnemySpawnPoints[i].position : new Vector3(i * 1.5f - 3f, 3.5f, 0);\n            \n            GameObject enemyObj = Instantiate(prefab, pos, Quaternion.identity);\n            EnemyUnit unit = enemyObj.GetComponent<EnemyUnit>();\n            if (unit == null) unit = enemyObj.AddComponent<EnemyUnit>();\n            \n            ActiveEnemies.Add(unit);\n        }\n        Debug.Log($\"New wave spawned: {count} enemies.\");\n    }\n}\n"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Scripts/CombatManager.cs
```

</details>

Thank you for your question. I will answer regarding the mechanism of the current implementation (`WaitForAnimation` method) and the cause of the "strange pause" you noticed.

To put it simply, the process **"waits for the duration (clip length in seconds) of the animation currently playing at that moment."** It is not waiting for an arbitrary fixed number of seconds (e.g., 0.5 seconds), but rather referencing a value obtained from the Animator.

However, the "strange pause" may be occurring for the following reasons:

1.  **Timing of state retrieval**: In the frame immediately after issuing a transition via `SetTrigger`, the system may still be "transitioning" or internally retrieving the information of the "previous state (e.g., Idle)." If Idle has a length of 1 second, it will wait for the Idle duration even after the attack motion has finished.
2.  **Mismatch with normalized time**: Since the current implementation uses "the length (in seconds) of the current state" directly as the wait time, discrepancies between the actual appearance and the wait time can occur depending on looping animation settings or how transitions overlap.

**Conclusion:**
It is "obtaining the animation's duration in seconds and waiting," but due to the nature of transitions, **it is highly likely that it is picking up and waiting for the duration of an unintended state (such as Idle).** This is likely the cause of what you perceive as a "strange pause after playback."
<details>
<summary>💭 Thinking</summary>

**Inspecting Animation Logic**

I'm currently reviewing the `WaitForAnimation` method within `CombatManager.cs`. The user's query about the animation waiting logic has prompted a closer examination of the recent implementation. I am confirming that the provided code functions as expected.

</details>

<details>
<summary>💭 Thinking</summary>

**Addressing Animation Transition Issues**

I'm now investigating a potential timing issue. Specifically, the `WaitForAnimation` method might be returning the duration of the *previous* animation state if called too quickly after triggering a new animation. This could lead to incorrect wait times. I need to make some code changes to ensure this waits for the *target* state.

</details>

<details>
<summary>💭 Thinking</summary>

**Explaining the Animation Wait**

I've been wrestling with the exact behavior of `WaitForAnimation`. The user's observation of a "strange gap" clarifies the core issue. I see now that my initial implementation grabs the *current* state's length, which can lead to waiting for the wrong duration if a transition is in progress. I will need to refine my explanation and revisit the implementation to ensure it accurately waits for the correct animation clip duration.

</details>

## 🧑 User

Are there any ways to improve this? Please only provide the answer.

## 🤖 Assistant

There are mainly three ways to improve this.

1. **Monitoring the State Name and Progress (NormalizedTime)**
   Rather than simply waiting a set number of seconds, this approach uses `animator.GetCurrentAnimatorStateInfo(0).IsName("Attack")` to confirm that a specific attack state has been entered, then loops and waits until `normalizedTime >= 1.0f` (100% playback). This allows dynamic adaptation to transition lag and varying animation lengths.

2. **Using Animation Events**
   This method embeds "events" at specific frames in the animation (such as the moment an attack lands or the animation ends) that call a method in your script. This is the most precise approach — the program side simply needs to wait (yield) until the event is fired.

3. **Accounting for Transitions (IsInTransition)**
   By checking `animator.IsInTransition(0)` and starting to measure playback time only after blending (transition) has finished, you can prevent incorrectly reading the elapsed time of the previous state.

**Recommended improvement:**
Combining **"identifying the state name"** with **"monitoring progress (normalizedTime)"** is the most reliable improvement that can be achieved with script alone. This makes it possible to move on to the next process the moment the attack finishes.
<details>
<summary>💭 Thinking</summary>

**Analyzing Animation Delays**

I'm focused on fine-tuning the animation wait logic in Unity to get rid of those irritating pauses. I've been examining the `WaitForAnimation` coroutine, specifically how it interacts with the animator. It seems like the core issue is within the animation state management. I am now looking at ways to determine the exact animation completion time.

</details>

<details>
<summary>💭 Thinking</summary>

**Investigating State Transitions**

I'm now diving into the nuances of state transitions. I'm trying to figure out how to reliably detect the intended animation state before calculating the wait time. Considering checking the state name directly, along with the normalized time, to ensure the animation has completed. I also need to account for transitions to prevent inaccurate duration estimations.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Wait Conditions**

I'm now prioritizing the most robust wait conditions. I've concluded checking the animation's state name in conjunction with its normalized time offers the most accurate, code-driven solution. Moreover, checking `IsInTransition` is critical to prevent premature execution. However, animation events offer precise timing control for designer-led synchronization.

</details>

## 🧑 User

Please proceed with that improvement proposal.

## 🤖 Assistant

I have improved the animation wait processing.

### What was improved
The `WaitForAnimation` method has been revamped to use a state-name-based monitoring approach.

1.  **Waiting for state start**: It loops and waits until the animator has actually transitioned to the specified state ("Attack" or "Magic"). This prevents false judgments caused by transition lag.
2.  **Progress monitoring**: It checks the animation's progress (`normalizedTime`) and ends the wait when **95% or more of the animation has played**. By cutting off slightly earlier than waiting for 100% (completion), it connects smoothly with the return motion to the next state (Idle, etc.), resulting in a snappier tempo.
3.  **Safety timeout**: A timeout mechanism is also included to prevent progress from stalling in the event that an animation fails to play.

With this, the "strange pause" that was occurring after animations ended should be resolved, and damage and subsequent actions should now transition smoothly the moment an attack finishes.
<details>
<summary>💭 Thinking</summary>

**Analyzing Animation Delays**

I'm currently focused on the `CombatManager.cs` script, and I've zeroed in on the `WaitForAnimation` method. It seems the current implementation, relying on `GetCurrentAnimatorStateInfo(0).length`, is causing unexpected pauses post-animation, indicating either an incorrect state being read, or transitions not being fully considered. I'm exploring solutions that can resolve this issue.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising Wait Logic**

I've decided to refine the `WaitForAnimation` function in `CombatManager.cs`. The plan is to pass in the animation state name for more precise control. Inside, I'll track the animator's state and normalized time, ensuring it reaches the end of the specified animation, while also accounting for transitions. Now, it's time to delve back into the code.

</details>

<details>
<summary>🔧 Tool: Unity.SaveFile (CoreAgent)</summary>

**引数**

```json
{
  "fileContent": "using UnityEngine;\nusing UnityEngine.UIElements;\nusing System.Collections;\nusing System.Collections.Generic;\n\npublic enum CombatActionType\n{\n    PlayerAttack,\n    PlayerMagicAttack,\n    PlayerHeal,\n    PlayerShield,\n    PlayerExp,\n    PlayerKey,\n    EnemyAttack\n}\n\npublic class CombatAction\n{\n    public CombatActionType Type;\n    public int Value;\n    public EnemyUnit SourceEnemy; // Only for EnemyAttack\n    public bool IsMagic; // For Zombie Mage\n}\n\npublic class CombatManager : MonoBehaviour\n{\n    public static CombatManager Instance { get; private set; }\n\n    [Header(\"Party Stats\")]\n    public int MaxHP = 100;\n    public int CurrentHP;\n    public int Shield;\n    public int Experience;\n    public bool HasKey;\n\n    [Header(\"Player Power (Base)\")]\n    public int BaseAttack = 5;\n    public int BaseMagicAttack = 3;\n    public int BaseHeal = 3;\n    public int BaseShield = 2;\n    public int BaseExp = 10;\n    public int KeyBonusExp = 50;\n\n    [Header(\"Enemy Settings\")]\n    public GameObject[] EnemyPrefabs;\n    public Transform[] EnemySpawnPoints;\n    public List<EnemyUnit> ActiveEnemies = new List<EnemyUnit>();\n\n    private LinkedList<CombatAction> eventQueue = new LinkedList<CombatAction>();\n    private bool isProcessingQueue = false;\n\n    [Header(\"UI References\")]\n    public UIDocument HUD;\n    private VisualElement hpBarFill;\n    private Label hpText;\n    private Label shieldText;\n    private Label expText;\n    private Label keyLabel;\n    private VisualElement notificationLayer;\n\n    [Header(\"Player Animators\")]\n    public Animator FighterAnimator;\n    public Animator MageAnimator;\n    public Animator TankAnimator;\n\n    private CharacterVisuals fighterVisuals;\n    private CharacterVisuals mageVisuals;\n    private CharacterVisuals tankVisuals;\n\n    private void Awake()\n    {\n        if (Instance == null) Instance = this;\n        else Destroy(gameObject);\n\n        CurrentHP = MaxHP;\n        SetupUI();\n\n        // Assign player animators and visuals\n        SetupPlayerComponents();\n    }\n\n    private void SetupPlayerComponents()\n    {\n        if (FighterAnimator == null)\n        {\n            GameObject f = GameObject.Find(\"Fighter\");\n            if (f != null) FighterAnimator = f.GetComponent<Animator>();\n        }\n        if (MageAnimator == null)\n        {\n            GameObject m = GameObject.Find(\"Mage\");\n            if (m != null) MageAnimator = m.GetComponent<Animator>();\n        }\n        if (TankAnimator == null)\n        {\n            GameObject t = GameObject.Find(\"Tank\");\n            if (t != null) TankAnimator = t.GetComponent<Animator>();\n        }\n\n        if (FighterAnimator != null) fighterVisuals = GetOrAddVisuals(FighterAnimator.gameObject);\n        if (MageAnimator != null) mageVisuals = GetOrAddVisuals(MageAnimator.gameObject);\n        if (TankAnimator != null) tankVisuals = GetOrAddVisuals(TankAnimator.gameObject);\n    }\n\n    private CharacterVisuals GetOrAddVisuals(GameObject go)\n    {\n        CharacterVisuals v = go.GetComponent<CharacterVisuals>();\n        if (v == null) v = go.AddComponent<CharacterVisuals>();\n        return v;\n    }\n\n    private void SetupUI()\n    {\n        if (HUD == null) HUD = GetComponent<UIDocument>();\n        if (HUD == null) return;\n\n        var root = HUD.rootVisualElement;\n        hpBarFill = root.Q<VisualElement>(\"hp-bar-fill\");\n        hpText = root.Q<Label>(\"hp-text\");\n        shieldText = root.Q<Label>(\"shield-text\");\n        expText = root.Q<Label>(\"exp-text\");\n        keyLabel = root.Q<Label>(\"key-label\");\n        notificationLayer = root.Q<VisualElement>(\"notification-layer\");\n        \n        UpdateUI();\n    }\n\n    private void UpdateUI()\n    {\n        if (hpBarFill != null)\n        {\n            float percentage = (float)CurrentHP / MaxHP * 100f;\n            hpBarFill.style.width = new Length(percentage, LengthUnit.Percent);\n        }\n        if (hpText != null) hpText.text = $\"{CurrentHP}/{MaxHP}\";\n        if (shieldText != null) shieldText.text = Shield.ToString();\n        if (expText != null) expText.text = Experience.ToString();\n        if (keyLabel != null) keyLabel.text = HasKey ? \"KEY: YES\" : \"KEY: NO\";\n    }\n\n    private void Start()\n    {\n        SpawnWave();\n        StartCoroutine(QueueProcessor());\n    }\n\n    public void AddPlayerAction(GridManager.BlockType type, int matchCount, int skaCount, Vector3 worldPos)\n    {\n        int effectiveCount = matchCount + (skaCount / 3);\n        if (effectiveCount <= 0) return;\n\n        CombatAction action = new CombatAction();\n        switch (type)\n        {\n            case GridManager.BlockType.Sword:\n                action.Type = CombatActionType.PlayerAttack;\n                action.Value = effectiveCount * BaseAttack;\n                break;\n            case GridManager.BlockType.Magic:\n                action.Type = CombatActionType.PlayerMagicAttack;\n                action.Value = effectiveCount * BaseMagicAttack;\n                break;\n            case GridManager.BlockType.Heal:\n                action.Type = CombatActionType.PlayerHeal;\n                action.Value = effectiveCount * BaseHeal;\n                break;\n            case GridManager.BlockType.Shield:\n                action.Type = CombatActionType.PlayerShield;\n                action.Value = effectiveCount * BaseShield;\n                break;\n            case GridManager.BlockType.Gem:\n                action.Type = CombatActionType.PlayerExp;\n                action.Value = effectiveCount * BaseExp;\n                break;\n            case GridManager.BlockType.Key:\n                action.Type = CombatActionType.PlayerKey;\n                action.Value = KeyBonusExp; \n                break;\n        }\n\n        // Show UI notification\n        ShowActionNotification(action.Type, action.Value, worldPos);\n\n        // Priority: Insert player actions at the head\n        eventQueue.AddFirst(action);\n        Debug.Log($\"Added Player Action: {action.Type} Value: {action.Value}. Interrupting queue.\");\n    }\n\n    private void ShowActionNotification(CombatActionType type, int value, Vector3 worldPos)\n    {\n        if (notificationLayer == null) return;\n\n        Label label = new Label();\n        label.AddToClassList(\"notification-label\");\n\n        // Position based on world coordinates\n        Vector2 panelPos = RuntimePanelUtils.CameraTransformWorldToPanel(notificationLayer.panel, worldPos, Camera.main);\n        label.style.left = panelPos.x;\n        label.style.top = panelPos.y;\n        \n        string text = \"\";\n        Color color = Color.white;\n\n        switch (type)\n        {\n            case CombatActionType.PlayerAttack:\n                text = $\"Attack! {value} pts.\";\n                color = Color.red;\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                text = $\"Magic! {value} pts.\";\n                color = new Color(0.6f, 0f, 0.8f);\n                break;\n            case CombatActionType.PlayerHeal:\n                text = $\"Heal! {value} pts.\";\n                color = Color.green;\n                break;\n            case CombatActionType.PlayerShield:\n                text = $\"Shield! {value} pts.\";\n                color = new Color(0.5f, 0.8f, 1f); \n                break;\n            case CombatActionType.PlayerExp:\n                text = $\"EXP! +{value}\";\n                color = Color.cyan;\n                break;\n            case CombatActionType.PlayerKey:\n                text = $\"Key! +{value} EXP\";\n                color = Color.yellow;\n                break;\n        }\n\n        label.text = text;\n        label.style.color = color;\n        notificationLayer.Add(label);\n\n        StartCoroutine(AnimateNotification(label));\n    }\n\n    private IEnumerator AnimateNotification(Label label)\n    {\n        // Initial state: Slightly below center, invisible\n        label.style.opacity = 0;\n        label.style.translate = new Translate(Length.Percent(-50), Length.Percent(0));\n\n        // Phase 1: Emergence (Ease Out) - Increased travel (3x)\n        float elapsed = 0f;\n        float duration = 0.3f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            float easedT = 1 - Mathf.Pow(1 - t, 3); // Ease Out Cubic\n            \n            label.style.opacity = t;\n            // From 0 to -150% (was -50%)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(0, -150, easedT)));\n            yield return null;\n        }\n\n        // Phase 2: Float and Fade (Slow) - Restored to original travel distance (100% delta)\n        elapsed = 0f;\n        duration = 1.0f;\n        while (elapsed < duration)\n        {\n            elapsed += Time.deltaTime;\n            float t = Mathf.Clamp01(elapsed / duration);\n            \n            label.style.opacity = 1 - t;\n            // From -150% to -250% (delta 100%, matching original travel speed)\n            label.style.translate = new Translate(Length.Percent(-50), Length.Percent(Mathf.Lerp(-150, -250, t)));\n            yield return null;\n        }\n\n        label.RemoveFromHierarchy();\n    }\n\n    public void AddEnemyAction(EnemyUnit enemy, int damage, bool isMagic)\n    {\n        CombatAction action = new CombatAction\n        {\n            Type = CombatActionType.EnemyAttack,\n            Value = damage,\n            SourceEnemy = enemy,\n            IsMagic = isMagic\n        };\n        eventQueue.AddLast(action);\n        Debug.Log($\"Added Enemy Action: {enemy.gameObject.name} Damage: {damage} (Magic: {isMagic})\");\n    }\n\n    private IEnumerator QueueProcessor()\n    {\n        while (true)\n        {\n            if (eventQueue.Count > 0 && !isProcessingQueue)\n            {\n                CombatAction action = eventQueue.First.Value;\n                eventQueue.RemoveFirst();\n                yield return StartCoroutine(ExecuteAction(action));\n            }\n            yield return null;\n        }\n    }\n\n    private IEnumerator ExecuteAction(CombatAction action)\n    {\n        isProcessingQueue = true;\n        \n        switch (action.Type)\n        {\n            case CombatActionType.PlayerAttack:\n                yield return StartCoroutine(HandlePlayerAttack(action.Value));\n                break;\n            case CombatActionType.PlayerMagicAttack:\n                yield return StartCoroutine(HandlePlayerMagicAttack(action.Value));\n                break;\n            case CombatActionType.PlayerHeal:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerExp:\n                Experience += action.Value;\n                Debug.Log($\"Gained {action.Value} EXP. Total: {Experience}\");\n                yield return new WaitForSeconds(0.1f);\n                break;\n            case CombatActionType.PlayerKey:\n                if (!HasKey)\n                {\n                    HasKey = true;\n                    Debug.Log(\"Key Obtained!\");\n                }\n                Experience += action.Value; \n                yield return new WaitForSeconds(0.3f);\n                break;\n            case CombatActionType.EnemyAttack:\n                yield return StartCoroutine(HandleEnemyAttack(action));\n                break;\n        }\n\n        UpdateUI();\n        isProcessingQueue = false;\n    }\n\n    private IEnumerator WaitForAnimation(Animator animator, string stateName)\n    {\n        if (animator == null) yield break;\n\n        // 1. Wait until the animator begins to enter the target state\n        // We check for transition or the state name itself\n        bool started = false;\n        float timeout = 2.0f; // Safety timeout\n        while (!started && timeout > 0)\n        {\n            AnimatorStateInfo state = animator.GetCurrentAnimatorStateInfo(0);\n            if (state.IsName(stateName))\n            {\n                started = true;\n            }\n            else\n            {\n                timeout -= Time.deltaTime;\n                yield return null;\n            }\n        }\n\n        // 2. Wait until the state reaches at least 95% completion\n        // (Using 0.95 instead of 1.0 for snappier feel, as transitions back to Idle usually start before 1.0)\n        while (started)\n        {\n            AnimatorStateInfo state = animator.GetCurrentAnimatorStateInfo(0);\n            if (!state.IsName(stateName) || state.normalizedTime >= 0.95f)\n            {\n                break;\n            }\n            yield return null;\n        }\n    }\n\n    private IEnumerator HandlePlayerAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        // 1. Player Flash\n        if (fighterVisuals != null) yield return StartCoroutine(fighterVisuals.TriggerAttackEffect());\n\n        // 2. Player Attack Animation\n        if (FighterAnimator != null)\n        {\n            FighterAnimator.SetTrigger(\"Attack\");\n            yield return StartCoroutine(WaitForAnimation(FighterAnimator, \"Attack\"));\n        }\n\n        // 3. Apply Damage and Enemy Reaction\n        EnemyUnit target = ActiveEnemies[0];\n        if (target != null)\n        {\n            Debug.Log($\"Player attacks {target.name} for {damage} damage.\");\n            yield return StartCoroutine(target.TakeDamage(damage));\n        }\n\n        CleanupEnemies();\n    }\n\n    private IEnumerator HandlePlayerMagicAttack(int damage)\n    {\n        if (ActiveEnemies.Count == 0) yield break;\n\n        // 1. Mage Flash\n        if (mageVisuals != null) yield return StartCoroutine(mageVisuals.TriggerAttackEffect());\n\n        // 2. Mage Magic Animation\n        if (MageAnimator != null)\n        {\n            MageAnimator.SetTrigger(\"Magic\");\n            yield return StartCoroutine(WaitForAnimation(MageAnimator, \"Magic\"));\n        }\n\n        // 3. Apply Damage to all and Enemy Reactions\n        Debug.Log($\"Mage casts AOE Magic for {damage} damage to ALL enemies.\");\n        List<EnemyUnit> targets = new List<EnemyUnit>(ActiveEnemies);\n        List<Coroutine> coroutines = new List<Coroutine>();\n        foreach (var enemy in targets)\n        {\n            if (enemy != null)\n            {\n                coroutines.Add(StartCoroutine(enemy.TakeDamage(damage)));\n            }\n        }\n        \n        foreach (var c in coroutines) yield return c;\n        \n        CleanupEnemies();\n    }\n\n    private void CleanupEnemies()\n    {\n        ActiveEnemies.RemoveAll(e => e == null || e.IsDead);\n        \n        if (ActiveEnemies.Count == 0)\n        {\n            StartCoroutine(SpawnWaveWithDelay());\n        }\n    }\n\n    private IEnumerator SpawnWaveWithDelay()\n    {\n        yield return new WaitForSeconds(1.0f);\n        SpawnWave();\n    }\n\n    private IEnumerator HandleEnemyAttack(CombatAction action)\n    {\n        if (action.SourceEnemy == null || action.SourceEnemy.IsDead) yield break;\n\n        // 1. Enemy Attack (Flash + Animation)\n        yield return StartCoroutine(action.SourceEnemy.Attack());\n        Animator enemyAnimator = action.SourceEnemy.GetComponent<Animator>();\n        if (enemyAnimator != null)\n        {\n            yield return StartCoroutine(WaitForAnimation(enemyAnimator, \"Attack\"));\n        }\n\n        // 2. Apply Damage\n        int finalDamage = action.Value;\n        if (action.IsMagic)\n        {\n            CurrentHP -= finalDamage;\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n            }\n        }\n\n        // 3. Player Damage Visual\n        List<Coroutine> coroutines = new List<Coroutine>();\n        if (fighterVisuals != null) coroutines.Add(StartCoroutine(fighterVisuals.TriggerDamageEffect()));\n        if (mageVisuals != null) coroutines.Add(StartCoroutine(mageVisuals.TriggerDamageEffect()));\n        if (tankVisuals != null) coroutines.Add(StartCoroutine(tankVisuals.TriggerDamageEffect()));\n        \n        foreach (var c in coroutines) yield return c;\n\n        if (CurrentHP <= 0)\n        {\n            CurrentHP = 0;\n            Debug.LogError(\"Game Over (Party Wiped) - Restarting prototype stats.\");\n            yield return new WaitForSeconds(1.0f);\n            CurrentHP = MaxHP;\n            Shield = 0;\n            SpawnWave(); \n        }\n\n        UpdateUI();\n    }\n\n    public void SpawnWave()\n    {\n        foreach (var enemy in ActiveEnemies) if (enemy != null) Destroy(enemy.gameObject);\n        ActiveEnemies.Clear();\n\n        int count = Random.Range(2, 6); \n        for (int i = 0; i < count; i++)\n        {\n            if (EnemyPrefabs.Length == 0) break;\n            \n            GameObject prefab = EnemyPrefabs[Random.Range(0, EnemyPrefabs.Length)];\n            Vector3 pos = EnemySpawnPoints.Length > i ? EnemySpawnPoints[i].position : new Vector3(i * 1.5f - 3f, 3.5f, 0);\n            \n            GameObject enemyObj = Instantiate(prefab, pos, Quaternion.identity);\n            EnemyUnit unit = enemyObj.GetComponent<EnemyUnit>();\n            if (unit == null) unit = enemyObj.AddComponent<EnemyUnit>();\n            \n            ActiveEnemies.Add(unit);\n        }\n        Debug.Log($\"New wave spawned: {count} enemies.\");\n    }\n}\n",
  "filePath": "Assets/Scripts/CombatManager.cs"
}
```

**結果**

```
Successfully created file /Users/keijiro/Documents/AI-Hackathon/Assets/Scripts/CombatManager.cs
```

</details>

Much better! Next, let's adjust the visual effects.
- When the Shield block activates its effect, instead of the Tank glowing white, make the Tank glow light blue.
- When an enemy attack is blocked by Shield, instead of the player characters and others glowing red, make only the Tank glow yellow.
- As a visual effect when the Magic block's effect activates, make all player characters glow green.
Please summarize what changes will be needed for the above. Do not start on the actual work yet.

---

Here is a summary of the proposed visual effect adjustments. Based on the current structure of `CombatManager.cs` and `CharacterVisuals.cs`, the following changes will be needed.

### 1. Extending CharacterVisuals.cs
Currently, `TriggerAttackEffect` (white) and `TriggerDamageEffect` (red) have fixed colors. To add more variation to the effects, we will take the following approach.
*   **Adding a general-purpose flash method**: Implement a method such as `TriggerFlash(Color color, float duration)` that allows the color to be specified externally.
*   Alternatively, add effect-specific methods (such as `TriggerShieldEffect`).

### 2. Changing Logic in CombatManager.cs
Adjust the timing, targets, and colors for triggering effects as follows.

#### **A. When Shield block activates (PlayerShield)**
*   **Before**: Executes `tankVisuals.TriggerAttackEffect()` (white).
*   **After**: Change to execute a **light blue (Cyan)** flash on `tankVisuals`.

#### **B. When an enemy attack is blocked by Shield (HandleEnemyAttack)**
*   **Before**: Executes `TriggerDamageEffect()` (red) on everyone.
*   **After**:
    *   When `Shield >= finalDamage` (fully blocked) or when the shield is determined to have decreased, execute an effect where **only the Tank glows yellow (Yellow)**.
    *   Add a conditional branch so that all characters glow red in the conventional way only when damage penetrates the shield and reaches HP.

#### **C. When Magic block activates (PlayerMagicAttack)**
*   **Before**: Only executes `mageVisuals.TriggerAttackEffect()` (white).
*   **After**: Change to execute effects where `fighterVisuals`, `mageVisuals`, and `tankVisuals` — **all characters glow green (Green)** — are run in parallel.

### Summary: Required Work
1.  **`CharacterVisuals.cs`**: Add a public method for glowing in any specified color.
2.  **`CombatManager.cs`**:
    *   Update the color specification inside the `PlayerShield` processing.
    *   Add loop/parallel processing inside `PlayerMagicAttack` to make all characters glow green.
    *   Add a conditional branch for "shield defense success" inside `HandleEnemyAttack` to switch the effect target and color.

With these changes, the battle situation (successful defense, magic activation, etc.) will be visually distinguishable in a clear and distinct manner.

Shall we proceed with this approach?
<details>
<summary>💭 Thinking</summary>

**Analyzing Combat Visuals**

I'm currently focused on the visual cues for combat, especially shield interactions. I've decided the tank's shield activation needs a cyan flash instead of the current white. Also, a yellow flash for the tank only, upon blocking an enemy attack, seems a better approach than the global red flash. Now considering the magic block.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Magic Visuals**

I'm now diving into the magic block visuals. I'm thinking the best approach is a unified green flash for all characters when a magic attack is blocked. I'm focusing on modifying the `HandleEnemyAttack` function and will need to implement a conditional check. The current logic uses  `TriggerDamageEffect` which seems the best starting point, but I must  ensure it correctly applies to all characters.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Flash Implementation**

I'm now implementing the color changes in `CharacterVisuals.cs`, focusing on a more flexible `TriggerFlash` method. I'm considering passing a duration value. I've successfully updated the `ExecuteAction` function in `CombatManager.cs` to trigger the cyan flash for shield activation. Next, I must address the yellow flash for blocked attacks, focusing on the conditional checks within `HandleEnemyAttack`.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Logic Refinements**

I'm now implementing the color changes in `CharacterVisuals.cs` for the Tank's shield and also the logic for damage mitigation. I've successfully implemented the cyan shield activation using a new `TriggerShieldEffect` method. I'm now modifying `HandleEnemyAttack` to check the damage against the shield value. I'm considering using an `if` statement to decide between triggering the yellow flash for the tank or the red flash for all characters.

</details>

## 🧑 User

Ah, I made a mistake. I was talking about when the Heal block activates, not the Magic block. Please summarize it again. Please do not start the actual work yet.

## 🤖 Assistant

I apologize for the confusion. I will revise the summary as the **Heal block** effect and start over.

Based on the current structure of `CombatManager.cs` and `CharacterVisuals.cs`, the following changes will be needed.

### 1. Extending CharacterVisuals.cs
To support effect variations (cyan, yellow, green, etc.), the following will be done:
*   **Adding a generic flash method**: Implement a method such as `TriggerFlash(Color color, float duration)` that accepts a color as an argument, allowing the color to be freely specified from outside.

### 2. Changing the Effect Logic in CombatManager.cs
The effect targets and colors for each action will be adjusted as specified.

#### **A. When the Shield block activates (PlayerShield)**
*   **Target**: Tank only
*   **Color**: **Cyan**
*   **Timing**: Immediately before the shield addition process.

#### **B. When an enemy attack is blocked by Shield (HandleEnemyAttack)**
*   **Target**: **Tank only**
*   **Color**: **Yellow**
*   **Logic**:
    *   Add a branch so that only the Tank flashes yellow when `Shield >= finalDamage` (the damage is completely absorbed by the shield).
    *   If the shield is penetrated and HP takes damage, everyone flashes red as usual (damage effect).

#### **C. When the Heal block activates (PlayerHeal)**
*   **Target**: **All player characters** (Fighter, Mage, Tank)
*   **Color**: **Green**
*   **Timing**: When the heal process executes. Process in parallel so everyone lights up simultaneously.

### Summary: Required Implementation Steps
1.  **`CharacterVisuals.cs`**: Add a public method to flash with any specified color.
2.  **`CombatManager.cs`**:
    *   Update the `PlayerHeal` process inside `ExecuteAction` so everyone flashes green.
    *   Update the `PlayerShield` process inside `ExecuteAction` so the Tank flashes cyan.
    *   After the damage calculation inside `HandleEnemyAttack`, determine whether it is a "successful shield block" or "HP damage," and differentiate the effects accordingly (Tank's yellow flash vs. everyone's red flash).

With this structure, the effect of each block and successful defense will be clearly distinguishable by color.

Shall we proceed with this plan?
<details>
<summary>💭 Thinking</summary>

**Clarifying Requirements Swiftly**

I've just processed the correction regarding the "Heal block effect." The key now is understanding how to visually represent this. When a Heal block triggers, all player characters must flash green.

</details>

<details>
<summary>💭 Thinking</summary>

**Analyzing Implementation Details**

I'm now zeroing in on the implementation. I'm planning to introduce a `TriggerColorFlash` method to `CharacterVisuals.cs`. In `CombatManager.cs`, I'll call this to make the Tank flash Cyan on shield block and Yellow when an enemy attack is completely blocked. Importantly, the "HandlePlayerHeal" will trigger a green flash for all player characters. If damage is only *partially* blocked, the attack will have a Red flash for everyone as before.

</details>

<details>
<summary>💭 Thinking</summary>

**Summarizing Block Mechanics**

I'm now integrating the shield block effects, refining the `HandleEnemyAttack` logic. Fully blocked attacks will cause the tank to flash yellow, ensuring a clear visual cue. Partially blocked attacks, which result in HP damage, retain the red flash for all characters, maintaining consistency. I am confident in this approach.

</details>

## 🧑 User

Yes, please proceed.

## 🤖 Assistant

The visual effects (VFX) adjustments are complete.

### Changes Made

1.  **Extended functionality in `CharacterVisuals.cs`**:
    *   Added a general-purpose method `TriggerFlash(Color color, float duration)` that allows specifying a color and duration for flashing from outside the class. This enables a variety of color-based effects depending on specific actions.

2.  **Updated effects for Heal / Shield activation**:
    *   **Heal**: Changed so that all player characters (Fighter, Mage, Tank) flash **green** when activated.
    *   **Shield**: Changed so that only the Tank flashes **cyan** when activated.

3.  **Updated effect for successful defense (Shield block)**:
    *   When an enemy attack is completely blocked by the shield (i.e., no damage reaches HP), the logic has been revised so that **only the Tank flashes yellow**, rather than everyone shaking red.
    *   When damage breaks through the shield or a magic attack is received, everyone still flashes red and shakes as before.

With these changes, it is now easier to intuitively understand the success or failure of defenses and the effects of each action during battle.
<details>
<summary>💭 Thinking</summary>

**Defining Flash Functionality**

I'm currently working on modifying the `CharacterVisuals.cs` script. The plan is to add a generic `TriggerFlash` method. This method, which will accept a color and duration, is designed to yield an `IEnumerator`. The goal is to encapsulate the visual flash effect for damage and other events within the game. I'll retain the existing `TriggerDamageEffect` method as well.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing the TriggerFlash Method**

I've begun implementing the `TriggerFlash` method in `CharacterVisuals.cs`. It's structured to accept a color and duration, and it will return an `IEnumerator`. Now I'm preparing to refactor the existing damage and attack effects to utilize this new, versatile flash functionality. This should streamline the code significantly.

</details>

<details>
<summary>🔧 Tool: Unity.CodeEdit (CoreAgent)</summary>

**引数**

```json
{
  "oldString": "    public IEnumerator TriggerDamageEffect()\n    {\n        // Parallel execution\n        var flash = StartCoroutine(FlashRoutine(new Color(1f, 0f, 0f, 0.8f), 0.2f));\n        var shake = StartCoroutine(ShakeRoutine(0.15f, 0.2f));\n        \n        yield return flash;\n        yield return shake;\n    }\n\n    public IEnumerator TriggerAttackEffect()\n    {\n        yield return StartCoroutine(FlashRoutine(new Color(1f, 1f, 1f, 0.8f), 0.1f));\n    }\n\n    public void Flash(Color color, float duration)\n",
  "newString": "    public IEnumerator TriggerDamageEffect()\n    {\n        // Parallel execution\n        var flash = StartCoroutine(FlashRoutine(new Color(1f, 0f, 0f, 0.8f), 0.2f));\n        var shake = StartCoroutine(ShakeRoutine(0.15f, 0.2f));\n        \n        yield return flash;\n        yield return shake;\n    }\n\n    public IEnumerator TriggerAttackEffect()\n    {\n        yield return StartCoroutine(FlashRoutine(new Color(1f, 1f, 1f, 0.8f), 0.1f));\n    }\n\n    public IEnumerator TriggerFlash(Color color, float duration)\n    {\n        yield return StartCoroutine(FlashRoutine(color, duration));\n    }\n\n    public void Flash(Color color, float duration)\n",
  "filePath": "Assets/Scripts/CharacterVisuals.cs",
  "description": "Add generic TriggerFlash method to CharacterVisuals.cs"
}
```

**結果**

```
{
  "result": "The file was successfully edited and saved at CharacterVisuals.cs, and it compiled successfully.",
  "compilationOutput": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Updating Combat Effects**

I'm currently focused on the `CombatManager.cs` script, specifically modifying the effects of actions. I'm starting with `PlayerHeal`, updating the logic there. The goal is to refine how these actions play out within the combat system, ensuring their effects are accurately represented.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Action Implementation**

I'm now diving into the `CombatManager.cs` script, refining the effects for actions. Specifically, I'm updating `PlayerHeal` to trigger a green flash for everyone, `PlayerShield` to initiate a cyan flash just for the tank, and revisiting the `HandleEnemyAttack` logic to ensure accuracy. I'm focusing on ensuring visual feedback aligns with the action's outcomes.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising Visual Feedback**

I'm now implementing the visual adjustments outlined. For `PlayerHeal`, I'm adding a green flash effect that will be triggered for all characters. `PlayerShield` now initiates a cyan flash exclusively for the tank. Lastly, I'm revising `HandleEnemyAttack` to incorporate a yellow flash if the shield fully blocks damage, and a red flash for everyone if damage gets through.

</details>

<details>
<summary>🔧 Tool: Unity.CodeEdit (CoreAgent)</summary>

**引数**

```json
{
  "description": "Update PlayerHeal and PlayerShield effects in CombatManager.cs",
  "oldString": "            case CombatActionType.PlayerHeal:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerAttackEffect());\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n",
  "filePath": "Assets/Scripts/CombatManager.cs",
  "newString": "            case CombatActionType.PlayerHeal:\n                // All players flash Green\n                List<Coroutine> healCoroutines = new List<Coroutine>();\n                Color healColor = new Color(0f, 1f, 0f, 0.8f);\n                if (fighterVisuals != null) healCoroutines.Add(StartCoroutine(fighterVisuals.TriggerFlash(healColor, 0.3f)));\n                if (mageVisuals != null) healCoroutines.Add(StartCoroutine(mageVisuals.TriggerFlash(healColor, 0.3f)));\n                if (tankVisuals != null) healCoroutines.Add(StartCoroutine(tankVisuals.TriggerFlash(healColor, 0.3f)));\n                foreach (var c in healCoroutines) yield return c;\n\n                CurrentHP = Mathf.Min(MaxHP, CurrentHP + action.Value);\n                Debug.Log($\"Healed {action.Value}. HP: {CurrentHP}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n            case CombatActionType.PlayerShield:\n                // Tank flashes Cyan\n                if (tankVisuals != null) yield return StartCoroutine(tankVisuals.TriggerFlash(new Color(0f, 1f, 1f, 0.8f), 0.3f));\n\n                Shield += action.Value;\n                Debug.Log($\"Gained {action.Value} Shield. Total: {Shield}\");\n                yield return new WaitForSeconds(0.2f);\n                break;\n"
}
```

**結果**

```
{
  "result": "The file was successfully edited and saved at CombatManager.cs, and it compiled successfully.",
  "compilationOutput": ""
}
```

</details>

<details>
<summary>💭 Thinking</summary>

**Analyzing Attack Effects**

I'm currently focused on implementing the `HandleEnemyAttack` function in `CombatManager.cs`. The goal is to properly trigger the shield block effects. Specifically, I'm working through the logic to determine when a tank should flash yellow (shield block) versus other outcomes. I'm taking into account whether the attack is magic or physical, and if the shield can withstand the damage.

</details>

<details>
<summary>💭 Thinking</summary>

**Finalizing Block Conditions**

I'm now refining the `HandleEnemyAttack` function. My focus has shifted to ensure the correct visual feedback. The tank should flash yellow when blocking physical damage with their shield. Otherwise, with magic attacks or when the shield is insufficient, everyone flashes red. I'm verifying the interplay between `action.IsMagic`, `Shield`, and `finalDamage` to achieve this.

</details>

<details>
<summary>🔧 Tool: Unity.CodeEdit (CoreAgent)</summary>

**引数**

```json
{
  "oldString": "        // 2. Apply Damage\n        int finalDamage = action.Value;\n        if (action.IsMagic)\n        {\n            CurrentHP -= finalDamage;\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n            }\n        }\n\n        // 3. Player Damage Visual\n        List<Coroutine> coroutines = new List<Coroutine>();\n        if (fighterVisuals != null) coroutines.Add(StartCoroutine(fighterVisuals.TriggerDamageEffect()));\n        if (mageVisuals != null) coroutines.Add(StartCoroutine(mageVisuals.TriggerDamageEffect()));\n        if (tankVisuals != null) coroutines.Add(StartCoroutine(tankVisuals.TriggerDamageEffect()));\n        \n        foreach (var c in coroutines) yield return c;\n",
  "description": "Update HandleEnemyAttack in CombatManager.cs with Shield vs HP damage visuals",
  "filePath": "Assets/Scripts/CombatManager.cs",
  "newString": "        // 2. Apply Damage and 3. Player Response Visual\n        int finalDamage = action.Value;\n        bool fullBlock = false;\n\n        if (action.IsMagic)\n        {\n            CurrentHP -= finalDamage;\n        }\n        else\n        {\n            if (Shield >= finalDamage)\n            {\n                Shield -= finalDamage;\n                fullBlock = true;\n            }\n            else\n            {\n                finalDamage -= Shield;\n                Shield = 0;\n                CurrentHP -= finalDamage;\n            }\n        }\n\n        List<Coroutine> responseCoroutines = new List<Coroutine>();\n        if (fullBlock)\n        {\n            // Only Tank flashes Yellow\n            if (tankVisuals != null) responseCoroutines.Add(StartCoroutine(tankVisuals.TriggerFlash(Color.yellow, 0.3f)));\n        }\n        else\n        {\n            // Trigger player damage visual (All characters Red Flash + Shake)\n            if (fighterVisuals != null) responseCoroutines.Add(StartCoroutine(fighterVisuals.TriggerDamageEffect()));\n            if (mageVisuals != null) responseCoroutines.Add(StartCoroutine(mageVisuals.TriggerDamageEffect()));\n            if (tankVisuals != null) responseCoroutines.Add(StartCoroutine(tankVisuals.TriggerDamageEffect()));\n        }\n        \n        foreach (var c in responseCoroutines) yield return c;\n"
}
```

**結果**

```
{
  "result": "The file was successfully edited and saved at CombatManager.cs, and it compiled successfully.",
  "compilationOutput": ""
}
```

</details>

## 🧑 User

In addition to the yellow flash when the Tank defends, please make only the Tank shake. It's the same shake as when taking damage.

## 🤖 Assistant

The visual effect adjustment is complete.

### Changes Made

*   **Enhanced shield defense effect**:
    *   When an enemy attack is completely blocked by the shield, the Tank now **flashes yellow and simultaneously plays the same shake effect as when taking damage**.

This means that even though the damage itself is negated, it conveys a strong visual feedback of "blocking the enemy's heavy blow with the shield."
<details>
<summary>💭 Thinking</summary>

**Implementing Tank Shake**

I'm currently focused on integrating the shake effect alongside the existing yellow flash when the tank blocks. My initial thought is to modify the `TriggerFlash` call to include parameters for shake intensity and duration, if possible. I'll need to check how the damage effect's shake is implemented in `CharacterVisuals.cs` to ensure consistency.

</details>

<details>
<summary>💭 Thinking</summary>

**Refining Block Implementation**

I'm now leaning toward the `TriggerFlashAndShake` method in `CharacterVisuals.cs` for a cleaner approach. This will allow the `CombatManager.cs` to trigger both effects with a single call, simplifying the code. I'm also examining the existing `Shake` implementation to ensure I'm using the correct parameters and that the shake aligns with the damage effect's visual behavior. I am also thinking I might want to pass in the `shakeAmount` as a percent, to make the value intuitive.

</details>

<details>
<summary>💭 Thinking</summary>

**Revising Block Implementation**

I've considered various options, and I'm now leaning towards a combined approach. I can create a new `TriggerShake` method within `CharacterVisuals.cs`, which will return an `IEnumerator`, for compatibility with the `CombatManager`. This seems the most streamlined, while also mirroring the behavior of the damage shake. I'm focusing on ensuring it uses the same parameters for consistency.

</details>

<details>
<summary>💭 Thinking</summary>

**Implementing Final Changes**

I've decided on the final implementation. I will add the shake directly within the `CombatManager.cs` to ensure code simplicity. The `TriggerShake` method won't be required. I can call `StartCoroutine(tankVisuals.ShakeRoutine(0.15f, 0.2f))` directly. This feels the most straightforward while mirroring existing functionality, and avoids any unnecessary new methods.

</details>

<details>
<summary>💭 Thinking</summary>

**Simplifying Tank Block Shake**

After assessing all options, I've decided the most streamlined approach is to directly call the `ShakeRoutine` in `CombatManager.cs`. This removes the need for a new method in `CharacterVisuals.cs` and ensures the block shake parameters match the damage effect's precisely, making the implementation cleaner.

</details>

<details>
<summary>💭 Thinking</summary>

**Finalizing Block Shake Implementation**

I've considered all the options, and I'm ready to make the changes. I will call `tankVisuals.ShakeRoutine(0.15f, 0.2f)` directly within `CombatManager.cs`, alongside the `TriggerFlash` call. This mirrors the existing damage effect, maintaining consistency, and simplifies the overall code structure by removing the need for a new method in `CharacterVisuals.cs`.

</details>

<details>
<summary>🔧 Tool: Unity.CodeEdit (CoreAgent)</summary>

**引数**

```json
{
  "description": "Add shake effect to Tank during full shield block in CombatManager.cs",
  "newString": "        List<Coroutine> responseCoroutines = new List<Coroutine>();\n        if (fullBlock)\n        {\n            // Only Tank flashes Yellow and Shakes (same shake as damage)\n            if (tankVisuals != null)\n            {\n                responseCoroutines.Add(StartCoroutine(tankVisuals.TriggerFlash(Color.yellow, 0.3f)));\n                responseCoroutines.Add(StartCoroutine(tankVisuals.ShakeRoutine(0.15f, 0.2f)));\n            }\n        }\n        else\n",
  "oldString": "        List<Coroutine> responseCoroutines = new List<Coroutine>();\n        if (fullBlock)\n        {\n            // Only Tank flashes Yellow\n            if (tankVisuals != null) responseCoroutines.Add(StartCoroutine(tankVisuals.TriggerFlash(Color.yellow, 0.3f)));\n        }\n        else\n",
  "filePath": "Assets/Scripts/CombatManager.cs"
}
```

**結果**

```
{
  "result": "The file was successfully edited and saved at CombatManager.cs, and it compiled successfully.",
  "compilationOutput": ""
}
```

</details>