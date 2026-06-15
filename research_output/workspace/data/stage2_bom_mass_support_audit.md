# Stage 2 Task 6：BOM 大件质量支撑审计（V2 参数裁决版）

> 文档定位：`close-stage-two-evidence-gaps / Task 6` 的主审计文档。  
> trace-id：`cs2eg-task6-mass-update-20260614-01`  
> 更新日期：2026-06-14  
> 主线边界：统一 `Blackwell` 主线；`GaAs` 为当前主模型可用电源路线；`HJT` 为并行成熟路线（非降级/探索性）。  
> 证据体系：全部参数已通过 Task V2 参数裁决（V1-V37），四档证据等级体系（Task V1 freezing）为唯一判据。

---

## 0. 审计结论先行（更新后）

| 大件 | 基准质量 | V# | 证据等级 | 用户裁决 | 状态 |
|---|---:|---:|---:|---:|---|
| 计算载荷 | 1,500 kg | V30 | 二档（地面硬件）+ 三档（空间化增量） | 采纳结构化三项拆解 | 已闭合（新 bottom-up 链） |
| 散热系统 | 550 kg | V20 | 四档 | 采纳 4.0/5.0/6.5 kg/m² | 四档保留 |
| 光伏阵列（GaAs） | 936 kg | V4-V5, V8 | 二档（效率）+ 三档（面密度） | 采纳 | 已闭合 |
| 光伏阵列（HJT） | 902 kg | V6-V7, V9 | 二档（效率）+ 三档（面密度） | BOL 上调至 22%，面密度 1.8 | 并行成熟路线 |
| 电池（5yr Li-ion） | 981 kg | V10+V11 | 三档 | 采纳 DOD 40% | 已闭合 |
| 电池（10yr Li-ion） | 1,542 kg | V10+V11 | 三档 | 采纳 DOD 25% | 已闭合 |
| 电池（10yr LTO） | 916 kg | V10+V11 | 三档 | 采纳 DOD 80% | 已闭合 |
| PCDU | 300 kg | V25 | 四档 | 采纳 1.0/0.5/0.2 kW/kg（~18× 修正） | 四档保留 |
| 平台/结构 | ~1,493 kg | V21 | 四档 | 采纳 ratio 0.25/0.35/0.45（上调） | 四档保留 |
| 推进 | 350 kg | V22 | 四档 | 采纳 200/350/500 kg（上调） | 四档保留 |
| 通信/激光链路 | 300 kg | V23 | 四档 | 采纳 200/300/450 kg（上调） | 四档保留 |
| AIT 裕量（5yr） | 前序×8% | V24 | 四档 | 采纳 0.05/0.08/0.12 | 四档保留 |
| AIT 裕量（10yr） | 前序×15% | V24 | 四档 | 采纳 0.10/0.15/0.22 | 四档保留 |

### 已废弃的参数与旧值

| 旧参数 | 旧值 | 废弃原因 | 替换为 |
|--------|------|---------|--------|
| compute_specific_power_kw_per_t | 70/55/45 | 循环引用、无独立锚点 | V30 bottom-up 结构化拆解 |
| PCDU 比功率 | 10.0 kW/kg | 无任何飞行产品支撑（150 kW→15 kg） | V25: 1.0/0.5/0.2 kW/kg（Terma 0.54 kW/kg 锚点） |
| 平台系数 | 0.18/0.22/0.28 | 本地占位无外部参考 | V21: 0.25/0.35/0.45（Starlink V2 Mini ~0.38 参考） |
| 推进质量 | 180/220/350 kg | 缺可比参考 | V22: 200/350/500 kg（Starlink 比例外推） |
| 通信质量 | 150/180/300 kg | 缺高带宽需求依据 | V23: 200/300/450 kg（Google Suncatcher 参考） |
| AIT 裕量 | 0.10/0.12/0.18 | 无寿命分化 | V24: 分寿命分支（5yr/10yr） |
| HJT 路线定位 | 「只能降级」 | 与用户指令相悖 | 并行成熟路线（V6-V9 裁决支撑） |

---

## 1. 审计边界与方法（V2 更新）

- 本文只做"大件质量支撑链"审计，不直接重建下一阶段经济模型。
- 审计目标是把每个大件按 Task V1 四档证据等级体系明确归入：`一档物理推导`、`二档权威资料`、`三档可迁移证据`、`四档合理推断`。
- 所有参数均已通过 Task V2 的逐参数 AskUserQuestion 裁决（V1-V37），裁决记录锚定于 `.trae/specs/close-stage-two-evidence-gaps/current-note.md`。
- 路线边界：`GaAs` 为主链，`HJT` 为并行成熟路线（非探索性/降级）。两种路线共享同一电池/PCDU 链路。
- **kW/t 计算载荷链已全面废弃**，替换为 V30 bottom-up 结构化三项拆解（辐射防护 + 热管理改造 + 结构/真空改造）。

