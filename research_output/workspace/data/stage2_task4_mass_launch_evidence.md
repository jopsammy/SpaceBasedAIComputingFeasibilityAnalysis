# Task 4：单星质量、发射装载与发射成本补证主文档

> 文档定位：`produce-stage-two-difference-analysis / Task 4` 的外部补证主证据文档。  
> 写法约束：中性审计式；只判断“证据能否支撑某一口径”，不把当前证据写成终局裁决。  
> 本文不修改共享跟踪文件 `tasks.md`、`checklist.md`、`current-note.md`。

---

## 0. 结论先行（供 Task 4 / Task 5 快速接续）

### 0.1 当前最稳妥的阶段性判断

1. **`2.14t` 口径已经有外部“反推链”支撑，但仍不是单星总质量的一手公开规格。**  
   外部二手来源反复出现同一组 AI1 参数：`150 kW peak / 120 kW average / 70 kW per ton / 70 m wingspan / ~600 km orbit`。  
   若把 `70 kW/t` 理解为整星级功率密度，则 `150 / 70 = 2.14 t` 可以成立；但这仍是**二手转述 + 本地反推**，不是官方 datasheet。

2. **原 paper 的 `5–10t/颗` 目前仍主要是工程假设，不是已被外部资料锁定的数字。**  
   当前本地 paper 在 [research_output/latex/sections/04_engineering.tex](../../latex/sections/04_engineering.tex) 中直接写入“质量估计 `5--10 t/颗`”，但没有在该段附近给出外部质量来源链，因此该口径目前仍应降级为“待补证的保守工程场景”。

3. **在“官方可核对”的 Starship 运力下，`80–100 颗/发` 并不自动成立。**  
   SpaceX 官网当前可直接核对的口径是“**fully reusable configuration 100+ t to orbit**”；若用 `2.14 t/颗` 去除，质量上限仅给出约 `46` 颗的理论上限，且还**未扣除适配器/分离机构/任务留裕**。  
   要达到 `80 颗` 需约 `171.2 t` 有效载荷；`100 颗` 需约 `214 t`。这已经超出官网当前“100+ t fully reusable”直接公开口径。

4. **`$/kg` 的“权威口径”与“工程披露/近未来推算”必须严格分层。**  
   目前能相对稳妥锚定的是：
   - 历史已实现：NASA 2018 对 Shuttle / Falcon 9 等历史成本口径；
   - 经济阈值：Google Suncatcher / arXiv 将 `<$200/kg` 视作使轨道算力接近经济可行的关键阈值；
   - 工程或市场披露：Starship `100–200/kg` 更像目标值/成熟复用口径，而不是官方已实现成本。

### 0.2 本文采用的证据等级

| 等级 | 含义 | 典型来源 |
|---|---|---|
| A1 | 官方一手公开资料 | 公司官网、监管机构原文 |
| A2 | 一手研究/论文/监管研究 | arXiv 论文、NASA/FAA正式材料 |
| B1 | 强二手，且可追到原始发布 | 主流媒体对官方视频/文件的直接转述 |
| B2 | 行业分析/研究报告 | 券商、行业机构、工程博客 |
| C | 本地反推/场景估算 | 本地 markdown、脚本、手工计算 |

---

## 1. 本地基线：原 paper 当前到底写了什么

### 1.1 与 Task 4 直接相关的本地锚点

| 本地锚点 | 与 Task 4 相关的当前口径 | 审计备注 |
|---|---|---|
| `research_output/latex/sections/04_engineering.tex` | AI1：`150 kW峰值/120 kW持续`、翼展 `70 m`、质量估计 `5--10 t/颗`；1 MW 约 `8--9` 颗；总质量 `40--90 t` | 这里把 `5--10 t` 直接写进工程基线，但没有直接外部质量来源 |
| `research_output/latex/sections/05_commercial.tex` | 2030 发射成本场景：`$50 / $200 / $500 per kg`；TCO 中基准发射成本写为 `1次Starship，200t` | 属于模型输入/情景口径，不等于现实已实现价格 |
| `research_output/workspace/scripts/launch_cost_learning_curve.py` | 脚本把 `5–10 t/颗`、`200 t/次` 作为输入，并做 Wright's Law 拟合 | 该脚本更像“情景演算器”，不能单独证明 `100–200/kg` |
| `research_output/workspace/data/launch_cost_results.txt` | 拟合 `R²` 仅 `0.29–0.37`，对 2030 得出的是约 `~$2,000/kg` 量级，而非 `$100–200/kg` | 反证：本地学习曲线结果并不能强支撑“2030 已达 $100–200/kg” |

