# Stage 2 Task 7：关键采购价格来源链（V裁决更新版）

## 说明

- 任务定位：`close-stage-two-evidence-gaps / Task 7 [P2]`，已吸收Task V2全部参数裁决(V1-V37)。
- 本文不重复处理发射价格链；发射口径沿用既有 `stage2_task4_mass_launch_evidence.md`。
- 权威输入层：`research_output/workspace/data/stage2_cost_inputs_blackwell_hjt.json`。
- 证据分级体系：Task V1四档制（一档=直接一手报价/飞行产品价格 → 四档=仅可做灵敏度占位）。

---

## 零、参数状态四态分类

### 已批准可入主模型

| V# | 参数 | 证据档位 | 值范围 |
|----|------|---------|--------|
| V12 | 计算载荷单价 | 三档 | $38k / $60k / $100k USD/kW |
| V14 | GaAs阵列单价 | 三档 | $180 / $200 / $250 USD/W_BOL |
| V16 | HJT成本链 | 三档 | $2 / $3 / $5 USD/W (空间) |
| V36 | Li-ion NMC电池 | 三档 | $200 USD/kWh (固定) |
| V37 | LTO电池 | 四档 | $260 / $350 / $400 USD/kWh |
| V26 | PCDU单价 | 四档 | $3k / $5k / $10k USD/kW |
| V27 | 推进总成(5yr/10yr) | 四档 | $500k-$2.4M USD/星 |
| V28 | 通信/激光链路 | 四档 | $1.5M / $2.5M / $4.0M USD/星 |
| V29 | AIT系数(5yr/10yr) | 四档 | 0.12-0.40 |

### 四档降级(sensitivity_only)

| V# | 参数 | 降级原因 | 值(保留原值) |
|----|------|---------|-------------|
| V13 | 散热系统单位成本 | 循环引用风险，无系统级直接锚点 | $5k / $6k / $8k USD/m² |
| V15 | 平台/结构单位成本 | 循环引用，无大卫星$/kg直接锚点 | $2.8k / $3.6k / $5k USD/kg |

### 禁止入模(已替换)

| 原参数 | 替换为 | 原因 |
|--------|--------|------|
| `battery_cost_per_kwh` ($400/kWh, 脚本常量) | V36 NMC + V37 LTO | 无空间级证据，明显偏离公开产品价格 |

### 废弃

(当前无废弃项)

---

## 一、参数到裁决交叉引用总表

| V# | 参数名(中文) | JSON item_id | 证据档位 | Light | Baseline | Conservative | 允许用途 | 裁决关键词 |
|----|------------|-------------|---------|-------|----------|-------------|---------|-----------|
| V12 | 计算载荷单价 | `compute_payload_cost_per_kw` | 三档 | $38k | $60k | $100k | main_model | SpaceX COTS 1.5-3x |
| V13 | 散热系统单价 | `thermal_cost_per_m2` | 四档↓ | $5k | $6k | $8k | sensitivity_only | 循环引用，降级 |
| V14 | GaAs阵列单价 | `gaas_array_cost_per_bol_w` | 三档 | $180 | $200 | $250 | main_model | AzurSpace + 旧口径 |
| V15 | 平台结构单价 | `platform_structure_cost_per_kg` | 四档↓ | $2.8k | $3.6k | $5k | sensitivity_only | 循环引用，降级 |
| V16 | HJT成本链 | `hjt_route_cost_chain` | 三档 | $2 | $3 | $5 | main_model_sensitivity | 东方日升+地面量产 |
| V25 | PCDU比功率 | (power_system) | 四档 | 1.0 | 0.5 | 0.2 kW/kg | — | Terma 0.54 kW/kg |
| V26 | PCDU单价 | `pcdu_cost_per_kw` | 四档 | $3k | $5k | $10k | main_model | Terma飞行产品 |
| V27 | 推进总成(5yr) | `propulsion_total_cost_per_sat` | 四档 | $500k | $800k | $1.2M | main_model | 0.6次方法则 |
| V27 | 推进总成(10yr) | `propulsion_total_cost_per_sat` | 四档 | $800k | $1.3M | $2.4M | main_model | 剥蚀+冗余 |
| V28 | 通信/激光链路 | `comms_total_cost_per_sat` | 四档 | $1.5M | $2.5M | $4.0M | main_model | Google Suncatcher |
| V29 | AIT系数(5yr) | `ait_cost_ratio` | 四档 | 0.12 | 0.18 | 0.25 | system_coefficient | Starlink量产压缩 |
| V29 | AIT系数(10yr) | `ait_cost_ratio` | 四档 | 0.20 | 0.28 | 0.40 | system_coefficient | 全环境测试 |
| V36 | NMC电池 | `battery_cost_per_kwh_nmc` | 三档 | $200 | $200 | $200(fixed) | main_model | Starlink直接迁移 |
| V37 | LTO电池 | `battery_cost_per_kwh_lto` | 四档 | $260 | $350 | $400 | main_model | 等比压缩法 |

