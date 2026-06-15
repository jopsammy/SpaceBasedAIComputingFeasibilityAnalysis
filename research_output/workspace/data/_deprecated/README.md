# 废弃资料目录

> 迁移时间：2026-06-14
> 迁移原因：第三轮 `close-stage-two-evidence-gaps` 已产出全新替代文件

## 已迁移文件

| 旧文件 | 废弃原因 | 替代文件 |
|--------|---------|---------|
| `stage2_mass_cost_results.md` | 基于已废弃的 kW/t 反推链（70/55/45 kW/t）和旧三分支模型（不含电池分支化） | `stage2_economic_branches_blackwell.md` |
| `stage2_power_system_results.md` | 不含 HJT 并行路线（HJT 被标记为"只能降级/禁止进入主模型"）；不含电池分支化；使用旧 cost item_id | `stage2_power_system_results_blackwell_hjt.md` |
| `stage2_architecture_reconciliation.md` | 基于旧 Rubin/Blackwell 架构映射，不再进入本轮主模型 | 无直接替代（Rubin 已降级为支线留痕） |

## 旧文件的核心问题

1. **kW/t 反推链**：`150 kW / (70/55/45 kW/t)` 的分母来源为二手媒体转述，定义域存在根本性歧义（整星 vs 载荷），存在循环引用风险。第三轮已通过 Task 2/V30 替换为 NVIDIA GB300 NVL72 地面硬件 A1 级锚点 + 三项空间化增量。
2. **HJT 定位错误**：旧定位为"只能降级/禁止进入主模型"，与用户指令相悖。第三轮 Task 3/V6-V9 已将 HJT 修正为并行成熟路线。
3. **参数无系统化分级**：旧文件中的参数没有四档证据分级、没有逐参数用户裁决、没有首次引用即 AskUserQuestion 的准入闸门。

## 如需追溯旧数字

- 旧数字链可参考第二轮 `refine-stage-two-blackwell-hjt-model` 的 spec 和 current-note
- 旧数字与第三轮新版数字的差异映射见 `stage2_branch_mapping_from_previous_round.md`
- 全量差异分析见本目录中的原始文件

## 不应将本目录文件用于新工作

> 本目录中所有文件的数字口径、方法学基线和路线定位均已被第三轮替代。仅保留用于历史追溯。任何新计算、新判断、新 paper 更新必须使用 `data/` 父目录中的新版文件。