### 1.2 本地基线的直接含义

- 原 paper 当前有三处需要外部补证：
  1. `5–10t/颗` 的质量区间是否有外部支撑；
  2. `80–100颗/发` 是否真的能从 Starship 公开约束推出；
  3. `100–200$/kg` 是目标、阈值、还是已实现口径。
- 因此 Task 4 的重点不是“重算所有模型”，而是把这些数字分别放回各自证据层级。

---

## 2. `2.14t` 反推链：现有外部支撑、成立条件与缺口

### 2.1 可追溯的外部参数链

| 参数 | 外部来源 | 证据等级 | 备注 |
|---|---|---|---|
| AI1 平均计算负载 `120 kW`、峰值 `150 kW`、功率密度 `70 kW/t`、约 `600 km` 轨道 | Tom’s Hardware 转载页（Inkl）<https://www.inkl.com/news/elon-musks-first-gen-orbital-data-center-craft-spans-wider-than-a-boeing-747-and-runs-an-interchangeable-chip-payload-ai1-satellite-compute-payload-is-120-kw-peaks-at-150-kw> | B1 | 可追到 SpaceX 在 X 发布的 30 分钟技术视频，但当前拿到的是媒体转述，不是官方 datasheet |
| 同一组参数的再转述：`150 kW peak / 120 kW avg / 70 kW/t / 70 m wingspan / 110 m² radiator / 250 W/m² solar` | Knight Li 总结页 <https://knightli.com/en/2026/06/10/spacex-ai1-orbital-ai-data-center-satellite/> | B1 | 与 Inkl/Tom’s 口径基本一致，可视作交叉二手一致性 |
| 同一组参数的再转述（含 20 m deployed height） | IndexBox 汇总页 <https://www.indexbox.io/blog/spacex-unveils-ai1-orbital-data-center-satellite-ahead-of-market-debut/> | B1 | 仍是媒体/摘要型来源，不可代替一手规格表 |

### 2.2 `2.14t` 的直接数学链

若采信“整星功率密度约 `70 kW/t`”与“峰值算力载荷 `150 kW`”两项，则：

```text
单星质量 = 150 kW / (70 kW/t) = 2.142857... t
```

若错误地把 `120 kW average` 代入同一公式，则会得到：

```text
单星质量 = 120 kW / (70 kW/t) = 1.714285... t
```

这意味着：**`2.14t` 这一数字本身已经隐含“取峰值 150 kW 作为分子”的选择。**

### 2.3 `2.14t` 反推链的证据审计

| 审计项 | 当前状态 | 结论 |
|---|---|---|
| 分子是否有外部来源 | 有，多个二手来源一致转述 `150 kW peak` | 可用，但仍是 B1 |
| 分母是否有外部来源 | 有，多个二手来源一致转述 `70 kW/t` | 可用，但仍是 B1 |
| 分母是否明确是“整星总质量”而非“有效载荷级”密度 | 未明确 | 这是当前最大缺口 |
| 是否存在官方一手质量 datasheet | 未找到 | `2.14t` 仍不是 A 级直接证据 |
| 是否可独立复算 | 可以 | 但复算对象是“被转述的功率密度口径”，不是一手总质量 |

### 2.4 对 `2.14t` 的当前最稳妥定性

- **可接受的表述**：  
  “外部二手报道反复出现 `150 kW peak` 与 `70 kW/t` 这组参数，因此可以形成 `2.14t` 的反推链；该口径当前属于‘有二手支撑的本地反推值’。”

- **不可接受的表述**：  
  “AI1 官方总质量已经证明是 `2.14t`。”  
  当前没有找到可公开核对的官方一手质量规格表支撑这一句。

### 2.5 证据等级判定

| 结论 | 等级 |
|---|---|
| “`2.14t` 可以从 `150/70` 反推出来” | B1 + C |
| “`2.14t` 已被官方公开确认为单星总质量” | 当前不可判定 |

---

## 3. 原 paper 的 `5–10t`：现有依据与证据缺口

### 3.1 当前能确认的“现有依据”

原 paper 在本地工程章节直接写道：

- AI1：`150 kW峰值 / 120 kW持续`
- 翼展 `70 m`
- **质量估计 `5--10 t/颗`**
- `1 MW ≈ 8--9 颗`
- 总质量 `40--90 t`

该口径位于本地文件：  
`research_output/latex/sections/04_engineering.tex`

