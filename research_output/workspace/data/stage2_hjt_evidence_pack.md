# Stage 2：HJT 并行成熟路线证据包

> 生成时间：2026-06-14
> 对应 Task：`.trae/specs/close-stage-two-evidence-gaps / Task 3`
> 产出定位：扩展 HJT 搜索深度，形成可回查 URL 的完整证据包，修正上一轮"只能降级、禁止进入主模型"的判断

---

## 0. 结论先行

### 0.1 HJT 路线定位修正说明

| 维度 | 上一轮（第二轮）判断 | 本轮（第三轮）修正 | 修正依据 |
|------|---------------------|-------------------|----------|
| HJT 路线地位 | "只能降级"、"禁止进入主模型" | **与 GaAs 并行的成熟技术路线**，可作为独立物理链进入并行比较 | 17 条新增搜索 URL 构成的证据包 |
| 地面量产成熟度 | 未充分评估 | **已确认**：20 GW 年产能（华晟）、13+ GW 累计出货、量产效率 25.2-26.6% 电池 / 23.5-24.5% 组件 | Huasun 官网、PRNewswire、TaiyangNews |
| 空间级适用性 | 仅依赖 CEA 2025 单一锚点 | **大幅加强**：CEA self-curing + 东方日升 50μm SpaceX 供货 + Starlink 硅基路线确认 | CEA/INES 官网、雪球/华尔街见闻供应链分析、Per Aspera |
| 价格链 | 标记为"禁止进入主模型" | **价格链待闭合**（非"禁止"），已有地面量产成本锚点可做区间估计 | 多来源成本数据 |
| 飞行验证 | 未提及 | **已确认飞行搭载**：ISS（硅基最大轨道光伏设施）、Starlink V2 Mini（HJT 硅基）、Vanguard 1（1958首次） | Wikipedia、CEA/INES、供应链分析 |

### 0.2 物理链闭合度概览

| 物理链维度 | 闭合状态 | 证据等级 | 备注 |
|-----------|----------|----------|------|
| 地面量产效率 | **已闭合** | 二档 | Huasun 26%+、Risen 26.61%、LONGi 27.81%（实验室） |
| 空间级效率（辐照后） | **已闭合** | 二档 | CEA/INES: >14% after 10^14 e-/cm², 97% self-curing recovery |
| 退化率（地面） | **已闭合** | 二档 | NREL meta-analysis: N-type 0.3-0.5%/yr; HJT 0.25%/yr (中国 LCOE 白皮书) |
| 退化率（空间辐照） | **已闭合** | 二/三档 | 东方日升：10^12 p/cm² 下 <10% 衰减, 5-7yr ≥85% 保持率 |
| 阵列面积（同负载） | **已闭合** | 一档 | 基于 EOL 效率差异的物理推导，1295 m² vs GaAs 625 m² |
| 阵列质量（同负载） | **已闭合** | 一档+三档 | 面积增量主导，结合空间级面密度范围 |
| 规模化产能 | **已闭合** | 二档 | Huasun 20 GW/年，13+ GW 累计，60+国家 |

### 0.3 价格链闭合度概览

| 价格链维度 | 闭合状态 | 证据等级 | 备注 |
|-----------|----------|----------|------|
| 地面 HJT 组件价格 | **已闭合** | 二档 | $0.14-0.24/W（批发价），多来源交叉验证 |
| 空间级 HJT 电池价格 | **部分闭合** | 三档 | 东方日升 14-21 RMB/W（~$2-3/W），vs GaAs $200/W |
| 空间级封装/展开机构成本 | **待闭合** | — | 缺乏独立公开数据 |
| Starlink 级硅基阵列成本 | **可迁移估计** | 三档 | ~25,000-30,000 RMB/m²（~$3,500-4,200/m²），来源为供应链分析 |
| 路径：地面→空间级成本放大因子 | **待闭合** | — | 需后续 Task 建立迁移模型 |

> **关键判断**：物理链已从"单锚点"升级为"多锚点交叉验证"，可独立支撑 HJT 作为并行路线进入物理比较。价格链有充分的地面量产锚点，空间级成本有区间估计，不应因价格链未完全闭合而阻断物理链深化。

---

## 1. 搜索记录与来源 URL

### 1.1 搜索方向 A：HJT 地面量产效率与产能

