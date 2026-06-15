# 第二阶段证据链关键缺口解除审计包

> 生成时间：2026-06-14
> 对应 Spec：`.trae/specs/close-stage-two-evidence-gaps/`
> 状态：Task 8 闭合

## 一、摘要

本轮（`close-stage-two-evidence-gaps`）以 `任务缺口分析报告.md` 识别的 9 个关键缺口为输入，经 Task 1（缺口矩阵）→ Task V1（证据分级规则冻结）→ Task 2（bottom-up 质量链重算）→ Task 3（HJT 并行路线证据包）→ Task 4（47 参数逐条重分级）→ Task 5（电源系统边界修复）→ Task V2（V1-V37 逐参数用户裁决）→ Task 6/7（P2 并行回写质量/价格 JSON）→ Task 8（脚本重建 + 结果文档 + 本审计包），已完成 9 缺口的全部分析、修正和回写。核心结构变化：(1) kW/t 反推链彻底废弃，替换为以 NVIDIA GB300 NVL72/HGX B200 地面硬件为 A1 级锚点的 bottom-up 计算载荷质量链；(2) HJT 从"禁止进入主模型"修正为与 GaAs 并行的成熟技术路线；(3) 电池从单参数分裂为 5yr NMC / 10yr Li-ion NMC / 10yr LTO 三分支；(4) 47 参数全部重分级并入模闸门化。当前状态：9 缺口已解除或转化为已知残余风险，模型输出已重建为 Blackwell 主线 + GaAs/HJT 并行 + 三分支经济结果，可转入下一轮可行性汇总。

## 二、9 缺口解除状态

