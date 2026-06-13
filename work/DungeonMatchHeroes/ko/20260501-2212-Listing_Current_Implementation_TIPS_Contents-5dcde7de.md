# Listing Current Implementation TIPS Contents

- **Date:** 2026-05-01 22:12
- **Task ID:** `5dcde7de-e0e6-40f0-8932-1ab34080acd9`
- **Messages:** 2

---

## 🧑 User

현재 구현에서 TIPS로 표시되는 내용을 열거해 주세요.

## 🤖 Assistant

현재 `Assets/Scripts/CombatManager.cs` 내의 `TIPS` 배열에 정의된 내용은 다음과 같습니다.

1.  **"Ska" (?) blocks cannot be matched. Shatter or Blast them.**（「Ska」블록은 매치시킬 수 없습니다. 파괴(Shatter)하거나 폭파(Blast)해 주세요.）
2.  **Shattering an elemental block drops a "Ska" block from above.**（속성 블록을 파괴하면 위에서 「Ska」블록이 떨어집니다.）
3.  **Shattering or Blasting a "Ska" block drops an elemental block from above.**（「Ska」블록을 파괴하거나 폭파하면 위에서 속성 블록이 떨어집니다.）
4.  **If stuck, focus on shattering "Ska" blocks to find new matches.**（막혔을 때는 「Ska」블록을 파괴해서 새로운 매치를 찾는 데 집중하세요.）
5.  **Match Shields to block incoming physical attacks.**（실드를 매치시켜 적의 물리 공격을 막으세요.）
6.  **Magic matches hit the entire enemy party.**（마법 매치는 적 파티 전체에 데미지를 줍니다.）
7.  **Shields cannot exceed your Max HP.**（실드 값은 최대 HP를 초과할 수 없습니다.）
8.  **Shields cannot block enemy magic attacks.**（실드로 적의 마법 공격을 막을 수는 없습니다.）
9.  **A Key is needed for chests, but you can only carry one.**（보물상자를 열려면 열쇠가 필요하지만, 가질 수 있는 건 하나뿐입니다.）
10. **Match Gems to gain EXP.**（젬을 매치시켜 경험치를 획득하세요.）
11. **Matching Heal blocks at full HP grants EXP.**（HP가 가득 찼을 때 회복 블록을 매치시키면 경험치를 획득할 수 있습니다.）
12. **Matching Keys while holding one grants EXP.**（이미 열쇠를 가지고 있을 때 열쇠를 매치시키면 경험치를 획득할 수 있습니다.）
13. **Enemies in the back row attack more slowly.**（뒷줄의 적은 공격 속도가 느려집니다.）
14. **Blasting "Ska" blocks near your matches slightly increases their power.**（매치 근처에서 「Ska」블록을 폭파하면 위력이 약간 상승합니다.）
<details>
<summary>🔧 도구: Unity.Grep (CoreAgent)</summary>

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
<summary>🔧 도구: Unity.GetFileContent (CoreAgent)</summary>

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