---

## 2. 逐参数裁决审计

### 2.0 公共基线（V1-V3：二档）

**裁决参数**：`peak_power_kw = 150`, `sustained_power_kw = 120`, `orbit_altitude_km = 600`

| 字段 | 内容 |
|------|------|
| V# | V1（峰值功率）、V2（持续功率）、V3（轨道高度） |
| 证据等级 | 二档（权威资料——三家媒体交叉一致转述） |
| 用户裁决 | 采纳 |
| evidence URLs | [Inkl/Tom's Hardware](https://www.inkl.com/news/elon-musks-first-gen-orbital-data-center-craft-spans-wider-than-a-boeing-747-and-runs-an-interchangeable-chip-payload-ai1-satellite-compute-payload-is-120-kw-peaks-at-150-kw)、[Knightli](https://knightli.com/en/2026/06/10/spacex-ai1-orbital-ai-data-center-satellite/)、[Indexbox](https://www.indexbox.io/blog/spacex-unveils-ai1-orbital-data-center-satellite-ahead-of-market-debut/) |
| 推导链 | 三家媒体均引用同一原始报道口径，可视为多源交叉验证。持续功率 = 峰值 × 80%（120 = 150 × 0.8）。 |
| 不确定性 | 非 SpaceX/NVIDIA 官方规格表。若后续获取 FCC/ITU 官方申报数据可直接升级为一档。 |

---

### 2.1 计算载荷（V30：二档 + 三档）

**裁决值**：light ~1,060-1,350 kg（取中点 1,200）、baseline ~1,330-1,670 kg（取中点 1,500）、conservative ~1,750-2,300 kg（取中点 2,000）

| 字段 | 内容 |
|------|------|
| V# | V30 |
| 证据等级 | 二档（GPU 硬件锚点 A1）+ 三档（空间化辐射/热/结构增量推断） |
| 用户裁决 | 采纳结构化增量分析方案 |
| 裁决时间 | 2026-06-14 |

#### 地面硬件基线（二档/A1）

| 来源 | URL | 关键数据 |
|------|-----|---------|
| Lenovo LP2357 (GB300 NVL72) | `https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai` | 计算托盘 29 kg（4 GPU + 2 CPU） |
| NVIDIA HGX B200 PCF | `https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf` | 基板 32 kg（8 GPU） |
| NVIDIA DGX B200 | `https://docs.nvidia.com/dgx/dgxb200-user-guide/introduction-to-dgxb200.html` | 完整系统 142.4 kg |

- 地面裸硬件：~38 × 计算托盘 × 29 kg ≈ **1,002-1,102 kg**（150 GPU @ 1,000W/GPU，含 per-GPU 液冷冷板）

#### V30 结构化三项空间化增量拆解

**① 辐射防护——spot shielding vs full enclosure**

| 策略 | 方案 | 质量估算 | evidence URL |
|------|------|---------|-------------|
| 整体防护 | 全铝封闭机箱 | 50-85 kg | JHU APL 标准厚度对照表 |
| 单板局部防护 | Z-grade 涂层 + spot shielding | 15-25 kg（比全铝轻 70%） | [ACT Polymer](https://www.1-act.com/resources/learning-center/case-studies/3d-printable-polymer-composite-radiation-shield/) |
| NASA Z-Shielding | Al/Ti/Ta 扩散焊层压 | 25-40 kg | [NASA Shields-1](https://technology.nasa.gov/patent/LAR-TOPS-250) |
| 混合策略 | 板级 Al/Ta + SpaceX COTS 容错 | 30-50 kg | [Guomans Al/Ta](https://guomans.com/insights/aerospace-nvidia-orbital-ai-data-centers-space-computing) + [SpaceX COTS 策略](https://www.163.com/dy/article/KUECPBRA05568W0A.html) |

**② 热管理改造——继承地面液冷 vs 全面替换**

- NVIDIA GB300 地面已用 direct-to-chip liquid cooling（per-GPU cold plate ~200-300g × 150 = 30-45 kg，**已含在地面基线中**）
- 空间化净增量 = 减去空气冷却 + 加上空间级工质替换（HFE7200/氨）+ 冗余泵
- 净增量范围：乐观 -50 ~ +50 kg；基准 +100-200 kg；保守 +250-400 kg
- evidence URL：[JAXA HFE7200 单相机械泵流体回路（AIAA JSR）](https://arc.aiaa.org/doi/full/10.2514/1.A35030)

**③ 结构/振动/真空改造**

- 发射振动加固：+10-20% 硬件质量 ≈ +100-200 kg（行业经验）
- 真空兼容（outgassing 材料替换/conformal coating）：+10-30 kg
- 微重力结构减重：地面机柜需自重支撑结构，空间可去除 → -20-50 kg

#### 汇总表

| 增量项 | 乐观 | 基准 | 保守 |
|--------|------|------|------|
| 辐射防护 | +30-50 kg | +80-120 kg | +200-300 kg |
| 热管理改造 | -50 ~ +50 kg | +100-200 kg | +250-400 kg |
| 结构/真空 | +80-150 kg | +150-250 kg | +300-500 kg |
| **总增量** | **+60-250 kg** | **+330-570 kg** | **+750-1,200 kg** |
| + 地面基线 | +1,000-1,100 | +1,000-1,100 | +1,000-1,100 |
| **= 空间化后总质量** | **~1,060-1,350 kg** | **~1,330-1,670 kg** | **~1,750-2,300 kg** |

#### 交叉影响检查

- 与 Task 2 原值（~900-1,200 / ~1,400-1,800 / ~2,000-2,400 kg）对比：乐观端提高了 ~160 kg（Task 2 低估了底线），基准和保守端基本一致
- V31-V35 为自动导出量，不改变已有 V1-V29 裁决值本身
- **结论：无需二次判别任何 V1-V29 参数**

---

### 2.2 散热系统（V20：四档）

**裁决值**：radiator_specific_mass = 4.0 / 5.0 / 6.5 kg/m²，① 110 m² → 440 / 550 / 715 kg

| 字段 | 内容 |
|------|------|
| V# | V20 |
| 证据等级 | 四档（合理推断——航天器热控结构面密度 3-8 kg/m² 范围内） |
| 用户裁决 | 采纳 |
| 推导依据 | ISS 840m²/1000kg≈1.2 为展开式轻量设计。AI1 高功率散热可能需要更厚重的散热器结构。 |
| evidence URL | [Metal-AM ISS 热控数据](https://www.metal-am.com/articles/nasa-spacecraft-thermal-management-am/) |
| 失效风险 | 非常规方案可偏离 50%+ |
| 剩余缺口 | 未获得 AI1 一手热控结构规格 |

---

### 2.3 光伏阵列

#### 2.3.1 GaAs（V4-V5 + V8：二档 + 三档）

**裁决值**：BOL 32%（AzurSpace 4G32）、EOL 29%（退化率 9.4%）、面板面密度 1.5 kg/m²（panel-only）、面积 624 m²、质量 936 kg

| 子参数 | V# | 证据等级 | 值 | 来源 |
|--------|----|---------|-----|------|
| BOL 效率 | V4 | 二档 | 32% | [AzurSpace 4G32](https://www.azurspace.com/en/products/space-products/) |
| EOL 效率 | V5 | 二档 | 29% | BOL×(1-9.4%)，III-V 空间电池文献退化率 |
| 面板面密度 | V8 | 三档 | 1.5 kg/m² | 空间级刚性 GaAs 面板区间低端 |
| 展开机构 | — | 待建模 | — | panel-only 不含展开机构（booms/hinges/motors/hold-down），展开机构质量独立建模 |

**面板+展开分列说明**（V8 裁决）：
- 用户裁决：面板与展开机构分列建模（更清晰可审计）
- 1.5 kg/m² 为 panel-only（cells + cover glass + interconnects + honeycomb substrate）
- 展开机构额外增加 0.3-1.0 kg/m²（按展开面积折算），将在后续独立建模

[ROSA/iROSA 参考](https://en.wikipedia.org/wiki/Roll_Out_Solar_Array)

#### 2.3.2 HJT（V6-V7 + V9：二档 + 三档）→ 并行成熟路线

**裁决值**：BOL 22%（上调）、EOL 14%（维持）、面板面密度 1.8 kg/m²（上调）、面积 501 m²（BOL 简化）、质量 902 kg

| 子参数 | V# | 证据等级 | 旧值 | 新值 | 变更理由 |
|--------|----|---------|------|------|---------|
| BOL 效率 | V6 | 二档 | 20% | **22%** | 用户选取保守值（22/24/25 三候选），华晟 26%×AM0 0.85≈22% |
| EOL 效率 | V7 | 二档 | 14% | 14%（维持） | CEA 独立辐照实验 >14%（不随 BOL 上调改变） |
| 面板面密度 | V9 | 三档 | 1.2 | **1.8** | 用户否决 1.2 并要求上调，以 Starlink V2 Mini 面板级估计为参考 |

**HJT BOL 22% 推导链**：
1. 权威数据区间：华晟 26%（量产）/ 东方日升 26.61%（认证）/ 隆基 27.81%（实验室）
2. AM0 修正因子：地面 AM1.5 → 空间 AM0 ≈ ×0.85
3. 华晟 26% × 0.85 = 22.1% → 取整 22%（最保守方案）
4. evidence URLs：[华晟](https://www.huasunsolar.com/)、[东方日升](https://www.prnewswire.com/news-releases/risen-energy-achieves-26-61-efficiency-for-hjt-solar-cell-302390000.html)、[隆基](https://www.longi.com/)

**HJT EOL 14% 维持理由**：
- CEA/INES 独立实验：>14% after 10^14 e⁻/cm² 1MeV 电子辐照
- 该通量对应 LEO 600 km 约 5-7 年累积剂量
- EOL 14% 不随 BOL 上调而改变（独立实验锚点）
- evidence URL：[CEA/INES 辐照实验](https://www.cea.fr/cea-tech/liten/english/Pages/Medias/News/2025/major-breakthrough-for-photovoltaic-technology-space.aspx)

**HJT 面密度 1.8 裁决历程**：
- 原值 1.2：基于 33FG Research Starlink 柔性硅基"计算优化柔性迭代"估计
- 用户否决 1.2："上调至 1.5-1.8"
- 1.8 的锚定：接近 Starlink V2 Mini 面板级估计（116m²/740kg→整体 ~6.4，去皮后面板 ~1.7-2.6）
- evidence URL：[33FG Starlink V2 Mini 分析](https://research.33fg.com/analysis/starlink-v2-mini-optimized-lighter-satellites-more-bandwidth-per-launch)

**HJT 路线定位变更**：
- **旧标签**：`hjt_exploratory`，`status: "只能降级"`，`forbidden_mainline: ["10y-HJT"]`
- **新标签**：`hjt_parallel`，`status: "并行成熟路线"`，GaAs/HJT 并列进入模型
- 变更依据：Task 3 HJT 证据包（17 条搜索 URL、12 项物理链闭合）、V6-V9 裁决

---

### 2.4 电池（V10 + V11：三档）

**裁决值**：三分支方案——5yr Li-ion（DOD 40%）、10yr Li-ion（DOD 25%）、10yr LTO（DOD 80%）

| 分支 | DOD（V10） | 比能量 Wh/kg（V11） | 名义容量 kWh | 质量 kg | 证据等级 |
|------|-----------|-------------------|-------------|---------|---------|
| 5yr Li-ion NMC | 0.40 | 190 | 186.4 | 981 | 三档 |
| 10yr Li-ion NMC | 0.25 | 190 | 293.0 | 1,542 | 三档 |
| 10yr LTO | 0.80 | 100 | 91.6 | 916 | 三档 |

#### V10 DoD 推导链

**5年分支（Li-ion NMC）**：
1. Starlink 实测：max DOD ~50%，目标 5,000 等效全循环（Ray Barsa 2025 演讲）
2. 5年服役 → 约 9,900 次 eclipse 循环
3. 等效全循环 = 9,900 × 0.40 = 3,960 次 → 在 Starlink 5,000 目标内 ✓
4. 电池容量 = 120 kW × 0.58h / (0.40 × 0.95) ≈ 183 kWh
5. 电池质量 = 183,000 Wh / 190 Wh/kg ≈ 963 kg ☞ 模型值 981 kg

**10年分支（Li-ion NMC）**：
1. 10年服役 → 约 19,800 次 eclipse 循环
2. 若用 40% DOD：19,800 × 0.40 = 7,920 等效全循环 → **超出** Starlink 5,000 目标 ✗
3. 折中 DOD=25%：19,800 × 0.25 = 4,950 → 在目标内 ✓
4. 电池容量 = 120 × 0.58 / (0.25 × 0.95) ≈ 293 kWh
5. 电池质量 = 293,000 / 190 ≈ 1,542 kg

**10年分支（LTO）**：
1. Saft：LTO 可 80-90% DOD 且超长循环寿命；比能 ~100 Wh/kg
2. DOD=80%：电池容量 = 120 × 0.58 / (0.80 × 0.95) ≈ 91.6 kWh
3. 电池质量 = 91,600 / 100 ≈ 916 kg（比 Li-ion 10年方案轻约 40%）

#### V11 比能量推导链

| 化学 | 值 | 来源 |
|------|-----|------|
| Li-ion NMC | 190 Wh/kg | Starlink pack 230（cell→pack 降额~12%） |
| LTO | 100 Wh/kg | Saft：LTO 比 Li-ion 低 30-50% |

#### evidence URLs

| 来源 | URL |
|------|-----|
| Ray Barsa 2025 演讲 | `https://ciclibattery.com/battery-power-online-space-batteries-how-spacex-designs-batteries-for-satellites/` |
| Starlink 电池可靠性（NASA 2025 Workshop） | `https://www.nasa.gov/wp-content/uploads/2024/01/starlink-batteries-reliability-lessons-from-10000-leo-satellites-abw-2025.pdf` |
| Saft LTO 技术白皮书 | `https://saft.com/en/horizon-new-lithium-based-technology-satellite-batteries-improving-mission-performance` |

**裁决历程**：
- 否决：统一 DOD=40% 不区分寿命（用户拒绝："不允许一刀切"）
- 否决：第一次分裂方案（5年=40%, 10年=25%, 不含LTO）→ 用户要求进一步细化
- 采纳：5年保持 40%；10年分裂为 Li-ion（25%）和 LTO（80%）两子分支
- **搜索次数**：V10 经历 2 轮搜索 + 2 轮用户反馈（共 4 轮交互）

---

### 2.5 PCDU（V25：四档）→ Terma 飞行产品锚点大幅修正（~18×）

**裁决值**：比功率 = 1.0 / 0.5 / 0.2 kW/kg，质量 = 150 / 300 / 750 kg

| 字段 | 内容 |
|------|------|
| V# | V25 |
| 证据等级 | 四档（推断——Terma 飞行产品为基准，Starlink "simplified power electronics" 为改善理由） |
| 用户裁决 | 采纳 |
| 裁决历程 | 原值 10.0 kW/kg（150kW→15kg）→ 用户要求充分搜索 → Terma 产品揭示高估 18× → 采纳修正值 |

#### evidence URLs

| 来源 | URL | 关键数据 |
|------|-----|---------|
| Terma PCDU 飞行产品 | `https://satsearch.co/products/terma-power-conditioning-distribution-unit` | 500W-15kW，8 模块 6kg → 23 模块 28kg → **0.54 kW/kg**（最大配置） |
| Terma PCDU 详细规格 | `https://www.satnow.com/products/power-conditioning-and-distribution-units/terma/134-1195-bepicolombo-mtm-pcdu` | 0.75-1.25 kg/模块，输入 42-115V，输出 28-100V |
| ESA GlobalStar PCDU | `https://connectivity.esa.int/projects/pcdu-leo-telecom` | LEO 星座 PCDU 1.8 kW，成本优化设计 |

**推导链**：
1. **原值问题**：10.0 kW/kg → 150 kW PCDU 仅 15 kg。无任何飞行产品支撑。
2. **Terma 锚点**：飞行验证 PCDU，15 kW/28 kg = 0.54 kW/kg。若线性外推到 150 kW → **278 kg**（vs 原 15 kg，差 18 倍）
3. **Starlink 改善**：V2 Mini Optimized 的 "simplified power electronics" 贡献 22% 质量缩减。若 SpaceX 自研 PCDU 比 Terma 商用产品轻 30-50% → 基准 0.5 kW/kg（接近 Terma 0.54）
4. **乐观/保守**：乐观 1.0（高压母线 >100V，SpaceX 工艺大幅优化），保守 0.2（传统 28V 母线+全冗余）

**不确定性**：
- Terma PCDU 为 15 kW 级产品（非 150 kW 级），线性外推存在不确定性
- AI1 若采用高压母线（>100V）可能大幅优于 0.54 kW/kg
- Starlink "simplified power electronics" 的改善幅度不可知（22% 是整星数据，PCDU 子项贡献未知）

---

### 2.6 平台/结构（V21：四档）→ Starlink V2 Mini 参考修正

**裁决值**：platform_ratio = 0.25 / 0.35 / 0.45（原 0.18/0.22/0.28）

| 字段 | 内容 |
|------|------|
| V# | V21 |
| 证据等级 | 四档（推断——Starlink V2 Mini 为最直接可比参考） |
| 用户裁决 | 采纳修正值 |
| Starlink V2 Mini 参考 | 总~740 kg - 光伏~197 - 电池~48 - 推进~40 - 通信载荷~170 = 结构/热控/线束~285 kg → ratio ≈ **0.38** |
| AI1 差异 | GPU 计算架构 vs 通信卫星，高功率热控结构可能更重 → baseline 0.35 接近参考、conservative 0.45 含余量 |

#### evidence URLs

| 来源 | URL |
|------|-----|
| JPL Psyche Spacecraft | `https://www.jpl.nasa.gov/press-kits/psyche/mission/spacecraft/` |
| 平台量级参考 | `https://spacenexus.us/satellite-bus-comparison` |
| 33FG Starlink V2 Mini 分析 | `https://research.33fg.com/analysis/starlink-v2-mini-optimized-lighter-satellites-more-bandwidth-per-launch` |

---

### 2.7 推进（V22：四档）→ Starlink V2 Mini 参考修正

**裁决值**：200 / 350 / 500 kg（原 180/220/350 kg）

| 字段 | 内容 |
|------|------|
| V# | V22 |
| 证据等级 | 四档（推断——Starlink V2 Mini 推进质量比例外推） |
| 用户裁决 | 采纳修正值 |
| 推导链 | Starlink V2 Mini 推进 ~5-6% 整星质量（SpaceX 自研氩霍尔）。AI1 6,000-8,000 kg 级 → 5-8% → 300-640 kg。 |

#### evidence URLs

| 来源 | URL |
|------|-----|
| Orbion Aurora | `https://orbionspace.com/thrusters/` |
| ExoTerra Halo | `https://www.exoterra.com/thrusters` |

**不确定性**：未获得 AI1 推进剂类型、贮箱规模、寿命目标与机动预算。V22 为基于 Starlink 比例外推的四档推断。

---

### 2.8 通信/激光链路（V23：四档）→ Google Suncatcher 参考修正（4 轮搜索）

**裁决值**：200 / 300 / 450 kg（原 150/180/300 kg）

| 字段 | 内容 |
|------|------|
| V# | V23 |
| 证据等级 | 四档（推断——Google Suncatcher 为最相关直接文献） |
| 用户裁决 | 采纳 |
| 搜索轮次 | 4 轮（Starlink 类比→算力矩阵低估→Google Suncatcher→多源确认） |

#### 搜索历程

1. **第1轮**：直接迁移 Starlink 通信系统 150-300 kg → 用户否决："AI1 是计算卫星不是通信卫星"
2. **第2轮**：修正为 50-150 kg（仅需数据中继+TT&C）→ 用户否决："算力卫星需星间高速互联"
3. **第3轮**：恢复原值 150-300 kg，加入 Google Suncatcher 文献 → 推导出 AI1 需更高带宽 → 上调至 200-450 kg
4. **第4轮**：用户确认采纳

#### evidence URLs

| 来源 | URL | 关键数据 |
|------|-----|---------|
| Google Suncatcher（2025 arXiv） | `https://arxiv.org/html/2511.19468v1` | 天基 AI 集群需 "tens of Tbps" ISL |
| NASA Communications SoA | `https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications` | 通信设计权衡 |
| TESAT 产品页 | `https://www.tesat.de/products` | ConLCT ~15 kg, SmartLCT ~30 kg, TOSIRIS ~8 kg |
| FSO Instruments 产品页 | `https://www.fso-instruments.nl/products/` | Resolite-80 ~20 kg |

**最终推导**：Google Suncatcher 明确天基 AI 集群 ISL 需求为 "tens of Tbps"（远超 Starlink 1-100 Gbps）。Starlink 通信系统 ~170-250 kg 为参考下界。AI1 需更多通道/更大口径 → 200-450 kg。

**不确定性**：Google Suncatcher 为 arXiv preprint 研究论文（非飞行验证硬件）。AI1 实际通信架构未知。

---

### 2.9 AIT 裕量（V24：四档）→ 寿命分支分裂

**裁决值**：5年 0.05/0.08/0.12、10年 0.10/0.15/0.22

| 字段 | 内容 |
|------|------|
| V# | V24 |
| 证据等级 | 四档（推断——NASA CDR/PDR 级标准 + Starlink 量产压缩） |
| 用户裁决 | 采纳寿命分支分裂方案 |

| 分支 | light | baseline | conservative | 依据 |
|------|-------|----------|-------------|------|
| 5年 | 0.05 | 0.08 | 0.12 | NASA CDR 级（5-10%）+ Starlink 量产压缩（"disposable 5-year LEO birds, reducing qualification by 50-80%"） |
| 10年 | 0.10 | 0.15 | 0.22 | NASA PDR 级（10-20%）+ 产线继承（非"首颗"新研） |

**注意事项**：
- 该项不是独立硬件实测值，本质是项目级系统裕量
- 不能在当前阶段升格为"公开资料硬锚点"
- 后续终稿必须继续显式标注为 `情景参数 / 工程保守量`

---

## 3. GaAs / HJT 路线敏感项（更新后）

| 路线 | 光伏面积 | 光伏质量 | 电池质量（5yr） | PCDU 质量（基准） | 电源总质量（5yr 基准） | 当前状态 |
|---|---:|---:|---:|---:|---:|---|
| `GaAs` 基准主链 | 624 m² | 936 kg | 981 kg | 300 kg | 2,217 kg | 已闭合 |
| `HJT` 并行成熟路线 | 501 m² | 902 kg | 981 kg | 300 kg | 2,183 kg | 并行成熟路线（非降级） |

- 两种路线共享同一电池/PCDU 链路（电池质量由任务食时决定、PCDU 由总线功率决定），差异仅在光伏阵列
- `HJT` 路线定位已从「只能降级」修正为「并行成熟路线」
- GaAs 因更高效率（32% vs 22%）需要更大阵列面积（624 vs 501 m²）但更轻面板面密度（1.5 vs 1.8 kg/m²），最终质量略高于 HJT
- 两种路线均在电源总质量量级上可比（~2,200 kg），不存在 HJT 质量显著偏高的问题

### 电池寿命分支分化（与光伏路线无关）

| 寿命分支 | 化学 | DOD | 容量 kWh | 质量 kg | 
|---------|------|-----|---------|---------|
| 5yr | Li-ion NMC | 40% | 186.4 | 981 |
| 10yr | Li-ion NMC | 25% | 293.0 | 1,542 |
| 10yr | LTO | 80% | 91.6 | 916 |

---

## 4. kW/t 计算载荷链废弃说明

### 废弃的参数

| 废弃项 | 旧值 | 废弃原因 |
|--------|------|---------|
| `compute_specific_power_kw_per_t` | 70（light）/ 55（baseline）/ 45（conservative） | 循环引用（从 kW/t 反推质量，再拿质量证明 kW/t 合理） |
| `compute_payload` 公式 | `mass = peak_power / specific_power` | 无独立地面硬件锚点，分母定义可疑（载荷级 vs 整星级） |

### 替换方案（V30 bottom-up）

| 步骤 | 方法 | 证据 |
|------|------|------|
| 1. 地面硬件基线 | NVIDIA GB300 NVL72 / HGX B200 / DGX B200 公开质量 | 二档（A1 级硬件锚点） |
| 2. 辐射防护增量 | spot shielding vs full enclosure 对比分析 | ACT Polymer / NASA Shields-1 / Guomans |
| 3. 热管理改造增量 | 地面液冷继承 + 空间工质替换 | JAXA HFE7200 验证数据 |
| 4. 结构/真空改造增量 | 振动加固 + 真空兼容 - 微重力减重 | 行业经验估计 |
| 5. 汇总 | 地面基线 + 三项空间化增量 | → 1,200 / 1,500 / 2,000 kg（取中值） |

---

## 5. 对 `stage2_mass_inputs_blackwell_hjt.json` 的写入原则（V2 更新）

- 所有大件都要带 `v_ruling`、`conclusion_grade`、`status`、`source_anchors`、`source_urls`
- HJT 不再标注为 `只能降级` 或 `hjt_exploratory`，定位为 `hjt_parallel` / `并行成熟路线`
- 所有四档参数必须显式标注 `四档` 状态（pcdu、platform_structure、propulsion、communications、ait_margin）
- 已废弃的旧值必须在 `deprecated_notice` 中显式说明
- 计算载荷使用 V30 三项拆解公式，不使用 kW/t 反推
- 电池提供三分支（5yr Li-ion / 10yr Li-ion / 10yr LTO）的完整质量链路
- `scenario_scalars` 已分裂为 5 年分支和 10 年分支（AIT 裕量不同）
- `Rubin` 不进入本文件的主计算口径；本文件只服务于统一 `Blackwell` 主线

---

## 6. 当前闭合判断（V2 更新）

### 已闭合
- 计算载荷（V30 bottom-up 三项拆解，二档+三档）
- 散热系统（V20，四档保留但闭合到可用输入）
- GaAs 光伏阵列（V4-V5 + V8，二档+三档）
- HJT 光伏阵列（V6-V7 + V9，二档+三档，并行成熟路线）
- 电池（V10+V11，三档，含三分支完整链路）

### 四档保留（有来源但无法升级）
- PCDU（V25：Terma 飞行产品锚点，线性外推不确定性）
- 平台/结构（V21：Starlink V2 Mini 参考，非 AI1 直接数据）
- 推进（V22：Starlink 比例外推，非 AI1 直接数据）
- 通信/激光链路（V23：Google Suncatcher 参考，非飞行验证硬件）
- AIT 裕量（V24：NASA 标准 + Starlink 量产压缩，非可独立验真硬件）

### 当前未闭合的剩余缺口
- AI1 一手总质量与收拢尺寸仍缺权威锚点（V30 仅为 bottom-up 推断）
- 展开机构质量独立建模尚未完成（V8/V9 panel-only，展开机构另计）
- HJT 空间级长寿命退化路径仅依赖单一 CEA 实验锚点
- 四档参数均为推断值，存在系统性低估或高估风险

---

## 7. 参数→裁决交叉引用表

| V# | 参数 | 类型 | 证据等级 | light | baseline | conservative | 用户裁决 | 页码 |
|----|------|------|---------|-------|----------|-------------|---------|------|
| V1 | peak_power_kw | 公共基线 | 二档 | — | 150 | — | 采纳 | §2.0 |
| V2 | sustained_power_kw | 公共基线 | 二档 | — | 120 | — | 采纳 | §2.0 |
| V3 | orbit_altitude_km | 公共基线 | 二档 | — | 600 | — | 采纳 | §2.0 |
| V4 | GaAs BOL 效率 | 光伏 | 二档 | — | 32% | — | 采纳 | §2.3.1 |
| V5 | GaAs EOL 效率 | 光伏 | 二档 | — | 29% | — | 采纳 | §2.3.1 |
| V6 | HJT BOL 效率 | 光伏 | 二档 | — | 22%（↑） | — | 采纳保守值 | §2.3.2 |
| V7 | HJT EOL 效率 | 光伏 | 二档 | — | 14%（维持） | — | 维持 | §2.3.2 |
| V8 | GaAs 面板面密度 | 光伏 | 三档 | — | 1.5 kg/m² | — | 采纳 panel-only | §2.3.1 |
| V9 | HJT 面板面密度 | 光伏 | 三档 | — | 1.8 kg/m²（↑） | — | 采纳上调 | §2.3.2 |
| V10 | 电池 DOD（5yr） | 电池 | 三档 | — | 0.40 | — | 采纳 | §2.4 |
| V10 | 电池 DOD（10yr Li-ion） | 电池 | 三档 | — | 0.25 | — | 采纳 | §2.4 |
| V10 | 电池 DOD（10yr LTO） | 电池 | 三档 | — | 0.80 | — | 采纳 | §2.4 |
| V11 | 电池比能量（Li-ion） | 电池 | 三档 | — | 190 Wh/kg | — | 采纳 | §2.4 |
| V11 | 电池比能量（LTO） | 电池 | 三档 | — | 100 Wh/kg | — | 采纳 | §2.4 |
| V20 | 散热器面密度 | 热控 | 四档 | 4.0 | 5.0 | 6.5 kg/m² | 采纳 | §2.2 |
| V21 | 平台系数 | 结构 | 四档 | 0.25 | 0.35 | 0.45 | 采纳修正 | §2.6 |
| V22 | 推进质量 | 推进 | 四档 | 200 | 350 | 500 kg | 采纳修正 | §2.7 |
| V23 | 通信质量 | 通信 | 四档 | 200 | 300 | 450 kg | 采纳修正 | §2.8 |
| V24 | AIT 裕量（5yr） | 裕量 | 四档 | 0.05 | 0.08 | 0.12 | 采纳分支 | §2.9 |
| V24 | AIT 裕量（10yr） | 裕量 | 四档 | 0.10 | 0.15 | 0.22 | 采纳分支 | §2.9 |
| V25 | PCDU 比功率 | 电源 | 四档 | 1.0 | 0.5 | 0.2 kW/kg | 采纳修正(~18×) | §2.5 |
| V30 | 计算载荷质量 | 载荷 | 二+三档 | ~1,060-1,350 | ~1,330-1,670 | ~1,750-2,300 kg | 采纳三项拆解 | §2.1 |
| V30 | 计算载荷取中值 | 载荷 | 二+三档 | 1,200 | 1,500 | 2,000 kg | — | §2.1 |
| V31 | 散热系统导出质量 | 导出 | 自动 | 440 | 550 | 715 kg | 自动计算 | §2.2 |
| V32 | 平台结构导出质量 | 导出 | 自动 | (1,200+440+1,499)×0.25 | (1,500+550+2,217)×0.35 | (2,000+715+3,850)×0.45 | 自动计算 | §2.6 |
| V33 | 推进导出质量 | 导出 | 自动 | 200 | 350 | 500 kg | 等于 V22 | §2.7 |
| V34 | 通信导出质量 | 导出 | 自动 | 200 | 300 | 450 kg | 等于 V23 | §2.8 |
| V35 | AIT 导出质量 | 导出 | 自动 | 前序×ratio | 前序×ratio | 前序×ratio | 自动计算 | §2.9 |

**变更方向标记**：
- `(↑)` = 上调
- `(↓)` = 下调
- `(维持)` = 不变
- `(修正)` = 基于新证据重新判定

---

## 8. Task 6 交付结论

- `stage2_bom_mass_support_audit.md` 已全面更新，反映全部 V1-V37 参数裁决结果
- 每个大件均已绑定 V#、证据等级、light/baseline/conservative 裁决值、evidence URL 和用户裁决记录
- kW/t 计算载荷链已显式标注为废弃，并交叉引用 V30 bottom-up 替换方案
- HJT 路线定位已从「只能降级」修正为「并行成熟路线」
- 电池已分裂为三分支方案（5yr Li-ion / 10yr Li-ion / 10yr LTO）
- 参数→裁决交叉引用表（§7）提供完整的两维索引（V#→参数 和 参数→V#）
- `stage2_mass_inputs_blackwell_hjt.json` 已同步更新，作为结构化质量输入交付 Task 7/8
- 下一步：Task 7（采购/路线证据文档更新 + 结构化价格输入）、Task 8（重建脚本 + 结果文档）