### 3.2 这条口径目前“有”什么

| 项 | 当前状态 |
|---|---|
| 作为本地工程保守情景的存在性 | 有 |
| 与“大翼展 + 大辐射器 + 电源/热控/平台冗余”相符的工程直觉 | 有 |
| 外部公开一手质量规格 | 无 |
| 可追溯的外部可比项目对标表 | 无 |
| 子系统质量分解链 | 无（这属于 Task 5 的重点） |

### 3.3 `5–10t` 的证据缺口

1. **缺少外部一手/强二手质量来源。**  
   当前没有找到“AI1 单星公开总质量 = 5–10t”的外部 URL 或论文。

2. **缺少拆项链。**  
   该数字还没有被拆成：
   - 计算载荷
   - 热控/辐射器
   - 光伏/电池
   - 平台/结构
   - 推进/通信
   - 冗余/裕量

3. **缺少与 `2.14t` 反推口径的同口径对齐。**  
   `2.14t` 看起来更像“由功率密度反推的整星/载荷候选质量”，而 `5–10t` 更像“含平台、电源、热控裕量的保守总质量假设”。  
   若不显式对齐分母定义，这两者并不是直接对撞关系。

### 3.4 当前最稳妥定性

- **`5–10t` 当前仍可保留为保守工程场景，但不能继续被写成外部已证实的事实口径。**
- 它更适合在后续文档中标为：`C级：本地保守工程假设，待 Task 5 子系统分解补强`。

---

## 4. Starship 运力与尺寸/装载约束：可直接核对的外部口径

### 4.1 可直接核对的 Starship 公开约束

| 约束项 | 数值 | 来源 | 等级 | 备注 |
|---|---:|---|---|---|
| 完全复用入轨载荷 | `100+ t` | SpaceX 官网 <https://www.spacex.com/vehicles/starship/> | A1 | 这是当前最干净的官方运力锚点 |
| 箭体/舱体直径 | `9 m` | SpaceX 官网 <https://www.spacex.com/vehicles/starship/> | A1 | 对体积装载的最基础几何约束 |
| 载荷舱直径 | `9 m outer diameter` | EO Portal / Starship Users Guide 转引 <https://www.eoportal.org/other-space-activities/starship-of-spacex> | B1 | 二手转引自 SpaceX 用户指南 |
| 载荷舱高度 | `18 m` | 同上 | B1 | 二手转引 |
| 动态包络 | `8 m diameter payload dynamic envelope` | 同上 | B1 | 对堆叠/翻转/分离机构更关键 |
| 扩展高度 | `up to 22 m` | 同上 | B1 | 仍非无限制可用空间 |
| 载荷体积 | `1,100 m³` | 同上 | B1 | 对大规模星座装载有参考意义 |

### 4.2 与 AI1 已知外部参数的碰撞

| AI1 已知或被转述参数 | 数值 | 来源 | 等级 |
|---|---:|---|---|
| 展开翼展 | `70 m` | Inkl / Knight Li 等转述页 | B1 |
| 展开高度 | `20 m` | IndexBox 等二手汇总 | B1 |
| 液冷辐射器面积 | `110 m²` | Inkl / Knight Li | B1 |
| 太阳能阵列功率 | `150 kW` | Knight Li / IndexBox | B1 |

### 4.3 当前能推、不能推什么

**能推的：**

- 质量上，Starship 官网当前公开“100+ t fully reusable”并不直接支持 `80–100 颗 × 2.14 t/颗`。
- 几何上，Starship 虽然有很大的 `9 m × 18 m` 级载荷舱，但 AI1 的**公开口径主要是展开尺寸，不是收拢尺寸**。

**不能直接推的：**

- 当前**不能**从 `70 m wingspan / 20 m height` 反推出其“发射时折叠包络”。
- 当前**不能**证明 `80–100颗/发` 在体积/分离安全/部署节奏上可行。

### 4.4 当前最稳妥定性

- **Starship 的质量约束可以先算。**
- **Starship 的体积/部署约束，目前只能做“缺口识别”，不能做硬结论。**

---

## 5. 单次发射装载数：至少一条独立推导链

### 5.1 独立推导链 A：只用“官方可核对运力 + `2.14t` 候选质量”

取：

- Starship fully reusable payload = `100+ t`（官方公开）
- 单星候选质量 = `2.14 t`（外部二手参数反推）

则理论质量上限：

```text
N_max,theoretical = 100 / 2.14 = 46.73
```

即：