| 缺口 | 归属 Task | 修复物 | 状态 | 关键证据 | 残余风险 |
|------|------|--------|------|---------|---------|
| 缺口 1：非纯物理链参数证据链普遍偏弱 | Task 4 | 参数准入清单（47 参数逐条分级） | 已解除 | 47 参数全部按四档重分级：一档 5 / 二档 7 / 三档 17 / 四档 14 / 禁止 1 / 废弃 3；每项标注分级理由、迁移逻辑、失效风险 | 四档参数占比 30%（14/47），是 AI1 信息公开不足的客观结果（非执行缺陷）；已嵌入 Task V2 逐参数用户裁决 |
| 缺口 2：计算载荷质量链逻辑不自洽（kW/t 反推） | Task 2 | bottom-up 质量链：地面硬件锚点 + 三项空间化增量分解 | 已解除 | GB300 NVL72 计算托盘 29 kg（Lenovo LP2357 Product Guide）、HGX B200 32 kg（NVIDIA PCF Datasheet）、DGX B200 142.4 kg（NVIDIA User Guide）——均为 A1/二档锚点；空间化增量拆解为辐射防护（spot shielding vs full enclosure）、热管理改造、结构/真空三项，各附 NASA/JAXA/Guomans 文献锚点 | 空间化增量三项各自为三档/四档，特别是热管理改造净增量范围跨度大（-50 ~ +400 kg）；V30 已通过结构化三项拆解 + AskUserQuestion 用户裁决，不改变已裁决的 V1-V29 值 |
| 缺口 3：未建立 Blackwell 地面→空间质量映射 | Task 2（同缺口 2） | 同上 bottom-up 质量链 + 三项空间化增量 | 已解除 | 同缺口 2；地面裸硬件基线 ~1,000-1,100 kg（约 38 托盘 × 29 kg/托盘），经三项增量后的空间化总质量：乐观 ~1,060-1,350 kg / 基准 ~1,330-1,670 kg / 保守 ~1,750-2,300 kg | 无 AI1 一手总质量与收拢尺寸（残余风险继承自第一轮，非阻断） |
| 缺口 4：HJT 路线处理与用户指令相悖（"禁止进入主模型"→并行成熟路线） | Task 3 + Task 5 | HJT 证据包（17 条搜索 URL + 12 项物理链闭合）+ 电源系统并行比较 | 已解除 | BOL 22%（华晟 26%+ 东方日升 26.61% 隆基 27.81% × AM0 0.85 修正）；EOL 14%（CEA/INES 独立辐照实验）；HJT 电源结果：阵列 1295 m²，电源总质量 3.73 t（vs GaAs 625 m²/2.34 t）；HJT 价格链三档（地面 $0.14-0.24/W × 10-15× 空间放大） | HJT 采购价格链闭合度低于 GaAs（单独标注，非阻断）；5年-HJT 完整总成本"当前不可判定"（仅能给出下界 $473.01M）；HJT 未被 AI1 一手确认采用（非阻断） |
| 缺口 5：DoD 系统边界写乱（误写成光伏路线评价维度） | Task 5 | 电源边界修复说明 + 公式链重写 | 已解除 | DoD 已放回电池容量/质量/成本公式链（E_battery = P × t_eclipse / (DoD × η_discharge)）；明确 DoD 与 GaAs/HJT 的关系是经储能约束耦合，非直接评价光伏路线 | 无——此为表达边界问题，非证据链问题 |
| 缺口 6：三档系数缺乏外部证据 | Task 4（同缺口 1） | 参数重分级表：17 项三档参数全部逐条写清可迁移部分/不可迁移部分/迁移理由/区间依据 | 已解除 | 见参数准入清单 §4.2（V8-V19），每项三档参数均有独立的迁移理由和乐观/基准/保守区间依据 | 三档参数的不可迁移部分为系统性局限（非 AI1 一手数据），已在 Task V2 中逐参数经用户裁决 |
| 缺口 7：HJT 公开支撑数据搜索深度不足 | Task 3（同缺口 4） | 17 条搜索 URL + 多锚点交叉验证 | 已解除 | 效率链：华晟/东方日升/隆基（3 锚点）、辐照退化：CEA/INES + ISFH Caltec（2 锚点）、面密度：33FG Research + Starlink V2 Mini + 东方日升 50μm（3 锚点）、路线资格：Per Aspera + 雪球 + GF Securities（3 独立来源确认 Starlink 硅基路线） | "星链硅基太阳能电池"公开锚点仍非一手官方文档（非阻断）；Starlink 级实际采购价未公开 |
| 缺口 8：BOM 质量搜索深度不足以支撑 AI1 拆解 | Task 2 + Task 4 | bottom-up 质量链 + 参数重分级 | 已解除 | 计算载荷：GPU 模块质量由 HGX B200 基板反推（8 GPU 32 kg → ~4 kg/GPU 级别）；散热器面积一档 S-B 推导；其余子系统（平台/推进/通信/AIT）均为四档且已标注推断依据和失效风险 | 推进/通信质量的跨度均达 2x（推进 200→500 kg，通信 200→450 kg），反映推断不确定性的客观上限（非阻断）；"当前不可判定"项已显式标注 |
| 缺口 9：采购链搜索覆盖面不足 | Task 4 + Task 7 | 采购来源文档 + 价格 JSON 更新 + 参数重分级 §2 | 已解除 | 10 项价格参数全部重分级（三档 4 / 四档 5 / 禁止 1）；电池成本从禁止入模的 $400/kWh 修正为 V36 NMC $200/kWh（Starlink 直接迁移，三档）+ V37 LTO $260/350/400/kWh（四档等比压缩）；PCDU 成本从工程占位修正为 V26 $3k/5k/10k/kW（Terma 飞行产品锚点，四档）；计算载荷成本修正为 V12 $38k/60k/100k/kW（三档，3 轮搜索） | 散热成本（V13）和平台成本（V15）因循环引用（源自原 paper 内部假设）降为四档；通信成本（V28）为四档 Google Suncatcher 推断；PCDU 成本无公开价格锚点 |

## 三、计算载荷质量链

