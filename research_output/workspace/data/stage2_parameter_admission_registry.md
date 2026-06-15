# Stage 2：参数重分级与准入清单

> 生成时间：2026-06-14
> 对应 Task：Task 4（参数重分级与准入清单）
> 输入文件：
> - `stage2_mass_inputs_blackwell_hjt.json`（质量参数，common_inputs + route_sensitive_inputs + components）
> - `stage2_cost_inputs_blackwell_hjt.json`（采购价格参数，10 items）
> - `stage2_blackwell_payload_mass_bottom_up.md`（Task 2：新 bottom-up 质量链）
> - `stage2_hjt_evidence_pack.md`（Task 3：HJT 并行成熟路线证据包）
>
> 证据分级规则：Task V1 冻结版四档体系（一档物理推导链 / 二档权威资料 / 三档可迁移证据 / 四档合理推断 / 禁止入模）

---

## 0. 总体概览

### 0.1 统计

| 类别 | 计数 |
|---|---|
| 已扫描参数总数（leaf input + 独立组件 + 独立价格项） | **47** |
| 一档（物理推导链，可直接入模） | **5** |
| 二档（权威资料，首次引用需 AskUserQuestion） | **7** |
| 三档（可迁移证据，首次引用需 AskUserQuestion） | **17** |
| 四档（合理推断，首次引用需 AskUserQuestion） | **14** |
| 禁止入模 | **1** |
| 已废弃/已替换 | **3** |

### 0.2 准入状态统计

| 准入状态 | 计数 | 说明 |
|---|---|---|
| **可直接入模** | 5 | 一档物理链参数，无需请示 |
| **待用户裁决** | 38 | 二/三/四档参数，需在 Task V2 中 AskUserQuestion |
| **禁止入模** | 1 | `battery_cost_per_kwh` 当前值 $400/kWh 远低于空间级电池列表价 |
| **已废弃/已替换** | 3 | `compute_specific_power_kw_per_t` (70/55/45) + `compute_payload` 旧质量值 + `hjt_route_cost_chain` 旧禁止状态 |

---

## 1. 质量参数逐条分级

### 1.1 公共输入参数（Public Baseline）

| # | 参数名 | 当前值 | 旧 evidence_grade | 旧 status | 新档位 | 分级理由 |
|---|---|---|---|---|---|---|
| M1 | `peak_power_kw` | 150.0 | — | — | **二档** | 来自多家二手媒体交叉转述（Inkl/Tom's Hardware、Knightli、Indexbox），引用同一原始报道口径。多源交叉一致但非官方规格表。 |
| M2 | `sustained_power_kw` | 120.0 | — | — | **二档** | 同上；120 kW sustained 为多源一致口径（80% of 150 kW peak）。 |
| M3 | `orbit_altitude_km` | 600.0 | — | — | **二档** | 来自上述媒体转述，非 FCC/ITU 官方申报参数。600 km 圆形轨道为多家媒体一致口径。 |
| M4 | `radiator_area_m2` | 110.0 | — | — | **一档** | 经 Stefan-Boltzmann 定律直接推导：A = P_rad / (εσT⁴)。散热通量工作点约 1400 W/m²（详见 `stefan_boltzmann_results.txt`），110 m² = 150 kW / 1.364 kW/m²。公式链完整，工程假设（T、ε）在合理约束内。 |
| M5 | `solar_constant_w_m2` | 1361.0 | — | — | **一档** | 物理常数（ASTM E-490 AM0 标准太阳常数），无需外部来源。 |

### 1.2 公共输入参数（Scenario Scalars → 已废弃项）

| # | 参数名 | 旧值（light/baseline/conservative） | 旧 evidence_grade | 旧 status | 新判定 | 理由 |
|---|---|---|---|---|---|---|
| M6 | `compute_specific_power_kw_per_t` | 70 / 55 / 45 | B1 + C（旧链） | 已闭合（旧） | **已废弃** | Task 2 的 bottom-up 质量链已证明：(a) `70 kW/t` 来源为二手转述（B1 级），非 NVIDIA 或 SpaceX 官方规格；(b) 该比率的定义域（整星 vs 载荷）存在根本性歧义；(c) 存在潜在循环引用风险（kW/t 可能从总质量反算）。三者均被新 bottom-up 链替代，不再作为独立输入。废弃不等于 2,143/2,727/3,333 kg 整星质量情景被废弃——仅废弃 kW/t 分母作为计算载荷质量的推导路径。 |

### 1.3 公共输入参数（Scenario Scalars → 非废弃项）

| # | 参数名 | 当前值（light/baseline/conservative） | 旧 evidence_grade / status | 新档位 | 分级理由 |
|---|---|---|---|---|---|
| M7 | `radiator_specific_mass_kg_per_m2` | 4.0 / 5.0 / 6.5 | B1 + C / 已闭合 | **四档** | 散热器面密度属于工程占位值。mass JSON 原始备注："散热器面密度仍属工程占位，未获得 AI1 一手热控结构规格"。无可追溯的 AI1 散热器面密度公开数据，仅能从通用航天器热控结构面密度范围（3-8 kg/m²）做工程推断。 |
| M8 | `platform_ratio` | 0.18 / 0.22 / 0.28 | B1/C / 只能降级 | **四档** | 平台/结构质量占比系数，由子系统求和比例 + 可比平台量级参考得出。无物理公式可直接推导此比值；可比平台映射关系并非一对一（Psyche 任务平台、卫星总线对比仅为量级参考）。mass JSON 备注："缺 AI1 平台级一手分项或可靠可比平台映射关系"。 |
| M9 | `propulsion_mass_kg` | 180 / 220 / 350 | B1/C / 只能降级 | **四档** | 基于公共推进组件量级（Orbion、ExoTerra 推力器）和任务场景的强推断，但未获得 AI1 推进剂类型、贮箱规模、寿命目标与机动预算。范围跨度 180→350 kg（近 2x）反映了推断的不确定性。 |
| M10 | `comms_mass_kg` | 150 / 180 / 300 | B1/C / 只能降级 | **四档** | 基于公开激光通信终端量级（NASA SoA、TESAT、FSO Instruments）和多终端系统的强推断，但缺 AI1 终端数量、天线构型、云台与 RF/激光并行架构信息。范围跨度 150→300 kg（2x）。 |
| M11 | `ait_margin_ratio` | 0.10 / 0.12 / 0.18 | C / 只能降级 | **四档** | 纯项目级系统裕量系数，不是独立硬件实测值。mass JSON 备注："该项不是独立硬件实测值，只能作为工程保守量保留"。无物理公式或权威来源可支撑具体取值。 |