```text
理论上限 ≈ 46 颗（未计适配器/分离机构/留裕）
```

若加入发射与部署留裕：

| 可用净载荷假设 | 公式 | 可装载数 |
|---|---|---:|
| 100 t（不扣留裕） | `100 / 2.14` | `46` |
| 90 t（约 10% 留裕） | `90 / 2.14` | `42` |
| 80 t（约 20% 留裕） | `80 / 2.14` | `37` |

### 5.2 独立推导链 B：反推 `80–100颗/发` 分别需要多大有效载荷

```text
80 颗 × 2.14 t = 171.2 t
100 颗 × 2.14 t = 214.0 t
```

| 目标颗数 | 所需有效载荷 |
|---|---:|
| 80 颗 | `171.2 t` |
| 90 颗 | `192.6 t` |
| 100 颗 | `214.0 t` |

### 5.3 这一推导链告诉我们什么

1. 若只采用 **SpaceX 官网 A1 级口径**，则 `80–100颗/发` 无法直接成立。
2. 若要接近 `80–100颗/发`，必须至少满足以下之一：
   - 实际单星质量显著低于 `2.14 t`；
   - 可用有效载荷显著高于官网当前“100+ t fully reusable”；
   - 或采用更接近 expendable / 极限成熟复用的高运力口径；
   - 同时仍要解决 stowage / adapter / deployment 安全性。

### 5.4 “80–100颗/发”当前该如何定级

| 命题 | 当前等级 | 原因 |
|---|---|---|
| “`80–100颗/发` 在质量上必然成立” | 不成立 | 被官网 `100+ t` 直接约束 |
| “`80–100颗/发` 在更激进高运力口径下有可能” | B2/C | 需要更高运力与更少留裕的组合假设 |
| “`37–46颗/发` 是基于官方 100t+ 与 2.14t 的更硬上限带” | A1 + B1/C | 至少质量链可复核 |

### 5.5 对 Task 5 的接口含义

Task 5 若要继续推装载数，应明确回填以下字段：

1. `satellite_mass_basis`：`2.14t / 3t / 5t / 10t` 哪个版本；  
2. `mass_definition`：总质量 / 仅载荷 / 含不含部署机构；  
3. `starship_payload_basis`：`100t reusable / 150t mature / 200t expendable`；  
4. `reserve_ratio`：适配器+分离+任务留裕占比；  
5. `stowed_geometry_assumed`：收拢包络是否有独立依据。

---

## 6. `$/kg`：权威口径 / 工程披露 / 近未来推算 三层证据表

### 6.1 总表

| 层级 | 数值/口径 | 来源 | 等级 | 可用于什么 | 不能用于什么 |
|---|---|---|---|---|---|
| 权威历史口径 | Shuttle `~$54,500/kg`；Falcon 9 expendable `~$2,720/kg` | NASA 2018《The Recent Large Reduction in Space Launch Cost》<https://ntrs.nasa.gov/api/citations/20200001093/downloads/20200001093.pdf> | A2 | 作为历史成本下降锚点 | 不能证明 Starship 当前已实现成本 |
| 官方运力口径 | Starship fully reusable `100+ t` | SpaceX 官网 <https://www.spacex.com/vehicles/starship/> | A1 | 约束每颗发射分摊下界 | 不能单独推出 `$100–200/kg` |
| 权威经济阈值 | LEO launch cost may reach `<$200/kg by the mid-2030s`；此价位可使空间数据中心接近经济可行 | Google Research 博客 <https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/>；arXiv <https://arxiv.org/html/2511.19468v1> | A2 | 说明 `$200/kg` 是“经济门槛/阈值” | 不能当作已实现或官方报价 |
| 工程披露/市场目标 | Starship target `~$100–200/kg` | 原 paper 外部引用链、行业转述、Jarsy 研究综述 <https://www.jarsy.com/blog/spacex-road-to-sub--200-kg-how-starship-could-make-orbital-ai-economically-viable> | B2 | 作为目标/成熟复用情景 | 不能当成现时稳态价格 |
| 工程现值估算 | Starship experimental phase `~$82–98M/flight`；若按 `100 t`，约 `~$820–980/kg` | Jarsy 研究综述同上 | B2 | 给“当前试验期量级感” | 非官方财务披露，不应写死为事实 |
| 物理下界讨论 | 长期物理地板 `~$20–30/kg` | 33fg Research《A World With 10,000 Starships》<https://research.33fg.com/analysis/a-world-with-10000-starships> | B2 | 给极限下界的物理想象边界 | 不能当作 2030 前可实现价格 |
| 本地情景输入 | `2030: $50 / $200 / $500 per kg` | 本地 paper / script | C | 用于情景敏感性分析 | 不能外部背书为现实价格 |