- **旧链（已废弃）**：`compute_payload_mass = 150 kW / (70/55/45 kW/t)` ——分母来源为二手媒体转述（B1 级），定义域存在根本性歧义（整星 vs 载荷），存在循环引用风险。三值（2143/2727/3333 kg）不再作为计算载荷质量的正式输入。
- **新链（已采用）**：GB300 NVL72 / HGX B200 / DGX B200 地面硬件基线 + 三项空间化增量（辐射防护 / 热管理改造 / 结构真空）。
- **地面硬件基线（二档/A1 锚点）**：
  - GB300 NVL72 计算托盘 29 kg（4 GPU + 2 CPU）——[Lenovo LP2357 Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai)
  - HGX B200 基板 32 kg（8 GPU）——[NVIDIA PCF Datasheet](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf)
  - DGX B200 完整系统 142.4 kg ——[NVIDIA DGX B200 User Guide](https://docs.nvidia.com/dgx/dgxb200-user-guide/introduction-to-dgxb200.html)
  - B200 TDP 1,000W/GPU → 150 GPU ≈ 150 kW → 38 托盘 × 29 kg ≈ 1,000-1,100 kg 地面裸硬件
- **空间化增量三项拆解**（V30，已通过 Task V2 用户裁决）：
  - 辐射防护：乐观 +30-50 kg（spot shielding，ACT Polymer Composite 支撑"比全铝机箱轻 70%"）、基准 +80-120 kg（混合策略 + SpaceX COTS 容错）、保守 +200-300 kg
  - 热管理改造：乐观 -50~+50 kg（继承地面液冷，去除空气冷却，JAXA HFE7200 热真空舱验证）、基准 +100-200 kg、保守 +250-400 kg
  - 结构/真空：乐观 +80-150 kg、基准 +150-250 kg、保守 +300-500 kg
- **空间化后总质量**：
  - light ~1,060-1,350 kg / baseline ~1,330-1,670 kg / conservative ~1,750-2,300 kg
- **证据等级**：二档（地面硬件锚点 A1）+ 三档（空间化增量推断）
- **源码锚点**：`stage2_mass_cost_model.py` 中 `compute_payload` 从 `components[compute_payload].scenario_mass_kg` 直接读取，不再经过 kW/t 分母计算

## 四、HJT 路线状态

- **旧定位**：只能降级 / `route_policy.forbidden_mainline` 包含 `"10y-HJT"` / 禁止进入主模型
- **新定位**：并行成熟路线，物理链可比较，与 GaAs 并列展示；价格链闭合度单独标注（非路线准入门槛）
- **HJT 物理链**：
  - BOL 效率：22%（华晟量产 >26% + 东方日升 26.61% + 隆基 27.81% × AM0 0.85 修正——用户从 22%/24%/25% 三候选选定最保守的 22%；EOL 14% 不随 BOL 上调而改变，为 CEA/INES 独立实验锚点）
  - EOL 效率：14%（CEA/INES 独立辐照实验：>14% after 10^14 e⁻/cm² 1MeV，ISFH Caltec 97% self-curing recovery）
  - 面密度面板级：1.8 kg/m²（面板+展开分列方案；上调自原值 1.2；Starlink V2 Mini 面板级反推 ~1.7-2.6 kg/m² 落入合理区间）
  - 证据等级：二档（效率链多锚点交叉验证）+ 三档（面密度为 Starlink 迁移）
- **HJT 价格链**：
  - 三档：地面量产 HJT $0.14-0.24/W（pmarketresearch、SolarInsightHub、PRNewswire 多源交叉验证）；空间级 ~$2-3/W（东方日升 50μm 14-21 RMB/W + 地面→空间放大 10-15×）
  - 闭合度单独标注：低于 GaAs（GaAs 有 AzurSpace 产品存在 + 旧口径 200-400 USD/W + satsearch 零售面板三锚点）
- **HJT 电源结果**（`stage2_power_system_results_blackwell_hjt.md`）：
  - 阵列面积 1295 m²，电源总质量 3.73 t（vs GaAs 625 m² / 2.34 t）
  - 阵列质量 2330 kg，电池 983 kg（共享），PCDU 419 kg（共享）
  - 物理上可比但系统代价明显更重：额外约 670 m² 阵列面积与 1.39 t 电源总质量

## 五、电池分支化

| 分支 | 化学 | 寿命 | DoD | 比能量 | 成本 | 证据等级 | 关键锚点 |
|------|------|------|-----|--------|------|---------|---------|
| 5yr NMC | Li-ion NMC | 5 年 | 40% | 190 Wh/kg | $200/kWh（固定） | 三档 Starlink 直接迁移 | Ray Barsa（SpaceX 首席电池工程师）演讲：max DOD ~50%，5,000 等效全循环，pack 级 230 Wh/kg，15 次部分放电/天；亿颗级 Panasonic 21700 采购；零溢价原则——Starlink pack 本身就是空间电池 |
| 10yr Li-ion NMC | Li-ion NMC | 10 年 | 25% | 190 Wh/kg | $200/kWh（固定） | 三档 | 19,800 次 eclipse × 25% = 4,950 等效全循环（在 Starlink 5,000 目标内）；Saft 文献：标准 Li-ion 需 20% DOD 达 50,000 循环 |
| 10yr LTO | LTO | 10 年 | 80% | 100 Wh/kg | $260/350/400/kWh | 四档等比压缩 | Saft LTO 白皮书：可 80-90% DOD 且超长循环寿命，比能量比 Li-ion 低 30-50%；地面 LTO/NMC 价格比 1.3-1.5× → 空间等比迁移；电池质量 916 kg（比 10yr Li-ion 方案轻约 40%） |

**电池成本裁决历程**：
- 旧注册表 $400/kWh → 禁止入模（与 satsearch €9,000/100Wh ≈ $90,000/kWh 数量级矛盾约 225 倍）
- V36 NMC $200/kWh → 用户采纳（Starlink 直接迁移，零额外溢价）
- V37 LTO $1,000-3,000/kWh 第一版 → 用户否决（"不应回到 Saft 传统认证定价"）→ 等比压缩法 → $260/350/400/kWh → 用户采纳

## 六、三分支经济结果摘要

> 源文件：`research_output/workspace/data/stage2_economic_branches_blackwell.md`（生成时间 2026-06-14T17:15:51）

| 分支 | 路线 | 电池 | 代数 | 单星质量 | 单星制造成本 | 10年总制造成本 | 10年总发射成本 | 10年总成本 | 状态 |
|------|------|------|------|---------|------------|-------------|-------------|----------|------|
| 10年-GaAs | GaAs | 10yr Li-ion NMC | 1 | 8.48 t | $83.61M | $696.72M | $14.13M | $764.98M | 主链完整——当前唯一可完整给出 10 年总成本的单代主链 |
| 5年-GaAs | GaAs | 5yr NMC | 2 | 7.10 t | $75.58M | $1,259.69M | $23.68M | $1,341.26M | 寿命敏感性对照——5 年寿命后自动坠毁并重射一次，制造成本近似翻倍 |
| 5年-HJT | HJT | 5yr NMC | 2 | 9.13 t | ≥$23.05M | ≥$384.13M | $30.44M | ≥$473.01M | 并行成熟路线——HJT 阵列采购价格链有三档锚点但闭合度低于 GaAs；当前仅能给出下界，完整总成本"当前不可判定" |

**补充**：
- 生命周期口径：以 1 MW 持续 IT 负载、10 年总窗口为共同分母；单代卫星当量 = 8.33
- 发射单价：$200/kg（统一假设）
- 总成本公式：制造成本 + 发射成本 + 保险（发射成本 × 8%）+ 运维（$5M/年 × 10 年）+ 退役/再入（$3M/代 × 代数）
- LTO 电池分支（10yr LTO，DoD 80%）为额外敏感性分支，未纳入主模型默认值

**10年-GaAs 基线单星拆解**（电池 10yr Li-ion NMC，DoD 25%）：

| 子系统 | 质量 | 制造成本 |
|------|------|------|
| 计算载荷 | 1,500 kg | $7.20M |
| 散热系统 | 550 kg | $0.66M |
| 光伏阵列 | 938 kg | $46.27M |
| 电池 | 1,573 kg | $0.06M |
| 功率电子/配电 | 419 kg | $1.05M |
| 平台/结构 | 1,743 kg | $6.27M |
| 推进 | 350 kg | $1.30M |
| 通信/激光链路 | 300 kg | $2.50M |
| 集成测试/冗余 | 1,106 kg | $18.29M |
| **合计** | **8,479 kg** | **$83.61M** |

## 七、参数准入统计

> 源文件：`research_output/workspace/data/stage2_parameter_admission_registry.md`

| 档位 | 数量 | 说明 |
|------|------|------|
| 一档（物理推导链，可直接入模） | 5 | solar_constant_w_m2 (1361.0)、radiator_area_m2 (110 m², S-B 推导)、array_area_m2 GaAs (624 m²)/HJT (1293 m²)、battery_nominal_kwh (186.4 kWh) |
| 二档（权威资料，首次引用需 AskUserQuestion） | 7 | peak_power_kw (150)、sustained_power_kw (120)、orbit_altitude_km (600)、array_efficiency_bol GaAs (0.32)、_eol (0.29)、_bol HJT (0.22)、_eol HJT (0.14) |
| 三档（可迁移证据） | 17 | V8-V19 及 P1-P4/P10：面密度 GaAs 1.5/HJT 1.8、DOD、比能量、计算载荷成本、散热成本、GaAs 阵列成本、平台成本、HJT 价格链、导出质量项 |
| 四档（合理推断） | 14 | V20-V29 及 V31-V35：散热器面密度、平台系数、推进质量/成本、通信质量/成本、AIT 裕量/成本、PCDU 比功率/成本、组件导出质量 |
| 禁止入模 | 1 | `battery_cost_per_kwh` 旧值 $400/kWh——与公开空间级电池列表价存在约 225 倍数量级矛盾；已替换为 V36 NMC $200/kWh + V37 LTO $260-400/kWh |
| 已废弃 | 3 | `compute_specific_power_kw_per_t` 三值 (70/55/45 kW/t) + `compute_payload` 旧质量值 (2143/2727/3333 kg) + HJT 旧路线资格（`forbidden_mainline` + `只能降级`） |
| **总计** | **47** | |

**V1-V37 用户裁决**：全部已裁决并锚定于 `current-note.md` §Task V2。裁决方式：每参数经搜索调研→证据整理→推导链展示→AskUserQuestion 用户裁决→锚定记录。关键裁决调整：
- V6 HJT BOL：20% → 22%（用户从 22%/24%/25% 三候选选定最保守）
- V9 HJT 面密度：1.2 → 1.8 kg/m²（面板+展开分列方案）
- V12 计算载荷成本：$28k/34k/45k → $38k/60k/100k/kW（3 轮搜索 + 用户选更低量产溢价）
- V13 + V15：散热成本和平台成本降为四档（循环引用）
- V25 PCDU 比功率：10.0 → 1.0/0.5/0.2 kW/kg（Terma 飞行产品揭示原值高估约 18×）
- V21 平台系数：0.18/0.22/0.28 → 0.25/0.35/0.45（Starlink V2 Mini 质量粗拆参考）
- V22 推进质量：180/220/350 → 200/350/500 kg（Starlink V2 Mini 推进占比参考）
- V23 通信质量：150/180/300 → 200/300/450 kg（4 轮搜索 + Google Suncatcher 参考）
- V27 推进成本：引入 0.6 次方缩放法则 + 寿命分支（用户亲自纠正线性缩放错误）
- V10 电池 DoD：从单一 40% → 5yr 40% / 10yr Li-ion 25% / 10yr LTO 80%（用户要求"不允许一刀切"）
- V36 电池成本 NMC：$200/kWh 固定（Starlink 直接迁移，零溢价）
- V37 电池成本 LTO：$260/350/400/kWh（等比压缩法）

## 八、已更新的文件清单

### 审计文档（Markdown）

- `research_output/workspace/data/stage2_gap_closure_verification.md` — 本文件
- `research_output/workspace/data/stage2_blackwell_payload_mass_bottom_up.md` — Task 2：bottom-up 计算载荷质量链
- `research_output/workspace/data/stage2_hjt_evidence_pack.md` — Task 3：HJT 并行路线证据包（17 条搜索 URL + 12 项物理链闭合）
- `research_output/workspace/data/stage2_parameter_admission_registry.md` — Task 4：47 参数逐条重分级与准入清单
- `research_output/workspace/data/stage2_power_boundary_and_formula_audit.md` — Task 5：电源系统边界修复与公式链审计
- `research_output/workspace/data/stage2_bom_mass_support_audit.md` — Task 6：BOM 质量支撑审计
- `research_output/workspace/data/stage2_procurement_price_sources.md` — Task 7：采购价格来源链审计
- `research_output/workspace/data/stage2_branch_mapping_from_previous_round.md` — 上一轮→本轮分支映射关系
- `research_output/workspace/data/stage2_evidence_routing_guide.md` — **人类可读的证据链路由手册**（结论→审计文档→JSON→V裁决→URL 五层追溯）
- `第二阶段差异分析初步研究.md`（项目根目录）— **第三轮刷新版**根目录交付物（2026-06-14 刷新，trace-id = cs2eg-root-deliverable-refresh-20260614-01）

### 结构化输入（JSON）

- `research_output/workspace/data/stage2_mass_inputs_blackwell_hjt.json` — Task 6 已更新：废弃 kW/t + PCDU 旧值 + 旧平台系数/旧推进/旧通信/旧 AIT 全部显式标注；新增 component 结构
- `research_output/workspace/data/stage2_cost_inputs_blackwell_hjt.json` — Task 7 已更新：V12/V26-V29/V36/V37 写入；V16 HJT 价格链修正；电池成本按 item_id 分支（`battery_cost_per_kwh_nmc` / `battery_cost_per_kwh_lto`）；分寿命 branch 字段

### Python 模型脚本

- `research_output/workspace/scripts/stage2_power_system_model.py` — Task 8 重建：固定 Blackwell 主线，GaAs/HJT 并行，废弃 kW/t 链，计算载荷质量从 `components[compute_payload].scenario_mass_kg` 直接读取
- `research_output/workspace/scripts/stage2_mass_cost_model.py` — Task 8 重建：三分支经济模型，电池分支化（5yr/10yr Li-ion/LTO），新 item_id 引用

### 生成的 Markdown 结果文档

- `research_output/workspace/data/stage2_power_system_results_blackwell_hjt.md` — Task 8 输出：Blackwell 主线电源系统结果（GaAs 主链 + HJT 并行路线）
- `research_output/workspace/data/stage2_economic_branches_blackwell.md` — Task 8 输出：三分支经济模型结果

### 废弃归档

- `research_output/workspace/data/_deprecated/` — 旧版文件归档目录（含 `README.md` 说明废弃原因与替代文件）
  - `_deprecated/stage2_mass_cost_results.md` — 已替代（基于 kW/t 链）
  - `_deprecated/stage2_power_system_results.md` — 已替代（不含 HJT 并行路线）
  - `_deprecated/stage2_architecture_reconciliation.md` — 已降级（Rubin 不再进入主模型）

- `.trae/specs/close-stage-two-evidence-gaps/spec.md` — 本 Spec 需求定义
- `.trae/specs/close-stage-two-evidence-gaps/tasks.md` — 任务拆分
- `.trae/specs/close-stage-two-evidence-gaps/checklist.md` — 验收清单
- `.trae/specs/close-stage-two-evidence-gaps/current-note.md` — 跨 Task 状态交接与裁决记录（V1-V37 全部裁决已锚定）

## 九、残余缺口（未闭合）

### 物理链仍缺口

| # | 条目 | 等级 | 是否可转入下一轮 | 说明 |
|---|------|------|----------------|------|
| R1 | AI1 一手总质量与收拢尺寸仍缺权威锚点 | 非阻断 | 是（残余风险继承） | 通过 Task 2 bottom-up 质量链部分缓解（地面硬件锚点 + 空间化增量），但无法闭合到一手总质量 |
| R2 | AI1/Starlink 一手太阳能路线、真实阵列面密度、真实空间级硅量产与寿命、真实采购价仍缺公开锚点 | 非阻断 | 是（残余风险继承） | Task 3 HJT 证据包部分补强，但不保证闭合到一手数据 |
| R3 | "Rubin 化后整星 BOM、寿命和辐射加固成本可否同步改善"仍缺一手数据 | 非阻断 | 是（支线） | Rubin 已降级为支线留痕，本轮未深化 |

### 采购链仍缺口

| # | 条目 | 等级 | 是否可转入下一轮 | 说明 |
|---|------|------|----------------|------|
| R4 | HJT 阵列采购价格链完整总成本"当前不可判定" | 非阻断 | 是（并行路线，非主线阻断） | 有三档锚点（地面 $0.14-0.24/W × 10-15×），但闭合度低于 GaAs；5年-HJT 仅能给出下界 $473.01M |
| R5 | 散热成本（V13）和平台成本（V15）降为四档——源自原 paper 内部假设（循环引用），缺少外部独立锚点 | 非阻断 | 是 | 已在 Task V2 中经用户裁决确认降级；材料级锚点存在（散热材料 $250-1,850/m²），但缺少系统级直接锚点 |
| R6 | 通信成本（V28 $1.5M/2.5M/4.0M）和 PCDU 成本（V26 $3k/5k/10k/kW）均为四档推断，无公开采购价格锚点 | 非阻断 | 是 | Google Suncatcher（arXiv preprint）支撑通信方向但非飞行验证；Terma PCDU 飞行产品存在但价格未公开 |
| R7 | 推进成本（V27）基于 Starlink 雪球分析反向估计 + 0.6 次方缩放法则（经验法则非物理定律） | 非阻断 | 是 | 用户亲自纠正线性缩放错误并引入 0.6 次方法则；Starlink 推进成本 "$125-250k" 为雪球分析口径 |

### 当前不可判定

| # | 条目 | 连续检查点 | 说明 |
|---|------|----------|------|
| R8 | 10年-GaAs 当前只把"寿命延长后不重射"写入总账，没有额外假定公开可证实的 10 年寿命增重或增价因子 | 1 | 属于保守占位，不是已证实硬件事实；需下一轮明确标注 |
| R9 | 电池与 PCDU 单价继续沿用合理推断/迁移证据（三档/四档），所有分支的成本链仍需保留"非一手采购价"的降级标签 | 1 | 系统性局限，非个别参数可闭合；已在结果文档中显式标注 |

## 十、下一轮可行性汇总入口

### 推荐基线

- **10年-GaAs**（电池 10yr Li-ion NMC）：当前唯一可完整给出 10 年总成本的单代主链（$764.98M）
  - 质量链：地面硬件 A1 锚点 + 三项空间化增量（二档+三档）
  - 电源链：GaAs 主链基准（AzurSpace 4G32 二档 + 面密度三档）
  - 价格链：阵列成本三档 / 电池成本三档（Starlink 迁移）/ PCDU 成本四档

### 敏感性分支

- **5年-GaAs**（电池 5yr NMC）：寿命敏感性对照（$1,341.26M，为 10年-GaAs 的 1.75×）
- **10年 LTO**（电池 10yr LTO，DoD 80%）：电池质量更轻（916 kg vs 1,573 kg）但单价更高（$350/kWh vs $200/kWh），为额外敏感性分支

### 并行路线

- **HJT**（5年-HJT）：物理链已完成并行比较（1295 m² vs 625 m²，3.73 t vs 2.34 t）；总成本仅能给出下界（≥$473.01M），完整成本待 HJT 阵列采购价格链进一步闭合

### 待闭合的价格链项（转入下一轮但不阻断）

1. HJT 阵列采购价：地面→空间放大因子（10-15×）需更精确的产业分析或可比交易锚点
2. 散热系统成本（V13）：需突破原 paper 内部假设的循环引用，寻找独立系统级锚点
3. 平台结构成本（V15）：同上
4. 通信系统成本（V28）：Google Suncatcher 为研究论文，需飞行验证或产业采购参考
5. PCDU 成本（V26）：Terma 产品存在但价格未公开，可尝试通过 ESA/NASA 公开合同数据获取可比价格

---

> **本审计包可作为下一轮可行性汇总（feasibility assessment）的直接输入底座。**

> **文档状态**：Task 8 产出物 v1.0。所有关键数字均附带证据档位标注。三种认知层级（已知事实 / 可计算链 / 当前不可判定）已显式区分。未提前写可行性倾向结论。