### 1.4 路线敏感参数（GaAs 基线）

| # | 参数名 | 当前值 | 旧 evidence_grade | 旧 status | 新档位 | 分级理由 |
|---|---|---|---|---|---|---|
| M12 | `array_efficiency_bol` (GaAs) | 0.32 | A2/B1 + C | 已闭合 | **二档** | AzurSpace 4G32 32% class 产品规格（URL：`azurspace.com/en/products/space-products/`），辐射加固空间级三结电池。厂商公开数据表，可回查。 |
| M13 | `array_efficiency_eol` (GaAs) | 0.29 | A2/B1 + C | 已闭合 | **二档** | 由 BOL 32% × 约 9.4% 退化率（LEO 10 年典型 GaAs 退化）推导。退化率来自 III-V 空间电池公开辐射测试文献，为行业共识值。 |
| M14 | `array_specific_mass_kg_per_m2` (GaAs) | 1.5 | A2/B1 + C | 已闭合 | **三档** | 空间级刚性 GaAs 面板面密度行业参考区间为 1.5-2.5 kg/m²，模型取值 1.5 处于低端（轻量化设计假设）。非 AI1 一手规格，属于从行业可比产品迁移。 |
| M15 | `battery_dod` | 0.40 (shared) | B1 + C | 已闭合 | **三档** | 40% DOD 为 LEO 长寿命任务的行业经验值（典型范围 20-40%）。非物理定律推导，也非 AI1 电池管理系统公开参数。 |
| M16 | `battery_specific_energy_wh_per_kg` | 190.0 (shared) | B1 + C | 已闭合 | **三档** | 基于公开空间级电池产品参数（satsearch：ICP25 155 Wh/kg 等）。190 Wh/kg 处于当前空间锂离子电池的典型上界，代表较优产品选型。非 AI1 一手电池选型数据。 |
| M17 | `pcdu_specific_power_kw_per_kg` | 10.0 (shared) | C | 只能降级 | **四档** | 纯工程占位值。mass JSON 备注："缺公开空间级 PCDU 质量与单价锚点，只能作为占位输入"。satsearch 上存在高功率 PCDU 产品（Exa Colossus 400-8000 W-hr），但无公开质量/比功率数据。 |

### 1.5 路线敏感参数（HJT 探索性路线 → 路线定位修正）

> **路线定位修正说明**（依据 Task 3 证据包）：
> - 旧 metadata 中 `route_policy.forbidden_mainline` 包含 `"10y-HJT"`，HJT 状态标记为 `"只能降级"`。
> - Task 3 证据包已提供 17 条搜索 URL + 12 项物理链闭合清单，将 HJT 从"只能降级、禁止进入主模型"修正为 **与 GaAs 并行的成熟技术路线**。
> - 以下参数分级反映修正后的定位：HJT 物理链项为二档/三档，但路线整体定位已从"禁止"改为"并行"。

| # | 参数名 | 当前值 | 旧 evidence_grade | 旧 status | 新档位 | 分级理由 |
|---|---|---|---|---|---|---|
| M18 | `array_efficiency_bol` (HJT) | 0.20 | A2 + C | 只能降级 | **二档** | 多家权威来源交叉验证：华晟量产 >26% 电池效率（Huasun 官网）、东方日升 26.61% 认证量产（PRNewswire 官方新闻稿）、隆基 27.81% 实验室纪录（LONGi 官网）。模型取值 20% 为保守工程选取（考虑 AM0 修正和空间级降额），在权威证据的保守区间内。 |
| M19 | `array_efficiency_eol` (HJT) | 0.14 | A2 + C | 只能降级 | **二档** | 直接对应 CEA/INES 官方认证结果：>14% after 10^14 e-/cm² 1 MeV 电子辐照（ISFH Caltec 独立认证）。公式链：20% BOL × (1 - 退化) ≈ 14% EOL，与 CEA 测量值一致。 |
| M20 | `array_specific_mass_kg_per_m2` (HJT) | 1.2 | A2 + C | 只能降级 | **三档** | 来自多源比较：Starlink V3-like 刚性基线 3.0 kg/m² vs V1 Starthink 柔性迭代 1.5 kg/m² vs 未来最优 1.0 kg/m²（33FG Research）。1.2 kg/m² 处于合理区间，但非 AI1 一手规格。柔性硅基阵列面密度由封装路径（刚性/半刚性/柔性展开）决定，当前无法确认 AI1 的具体封装方案。 |
| M21 | `battery_dod` (HJT, shared) | 0.40 | — | — | **三档** | 同 M15，GaAs/HJT 共享。 |
| M22 | `battery_specific_energy_wh_per_kg` (HJT, shared) | 190.0 | — | — | **三档** | 同 M16，GaAs/HJT 共享。 |
| M23 | `pcdu_specific_power_kw_per_kg` (HJT, shared) | 10.0 | — | — | **四档** | 同 M17，GaAs/HJT 共享。 |

### 1.6 路线敏感参数中的导出量

> 以下为从上述 leaf input 通过物理公式导出的中间量，不独立分级。列入供完整性追溯。