### 6.2 三层证据的正确读法

1. **权威层**能回答：历史上成本已经从哪里降到了哪里、以及“如果将来低于 `$200/kg`，某些经济假设会开始松动”。  
   它**不能**回答“Starship 现在就是 `$100/kg`”。

2. **工程披露层**能回答：市场和行业研究怎样描述 Starship 的目标成本、当前试验态可能在什么量级。  
   它**不能**替代审计意义上的官方实现值。

3. **近未来推算层**能回答：若采用某些成熟复用假设，单星分摊发射成本大致会落在哪个区间。  
   它本质上仍是**场景分析**。

### 6.3 单星分摊：用不同 `$/kg` 口径反推 `2.14t` 单星发射成本

以 `2.14 t = 2,140 kg` 为候选质量：

| `$/kg` 口径 | 单星发射成本 | 证据层含义 |
|---|---:|---|
| `$820/kg` | `$1.75M` | 更接近“当前试验期工程估算” |
| `$500/kg` | `$1.07M` | 保守近未来情景 |
| `$200/kg` | `$0.428M` | Google/Suncatcher 经济阈值；也是原 paper 基准情景 |
| `$100/kg` | `$0.214M` | 成熟复用目标情景 |
| `$50/kg` | `$0.107M` | 极乐观近未来情景 |

### 6.4 当前最稳妥定性

- **`$200/kg` 更像“关键经济门槛”而非“当前已实现官方价格”。**
- **`$100–200/kg` 可以保留为工程目标/成熟复用情景。**
- **若想写“当前更可信的现实工程量级”，`$500/kg` 以上甚至接近 `$820–980/kg` 的保守写法，反而更审计安全。**

---

## 7. “单星质量—装载数—$/kg”三者联动的审计结论

### 7.1 如果采用 `2.14t`

| 维度 | 结果 | 审计结论 |
|---|---|---|
| 质量来源 | `150/70` 反推 | 可追溯，但不是一手规格 |
| 100t 可复用 Starship 装载数 | `37–46`（含/不含留裕） | 比 `80–100` 更硬 |
| 单星发射成本（`$200/kg`） | `$0.43M` | 可作为“达到经济阈值时的分摊值” |
| 单星发射成本（`$500/kg`） | `$1.07M` | 更保守 |

### 7.2 如果采用 `5–10t`

| 维度 | 结果 | 审计结论 |
|---|---|---|
| 质量来源 | 本地保守工程场景 | 需要 Task 5 拆项补证 |
| 100t 可复用 Starship 装载数 | `10–20` | 与 paper 现有“低装载数”更一致 |
| 单星发射成本（`$200/kg`） | `$1.0M–2.0M` | 与原 paper 当前写法接近 |
| 单星发射成本（`$500/kg`） | `$2.5M–5.0M` | 明显偏高 |

### 7.3 这意味着什么

- 当前争议的核心并不是公式，而是**输入口径选哪个**。
- `2.14t` 一旦被采信，装载数与单星发射成本都会显著下修；
- 但因为 `2.14t` 仍缺少一手总质量规格，所以它目前**还不能单独把 `5–10t` 一票否决**；
- 更稳妥的阶段表达应是：  
  **“轻星反推场景”和“重星保守场景”并存，但两者证据等级不同。**

---

## 8. 仍未闭合的关键证据缺口

### 8.1 与 `2.14t` 直接相关

1. `70 kW/t` 究竟对应：
   - 整星总质量；
   - 还是仅计算载荷/可用平台质量；
   - 或者是宣传口径下的某种近似密度。

2. AI1 是否存在：
   - 官方参数表；
   - FCC/SEC/招股书附件；
   - 公开视频逐帧可读出的原始图表。

### 8.2 与装载数直接相关

1. AI1 的**收拢尺寸**未公开；  
2. 发射适配器/分离机构的质量与体积未公开；  
3. `80–100颗/发` 是否对应：
   - expendable Starship；
   - 还是极限成熟复用；
   - 还是不同于 AI1 当前版本的后续轻量化版本。

### 8.3 与 `$/kg` 直接相关

1. SpaceX 官方网站目前未公开 Starship 已实现的 `$/kg`；  
2. `100–200/kg` 更多出现在目标/行业转述/研究阈值，而不是财务审计口径；  
3. 本地 Wright's Law 脚本并没有推出同一量级的低价，因此不能把脚本当作该结论的强支撑。