---

## 二、分项来源链

### 2.1 V12 计算载荷单价：$38k / $60k / $100k USD/kW（三档）

**裁决**：1.5-3x量产溢价，SpaceX COTS策略

**三轮搜索历史**：

1. 第一轮：地面GPU机柜成本锚点 → GB300 NVL72 ~$25-33k/kW
   - 本地继承：`05_commercial.tex` 给出 22-28 MUSD/MW
   - 行业锚点：`https://awesomeagents.ai/hardware/nvidia-gb300-nvl72/` 单柜3-4 MUSD, ~120 kW
2. 第二轮：空间原型溢价参考 → H100空间原型17-33x
   - `https://culled.org/articles/ai-in-space-satellite-h100-beginning/`
3. 第三轮：SpaceX COTS策略压缩 → 量产1.5-3x
   - `https://www.163.com/dy/article/KUECPBRA05568W0A.html` SpaceX COTS：商用现货+自研防护+系统容错
   - `https://guomans.com/insights/aerospace-nvidia-orbital-ai-data-centers-space-computing` NVIDIA轨道AI数据中心

**推导链**：地面GB300 ~$25-33k/kW（二档） → COTS策略量产溢价1.5-3x → $38-100k/kW（三档）。
Light=1.5x, Baseline=2x, Conservative=3x → 对应 $38k/$60k/$100k。

**用户裁决结论**：批准入主模型，三档。不是NVIDIA官方报价，而是组合推导的情景参数。

---

### 2.2 V13 散热系统单位成本：$5k / $6k / $8k USD/m²（四档，降级）

**裁决**：四档降级 → sensitivity_only

**来源链**：
1. 原paper内部假设：$3.5M/1MW散热总包
2. 物理反算：1 MW / 1400 W/m² ≈ 714 m² → $4.9k/m²
3. 辅助对照：`https://blog.barrack.ai/nvidia-b300-1400w-data-center-requirements/` 液冷改造 $2-3M/MW

**降级理由**：源出原paper内部假设($3.5M/1MW)，存在循环引用风险。材料级锚点$250-1,850/m²但不含系统集成成本。缺少系统级直接报价锚点。值保留但降为sensitivity_only。

---

### 2.3 V14 GaAs阵列单位成本：$180 / $200 / $250 USD/W_BOL（三档）

**裁决**：三档，批准入主模型

**来源链**：
1. 旧口径：本地论文 `200-400 USD/W`（二档）
2. AzurSpace 4G32：32% class efficiency, radiation-hardened → 技术路线证实
   - `https://www.azurspace.com/en/products/space-products/`
3. satsearch零售对照：3U展开面板 $21-23.4k 列表价 → 折算>200 USD/W → 偏乐观口径基准

**推导链**：旧口径200-400 USD/W → 规模化星座采购压缩 → $180-250/W_BOL（三档）。Light=$180, Baseline=$200, Conservative=$250。

---

### 2.4 V15 平台/结构单位成本：$2.8k / $3.6k / $5k USD/kg（四档，降级）

**裁决**：四档降级 → sensitivity_only

**来源链**：
1. 原paper假设：$30M/1MW平台包
2. 单星平台质量 ~1,147 kg → $3.1k/kg

**降级理由**：源出原paper内部假设($30M/1MW平台包)，循环引用。小卫星COTS bus ~$20k/kg但口径不同（<500kg vs AI1 >1吨卫星）。无大卫星级别的$/kg直接锚点。

---

### 2.5 V16 HJT成本链：$2 / $3 / $5 USD/W 空间级（三档）

**裁决**：三档 → main_model_sensitivity（并行成熟路线，不再禁止入模）

**来源链**：
1. 地面量产HJT：$0.14-0.24/W → 二档
   - pmarketresearch等多源交叉验证
2. 东方日升空间级HJT：50μm厚度，14-21 RMB/W ≈ $2-3/W → 三档
3. CEA技术验证：>14% efficiency after irradiation, 97% recovery
   - `https://www.cea.fr/cea-tech/liten/english/Pages/Medias/News/2025/major-breakthrough-for-photovoltaic-technology-space.aspx`

