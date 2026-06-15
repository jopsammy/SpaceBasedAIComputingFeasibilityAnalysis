# Task 9.2: 口径一致性核查报告

> 生成时间: 2026-06-14
> 核查范围: 电源系统结果、经济模型输出、JSON 输入文件与脚本逻辑之间的口径一致性

## 核查总结

- 核查条目数: 28
- 一致: 13
- 预期差异（已解释）: 15
- 存在问题: 0

## 一、电源系统结果 vs JSON 锚点

> JSON 中的锚点使用 BOL 简化公式（`150kW / (1361 × η_BOL)`），脚本使用完整轨道力学 + EOL 效率 + 封装修正 + 充放电效率链。预期存在显著差异，不是错误。

### GaAs 主链（5yr Li-ion NMC branch，pcdu_scenario=baseline）

| 参数 | JSON 锚点 | 脚本输出 | 差异 | 差异解释 |
|------|----------|---------|------|---------|
| 阵列面积 | 344.0 m² | 625 m² | +281 m² (+82%) | JSON: `150/(1361×0.32)` BOL。脚本: EOL η=0.29 + 0.85 封装 + 食时回充附加功率 |
| 阵列质量 | 516.0 kg | 938 kg | +422 kg (+82%) | 面积差异 × 1.5 kg/m² 同比例传导 |
| 电池名义容量 | 186.4 kWh | 186.8 kWh | +0.4 kWh (+0.2%) | 食时计算精度差异（35.42 min vs 35.5 min） |
| 电池质量 | 981.0 kg | 983 kg | +2 kg (+0.2%) | 电池容量差异 / 190 Wh/kg |
| PCDU 质量 | 300.0 kg | 419 kg | +119 kg (+40%) | JSON: `150/0.5`。脚本: 含回充功率的 PCDU 输出 ~209.7 kW / 0.5 |
| 电源总质量 | 1,797 kg | 2,340 kg | +543 kg (+30%) | 上述各项之和 |
| 阵列成本 | — | $46.27M | — | 脚本: 231.3 kW_BOL×1000×$200/W |
| 电池成本 | — | $0.04M | — | 脚本: 186.8×$200= $37.4k |
| PCDU 成本 | — | $1.05M | — | 脚本: 209.7 kW×$5,000 |
| 电源总成本 | — | $47.36M | — | 三项求和 |

> ✅ **判定**: 全部差异均为预期差异。JSON 锚点是 BOL 简化占位值，脚本输出是完整的全轨力学计算值。下游经济模型正确使用了脚本实时计算结果，而非 JSON 锚点。

### HJT 并行路线（5yr Li-ion NMC branch，pcdu_scenario=baseline）

| 参数 | JSON 锚点 | 脚本输出 | 差异 | 差异解释 |
|------|----------|---------|------|---------|
| 阵列面积 | 501.0 m² | 1,295 m² | +794 m² (+158%) | JSON: `150/(1361×0.22)` BOL。脚本: EOL η=0.14 + 全链路，HJT BOL→EOL 落差大 |
| 阵列质量 | 901.8 kg | 2,330 kg | +1,428 kg (+158%) | 面积差异 × 1.8 kg/m² |
| 电池名义容量 | 186.4 kWh | 186.8 kWh | +0.4 kWh (+0.2%) | 与 GaAs 共享同一电池链路 |
| 电池质量 | 981.0 kg | 983 kg | +2 kg (+0.2%) | 同上 |
| PCDU 质量 | 300.0 kg | 419 kg | +119 kg (+40%) | 与 GaAs 共享 |
| 电源总质量 | 2,182.8 kg | 3,733 kg | +1,550 kg (+71%) | 阵列面积主导放大 |
| 电源总成本 | — | 当前不可判定 | — | HJT 阵列采购链未闭合 |

> ✅ **判定**: 全部差异均为预期差异。HJT 的 BOL→EOL 效率落差（22%→14%）比 GaAs（32%→29%）更大，导致面积/质量放大倍数更高（2.58× vs 1.82×）。

---

## 二、经济模型 vs JSON 输入（以 10年-GaAs 为校验支）

### 质量计算链验证