---

## 9. 给 Task 5 的合流字段清单

Task 5 在做单星质量范围与制造成本本地核算时，建议至少向合流方提供以下字段，避免口径漂移：

| 字段名 | 含义 |
|---|---|
| `mass_case_id` | `light_2p14t` / `mid_3to5t` / `heavy_5to10t` |
| `mass_definition` | 总质量 / 仅计算载荷 / 含不含部署机构 |
| `power_basis` | 采用 `150 kW peak` 还是 `120 kW average` |
| `power_density_basis` | `70 kW/t` 是否用于整星级 |
| `starship_payload_case` | `100t_reusable` / `150t_mature` / `200t_expendable_like` |
| `reserve_ratio` | 适配器、结构、留裕占比 |
| `stowed_geometry_assumption` | 是否存在折叠尺寸依据 |
| `launch_cost_basis` | `current_engineering` / `500` / `200` / `100` / `50` 美元每千克 |
| `dollar_year` | 使用的币值年份 |
| `single_sat_launch_cost_usd` | 单星分摊发射成本结果 |
| `evidence_grade` | 对应 A1/A2/B1/B2/C |
| `source_urls` | 外部 URL 列表 |

---

## 10. 当前闭合性判断（仅针对 Task 4 范围）

### 10.1 已基本闭合的部分

- `2.14t` 已形成一条**可复核外部支撑链**：  
  `二手规格一致转述 → 本地反推 → 证据等级说明`

- Starship 装载数已形成至少一条**独立推导链**：  
  `官方 100+ t 运力 → 2.14t 单星 → 37–46 颗/发质量上限带`

- `$/kg` 已形成**三层证据表**：  
  `权威历史 / 工程披露 / 近未来推算`

### 10.2 仍未闭合的部分

- AI1 一手总质量规格仍未找到；
- AI1 收拢尺寸/部署约束仍未找到；
- `80–100颗/发` 目前还不能升格为高置信结论；
- `5–10t` 仍缺子系统级拆解证据，这一部分需要 Task 5 接手。

### 10.3 对后续根目录研究文档的建议写法

建议在最终交付文档中使用如下三分法：

1. **外部资料支撑较强**：  
   Starship 官方复用运力 `100+ t`；Google 将 `<$200/kg` 视作关键经济门槛。

2. **外部二手支撑 + 本地反推**：  
   AI1 `2.14t` 候选质量；`37–46颗/发` 的质量上限带。

3. **保守工程场景 / 待 Task 5 补强**：  
   `5–10t/颗`、低装载数、以及对应更高单星发射成本。

---

## 附：外部来源 URL 清单（便于复核）

1. SpaceX Starship 官方页：<https://www.spacex.com/vehicles/starship/>  
2. Google Research 博客（Project Suncatcher）：<https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/>  
3. Suncatcher arXiv HTML：<https://arxiv.org/html/2511.19468v1>  
4. NASA 2018 发射成本报告：<https://ntrs.nasa.gov/api/citations/20200001093/downloads/20200001093.pdf>  
5. FAA Boca Chica 项目档案：<https://www.faa.gov/space/stakeholder_engagement/spacex_starship/activity_archive>  
6. FAA KSC LC-39A 项目页：<https://www.faa.gov/space/stakeholder_engagement/spacex_starship_ksc>  
7. EO Portal / Starship Users Guide 转引：<https://www.eoportal.org/other-space-activities/starship-of-spacex>  
8. Inkl / Tom’s Hardware AI1 规格转述：<https://www.inkl.com/news/elon-musks-first-gen-orbital-data-center-craft-spans-wider-than-a-boeing-747-and-runs-an-interchangeable-chip-payload-ai1-satellite-compute-payload-is-120-kw-peaks-at-150-kw>  
9. Knight Li AI1 规格汇总：<https://knightli.com/en/2026/06/10/spacex-ai1-orbital-ai-data-center-satellite/>  
10. IndexBox AI1 规格汇总：<https://www.indexbox.io/blog/spacex-unveils-ai1-orbital-data-center-satellite-ahead-of-market-debut/>  
11. Jarsy Research Starship 成本综述：<https://www.jarsy.com/blog/spacex-road-to-sub--200-kg-how-starship-could-make-orbital-ai-economically-viable>  
12. 33fg Research：<https://research.33fg.com/analysis/a-world-with-10000-starships>