| 导出量 | 公式 | 值 (GaAs / HJT) | 继承档位 |
|---|---|---|---|
| `array_area_m2` | P / (G × η) | 624 / 1293 | **一档**（面积公式为纯物理推导，但 BOL 效率输入为二档，整体链为二档） |
| `array_mass_kg` | area × specific_mass | 936 / 1552 | **三档**（面积物理推导 × 面密度三档迁移） |
| `battery_nominal_kwh` | P × t_eclipse / DOD | 186.4 / 186.4 | **一档**（轨道力学 eclipse 时间 + 任务功率，公式链封闭，但 DOD 为三档） |
| `battery_mass_kg` | kWh / specific_energy | 981 / 981 | **三档**（kWh 一档链 × 比能量三档） |
| `pcdu_mass_kg` | P / specific_power | 21 / 21 | **四档**（功率二档 × 比功率四档占位） |
| `total_power_mass_kg` | sum of above | 1938 / 2554 | 取最低档 = **四档**（受 PCDU 四档拖累） |

### 1.7 组件级参数（质量）

| # | 组件 | 旧值 (light/baseline/conservative) kg | 旧 grade | 旧 status | 新档位 | 分级理由 |
|---|---|---|---|---|---|---|
| C1 | `compute_payload` | 2143 / 2727 / 3333 | B1 + C | 已闭合 | **已废弃** | 旧值由 `150 kW / (70/55/45 kW/t)` 派生，分母已废弃（见 M6）。替换为新 bottom-up 链（Task 2）：~900-1200 / ~1400-1800 / ~2000-2400 kg。新链核心锚点（HGX B200 32 kg、GB300 托盘 29 kg）为 A1 级，空间化增量系数为三/四档，新链整体为 **二档+三档**。 |
| C2 | `thermal` | 440 / 550 / 715 | B1 + C | 已闭合 | **四档** | 面积为一档（Stefan-Boltzmann），但面密度为四档工程占位（见 M7）。整体受最弱链节约束。 |
| C3 | `solar_array` | 936 (GaAs) / 1552 (HJT) | A2/B1 + C | 已闭合 | **三档** | 面积为一档物理推导，面密度为三档迁移（见 M14/M20）。 |
| C4 | `battery` | 981 (shared) | B1 + C | 已闭合 | **三档** | kWh 为一档轨道力学链，比能量为三档（见 M16）。 |
| C5 | `pcdu` | 21 (shared) | C | 只能降级 | **四档** | 比功率为四档工程占位（见 M17），无可追溯质量锚点。 |
| C6 | `platform_structure` | 698 / 1147 / 2047 | B1/C | 只能降级 | **四档** | 由 platform_ratio × (子系统和) 得出，platform_ratio 为四档推断（见 M8）。缺乏 AI1 平台级一手分项。 |
| C7 | `propulsion` | 180 / 220 / 350 | B1/C | 只能降级 | **四档** | 强推断值（见 M9），范围跨度近 2x。有公开推力器量级锚点，但缺 AI1 任务剖面确认。 |
| C8 | `communications` | 150 / 180 / 300 | B1/C | 只能降级 | **四档** | 强推断值（见 M10），范围跨度 2x。有公开终端量级锚点，但缺 AI1 架构信息。 |
| C9 | `ait_margin` | 491 / 812 / 1801 | C | 只能降级 | **四档** | 纯工程裕量（见 M11），不是独立硬件实测值。 |

---

## 2. 采购价格参数逐条分级

| # | 参数名 | 旧 item_id | 当前值 | 旧 evidence_grade | 旧 source_type | 新档位 | 分级理由 |
|---|---|---|---|---|---|---|---|
| P1 | `compute_payload_cost_per_kw` | `compute_payload_cost_per_kw` | $28,000 / 34,000 / 45,000 /kW | B2+C | 情景参数 | **三档** | 由地面 GPU 机柜成本锚点（地面 GPU 硬件 22-28 MUSD/MW）与空间化溢价换算。可迁移部分：地面 GPU 硬件采购价有公开锚点（GB300 NVL72 3-4 MUSD/柜，约 120 kW）。不可迁移部分：空间化溢价（辐照加固筛选、真空封装、低批量溢价、测试认证）的放大因子无一手数据支撑。 |
| P2 | `thermal_cost_per_m2` | `thermal_cost_per_m2` | $5,000 / 6,000 / 8,000 /m² | B2+C | 情景参数 | **三档** | 由 1 MW 轨道散热系统基准成本 3.5 MUSD 与物理散热面积反算。可迁移部分：散热面积为 Stefan-Boltzmann 一档推导。不可迁移部分：3.5 MUSD/1MW 的散热系统总包成本来自既有商业稿，非 AI1 实际采购数据；散热系统成本是否随面积线性缩放存疑。 |
| P3 | `gaas_array_cost_per_bol_w` | `gaas_array_cost_per_bol_w` | $180 / 200 / 250 /W_BOL | A2+B2+C | 情景参数 | **三档** | 锚点：AzurSpace 4G32 产品（存在但无公开批量价）、空间光伏旧口径 200-400 USD/W、satsearch 小型零售面板。当前值代表"规模化工程情景"而非公开零售价。不可迁移部分：小批量零售价（>400 USD/W）向大批量工程价的缩放关系不明，当前 180-250 低于已知零售价，其规模化假设幅度无法独立验证。 |
| P4 | `platform_structure_cost_per_kg` | `platform_structure_cost_per_kg` | $2,800 / 3,600 / 5,000 /kg | B2+C | 情景参数 | **三档** | 由 1 MW 平台包 30 MUSD ÷ 约 1147 kg 平台质量反算。可迁移部分：30 MUSD 平台包有本地分析支撑。不可迁移部分：平台包总价非分包商报价，"每 kg"的线性假设未经分包报价验证；平台结构成本是否包含全部平台子系统（推进、通信、姿控等）存疑。 |
| P5 | `battery_cost_per_kwh` | `battery_cost_per_kwh` | $400 /kWh | C | 待替换参数 | **禁止入模** | 当前 $400/kWh 为脚本常量，与公开空间级电池列表价存在数量级矛盾：satsearch 上 100 Wh 模块列表价 €9,000（≈$90,000/kWh），当前值低约 225 倍。参数本身有存在价值（空间级电池采购价是必要的模型输入），但**当前具体数值无任何支撑且被公开证据直接反驳**，必须替换后才能入模。建议以 satsearch 锚点重新估计（三档区间）后提交用户裁决。 |
| P6 | `pcdu_cost_per_kw` | `pcdu_cost_per_kw` | $5,000 / 7,000 / 10,000 /kW | C | 待替换参数 | **四档** | 公开产品（Exa Colossus PCDU 400-8000 W-hr）只能证明设备存在，未取得任何公开价格。当前值完全为工程估计，无价格锚点支撑。satsearch 列表均无价格字段。 |
| P7 | `propulsion_total_cost_per_sat` | `propulsion_total_cost_per_sat` | $400,000 / 600,000 / 900,000 /sat | C | 待替换参数 | **四档** | 当前仅有本地工程分摊，无可追溯报价链。推进系统成本取决于推进剂类型（电推/化学）、推力器数量和冗余配置，AI1 的这些参数均未知。 |
| P8 | `comms_total_cost_per_sat` | `comms_total_cost_per_sat` | $800,000 / 1,200,000 / 2,000,000 /sat | C | 待替换参数 | **四档** | 仅有激光通信终端存在性锚点（AAC Clyde CubeCAT），无公开可比价格。光学终端价格与数据率、指向精度、冗余度高度相关，AI1 的通信架构未公开。 |
| P9 | `ait_cost_ratio` | `ait_cost_ratio` | 0.15 / 0.18 / 0.28 | C | 非采购系数 | **四档** | 系统级集成/筛选/冗余/验证成本系数，非单件采购价。属于项目管理和系统工程范畴的工程裕量。无独立可验证的外部基准。 |
| P10 | `hjt_route_cost_chain` | `hjt_route_cost_chain` | status: "missing" | A2 (技术) | 禁止进入主模型 | **三档** | **路线定位修正**（依据 Task 3 证据包）：旧判定为"禁止进入主模型"，现修正为三档可迁移价格。地面量产 HJT 组件 $0.14-0.24/W 为二档（pmarketresearch、SolarInsightHub 交叉验证）。东方日升 50μm 空间级 HJT 电池 14-21 RMB/W（≈$2-3/W）为三档（雪球/产业分析口径）。地面→空间放大倍数约 10-15x。不可迁移部分：空间级 HJT 的封装/筛选/认证成本分解尚缺独立公开数据；Starlink 级阵列实际采购价仅有产业分析口径。 |