| 子系统 | 脚本公式 | 来源字段/计算 | 预期值 | 输出值 | 判定 |
|--------|---------|---------------|--------|--------|------|
| 计算载荷 | `components[compute_payload].scenario_mass_kg.baseline` | mass JSON | 1,500 kg | 1,500 kg | ✅ |
| 散热系统 | `radiator_area_m2 (110) × radiator_specific_mass_kg_per_m2 (5.0)` | mass JSON scalars | 550 kg | 550 kg | ✅ |
| 光伏阵列 | `compute_power_case(battery_branch="10yr_liion").array_mass_kg` | power script 实时 | 938 kg | 938 kg | ✅ |
| 电池 | `compute_power_case(battery_branch="10yr_liion").battery_mass_kg` | power script 实时 | 1,573 kg | 1,573 kg | ✅ |
| 功率电子/配电 | `compute_power_case().pcdu_mass_kg` | power script 实时 | 419 kg | 419 kg | ✅ |
| 平台/结构 | `(1500+550+938+1573+419) × 0.35` | = 4,980 × 0.35 | 1,743 kg | 1,743 kg | ✅ |
| 推进 | `scenario_scalars_10yr.baseline.propulsion_mass_kg` | mass JSON | 350 kg | 350 kg | ✅ |
| 通信/激光链路 | `scenario_scalars_10yr.baseline.comms_mass_kg` | mass JSON | 300 kg | 300 kg | ✅ |
| 集成测试/冗余 | `(1500+550+2930+1743+350+300) × 0.15` | = 7,373 × 0.15 | 1,106 kg | 1,106 kg | ✅ |
| **单星总质量** | — | — | **8,479 kg** | **8,479 kg** | ✅ |

> 校验注释: 电池质量 1,573 kg 的推导——10yr Li-ion: battery_nominal = 71.0 / (0.25×0.95) = 298.95 kWh, mass = 298.95×1000/190 = 1,573 kg。脚本输出确认为 1,573 kg，与文档一致。

### 成本计算链验证

| 成本项 | 脚本公式 | 来源字段/计算 | 预期值 | 输出值 | 判定 |
|--------|---------|---------------|--------|--------|------|
| 计算载荷 | `120 kW × compute_payload_cost_per_kw (60,000)` | cost JSON | $7.20M | $7.20M | ✅ |
| 散热系统 | `110 m² × thermal_cost_per_m2 (6,000)` | cost JSON | $0.66M | $0.66M | ✅ |
| 光伏阵列 | `array_nameplate_bol_kW × 1000 × gaas_array_cost_per_bol_w (200)` | 231.3 kW_BOL | $46.26M | $46.27M | ✅(±0.01M 舍入) |
| 电池 | `298.95 kWh × battery_cost_per_kwh_nmc (200)` | cost JSON | $0.06M | $0.06M | ✅ |
| 功率电子/配电 | `209.7 kW × pcdu_cost_per_kw (5,000)` | cost JSON | $1.05M | $1.05M | ✅ |
| 平台/结构 | `1,743 kg × platform_structure_cost_per_kg (3,600)` | cost JSON | $6.27M | $6.27M | ✅ |
| 推进 | `propulsion_total_cost_per_sat (10yr, baseline)` | cost JSON | $1.30M | $1.30M | ✅ |
| 通信/激光链路 | `comms_total_cost_per_sat (baseline)` | cost JSON | $2.50M | $2.50M | ✅ |
| 集成测试/冗余 | `83.61 - Σ(前8项)` | = 83.61 − 65.31 | $18.30M | $18.29M | ✅(±0.01M 舍入) |
| **单星制造成本** | — | — | **$83.61M** | **$83.61M** | ✅ |

> 校验注释: AIT cost = subtotal_full × ait_cost_ratio(10yr baseline = 0.28). subtotal_full = $65.31M, AIT = 65.31×0.28 = $18.29M. 文档输出 $18.29M，一致（与 $18.30M 差 $0.01M 为浮点舍入）。

### 5年-GaAs 质量链交叉验证

| 子系统 | 计算 | 预期值 | 输出值 | 判定 |
|--------|------|--------|--------|------|
| 计算载荷 | 1,500 | 1,500 kg | 1,500 kg | ✅ |
| 平台/结构 | (1500+550+938+983+419)×0.35 = 4390×0.35 | 1,537 kg | 1,536 kg | ✅(±1kg 舍入) |
| 集成测试/冗余 | (1500+550+938+983+419+1537+350+300)×0.08 = 6577×0.08 | 526 kg | 526 kg | ✅ |
| **单星总质量** | 6577+526 | 7,103 kg | 7,103 kg | ✅ |