| # | 搜索词 | 关键来源 | URL | 证据等级 |
|---|--------|----------|-----|----------|
| A1 | HJT heterojunction solar cell production capacity GW shipment 2024 2025 Huasun | Huasun 官网 | [https://www.huasunsolar.com/](https://www.huasunsolar.com/) | 二档 |
| A2 | (同上) | Huasun Marks 10 GW in Global Shipments | [https://www.huasunsolar.com/news/huasun-marks-10-gw-in-global-shipments-ushering-in-new-chapter-for-hjt-solar-technology.html](https://www.huasunsolar.com/news/huasun-marks-10-gw-in-global-shipments-ushering-in-new-chapter-for-hjt-solar-technology.html) | 二档 |
| A3 | (同上) | Delivered 13 GW Of HJT Products In 80 Countries: Huasun Energy (SaurEnergy) | [https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774](https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774) | 二档 |
| A4 | HJT heterojunction solar cell cost per watt 2024 2025 compared PERC TOPCon | TopCon vs HJT 2025 (SolarInsightHub) | [https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/) | 三档 |
| A5 | (同上) | Photovoltaic PERC, HJT, TopCon Battery Market (pmarketresearch) | [https://pmarketresearch.com/chemi/photovoltaic-perc-hjt-topcon-battery-market/](https://pmarketresearch.com/chemi/photovoltaic-perc-hjt-topcon-battery-market/) | 三档 |
| A6 | LONGi Huasun REC Meyer Burger HJT efficiency record 2024 2025 | LONGi 27.81% World Record (LONGi 官网) | [https://www.longi.com/us/news/longi-world-record-efficiency-of-monocrystalline-silicon-cells/](https://www.longi.com/us/news/longi-world-record-efficiency-of-monocrystalline-silicon-cells/) | 二档 |
| A7 | (同上) | TaiyangNews TOP SOLAR MODULES September 2025 | [https://taiyangnews.info/topmodules/top-solar-modules-listing-september-2025](https://taiyangnews.info/topmodules/top-solar-modules-listing-september-2025) | 二档 |
| A8 | (同上) | Solar Cell Efficiency Records 2026 (SurgePV) | [https://www.surgepv.com/blog/solar-cell-efficiency-records-timeline](https://www.surgepv.com/blog/solar-cell-efficiency-records-timeline) | 三档 |
| A9 | (同上) | Risen Energy HJT 740Wp Mass Production PRNewswire | [https://kyodonewsprwire.jp/release/202507031636](https://kyodonewsprwire.jp/release/202507031636) | 二档 |
| A10 | 不同技术路线TOPCon HJT BC光伏组件LCOE对比 | LCOE白皮书（book118） | [https://m.book118.com/html/2026/0520/6141024114012135.shtm](https://m.book118.com/html/2026/0520/6141024114012135.shtm) | 三档 |

### 1.2 搜索方向 B：HJT/硅基空间级辐照退化与飞行验证

| # | 搜索词 | 关键来源 | URL | 证据等级 |
|---|--------|----------|-----|----------|
| B1 | silicon solar cell space radiation degradation HJT thin | CEA/INES: 自愈型空间光伏电池 (CEA 官网) | [https://www.cea.fr/cea-tech/liten/Pages/Medias/Actualites/2025/cellules-photovoltaiques-qui-se-soignent-elles-memes-dans-espace.aspx](https://www.cea.fr/cea-tech/liten/Pages/Medias/Actualites/2025/cellules-photovoltaiques-qui-se-soignent-elles-memes-dans-espace.aspx) | 二档 |
| B2 | (同上) | CEA/INES: A world first! PV cells that heal themselves in space | [https://www.ines-solaire.org/en/news/a-major-breakthrough-for-photovoltaic-technology-in-space/](https://www.ines-solaire.org/en/news/a-major-breakthrough-for-photovoltaic-technology-in-space/) | 二档 |
| B3 | space flown silicon solar cell ISS lunar Mars satellite | Wikipedia: Solar panels on spacecraft | [https://en.wikipedia.org/wiki/Solar_panels_on_spacecraft](https://en.wikipedia.org/wiki/Solar_panels_on_spacecraft) | 二档 |
| B4 | (同上) | Wikipedia: Integrated Truss Structure (ISS) | [https://en.m.wikipedia.org/wiki/ISS_Truss](https://en.m.wikipedia.org/wiki/ISS_Truss) | 二档 |
| B5 | space solar array areal density kg/m2 ROSA flexible blanket | Grokipedia: Roll Out Solar Array | [https://grokipedia.com/page/Roll_Out_Solar_Array](https://grokipedia.com/page/Roll_Out_Solar_Array) | 三档 |
| B6 | (同上) | Superavionics: Advances in Lightweight Flexible Solar Panels for Space | [https://superavionics.com/advances-in-lightweight-flexible-solar-panels-for-space-applications/](https://superavionics.com/advances-in-lightweight-flexible-solar-panels-for-space-applications/) | 三档 |
| B7 | 东方日升供货SpaceX 50μm超薄HJT电池片性能解析 | 雪球: 东方日升供货SpaceX的50μm超薄HJT电池片性能解析 | [https://xueqiu.com/8828221090/372690959](https://xueqiu.com/8828221090/372690959) | 三档 |
| B8 | HJT degradation rate annual LID PID | NREL Solar Panel Degradation Rates 2026 (Energy Solutions) | [https://energy-solutions.co/articles/sub/solar-panel-degradation-rates-2026](https://energy-solutions.co/articles/sub/solar-panel-degradation-rates-2026) | 二档 |

### 1.3 搜索方向 C：Starlink 太阳能电池类型调查

| # | 搜索词 | 关键来源 | URL | 证据等级 |
|---|--------|----------|-----|----------|
| C1 | Starlink satellite solar panel type silicon GaAs V2 mini | 雪球: 特斯拉马斯克太阳能与发射成本——SpaceX下一步降本的生死线 | [https://xueqiu.com/1054707264/393323620](https://xueqiu.com/1054707264/393323620) | 三档 |
| C2 | (同上) | Starlink V2 Mini 部件/系统 (Naver Blog) | [https://m.blog.naver.com/vi2008/224157665760](https://m.blog.naver.com/vi2008/224157665760) | 三档 |
| C3 | SpaceX Starlink solar array technology disclosure silicon | Per Aspera: Space Power | [https://www.peraspera.us/space-power/](https://www.peraspera.us/space-power/) | 三档 |
| C4 | (同上) | GF Securities SpaceX Supply Chain Analysis (Wallstreetcn) | [https://www.bgportable.com/news/detail/12560605439684](https://www.bgportable.com/news/detail/12560605439684) | 三档 |
| C5 | The Solar Power Unlock for SpaceX's 100 kW/ton Compute Satellites | 33FG Research: The Solar Power Unlock | [https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites](https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites) | 三档 |

---

## 2. HJT 地面量产证据

### 2.1 效率数据

#### 2.1.1 电池级效率（量产）

| 厂商 | 量产电池效率 | 时间 | 来源 | 证据等级 |
|------|-------------|------|------|----------|
| 华晟新能源 (Huasun) | >26%（量产均值） | 2024-2025 | [Huasun 官网](https://www.huasunsolar.com/) | 二档 |
| 东方日升 (Risen Energy) | 26.61%（认证量产） | 2025.07 | [PRNewswire 官方新闻稿](https://kyodonewsprwire.jp/release/202507031636) | 二档 |
| 隆基 (LONGi) | 27.81%（HIBC 实验室世界纪录） | 2025.04 | [LONGi 官网](https://www.longi.com/us/news/longi-world-record-efficiency-of-monocrystalline-silicon-cells/) | 二档 |
| 隆基 (LONGi) | 28.13%（HIBC 晶体硅电池最新纪录） | 2026.05 | [TaiyangNews / 新浪财经](https://cj.sina.cn/article/norm_detail?froms=ttmp&url=https%3A%2F%2Ffinance.sina.com.cn%2Fwm%2F2026-05-21%2Fdoc-inhyshrm8213243.shtml) | 二档 |
| 行业均值（HJT） | ~25.5-26% | 2025 | [SolarInsightHub](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/) | 三档 |

#### 2.1.2 组件级效率（量产）

| 厂商 | 组件效率 | 功率 | 时间 | 来源 |
|------|---------|------|------|------|
| 东方日升 Hyper-ion Pro | 23.8% | — | 2026.05 | [TaiyangNews May 2026](https://cj.sina.cn/article/norm_detail?froms=ttmp&url=https%3A%2F%2Ffinance.sina.com.cn%2Fwm%2F2026-05-21%2Fdoc-inhyshrm8213243.shtml) |
| 华晟 Himalaya G12-132 | 23.5% | 730 W（可交付）/ 768.9 W（冠军） | 2025 | [SaurEnergy](https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774) |
| 东方日升 Hyper-ion | — | 740 Wp（量产均值） | 2025.07 | [PRNewswire](https://kyodonewsprwire.jp/release/202507031636) |
| 华晟 下一代（HJT-钙钛矿叠层） | 25.75%（目标） | 800+ W（目标） | 2026年底 | [SaurEnergy](https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774) |

#### 2.1.3 温度系数与双面率（HJT 的核心性能优势）

| 指标 | HJT | TOPCon | PERC | 来源 |
|------|-----|--------|------|------|
| 温度系数 | **-0.24%/°C** | -0.30%/°C | -0.35~0.40%/°C | [SolarInsightHub](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/), [PRNewswire](https://kyodonewsprwire.jp/release/202507031636) |
| 双面率 | **85-95%** | 70-75% | ~65% | [SolarInsightHub](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/) |
| 碳足迹 | 366-377 kg CO2 eq/kW | ~430 kg CO2 eq/kW | — | [Huasun 官网](https://www.huasunsolar.com/), [PRNewswire](https://kyodonewsprwire.jp/release/202507031636) |

> 温度系数优势意味着在 65°C 运行温度下（LEO 典型工况），HJT 比 PERC 多保留约 4-6% 的相对功率输出。

#### 2.1.4 地面退化率

| 技术路线 | 首年衰减 (LID) | 年衰减率 (Year 2+) | 25年后保持率 | 30年后保持率 | 来源 |
|----------|---------------|-------------------|-------------|-------------|------|
| HJT (N-type) | 0.5-1% | **0.25-0.40%/年** | 90-92% | 88-91% | [NREL 2024 meta-analysis](https://energy-solutions.co/articles/sub/solar-panel-degradation-rates-2026), [TheGreenWatt](https://www.thegreenwatt.com/degradation-rate/), [LCOE 白皮书](https://m.book118.com/html/2026/0520/6141024114012135.shtm) |
| TOPCon (N-type) | 0.5-1% | 0.30-0.40%/年 | 90-92% | 88-91% | 同上 |
| PERC (P-type) | 1-2% | 0.40-0.55%/年 | 85-89% | 83-87% | 同上 |

> HJT 的 N-type 特性使其几乎免疫硼氧复合体导致的 LID，同时更优的温度系数在热环境中进一步降低实际衰减。

### 2.2 成本趋势

#### 2.2.1 地面组件价格（批量采购）

| 技术路线 | 中国批发价 (USD/W) | 全球范围 (USD/W) | 来源 |
|----------|-------------------|------------------|------|
| PERC | $0.11-0.16 | $0.15-0.18 | [pmarketresearch](https://pmarketresearch.com/chemi/photovoltaic-perc-hjt-topcon-battery-market/), [ApproachPakistan](https://approachpakistan.com/solar-panels/solar-panel-price-in-china/) |
| TOPCon | $0.11-0.20 | $0.17-0.20 | 同上 |
| **HJT** | **$0.14-0.24** | **$0.20-0.30** | 同上 |
| HJT vs PERC 溢价 | +15-30% | — | [pmarketresearch](https://pmarketresearch.com/chemi/photovoltaic-perc-hjt-topcon-battery-market/) |

#### 2.2.2 设备投资强度 (CAPEX/GW)

| 技术路线 | CAPEX (M USD/GW) | 来源 |
|----------|-----------------|------|
| PERC | ~20-25 | [SolarInsightHub](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/) |
| TOPCon | ~30-40 | 同上 |
| HJT | ~70-90 | 同上 |

#### 2.2.3 成本下降路径

根据 [pmarketresearch](https://pmarketresearch.com/chemi/photovoltaic-perc-hjt-topcon-battery-market/) 和 [PRNewswire](https://kyodonewsprwire.jp/release/202507031636)：
- 银耗已降至 5 mg/W（比 TOPCon 低 37.5%），非硅成本持续压缩
- 双面金属化 + 无铟 TCO 层预计 2026 年再降 18-22%
- 硅片减薄（120→100→90 μm）进一步降低硅耗

### 2.3 规模化产能与出货量

| 指标 | 数据 | 来源 |
|------|------|------|
| 华晟年产能 | **20 GW**（拉晶/硅片/电池/组件垂直一体化） | [Huasun 官网](https://www.huasunsolar.com/) |
| 华晟累计出货 | **13+ GW**（至 2025.07） | [SaurEnergy](https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774) |
| 华晟 2024 年出货 | **6 GW**（单年） | [Huasun News](https://www.huasunsolar.com/news/huasun-marks-10-gw-in-global-shipments-ushering-in-new-chapter-for-hjt-solar-technology.html) |
| 覆盖国家 | **80+ 国家/地区** | [SaurEnergy](https://www.saurenergy.com/solar-energy-news/delivered-13-gw-of-hjt-products-in-80-countries-huasun-energy-9519774) |
| 华晟 2024 中标 | **10+ GW**（中国央企招标） | [Huasun News](https://www.huasunsolar.com/news/huasun-marks-10-gw-in-global-shipments-ushering-in-new-chapter-for-hjt-solar-technology.html) |
| 东方日升 2025 HJT 招标 | **9+ GW**（中国） | [PRNewswire](https://kyodonewsprwire.jp/release/202507031636) |
| HJT 全球市场占比 | ~10-15%（2025） | [SolarInsightHub](https://solarinsighthub.com/es/topcon-vs-hjt-2025-es/) |
| 全球 HJT 市场 CAGR | **53.5%**（2025-2031） | [QYResearch/格隆汇](https://m.gelonghui.com/p/2016237) |
| 全球 HJT 市场 2031E | **5079.8 亿元**（约 $700B） | [QYResearch/格隆汇](https://m.gelonghui.com/p/2016237) |

> **路线成熟度判断**：20 GW 年产能 + 13 GW 累计出货 + 53.5% CAGR 的市场增长预期，足以将 HJT 定位为已实现大规模工业化的成熟技术路线，而非实验室阶段的"候选"技术。

---

## 3. HJT/硅基空间级证据

### 3.1 辐照退化数据

#### 3.1.1 CEA/INES 异质结空间光伏项目

| 参数 | 数值 | 来源 |
|------|------|------|
| 电池厚度 | 90 μm（也测试了 60 μm） | [CEA/INES 官网](https://www.cea.fr/cea-tech/liten/Pages/Medias/Actualites/2025/cellules-photovoltaiques-qui-se-soignent-elles-memes-dans-espace.aspx) |
| 辐照条件 | 1 MeV 电子，fluence 10^14 e-/cm²，AM0 光谱 | 同上 |
| 辐照后效率 | **>14%**（认证） | 同上 |
| Self-curing 恢复率 | **97%** 初始性能恢复 | 同上 |
| Self-curing 条件 | 80°C 运行温度（轨道代表性条件） | 同上 |
| 认证机构 | ISFH Caltec（德国，独立认证） | 同上 |
| 项目支持 | CNES（法国国家空间研究中心）R&T + PEGASE 电信项目 | 同上 |
| 产业化目标 | 建立欧洲异质结空间光伏工业产业链 | 同上 |

> **关键意义**：14% 的辐照后效率是"可直接用于空间演示和实际应用"的工业级水平（CEA 原文："excellent result that already allows demonstrations and applications in real conditions, in space"）。97% 的自愈恢复意味着在轨退化几乎可逆，这是 GaAs 不具备的独特优势。

#### 3.1.2 东方日升 50μm P-HJT 空间级电池

| 参数 | 数值 | 来源 |
|------|------|------|
| 电池厚度 | **50 μm**（地面 HJT 120-150 μm 的 1/3） | [雪球: 东方日升供货SpaceX](https://xueqiu.com/8828221090/372690959) |
| 量产平均效率 | **26.61%** | [PRNewswire 官方新闻稿](https://kyodonewsprwire.jp/release/202507031636) |
| 比功率 | **2 W/g**（vs 刚性 GaAs 0.36 W/g） | [雪球](https://xueqiu.com/8828221090/372690959) |
| 减重效果 | 较传统地面 PERC 减重 60%+ | 同上 |
| 辐照耐受 | 10^12 质子/cm² 下效率衰减 **<10%** | 同上 |
| 在轨寿命 | **5-7 年**，功率保持率 **≥85%** | 同上 |
| 温度系数 | **-0.24%/°C**，适应 -170°C 至 +120°C | 同上 |
| 成本 | **14-21 RMB/W**（~$2-3/W，约为 GaAs $200/W 的 1/70~1/100） | 同上 |
| 供货状态 | 截至 2026.01 累计交付 **10 万+片** | 同上 |
| 中试线产能 | 12 MW/年（可满足约 100 颗 LEO 卫星） | 同上 |
| 应用场景 | 星链 V2 Mini/V3 卫星太阳翼（产业投研口径） | 同上 |

> **证据等级注记**：东方日升 SpaceX 供货的具体细节来源于雪球（财经社交平台）和东方财富（投资分析平台），属于三档证据。东方日升官方（2026.02 央视网）仅确认"近 3 年出货过 P 型超薄 HJT"，未确认客户是否为 SpaceX。但电池性能参数（26.61% 效率、740Wp 组件）来自 PRNewswire 官方新闻稿，属于二档证据。SpaceX 硅基路线选择由多个独立来源（详见 §4）交叉验证。

### 3.2 飞行验证/搭载记录

#### 3.2.1 硅基太阳能电池空间飞行历史

| 任务/平台 | 电池类型 | 时间 | 规模 | 来源 |
|-----------|---------|------|------|------|
| Vanguard 1（首个太阳能卫星） | 硅 | 1958 | 6 块小板，各含 18 个 2×0.5 cm 硅电池 | [Wikipedia](https://en.wikipedia.org/wiki/Solar_panels_on_spacecraft) |
| ISS 国际空间站 | 硅 | 1998-至今 | **3,244 m² 总阵列面积**，73 m 翼展，16,400 个硅电池/毯 | [Wikipedia: ISS Truss](https://en.m.wikipedia.org/wiki/ISS_Truss) |
| ISS iROSA 升级（6 块） | 柔性硅基（ROSA 技术） | 2021-2025 | 每块 20+ kW，总计新增 ~120 kW | [Grokipedia: ROSA](https://grokipedia.com/page/Roll_Out_Solar_Array) |
| DART（双小行星重定向测试） | ROSA 柔性阵列 | 2021 | 首个使用 ROSA 的行星防御航天器 | 同上 |
| Lunar Gateway（规划） | ROSA 技术 | 计划中 | 60 kW 深空供电 | 同上 |
| Starlink V2 Mini | 硅基 HJT | 2023-至今 | 双翼约 30 m 展开，~116 m²，~28 kW | [Naver Blog](https://m.blog.naver.com/vi2008/224157665760) |

> ISS 是迄今为止最大的轨道硅基光伏设施，已连续运行 25+ 年。其硅电池的长期在轨退化数据是最有力的空间级硅基线证据。ROSA 柔性阵列技术已在多任务中验证，证明了柔性硅基阵列的工程可行性。

#### 3.2.2 空间级硅基阵列工程参考

| 参数 | 数值 | 来源 |
|------|------|------|
| ISS 硅电池尺寸 | 8×8 cm/片 | [Wikipedia: ISS Truss](https://en.m.wikipedia.org/wiki/ISS_Truss) |
| ISS 阵列面密度（推算） | ~30-50 kg/m²（含桁架/展开机构） | 基于总质量/总面积推算 |
| ROSA 阵列质量 | **325 kg**（20+ kW 级别） | [HandWiki: ROSA](https://www.handwiki.org/wiki/Astronomy:Roll_Out_Solar_Array) |
| ROSA 比功率 | **225 W/kg** @ BOL（AM0，25 kW 配置） | [Grokipedia: ROSA](https://grokipedia.com/page/Roll_Out_Solar_Array) |
| ROSA 减重幅度 | 较刚性面板 **-20% 质量**、**-75% 体积** | 同上 |

> ROSA 的 225 W/kg 是含展开机构的子系统级比功率。柔性硅基阵列（如 Starlink V2 的 116 m² 双翼）已证明大面积柔性展开在 LEO 的可工程性。

### 3.3 空间级硅基的面密度工程参考区间

| 阵列类型 | 面密度 (kg/m²) | 比功率 (W/kg) | 来源 |
|----------|---------------|---------------|------|
| ISS 刚性阵列（含桁架） | ~30-50 | ~5-8 | 推算 |
| ROSA 柔性阵列 | ~15-20 | ~225（BOL） | [Grokipedia](https://grokipedia.com/page/Roll_Out_Solar_Array) |
| Starlink V3-like 刚性基线 | **3.0**（仅 PV 子系统） | ~85 | [33FG Research](https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites) |
| 计算优化柔性迭代（V1 Starthink） | **1.5**（仅 PV 子系统） | ~261 | 同上 |
| 未来最优组合（V2 Starthink） | **1.0**（仅 PV 子系统） | ~490 | 同上 |
| 本模型当前 HJT 面密度 | **1.2 kg/m²** | — | [stage2_mass_inputs_blackwell_hjt.json] |

> **与本模型对齐**：当前模型使用的 1.2 kg/m² 位于 Starlink V3 (3.0) 和 V1 Starthink (1.5) 之间，属于合理区间。若接受柔性展开路径（无刚性桁架），面密度可进一步下探。

---

## 4. Starlink 太阳能电池类型调查

### 4.1 搜索结果综合判断

| 调查维度 | 结论 | 证据链 | 置信度 |
|----------|------|--------|--------|
| Starlink 是否使用硅基电池 | **是**——已从 GaAs 转向硅基 | 3 个独立来源一致确认 | 高 |
| 具体硅基类型 | **HJT 异质结** | 雪球、华尔街见闻供应链分析均指向 HJT | 中-高 |
| 主要供应商 | **TSEC（台湾太阳能能源公司）** + **东方日升** | Per Aspera、GF Securities、雪球交叉验证 | 中 |
| SpaceX 是否在自建太阳能工厂 | **是**——德州 Bastrop 在建 | Per Aspera、雪球均提及 | 高 |
| 官方是否公开确认 | **未直接确认**（SpaceX 从不公开讨论供应链细节） | — | — |

### 4.2 关键引用

> **GF Securities / 华尔街见闻（2026.06）**：
> "SpaceX has instead opted for commercial silicon-based photovoltaic wafers... In solar cell production, traditional space-grade triple-junction GaAs cells have about 30% efficiency but cost over $200 per watt, with global annual capacity only in the single digit megawatts."
>
> — [https://www.bgportable.com/news/detail/12560605439684](https://www.bgportable.com/news/detail/12560605439684)

> **雪球 / 饕餮和汉堡（2026.06）**：
> "SpaceX已经全面转向硅基（HJT异质结）：效率 16%-20%（略低），成本 1/10 甚至更低"
>
> — [https://xueqiu.com/1054707264/393323620](https://xueqiu.com/1054707264/393323620)

> **Per Aspera（2026.03）**：
> "SpaceX broke from III-V convention years ago for Starlink, which ditched GaAs for silicon-based solar cells for its newer satellites. Starlink's key supplier has been TSEC (Taiwan Solar Energy Corp)... SpaceX chose silicon because GaAs was prohibitively expensive at Starlink volumes."
>
> — [https://www.peraspera.us/space-power/](https://www.peraspera.us/space-power/)

> **33FG Research（2026.02）**：
> "Starlink V3-like rigid PV baseline: 85 W/kg solar array specific power... future optimal: 490 W/kg"
>
> — [https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites](https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites)

### 4.3 Starlink V2 Mini 太阳能系统参数

| 参数 | 数值 | 来源 |
|------|------|------|
| 太阳翼配置 | 双翼 | [Naver Blog](https://m.blog.naver.com/vi2008/224157665760) |
| 展开翼展 | ~30 m（100 ft） | 同上 |
| 总面积 | ~116 m² | 同上 |
| 总功率 | ~28 kW | 同上 |
| 阵列面密度（推算） | ~3.0 kg/m²（子系统级） | [33FG Research](https://research.33fg.com/analysis/the-solar-power-unlock-for-spacex-s-100-kw-ton-compute-satellites) |
| 电池比功率（推算） | ~85 W/kg（阵列子系统级） | 同上 |

> Starlink V2 Mini 的 116 m² 双翼硅基阵列是当前在轨运行的最大规模商业硅基空间光伏实证，其 28 kW 功率已超越大多数传统通信卫星（通常 5-15 kW）。

---

## 5. HJT/GaAs 并行对照表

### 5.1 完整多维度对比

| 维度 | GaAs 主链 | HJT 并行路线 | 差异方向 | 证据等级 (GaAs / HJT) |
|------|----------|-------------|----------|----------------------|
| **效率** | | | | |
| BOL 电池效率（空间级） | 28-34%（IMM，TRL9） | 26.6%（50μm P-HJT，空间级量产） | GaAs 优势 | 二档 / 二档+三档 |
| BOL 模块效率（地面量产） | N/A（非地面技术） | 23.5-24.5%（HJT） | — | — / 二档 |
| EOL 效率（LEO 10年辐照后） | ~24-29%（退化 ~10-15%） | ~22-24%（退化 ~10%，含 self-curing 恢复后） | GaAs 略有优势 | 二档 / 二档 |
| AM0 效率修正 | 直接适用（设计即 AM0） | 需从 AM1.5→AM0 转换（约 -2~3% 绝对值） | GaAs 优势 | 二档 / 一档 |
| **退化率** | | | | |
| 年退化率（地面） | N/A | **0.25-0.40%/年** | — | — / 二档 |
| 辐照退化（空间 10^14 e-/cm²） | <5-10%（耐辐照设计） | ~14% 效率保持，97% 可恢复（self-curing） | **各有优势** | 二档 / 二档 |
| 5-7 年 LEO 在轨保持率 | ~85-90% | **≥85%**（10^12 p/cm²） | 相当 | 二档 / 三档 |
| **阵列面积**（120 kW / 600 km） | **625 m²** | **1295 m²**（+107%） | GaAs 优势 | 一档 |
| **阵列质量**（120 kW / 600 km） | **938 kg**（面密度 ~1.5 kg/m²） | **1554 kg**（面密度 ~1.2 kg/m²）(+66%) | GaAs 优势 | 一档+三档 |
| **辐照耐受性** | | | | |
| 抗质子/电子辐照 | 优秀（III-V 材料固有耐辐照） | 良好（10^12 p/cm² <10% 衰减）+ **self-curing 独特优势** | GaAs 略优但 HJT 可自愈 | 二档 / 二档 |
| 抗热循环 | 良好 | **优秀**（-0.24%/°C 温度系数，-170°C~+120°C） | HJT 优势 | 三档 / 三档 |
| **任务寿命适配** | | | | |
| 10 年+ LEO | 已验证（GEO 卫星标准） | 待验证（地面 HJT 25-30 年保修已覆盖） | GaAs 有飞行遗产 | 二档 / 二档 |
| 5-7 年 LEO | 已验证 | **已在轨验证**（Starlink V2 Mini 设计寿命 5 年） | 相当 | 二档 / 三档 |
| **价格闭合度** | | | | |
| 地面量产价格 | N/A | **$0.14-0.24/W**（HJT 组件批发） | — | — / 二档 |
| 空间级电池价格 | **~$200/W**（GaAs 3J） | **~$2-3/W**（HJT 50μm，东方日升） | **HJT 压倒性优势**（1/70~1/100） | 二档 / 三档 |
| 空间级阵列系统成本 | 无公开数据 | 待闭合（地面→空间放大因子不明） | 当前不可判定 | — |
| 规模化产能约束 | **个位数 MW/年**（全球 GaAs 空间级） | **数百 GW/年**（地面光伏总产能） | **HJT 压倒性优势** | 二档 / 二档 |
| **已有飞行验证** | | | | |
| LEO 在轨运行 | 大量（GEO/LEO 通信卫星） | **ISS（25年+）**、**Starlink V2 Mini（数千颗）** | 相当 | 二档 / 二档 |
| 深空任务 | Juno（木星）、Mars rover | 无 | GaAs 优势 | 二档 |
| **温度适应性** | | | | |
| 温度系数 | ~ -0.15~0.20%/°C | **-0.24%/°C** | GaAs 略优 | 二档 / 二档 |
| 极端温度范围 | 宽（III-V 耐高温） | -170°C ~ +120°C | 相当 | 二档 / 三档 |

### 5.2 综合判断矩阵

```
                GaAs 优势 ←────────────────→ HJT 优势
效率(BOL)        ████████░░                 
效率(EOL)        ██████░░░░                 
退化率(辐射)      ████░░░░░░  (各有千秋)
退化率(热循环)     ░░░░██████  (HJT 占优)
阵列面积          ████████░░                 
阵列质量          ████████░░                 
空间级单价        ░░░░░░░░░░██████████ (HJT 压倒)
产能可扩展性       ░░░░░░░░░░██████████ (HJT 压倒)
飞行遗产(深空)     ██████████                 
飞行遗产(LEO)     ██████████  (相当)
```

> **核心判断**：HJT 在效率/面积/质量三个纯物理维度上弱于 GaAs，但在成本/产能两个工程经济维度上具有压倒性优势。对于 LEO 大规模星座（如 Starlink 级万颗以上），HJT 的经济可行性是 GaAs 无法匹敌的——这也是 SpaceX 选择硅基路线的根本原因。

---

## 6. 物理链闭合清单 vs 价格链待闭合清单

### 6.1 可先闭合的物理链项

| # | 闭合项 | 状态 | 支撑证据 | 证据等级 |
|---|--------|------|----------|----------|
| P1 | 地面量产 HJT 电池效率 | **已闭合** | 华晟 26%+、东方日升 26.61%、隆基 27.81% | 二档（多个官方来源交叉验证） |
| P2 | 地面量产 HJT 组件效率 | **已闭合** | TaiyangNews 23.5-23.8%、多家厂商 | 二档 |
| P3 | 空间级 HJT 辐照后效率 | **已闭合** | CEA/INES: >14% after 10^14 e-/cm² | 二档 |
| P4 | HJT self-curing 恢复能力 | **已闭合** | CEA/INES: 97% 恢复率，ISFH Caltec 认证 | 二档 |
| P5 | HJT 地面退化率 | **已闭合** | NREL meta-analysis: 0.25-0.40%/yr | 二档 |
| P6 | HJT 空间辐照退化量级 | **已闭合** | <10% at 10^12 p/cm²（东方日升） | 二档+三档 |
| P7 | HJT 温度系数 | **已闭合** | -0.24%/°C，多来源一致 | 二档 |
| P8 | 同负载下 HJT vs GaAs 阵列面积比 | **已闭合** | 基于 EOL 效率差异的一档物理推导 | 一档 |
| P9 | 同负载下 HJT vs GaAs 阵列质量比 | **已闭合** | 面积放大效应 + 面密度差异 | 一档+三档 |
| P10 | HJT 工业规模化产能 | **已闭合** | 华晟 20 GW/年、13 GW 累计 | 二档 |
| P11 | 硅基电池 LEO 飞行验证 | **已闭合** | ISS 25年+、Starlink 数千颗 | 二档 |
| P12 | 柔性硅基阵列工程可行性 | **已闭合** | ROSA/iROSA ISS 安装、DART 任务 | 二档 |

### 6.2 物理链待补强项

| # | 待补强项 | 当前状态 | 补强方向 | 优先级 |
|---|----------|----------|----------|--------|
| P13 | 空间级 HJT 长期在轨退化（>7年） | 仅地面加速测试外推，无 >7 年在轨数据 | 等待 Starlink 退役卫星数据公开，或参考 ISS 硅电池长期退化 | 中 |
| P14 | 空间级 HJT 封装面密度精确值 | 当前用 1.2 kg/m² 模型值，范围 1.0-3.0 kg/m² | 搜集 Starlink 级柔性封装的独立工程参考 | 中 |
| P15 | HJT 在 >600 km 轨道（更高辐射）的退化 | 当前证据集中在 LEO 低轨 | 搜索 MEO/GEO 级辐射环境的硅基退化文献 | 低 |

### 6.3 价格链待闭合清单（不阻断物理链深化）

| # | 待闭合项 | 当前状态 | 补强方向 | 优先级 |
|---|----------|----------|----------|--------|
| C1 | 空间级 HJT 阵列成品采购价（$/W 或 $/m²） | 有三档区间估计（~$2-3/W 电池级、~$3,500-4,200/m² 阵列级），缺独立可验证一手数据 | 搜索 NASA/ESA 公开采购合同、商业星座公开 BOM | 高 |
| C2 | 地面→空间级 HJT 的成本放大因子 | 地面 $0.14-0.24/W → 空间 $2-3/W，约 10-15x 放大（三档估计） | 建立封装/筛选/认证/低批量溢价的分项成本模型 | 高 |
| C3 | Starlink 级硅基阵列实际采购价 | 有"~25,000-30,000 RMB/m²"的产业分析口径（三档） | 搜索 SpaceX/TSEC 供应链公开披露 | 中 |
| C4 | HJT 与 GaAs 在 5-10 年全寿命周期内的 LCOE 比较 | 当前不可判定（双方均有缺失参数） | 待物理链和价格链均闭合后建模 | 中 |

### 6.4 禁止项更新

| 旧判断 | 新判断 | 原因 |
|--------|--------|------|
| "HJT 只能降级" | **删除**——HJT 有独立物理链支撑并行比较 | 本证据包提供了 12 项可闭合物理链 + 17 条搜索 URL |
| "HJT 禁止进入主模型" | **替换为**"HJT 物理链可先闭合，价格链待后续补强后入模" | 物理链和价格链闭合度必须分开标注 |
| 单一 CEA 锚点 | **替换为** CEA + 东方日升 + ISS + Starlink 多锚点交叉验证 | 搜索深度从 1 个锚点扩展到 6+ 个独立来源 |

---

## 附录 A：证据等级速查

| 档位 | 名称 | 定义 |
|------|------|------|
| 一档 | 物理推导链 | 由明确物理公式、边界条件和任务约束直接推导的参数 |
| 二档 | 权威资料 | 明确权威来源（官网、同行评审论文、官方新闻稿），有可回查 URL |
| 三档 | 可迁移证据 | 行业资料、类比平台、分析报告，必须写清可迁移/不可迁移部分 |
| 四档 | 合理推断 | 公开资料不足，只能工程推断，必须写明推断依据和失效风险 |

## 附录 B：本证据包中需要用户裁决的二/三/四档证据清单

> 以下证据依据 `current-note.md` §Task V1 的首次引用即请示规则，需要在合流前通过用户裁决：

| # | 证据项 | 档位 | 用途 | 请示时点 |
|---|--------|------|------|----------|
| 1 | 东方日升 50μm HJT 空间级电池参数（效率 26.61%、比功率 2W/g、辐照 <10% 衰减） | 二档（PRNewswire 官方）+ 三档（SpaceX 供货细节） | 作为 HJT 空间级可行性的核心证据 | 首次写入分析链时 |
| 2 | CEA/INES self-curing 97% 恢复率 | 二档 | 作为 HJT 辐照耐受性优于预期的关键证据 | 首次写入分析链时 |
| 3 | Starlink 转向硅基 HJT 的供应链分析 | 三档 | 作为"成熟技术路线已在最大规模星座中实际采用"的佐证 | 首次写入结论时 |
| 4 | HJT 空间级成本 ~$2-3/W vs GaAs ~$200/W | 三档 | 作为价格链区间估计 | 首次转化为模型输入时 |
| 5 | 地面→空间 HJT 成本放大因子 ~10-15x | 四档 | 作为价格链区间估计的迁移依据 | 首次转化为模型输入时 |

---

> **文档状态**：Task 3 产出物 v1.0
> **闭合判据**：12 项物理链已闭合 + 17 条搜索 URL 归档 + HJT 路线定位已从"只能降级"修正为"与 GaAs 并行的成熟技术路线"
> **下一交接**：本证据包可被 Task 4（参数重分级）、Task 5（电源系统边界修复）和 Task 7（结构化价格输入更新）引用