---

## 3. 可直接入模清单（一档参数，无需请示）

| # | 参数名 | 值 | 物理推导链 | 位置 |
|---|---|---|---|---|
| A1 | `solar_constant_w_m2` | 1361.0 W/m² | ASTM E-490 AM0 标准太阳常数，公认物理常数 | mass JSON: `common_inputs.public_baseline` |
| A2 | `radiator_area_m2` | 110.0 m² | Stefan-Boltzmann: A = P_rad/(εσT⁴)，P_rad ≈ 150 kW，热通量工作点 ≈ 1400 W/m² | mass JSON: `common_inputs.public_baseline` |
| A3 | `array_area_m2` (GaAs) | 624 m² | A = P_solar / (G × η_BOL × degradation_factor)，P=150 kW，G=1361 W/m²，η=0.32 | mass JSON: `route_sensitive_inputs.gaas_baseline` |
| A4 | `array_area_m2` (HJT) | 1293 m² | 同上公式，η=0.20 | mass JSON: `route_sensitive_inputs.hjt_exploratory` |
| A5 | `battery_nominal_kwh` | 186.4 kWh | E = P_sustained × t_eclipse / DOD，P=120 kW，t_eclipse 由 600 km 轨道力学确定，DOD=0.40 | mass JSON: `route_sensitive_inputs.*.battery_nominal_kwh` |

> 注：A3-A5 的推导链包含非一档输入（效率为二档、DOD 为三档），因此其**数值精度**受上游输入约束。但**公式本身**为一档物理推导，可在任何上游参数更新后自动重算。

---

## 4. 待用户裁决清单（Task V2 输入）

> 以下参数按档位分组。每个参数首次写入模型分析链时，必须通过 AskUserQuestion 向用户请示。

### 4.1 二档参数（权威资料，需首次引用裁决）

| # | 参数名 | 档位 | 当前值 | 权威来源 | URL | 用途 |
|---|---|---|---|---|---|---|
| V1 | `peak_power_kw` | 二档 | 150.0 | Inkl/Tom's Hardware、Knightli、Indexbox 多源交叉转述 | 见 mass JSON 中 `source_urls[]` | 整星功率基线，所有电源/散热推导的起点 |
| V2 | `sustained_power_kw` | 二档 | 120.0 | 同上 | 同上 | 电池容量、轨道 eclipse 功耗推导 |
| V3 | `orbit_altitude_km` | 二档 | 600.0 | 同上 | 同上 | 轨道 eclipse 时长、辐射环境推导 |
| V4 | `array_efficiency_bol` (GaAs) | 二档 | 0.32 | AzurSpace 4G32 产品规格 | `azurspace.com/en/products/space-products/` | GaAs 阵列面积与质量推导 |
| V5 | `array_efficiency_eol` (GaAs) | 二档 | 0.29 | III-V 空间电池退化文献（行业共识） | 退化率来自公开辐射测试 | GaAs EOL 功率输出推导 |
| V6 | `array_efficiency_bol` (HJT) | 二档 | 0.20 | 华晟 26%+（官网）、东方日升 26.61%（PRNewswire）、隆基 27.81%（官网） | 见 HJT 证据包 §2.1 | HJT 阵列面积与质量推导 |
| V7 | `array_efficiency_eol` (HJT) | 二档 | 0.14 | CEA/INES 认证（ISFH Caltec） | `cea.fr/cea-tech/liten/...`、`ines-solaire.org/...` | HJT EOL 功率输出推导 |