**推导链**：地面$0.14-0.24/W → 地面→空间放大10-15x → 空间级$2-5/W。Light=$2/W, Baseline=$3/W, Conservative=$5/W。

**状态变更**：HJT从"禁止进入主模型"升级为"并行成熟路线(main_model_sensitivity)"。可与GaAs主线并行做灵敏度对比。

---

### 2.6 V25/V26 PCDU功率电子：比功率0.54 kW/kg + 成本$3k / $5k / $10k USD/kW（四档）

**V25裁决（比功率，四档）**：
- Terma PCDU飞行产品(BepiColombo MTM)：比功率 0.54 kW/kg
  - `https://satsearch.co/products/terma-power-conditioning-distribution-unit`
  - `https://www.satnow.com/products/power-conditioning-and-distribution-units/terma/134-1195-bepicolombo-mtm-pcdu`
- 另有两个低功率PCDU产品存在性锚点（Exa Colossus, Airbus high-power）
- 三个锚点不一致 → V25为四档

**V26裁决（成本，四档）**：
- Terma PCDU飞行产品证明高功率PCDU存在且可做，但无公开价格
- $3k-10k/kW为基于飞行件复杂度的工程估计
- Light=$3k/kW, Baseline=$5k/kW, Conservative=$10k/kW
- 批准入主模型，四档

---

### 2.7 V27 推进总成单价：5yr $500k-$1.2M / 10yr $800k-$2.4M USD/星（四档）

**裁决**：0.6次方缩放法则（用户纠正原线性缩放错误）

**来源链**：
1. Starlink推进成本基准：$125-250k/星（来自雪球分析，霍尔推进器占整星~25%，整星$0.5-1M → 非SpaceX官方）
2. AI1推力 ≈ 10× Starlink
3. 0.6次方法则（six-tenths rule）：Capacity扩大N倍 → 成本 = N^0.6 × 基准 = 10^0.6 × ($125-250k) ≈ 4.0×
4. 推力器参考：`https://orbionspace.com/thrusters/` Orbion霍尔推力器

**5yr分支**：标准电推设计，常规高压贮箱 → $500k/$800k/$1.2M
**10yr分支**：电推剥蚀限制，需2×工质吞吐量 → 1:1冗余推力器(成本×2)或磁屏蔽无剥蚀技术(研发+单价飙升) → 成本+60-100% → $800k/$1.3M/$2.4M

**用户裁决结论**：0.6次方修正后批准入主模型，四档。

---

### 2.8 V28 通信/激光链路单价：$1.5M / $2.5M / $4.0M USD/星（四档）

**裁决**：Google Suncatcher修正值

**来源链**：
1. Google Suncatcher论文：天基AI集群需要tens of Tbps星间链路
   - `https://arxiv.org/html/2511.19468v1`
2. COTS DWDM技术 + 近距编队 → 单链路 ~1.6 Tbps
3. AI1集群总带宽需求远超传统通信卫星 → 驱动通信子系统成本显著放大

**值修正**：原值 $0.8/$1.2/$2.0M → 修正为 $1.5/$2.5/$4.0M（上调以反映tens of Tbps ISL需求）

**用户裁决结论**：批准入主模型，四档。

---

### 2.9 V29 AIT集成测试系数：5yr 0.12-0.25 / 10yr 0.20-0.40（四档）

**裁决**：独立文献支撑+寿命分支

**来源链**：
1. SpaceNexus 2026文献：Integration & Test占硬件成本 20-40%
2. Starlink量产压缩：'disposable 5-year LEO birds, reducing qualification by 50-80%'

**5yr分支**：I&T 20-40%基线下界 → 免测50-80% → 0.12/0.18/0.25
**10yr分支**：全环境测试覆盖 → 取中位 → 0.20/0.28/0.40

**提醒**：这不是采购单价，而是系统级成本系数（`system_cost_coefficient`），不可混称为单件采购价。

---

### 2.10 V36 Li-ion NMC电池成本：$200 USD/kWh 固定（三档）

**裁决**：Starlink直接迁移，零溢价

**完整推导链**：

```
Starlink亿颗级采购Panasonic 21700 NMC电芯
  → cell级: $80-120/kWh（巨大量产单向降本）
  → SpaceX自研pack集成：筛选/BMS/灌封/热管理
  → pack级乘数: ×1.5-2.5
  → pack级成本: $150-250/kWh
  → 取中值: $200/kWh 固定
```