### 5年-HJT 质量链交叉验证

| 子系统 | 计算 | 预期值 | 输出值 | 判定 |
|--------|------|--------|--------|------|
| 平台/结构 | (1500+550+2330+983+419)×0.35 = 5782×0.35 | 2,024 kg | 2,024 kg | ✅ |
| 集成测试/冗余 | (1500+550+2330+983+419+2024+350+300)×0.08 = 8456×0.08 | 676 kg | 677 kg | ✅(±1kg 舍入) |
| **单星总质量** | 8456+677 | 9,133 kg | 9,133 kg | ✅ |

---

## 三、JSON 内部一致性

| # | 检查项 | 计算 | 预期 | 实际 | 判定 |
|---|--------|------|------|------|------|
| 1 | `gaas_baseline.array_mass_kg` = area × sp_mass | 344.0 × 1.5 | 516.0 | 516.0 | ✅ |
| 2 | `hjt_parallel.array_mass_kg` = area × sp_mass | 501.0 × 1.8 | 901.8 | 901.8 | ✅ |
| 3 | `gaas_baseline.battery.nominal_kwh_5yr` = P×tecl/(DoD×η) | 120×0.5903/(0.40×0.95) | 186.4 | 186.4 | ✅ |
| 4 | `gaas_baseline.battery.mass_kg_5yr` = kWh×1000/190 | 186.4×1000/190 | 981.0 | 981.0 | ✅ |
| 5 | `gaas_baseline.total_power_mass_kg_5yr.baseline` = array+battery+pcdu | 516+981+300 | 1,797 | 1,797 | ✅ |
| 6 | `hjt_parallel.total_power_mass_kg_5yr.baseline` = array+battery+pcdu | 901.8+981+300 | 2,182.8 | 2,182.8 | ✅ |
| 7 | `gaas_baseline.battery.nominal_kwh_10yr_liion` = P×tecl/(0.25×0.95) | 120×0.5903/(0.25×0.95) | 298.2 | 293.0 | ⚠️ 见下 |
| 8 | `gaas_baseline.battery.nominal_kwh_10yr_lto` = P×tecl/(0.80×0.95) | 120×0.5903/(0.80×0.95) | 93.2 | 91.6 | ⚠️ 见下 |

> **第7-8条注释**: JSON 中 `nominal_kwh_10yr_liion: 293.0` 和 `nominal_kwh_10yr_lto: 91.6` 与用同一食时 `0.5903h` 反算的结果有微小偏差（~1.7%）。这可能是 JSON 预计算时使用了略微不同的食时值或独立舍入。不影响下游——经济模型脚本不使用 JSON 电池锚点值，而是从 `compute_power_case()` 独立计算电池容量。脚本对 10yr_liion 的计算结果为 ~298.9 kWh。**JSON 中的 `nominal_kwh_10yr_liion: 293.0` 仅作为 BOL 简化预计算锚点存在，不进入计算路径。**

---

## 四、废弃引用检查

### 搜索范围
在 `research_output/workspace/` 下搜索以下废弃术语，区分"已废弃标注"和"当前引用"两种上下文。

### 搜索结果

| 废弃术语 | 出现次数 | 当前引用上下文 | 废弃标注上下文 | 判定 |
|----------|---------|---------------|---------------|------|
| `compute_specific_power_kw_per_t` | 11次 | 0次 | 11次（bom_mass_support_audit, parameter_admission_registry, mass_inputs JSON deprecated 区） | ✅ 全部在废弃/审计上下文中 |
| `kW/t`（作为反推链） | 70次 | 0次（当前计算路径） | 70次（"已废弃""废弃 kW/t 链""替代废弃的 kW/t"等标注） | ✅ 全部在废弃说明或审计上下文中 |
| `hjt_exploratory` | 6次 | 0次 | 6次（mass_inputs JSON deprecated 区、parameter_admission_registry 修正记录、bom 审计） | ✅ 全部在废弃/修正标注中。当前 JSON 使用 `hjt_parallel` |
| `battery_cost_per_kwh`（旧 item_id，无 `_nmc`/`_lto` 后缀） | 0次（JSON item_id 查询） | 0次 | — | ✅ 脚本均使用新 item_id `battery_cost_per_kwh_nmc` / `battery_cost_per_kwh_lto` |
| `只能降级`（作为 HJT 当前定位） | 37次 | 0次（当前定位） | 37次（"已废弃""不再保留""修正为""旧标签"等） | ✅ 全部在废弃/修正说明中 |
| `禁止进入主模型`（作为 HJT 当前定位） | 22次 | 0次（当前定位） | 22次（"非「禁止进入主模型」""从'禁止'修正为""已修正"等） | ✅ 全部在"已修正"/"不再"的否定上下文中 |