**V1-V3 裁决提示**：这三个参数来自二手媒体转述，非 SpaceX/NVIDIA 官方规格表。若后续获取官方 FCC/ITU 申报数据，可直接升级为一档。

**V6-V7 裁决提示**：HJT 效率参数已获 Task 3 多锚点交叉验证。V6 的 20% 是模型保守选取值（权威证据区间为 16-27%），V7 的 14% 直接对应 CEA/INES 认证值。建议确认是否接受 20%/14% 作为 HJT 并行路线的效率基线。

### 4.2 三档参数（可迁移证据，需首次引用裁决 + 迁移理由）

| # | 参数名 | 档位 | 当前值 | 迁移理由 | 乐观/基准/保守区间依据 | 不可迁移部分 |
|---|---|---|---|---|---|---|
| V8 | `array_specific_mass_kg_per_m2` (GaAs) | 三档 | 1.5 | 空间级刚性 GaAs 面板面密度行业区间为 1.5-2.5 kg/m²。AzurSpace 等厂商提供电池级产品但无系统级面板面密度公开数据。1.5 取行业区间的低端，对应轻量化设计假设。 | 乐观 1.2（超轻基板）/ 基准 1.5 / 保守 2.5（标准刚性面板） | 无 AI1 面板设计一手规格（基板材料、蜂窝结构、展开机构集成方式） |
| V9 | `array_specific_mass_kg_per_m2` (HJT) | 三档 | 1.2 | 33FG Research 给出 Starlink 级硅基阵列面密度区间 1.0-3.0 kg/m²。东方日升 50μm P-HJT 比功率 2 W/g 等效面密度约 0.5 kg/m²（仅电池），封装/展开机构另计。1.2 取"计算优化柔性迭代"(V1 Starthink) 和"未来最优"(V2) 之间的合理值。 | 乐观 1.0（最优柔性封装）/ 基准 1.2 / 保守 3.0（刚性 Starlink V3 级） | HJT 空间级封装的精确面密度取决于展开机构类型（柔性展开 vs 刚性面板），当前无法确认 AI1 方案 |
| V10 | `battery_dod` | 三档 | 0.40 | LEO 长寿命任务行业典型 DOD 范围为 20-40%。40% 代表较激进的使用策略（更小电池质量，更高循环应力）。可迁移自：GEO 通信卫星通常 20-30% DOD、ISS 锂离子电池约 30-35% DOD、Starlink 级 LEO 星座为降低质量可能采用 40%。 | 乐观 0.50（激进）/ 基准 0.40 / 保守 0.30（行业常规） | AI1 的电池化学体系和 BMS 策略未知；DOD 与循环寿命的 trade-off 未建模 |
| V11 | `battery_specific_energy_wh_per_kg` | 三档 | 190.0 | 公开空间级锂离子电池产品参数：ICP25 155 Wh/kg（satsearch）、BAT600-P3 100 Wh 模块。190 Wh/kg 处于当前空间级锂离子电池典型范围上界，对应高性能选型。 | 乐观 210（下一代）/ 基准 190 / 保守 155（ICP25 级） | 非 AI1 实际选型数据；空间级电池的实际 pack 级比能量低于 cell 级 |
| V12 | `compute_payload_cost_per_kw` | 三档 | $28,000 / 34,000 / 45,000 /kW | 可迁移：地面 GPU 硬件采购价有公开锚点（GB300 NVL72 3-4 MUSD/柜）。空间化溢价参考卫星电子设备的地面→空间成本放大因子（典型 3-10x）。 | 乐观 $22,000（3x 放大）/ 基准 $34,000 / 保守 $50,000（10x 放大，含冗余） | 空间化溢价的具体构成（辐照加固筛选损失率、真空封装成本、低批量工程溢价）无一手数据 |
| V13 | `thermal_cost_per_m2` | 三档 | $5,000 / 6,000 / 8,000 /m² | 可迁移：1 MW 轨道散热系统总包 3.5 MUSD（商业分析）。面积由 Stefan-Boltzmann 一档推导。 | 乐观 $4,000（规模化效应）/ 基准 $6,000 / 保守 $10,000（高可靠性需求） | 散热系统成本是否与面积线性缩放（管路、泵、工质的非线性部分）；3.5 MUSD 非 AI1 实际采购数据 |
| V14 | `gaas_array_cost_per_bol_w` | 三档 | $180 / 200 / 250 /W_BOL | 可迁移：空间光伏旧口径 200-400 USD/W。satsearch 零售面板价可作锚点。AzurSpace 产品技术存在但无批量价。 | 乐观 $150（大批量+自动化）/ 基准 $200 / 保守 $300（传统小批量采购） | 小批量零售→大批量工程价的缩放关系；当前值低于已知零售下限，规模化假设幅度不可验证 |
| V15 | `platform_structure_cost_per_kg` | 三档 | $2,800 / 3,600 / 5,000 /kg | 可迁移：1 MW 平台包 30 MUSD ÷ 1147 kg。30 MUSD 有本地分析支撑。 | 乐观 $2,000（简化平台）/ 基准 $3,600 / 保守 $6,000（复杂深空级平台） | 平台包总价非分包商报价；"每 kg"线性假设未经验证；平台包是否包含推进/通信/姿控等全部子系统存在歧义 |
| V16 | `hjt_route_cost_chain` | 三档 | 地面 $0.14-0.24/W；空间 ~$2-3/W | 可迁移：地面 HJT 量产价格链完整（pmarketresearch、SolarInsightHub、PRNewswire 多源交叉验证）。东方日升空间级 50μm 14-21 RMB/W 提供电池级价格锚点。地面→空间放大 10-15x（参考卫星电子设备通用放大因子）。 | 乐观 $1.5/W（量产降本+简化封装）/ 基准 $2.5/W / 保守 $5/W（传统空间级认证路径） | 空间级 HJT 封装/筛选/认证成本分解无独立数据；东方日升价格来源为三档产业分析；Starlink 级实际采购价未公开 |
| V17 | `array_mass_kg` (GaAs) | 三档 | 936 | 由一档面积（624 m²）× 三档面密度（1.5 kg/m²）得出。面积推导可靠，不确定性主要来自面密度。 | — | 同 V8 面密度迁移局限 |
| V18 | `array_mass_kg` (HJT) | 三档 | 1552 | 由一档面积（1293 m²）× 三档面密度（1.2 kg/m²）得出。 | — | 同 V9 面密度迁移局限 |
| V19 | `battery_mass_kg` | 三档 | 981 | 由一档 kWh（186.4）× 三档比能量（190 Wh/kg）得出。 | — | 同 V11 比能量迁移局限 |