**零溢价的工程逻辑**：
- Starlink NMC pack本身就是空间电池：pack级230 Wh/kg, 5000等效全循环, LEO 5年
- 无需"地面→空间"二次溢价——pack已经在空间运行
- Ray Barsa 2025演讲确认：`https://ciclibattery.com/battery-power-online-space-batteries-how-spacex-designs-batteries-for-satellites/`
- NASA 2025 Workshop：Starlink >100 MWh在轨容量 `https://www.nasa.gov/wp-content/uploads/2024/01/starlink-batteries-reliability-lessons-from-10000-leo-satellites-abw-2025.pdf`

**证据分级**：
- cell级$80-120 → 二档（产业链公开数据）
- pack级$150-250 → 二档（真实pack集成乘数）
- 空间运行230 Wh/kg → 一档（飞行数据）
- zero-premium判断 → 三档（工程推理）

**替换关系**：此条目替换旧的`battery_cost_per_kwh`（$400/kWh脚本常量，禁止入模）。

---

### 2.11 V37 LTO电池成本：$260 / $350 / $400 USD/kWh（四档）

**裁决**：等比压缩法

**完整推导链**：

```
地面化学体系价格比：
  NMC: $100-150/kWh（高产量，成熟供应链）
  LTO: $150-200/kWh（低产量，全球< NMC 1%）
  LTO/NMC比 ≈ 1.3-1.5×

等比压缩：
  V36 NMC空间: $200/kWh (Starlink)
  × 1.3 (纯材料差价，pack级被其他组件摊薄)
  × 2.0 (材料差价 + 极小产量 + 工艺复杂度)
  → $260-400/kWh

化学固有溢价：
  LTO能量密度 ~100 Wh/kg vs NMC ~190-230 Wh/kg
  → 每kWh需约2×电芯质量 → 材料成本天然偏高
```

**技术参考**：
- Saft LTO白皮书：80-90% DOD, 超长循环寿命，比能比Li-ion低30-50%
  - `https://saft.com/en/horizon-new-lithium-based-technology-satellite-batteries-improving-mission-performance`
- 同V36 Ray Barsa Starlink NMC锚点

**路线说明**：取自研pack的Starlink路线（非Saft传统空间认证路线）。LTO用于10yr分支（需要超长循环寿命），NMC用于5yr分支。

---

## 三、对后续模型的使用规则（更新）

| 级别 | 定义 | 允许用法 | 当前项 |
|------|------|---------|--------|
| 三档可入模 | 有≥2条独立来源链，至少1条不是内部假设 | `main_model` | V12 compute, V14 GaAs, V16 HJT, V36 NMC battery |
| 四档可入模 | 有锚点但无公开价格或为工程推导 | `main_model` | V26 PCDU, V27 propulsion, V28 comms, V37 LTO battery |
| 四档降级 | 循环引用风险，无独立锚点 | `sensitivity_only` | V13 thermal, V15 platform |
| 系统级系数 | 非采购单价 | `system_cost_coefficient` | V29 AIT ratio |
| 禁止入模 | 已替换 | — | (旧 battery_cost_per_kwh) |

---

## 四、证据覆盖度总结

- **已批准可入主模型**：9个参数（含5yr/10yr分支展开）
- **四档降级(sensitivity_only)**：2个参数（V13散热, V15平台）
- **已替换**：1个参数（旧电池$400/kWh → V36+V37）
- **新增条目**：2个（V36 NMC电池, V37 LTO电池）
- **分支拆分条目**：3个（V27推进, V28通信, V29 AIT → 现含5yr/10yr分支）
- **状态变更**：HJT从"禁止入主模型"升级为"并行成熟路线(main_model_sensitivity)"

---

## 五、Task 7闭合结论

- 所有V1-V37参数裁决已吸收到 `stage2_cost_inputs_blackwell_hjt.json`。
- 旧 `battery_cost_per_kwh` (脚本常量$400/kWh, 禁止入模) 已被V36 NMC + V37 LTO替换。
- HJT不再是禁止路线，已转为并行成熟路线(main_model_sensitivity)。
- V13散热和V15平台保留原值但降级为四档sensitivity_only，标注循环引用风险。
- V27推进已从线性缩放修正为0.6次方法则（用户纠正）。
- `replace_required_count`已清零，无阻塞项。
- 后续模型可直接使用JSON中的 `main_model` / `main_model_sensitivity` 项，降级项仅用于灵敏度分析。