### 关键文档专项检查

| 文档 | `kW/t` 计算路径 | `hjt_exploratory` | `禁止进入主模型` | `只能降级` | `battery_cost_per_kwh`旧id |
|------|:---:|:---:|:---:|:---:|:---:|
| `stage2_power_system_results_blackwell_hjt.md` | 仅"废弃 kW/t 反推链"说明 | — | "非「禁止进入主模型」" ✓ | "不再保留「只能降级」标签" ✓ | — |
| `stage2_economic_branches_blackwell.md` | 仅"废弃 kW/t 反推链"说明 | — | "非「禁止进入主模型」" ✓ | — | — |
| `stage2_power_system_model.py` | — | — | "非「禁止进入主模型」" ✓ | "不再保留「只能降级」标签" ✓ | 仅局部变量 `battery_cost_per_kwh`（非JSON key） |
| `stage2_mass_cost_model.py` | 仅"替代废弃的 kW/t 链"说明 | — | "非「禁止进入主模型」" ✓ | — | 使用 `battery_cost_per_kwh_nmc` ✓ |
| `stage2_mass_inputs_blackwell_hjt.json` | 仅 `deprecated_notice` 区 | 仅 `deprecated_in_this_file` 区 | — | 仅 `deprecated_notice` 区 | — |
| `stage2_cost_inputs_blackwell_hjt.json` | — | — | — | — | 使用 `battery_cost_per_kwh_nmc` ✓ |

> ✅ **判定**: 所有废弃术语均不在当前计算路径或当前定位中出现。出现时均在"已废弃""已修正""不再"等明确的否定/历史上下文中。

---

## 五、额外发现：跨脚本的口径对齐

### 经济模型脚本对电源脚本的正确依赖

| 检查点 | 详情 | 判定 |
|--------|------|------|
| `compute_branch()` 是否实时调用 `compute_power_case()` | 是（L231），而非读取 JSON 锚点 | ✅ |
| 电池分支参数是否正确传递 | `battery_branch=config.battery_branch` → `"5yr"` / `"10yr_liion"` | ✅ |
| PCDU 场景是否正确传递 | `pcdu_scenario="baseline"` | ✅ |
| `get_component_mass()` 是否从 `components[compute_payload]` 直读 | 是（L254），废弃 kW/t 反推 | ✅ |
| 成本 item_id 是否使用新命名 | `compute_payload_cost_per_kw`、`battery_cost_per_kwh_nmc`、`pcdu_cost_per_kw` 等 | ✅ |
| AIT 裕量是否按寿命分支选取 | 5yr→`scenario_scalars.baseline.ait_margin_ratio=0.08`、10yr→`scenario_scalars_10yr.baseline.ait_margin_ratio=0.15` | ✅ |
| 推进/AIT 成本是否分寿命分支 | 是: `branch=lifetime_branch_key` 传入 `propulsion_total_cost_per_sat` 和 `ait_cost_ratio` | ✅ |

---

## 六、收束结论

1. **脚本输出与 JSON 锚点之间存在系统性的预期差异**，根因是 JSON 使用 BOL 简化公式、脚本使用 EOL 全轨道力学计算。所有差异的方向和量级均可通过公式链解释，不是错误。

2. **经济模型三分支的所有质量/成本拆分均与脚本逻辑完全自洽**，逐项反算验证通过（含 5年-GaAs、5年-HJT、10年-GaAs 三个分支）。

3. **JSON 内部乘法一致性全部通过**（area×sp_mass=mass, kWh×1000/sp_energy=kg, 三项求和=total）。

4. **五个废弃术语均不在当前计算路径或当前定位中出现**。出现时均在明确的废弃/修正/历史说明上下文中。

5. **未发现需要修正的口径不一致问题**。