### 4.3 四档参数（合理推断，需首次引用裁决 + 推断依据 + 失效风险）

| # | 参数名 | 档位 | 当前值 | 推断依据 | 边界条件 | 为何必须推断 | 推断失效风险 |
|---|---|---|---|---|---|---|---|
| V20 | `radiator_specific_mass_kg_per_m2` | 四档 | 4.0 / 5.0 / 6.5 | 航天器热控结构面密度通用工程范围 3-8 kg/m²。参考：ISS 散热器面板、通信卫星热控面板等可比硬件。4.0-6.5 覆盖从轻量化设计到保守设计的区间。 | 散热器类型（体装式/展开式/热管耦合式）影响面密度数倍；高温散热器（>400K）可能需要特殊材料（C-C复合材料），面密度显著不同于常规铝面板。 | AI1 散热器设计的详细规格（材料、构型、展开机构）在当前阶段不可获取，且没有可直接引用的权威来源。 | 若 AI1 采用非常规散热方案（如液滴散热器、展开式柔性散热器），实际面密度可能偏离 3-8 kg/m² 范围 50% 以上。 |
| V21 | `platform_ratio` | 四档 | 0.18 / 0.22 / 0.28 | 可比大型卫星平台（GEO 通信卫星、Psyche 深空探测器）的结构/机构占比通常在 15-30% 之间。0.18-0.28 覆盖从"结构优化"到"保守设计"的区间。参考 URL：`jpl.nasa.gov/press-kits/psyche/`、`spacenexus.us/satellite-bus-comparison`。 | 平台质量占比高度依赖于载荷集成密度和发射环境：若计算载荷高度集成化（刀片式/机柜式），平台占比可降低；若需要大面积散热器和独立承力结构，占比增大。 | AI1 的载荷-平台集成方案未公开。目前无任何公开资料描述 AI1 的机械结构架构。 | 若 AI1 采用高度集成化的"机柜即结构"方案（减少独立平台质量），ratio 可能低至 0.10；若需要复杂展开机构和独立热控框架，ratio 可能高至 0.40。 |
| V22 | `propulsion_mass_kg` | 四档 | 180 / 220 / 350 | 可参考的推力器量级：Orbion 霍尔推力器 ~5-10 kg/台（`orbionspace.com/thrusters/`）、ExoTerra 电推系统（`exoterra.com/thrusters`）。假设 4-8 台推力器 + 贮箱 + 推进剂管理 + 管路，总量估计 180-350 kg。 | 推进剂类型（氙/氪/碘）决定贮箱规模和压强；机动预算（相位调整、离轨、避碰）决定推进剂总需求，进而决定贮箱质量。电推系统的高压氙气贮箱质量占比可达系统质量的 40-60%。 | 无 AI1 推进系统架构的公开信息（电推类型、推力器数量、推进剂类型与质量、ΔV 预算）。 | 若 AI1 采用全化学推进，系统质量可能远超 350 kg（化学推进的推重比远低于电推）；若采用无推进的被动编队方案，质量可能接近 0。跨度可达一个数量级。 |
| V23 | `comms_mass_kg` | 四档 | 150 / 180 / 300 | 可参考的终端量级：激光通信终端（如 TESAT Laser Communication Terminal ~30-50 kg/台）、RF 终端（如 NASA SmallSat 通信终端 ~5-15 kg/台）。假设 2-4 台激光终端 + 备份 RF 链路 + 云台/天线，总量 150-300 kg。 | 终端数量（星间链路 + 星地链路）、数据率要求、指向精度需求、冗余度均影响质量。高空量激光终端（如 TESAT 的 1.8 Gbps 终端）质量显著高于低数据率终端。 | 无 AI1 通信架构的公开信息（激光或 RF、链路数量、数据率、地面段配合）。 | 若 AI1 仅需星地链路（无星间），质量可能低至 50-80 kg；若需要多向星间激光骨干网 + 多星地链路，质量可能达 400+ kg。 |
| V24 | `ait_margin_ratio` | 四档 | 0.10 / 0.12 / 0.18 | 大型航天项目的系统级质量裕量通常在 10-30% 之间。NASA GSFC-STD-7000 等标准建议按设计成熟度分级：概念设计阶段 30%、初步设计 20%、详细设计 10%。当前阶段（概念/初步）取 10-18% 为合理区间。 | 裕量取值高度依赖于设计的成熟度和复杂度：首颗卫星（高不确定性）vs 批产卫星（低不确定性）、新研制平台（高裕量）vs 继承平台（低裕量）。 | AI1 的设计成熟度和平台继承程度未知。无 AI1 项目管理文件的公开访问。 | 若 AI1 为首颗全新技术验证星，实际所需裕量可能达 30%（当前保守情景已以 18% 覆盖）；若为第 N 颗批产星，裕量可低至 5%。 |
| V25 | `pcdu_specific_power_kw_per_kg` | 四档 | 10.0 | 航天器 PCDU 的比功率受拓扑（集中式/分布式）、母线电压（28V/50V/100V）、效率和冗余度影响。10 kW/kg 为当前工程占位值——假设 150 kW PCDU 系统约 15 kg（纯功能部分），实际还需考虑结构封装、线缆、连接器和冗余切换。 | PCDU 比功率在高功率应用中通常优于低功率：高压母线（100V+）减少电流和线缆质量。若 AI1 采用高压光伏母线（>100V），比功率可显著优于 10 kW/kg；若采用传统 28V 母线，比功率可能低于 5 kW/kg。 | 无 AI1 电源架构的公开信息（母线电压、拓扑、冗余度）。仅知道存在相应功率等级的产品，但无公开质量数据。 | 实际比功率可能在 2-20 kW/kg 之间，取决于具体架构（一个数量级的不确定性）。 |
| V26 | `pcdu_cost_per_kw` | 四档 | $5,000 / 7,000 / 10,000 /kW | 推断为基础电子设备价格区间。无公开空间级 PCDU 价格锚点。仅能参考地面工业级电力电子设备（~$100-500/kW）并乘以空间级放大因子（10-50x）得出。 | 空间级电子设备的价格高度依赖于：认证等级（Class S/Mil-Std vs 商业级）、批量（单件 vs 百件级）、复杂度（集中式 vs 分布式）。 | 无任何公开空间级 PCDU 价格数据可供引用。此为当前所有价格参数中证据链最弱的参数之一。 | 实际空间级 PCDU 价格可能为地面工业级的 50-200x 放大，当前 10-50x 假设可能在乐观方向。 |
| V27 | `propulsion_total_cost_per_sat` | 四档 | $400,000 / 600,000 / 900,000 /sat | 推断为本地工程分摊值。参考推力器零售价（Orbion 霍尔推力器 ~$50-100k/台，ExoTerra 电推系统 ~$100-200k/台）+ 贮箱/管路/控制器估计。4-8 台推力器 × $50-100k + 系统集成。 | 推进剂类型、推力器数量、供应商选择、采购批量均显著影响成本。 | 无 AI1 推进系统选型和采购信息。 | 若采用全化学推进（更便宜的推力器但更重的系统），成本结构将完全不同。 |
| V28 | `comms_total_cost_per_sat` | 四档 | $800,000 / 1,200,000 / 2,000,000 /sat | 推断为本地工程分摊值。参考激光终端行业量级（TESAT 级终端估计 $200-500k/台）+ RF 备份 + 云台/天线。2-4 台激光终端 × $200-500k + 系统集成。 | 终端数据率、指向精度、供应商选择、采购批量均显著影响成本。 | 无 AI1 通信系统选型和采购信息。 | 光学终端的成本跨度极大（Cubesat 级 $50k vs 骨干网级 $500k+）。 |
| V29 | `ait_cost_ratio` | 四档 | 0.15 / 0.18 / 0.28 | 推断为项目级系统集成系数。大型航天项目的 AI&T 成本占比通常在 10-30% 之间。NASA 项目经验：集成测试约占硬件成本的 15-25%。 | 集成复杂度取决于：模块化程度（即插即用 vs 手工集成）、测试深度（全环境测试 vs 抽样）、批量（首件 vs 批产）。 | 无 AI1 项目管理和制造策略的公开信息。 | 若 AI1 采用高度自动化的批量生产线，比率可能低至 5-10%；若为首件高可靠手工集成，可能高至 30-40%。 |

