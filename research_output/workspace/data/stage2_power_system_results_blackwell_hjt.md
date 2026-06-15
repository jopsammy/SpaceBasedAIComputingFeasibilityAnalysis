# Stage 2 Task 5/8：Blackwell 主线下的电源系统结果

## 说明

- 生成时间：`2026-06-14T17:15:42`
- 任务定位：服务于 Task 5/8，吸收 Task 6 的质量输入（含废弃 kW/t 链）与 Task 7 的价格输入（含新 item_id 与电池分支化）。
- 写法原则：中性审计式；明确区分 `已闭合`、`四档`、`三档` 与 `当前不可判定`。
- 当前主线：统一 `Blackwell`，电源路线按 `GaAs` 主链与 `HJT` 并行成熟路线比较展开。

## 一、先行结论

- `600 km`、`beta = 0` 最保守近似下，轨道周期约 `96.7 min`，食时约 `35.5 min`，日照约 `61.2 min`。
- `GaAs` 主链基准重算得到：阵列面积约 `625 m^2`、电池名义容量 `186.8 kWh`、电源总质量 `2.34 t`。
- `HJT` 并行路线在相同负载与轨道假设下，需要额外约 `670 m^2` 阵列面积与 `1.39 t` 电源总质量；说明其物理上可比，但系统代价明显更重。
- `GaAs` 的阵列成本可作为情景参数进入后续模型；`HJT` 阵列采购价格链有三档支撑（地面 HJT $0.14-0.24/W × 10-15×），但闭合度低于 GaAs，单独标注。
- 电池成本已更新为 Task 7 新 item_id：`battery_cost_per_kwh_nmc`（NMC 固定 $200/kWh，三档 Starlink 迁移）与 `battery_cost_per_kwh_lto`（LTO 三场景，四档等比压缩）。PCDU 成本沿用 Task 7 的 $3k-10k/kW 四档。

## 二、Task 6/7 输入吸收关系

| 输入层 | 来源文件 | Task 5/8 吸收方式 | 约束 |
|---|---|---|---|
| 质量输入 | `stage2_mass_inputs_blackwell_hjt.json` | 读取 `public_baseline`、`route_sensitive_inputs`（`hjt_parallel`）和 `components`，重算轨道食时、电池容量、阵列面积、功率电子质量 | HJT 定位为并行成熟路线，不再保留「只能降级」标签 |
| 价格输入 | `stage2_cost_inputs_blackwell_hjt.json` | 读取 GaAs 阵列成本情景参数、电池 NMC/LTO 单价、PCDU 单价、HJT 价格链 | 电池成本按 item_id 分支（NMC 固定/LTO 三场景）；HJT 阵列采购链单独标注闭合度 |
| 方法学边界 | 审计文档与 `current-note.md` | 固定 `Blackwell` 主线、`GaAs/HJT` 并行、电池分支化（5yr/10yr Li-ion/10yr LTO） | 废弃 kW/t 反推链；不把 Rubin 带回主线 |

## 三、路线重算结果

| 路线 | Task 5/8 角色 | 状态 | 阵列面积 | 阵列质量 | 电池质量 | PCDU 质量 | 电源总质量 | 电源总成本 | 价格链状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| GaAs 主链基准 | Task 5/8 主模型电源路线 | 已闭合 | 625 m^2 | 938 kg | 983 kg | 419 kg | 2340 kg | $47.36M | 阵列成本为情景参数（三档）；电池 NMC 成本为三档（Starlink 迁移）；PCDU 成本为四档（Terma 锚点） |
| HJT 并行路线 | Task 5/8 并行成熟路线，物理链可比较，价格链单独标注 | 并行成熟路线 | 1295 m^2 | 2330 kg | 983 kg | 419 kg | 3733 kg | 当前不可判定 | HJT 阵列采购价格链为三档（地面 HJT $0.14-0.24/W × 10-15× 空间放大）；电池与 PCDU 与 GaAs 共享同一链路 |

## 四、公式链

```text
轨道周期 = 2*pi*sqrt((R_earth + h)^3 / mu)
食时占比(beta=0近似) = asin(R_earth / (R_earth + h)) / pi
食区负载能量 = 持续功率 * 食时
电池名义容量 = 食区负载能量 / (DoD * 放电效率)  ← DoD 按电池分支选取
回充能量 = 食区负载能量 / (充电效率 * 放电效率)
日照段额外回充功率 = 回充能量 / 日照时长
PCDU 输出需求 = 持续功率 + 日照段额外回充功率
EOL 阵列需求功率 = PCDU 输出需求 / 母线效率
阵列面积 = EOL 阵列需求功率 / (太阳常数 * EOL 电池效率 * 封装修正)
阵列质量 = 阵列面积 * 阵列面密度
PCDU 质量 = 额定功率 / 比功率  ← 比功率按 PCDU 场景选取
```

## 五、兼容旧接口的 `GaAs` 三场景

> 该表只用于维持 `get_task5_power_replacements()` 的后续脚本接口，不新增新的事实结论。

| 兼容场景 | 光伏质量 | 电池质量 | 功率电子质量 | 电源总质量 | 光伏面积 | 电池名义容量 | 电源总成本 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 轻量化 | 714 kg | 566 kg | 419 kg | 1,699 kg | 549 m^2 | 124.5 kWh | $42.25M |
| 基准 | 938 kg | 983 kg | 419 kg | 2,340 kg | 625 m^2 | 186.8 kWh | $47.36M |
| 保守 | 1,165 kg | 1,384 kg | 419 kg | 2,968 kg | 647 m^2 | 249.0 kWh | $61.01M |

## 六、审计判断

- `GaAs`：质量链为 `已闭合`（二档 AzurSpace 4G32 + 三档面密度），价格链为"阵列情景参数 + 电池 NMC 三档 + PCDU 四档"，可进入下一步主经济模型。
- `HJT`：现为并行成熟路线（非「禁止进入主模型」），物理链可用于并行比较（二档 CEA/INES 辐照实验 + 三档面密度）；采购价格链有三档地面 HJT 锚点 + 10-15× 空间放大，闭合度单独标注。
- `Task 6` 中废弃的 kW/t 反推链已从本脚本中彻底移除，计算载荷质量改为从 `components[compute_payload].scenario_mass_kg` 直接读取（Task 8 在 stage2_mass_cost_model.py 中落实）。
- `Task 7` 的新 item_id（`battery_cost_per_kwh_nmc` / `battery_cost_per_kwh_lto`）已在本脚本中被正确引用，旧 `battery_cost_per_kwh` 不再使用。

## 七、对下游的交接输入

- 主模型电源路线：继续使用 `GaAs` 主链。
- 并行比较路线：保留 `HJT` 为并行成熟路线（非探索性/降级）。
- 电池分支：5yr NMC（DoD 40%）、10yr Li-ion NMC（DoD 25%）、10yr LTO（DoD 80%）三分支可用于下游敏感性。
- 兼容接口：后续脚本可继续调用 `get_task5_power_replacements()` 获取 `轻量化 / 基准 / 保守` 三个 `GaAs` 场景的替换值。