### 4.4 组件级四档参数（质量链导出）

| # | 参数名 | 档位 | 当前值 | 推断依据 | 为何必须推断 |
|---|---|---|---|---|---|
| V30 | `compute_payload`（新 bottom-up 值） | 二档+三档 | ~900-1200 / ~1400-1800 / ~2000-2400 kg | Task 2 bottom-up 链：GPU 质量锚点 A1（HGX B200 32 kg、GB300 托盘 29 kg）；空间化增量系数为三档/四档推断。 | GPU 单模块质量不可直接获取；空间化增量来自通用工程经验 |
| V31 | `thermal` | 四档 | 440 / 550 / 715 kg | 面积一档但面密度四档。质量不确定性来自面密度工程占位。 | 同 V20 |
| V32 | `platform_structure` | 四档 | 698 / 1147 / 2047 kg | 由 platform_ratio × 子系统求和。ratio 和子系统和均含推断。范围跨度近 3x。 | 同 V21 |
| V33 | `propulsion` | 四档 | 180 / 220 / 350 kg | 同 V22 | 同 V22 |
| V34 | `communications` | 四档 | 150 / 180 / 300 kg | 同 V23 | 同 V23 |
| V35 | `ait_margin` | 四档 | 491 / 812 / 1801 kg | 同 V24。范围跨度近 4x 反映了裕量的高度不确定性。 | 同 V24 |

---

## 5. 禁止入模清单

| # | 参数名 | 当前值 | 原 grade | 禁止理由 | 替代建议 |
|---|---|---|---|---|---|
| F1 | `battery_cost_per_kwh` | **$400 /kWh** | C | 当前值 $400/kWh 与公开空间级电池列表价（satsearch：100 Wh 模块 €9,000 ≈ $90,000/kWh）存在约 **225 倍**的数量级矛盾。该值也低于地面电动车电池包价格（$100-150/kWh），无法解释空间级溢价。 | **必须替换**。建议以 satsearch 锚点建立三档区间估计（乐观 $20,000 / 基准 $50,000 / 保守 $100,000 per kWh），提交 Task V2 AskUserQuestion 裁决后入模。保留参数但更换数值。 |

---

## 6. 已废弃/已替换参数

### 6.1 kW/t 派生链废弃说明

| 废弃项 | 旧值 | 废弃理由 | 替代物 | 替代物档位 |
|---|---|---|---|---|
| `compute_specific_power_kw_per_t` (light) | **70 kW/t** | 来源为二手媒体转述（B1 级），非 NVIDIA 或 SpaceX 官方规格；定义域（整星 vs 载荷）存在根本性歧义；存在循环引用风险（kW/t 可能从总质量反算）。 | 已不需要——Task 2 bottom-up 链不依赖 kW/t 分母，直接通过地面硬件质量 + 空间化增量计算载荷质量 | — |
| `compute_specific_power_kw_per_t` (baseline) | **55 kW/t** | 从 70 kW/t 本地衍生，无任何独立外部来源。这是典型的"二次推导 + 本地调整"，违反 Task V1 禁止"把本地反算写成主链基线"的原则。 | 同上 | — |
| `compute_specific_power_kw_per_t` (conservative) | **45 kW/t** | 同上，纯本地情景参数，无独立支撑。 | 同上 | — |
| `compute_payload` 旧质量值 | **2143 / 2727 / 3333 kg** | 由 kW/t 派生链导出，其推导路径已被废弃（分母无效）。注：三个数值本身可能仍有参考价值（作为整星质量情景的交叉校验），但不应作为计算载荷质量的正式输入。 | Task 2 bottom-up 链的新值：~900-1200 / ~1400-1800 / ~2000-2400 kg | 二档+三档（新链） |

### 6.2 HJT 路线资格修正说明

| 修正项 | 旧判定 | 新判定 | 修正依据 |
|---|---|---|---|
| `route_policy.forbidden_mainline` 中 `"10y-HJT"` | **禁止进入主模型** | **删除**：HJT 为与 GaAs 并行的成熟技术路线 | Task 3 证据包：17 条搜索 URL + 12 项物理链闭合 + 多锚点交叉验证（CEA/INES + 东方日升 + ISS + Starlink + 华晟 20 GW 产能） |
| `hjt_exploratory.status` | `"只能降级"` | **已修正为**：物理链可独立支撑并行比较；价格链待后续补强 | 物理链维度（效率、退化、面积、质量）已通过多锚点交叉验证闭合；价格链维度有地面量产锚点和空间级区间估计 |
| `hjt_route_cost_chain.allowed_usage` | `"reference_only"` (禁止进入主模型) | **修正为**：三档可迁移价格，可进入敏感性分析 | 地面 HJT 组件 $0.14-0.24/W（二档）+ 东方日升空间级 ~$2-3/W（三档）+ 地面→空间放大 10-15x |
| HJT "仅能表示探索性面积/质量灵敏度，不能代表 AI1 或 Starlink 已采用路线" | 原约束 | **解除**：Starlink 硅基路线已通过 3 个独立来源交叉确认（Per Aspera、雪球供应链分析、华尔街见闻 GF Securities） | 见 HJT 证据包 §4 |

### 6.3 旧禁止项状态更新

| 旧 task5_interface 约束 | 新状态 |
|---|---|
| `must_keep_downgraded_labels: [pcdu, platform_structure, propulsion, communications, ait_margin]` | **部分解除**：HJT 路线资格已修正（见 6.2），但 pcdu/platform/propulsion/comms/ait 五个参数的 evidence grade 仍为四档（低证据），其"只能降级"的实质含义在本清单中以四档 + 推断依据 + 失效风险重新表达 |
| `must_not_promote_to_fact: ["HJT 已被 AI1 或 Starlink 采用"]` | **维持**：HJT 证据包确认 SpaceX/Starlink 已转向硅基路线（多源交叉验证），但"AI1 是否采用 HJT"仍无一手确认。HJT 作为并行路线的地位来自其独立技术成熟度（可比较），而非来自"已被 AI1 采用"的事实确认 |

---

## 7. 交叉引用

| 文档 | 用途 | 路径 |
|---|---|---|
| Task 2：bottom-up 质量链 | 废弃 kW/t 链、更新计算载荷质量 | `stage2_blackwell_payload_mass_bottom_up.md` |
| Task 3：HJT 证据包 | HJT 路线资格修正、效率/退化/价格证据 | `stage2_hjt_evidence_pack.md` |
| 质量参数源 JSON | 本次分级的输入 | `stage2_mass_inputs_blackwell_hjt.json` |
| 价格参数源 JSON | 本次分级的输入 | `stage2_cost_inputs_blackwell_hjt.json` |
| Stefan-Boltzmann 结果 | 散热器面积的一档推导支撑 | `stefan_boltzmann_results.txt` |

---

## 8. 未闭合项

| # | 条目 | 状态 | 说明 |
|---|---|---|---|
| U1 | 新 bottom-up 计算载荷质量值（Task 2）尚未写入 mass JSON | **待 Task 5/6 执行** | 本清单仅标注旧值为"已废弃"，新值来自 Task 2 独立产出文档。实际 JSON 文件更新由下游 Task 负责 |
| U2 | HJT 路线资格修正尚未更新 mass JSON 的 metadata | **待 Task 5/6 执行** | `route_policy.forbidden_mainline` 中 `"10y-HJT"` 和 `hjt_exploratory.status: "只能降级"` 需在 JSON 中更新 |
| U3 | `battery_cost_per_kwh` 新值待建立 | **需 Task V2** | 当前 $400/kWh 禁止入模，建议以 satsearch 锚点建立三档区间后提交裁决 |
| U4 | `hjt_route_cost_chain` 的新值（地面→空间价格链）待结构化 | **需 Task 7 或后续** | 当前仅在三档定性描述，未转化为可入模的具体数值区间 |
| U5 | 四档参数占比高（14/47=30%） | **系统性风险** | 大量质量/价格参数仅能靠工程推断支撑。这是 AI1 信息公开不足的客观结果，不是执行缺陷。建议在 Task V2 中评估是否接受当前四档参数作为模型输入或要求进一步补强 |

---

> **文档状态**：Task 4 产出物 v1.0
> **闭合判据**：47 个参数全部扫描并重分级；三档参数均有迁移理由 + 区间依据；四档参数均有推断依据 + 边界条件 + 失效风险；禁止入模参数已标识并给出替代建议；废弃参数已说明替换路径；HJT 路线资格已修正
> **下一交接**：本清单为 Task V2（用户裁决）和 Task 5/6/7（JSON 更新与模型修改）的输入
