---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  :root {
    --color-bg: #fff;
    --color-text: #2D2D2D;
    --color-heading: #1B2A3B;
    --color-accent: #5D727D;
    --color-text-secondary: #757575;
    --color-border: #D0D0D0;
    --font-system: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  }
  section {
    background-color: var(--color-bg);
    color: var(--color-text);
    font-family: var(--font-system);
    font-size: 32px;
    padding: 80px 100px;
    line-height: 1.6;
  }
  h1, h2 { color: var(--color-heading); font-weight: bold; margin-top: 0; }
  h1 { font-size: 2.5em; margin-bottom: 0.6em; }
  h2 { font-size: 1.8em; margin-bottom: 0.8em; }
  h3 {
    font-size: 1.3em;
    color: var(--color-text);
    border-left: 6px solid var(--color-accent);
    padding-left: 15px;
  }
  strong { color: var(--color-heading); font-weight: 800; }
  em { color: var(--color-accent); font-style: normal; font-weight: bold; }
  ul { padding-left: 1.2em; }
  li { margin-bottom: 0.8em; }
  section.center-statement {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.center-statement h1 { font-size: 3em; line-height: 1.2; }
  section.center-statement p { font-size: 1.5em; color: var(--color-text); opacity: 0.8; }
  section.section-divider {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background-color: #f5f5f5;
  }
  section.section-divider h2 { font-size: 2.2em; }
  table { border-collapse: collapse; width: 100%; font-size: 0.75em; margin: 0 auto; }
  th, td { border: 1px solid var(--color-border); padding: 8px 12px; text-align: left; }
  th { background-color: #f6f8fa; font-weight: bold; }
  img { display: block; margin: 0 auto; max-width: 100%; max-height: 60vh; }
---

<!-- _class: center-statement -->

# 黄仁勋 vs 马斯克
# 太空AI算力十年可行分析

基于斯特藩-玻尔兹曼定律、发射成本学习曲线
与TCO全生命周期建模的独立工程评估

---

## 背景：马斯克（SpaceX）视角

- 太空AI是Kardashev-II文明的唯一路径
- 4-5年内太空算力将比地面更便宜
- AI1卫星已发布：翼展70m，峰值150kW，散热1,400W/m²

---

## 背景：黄仁勋（NVIDIA）视角

- 真空辐射散热是最大技术壁垒，"需要数年"
- 当前经济性不理想，涉及冷却、宇宙射线、太阳风暴等系统性差异
- 但已发布Space-1 Rubin平台，实质性押注太空算力

---

## 双方发言速览

| 维度 | 马斯克 | 黄仁勋 |
|------|--------|--------|
| 核心命题 | 太空AI不可避免，4-5年更便宜 | 散热是根本瓶颈，需要数年 |
| 时间节点 | 2028起年部署100GW | 不给具体年份 |
| 已发布产品 | AI1卫星（70m翼展，150kW） | Space-1 Rubin（推理25x H100） |
| 关键数据 | 星舰年300-500GW运力 | 机架~97.5%重量是冷却（修辞夸张） |
| 交叉验证 | 2025.11同台论坛，未互相直接批评 | — |

---

## 斯特藩-玻尔兹曼定律

真空中唯一散热途径：辐射。单位面积散热通量上限：

$$ \frac{P}{A} = \varepsilon \sigma T^{4} \quad (\sigma = 5.6704 \times 10^{-8}\ \text{W/(m}^2\cdot\text{K}^4)) $$

**AI1 1,400 W/m² 验证**：双面辐射，ε=0.90，T=342.5K → **物理成立**

- 面板温度仅69.5°C，在液冷散热器正常工作范围内
- 但已接近当前材料天花板：EOL退化后ε降至约0.83，散热衰减5-10%

---

## 1GW轨道数据中心需要多大散热面积？

1GW × 95%废热 = 950MW待散热

| 场景 | 辐射参数 (ε, T) | 通量(W/m²) | 面积(km²) |
|------|-----------------|-----------|----------|
| AI1 BOL（双面辐射） | ε=0.90, T=342.5K | 1,403 | 0.71 |
| AI1 EOL（涂层退化） | ε=0.83, T=340K | ~1,250 | ~0.80 |
| 保守设计（单面） | ε=0.85, T=323K | 523 | 1.91 |

**0.71 km² ≈ 840m × 840m，约需6,400颗AI1级卫星**

---

## LEO真实热环境：不是"理想冷库"

LEO是多热源动态环境，散热器净效率比理想真空**低15-40%**

| 衰减因素 | 效率损失 | 应对策略 |
|---------|---------|---------|
| 太阳直射吸收 | 100%（完全丧失） | knife-edge定向+太阳盾 |
| 地球反照加热 | 10-20% | 散热面朝向深空 |
| 地球红外加热 | 5-10% | 同上 |
| 热控涂层退化(EOL) | ε下降5-15% | 抗退化涂层选择 |

90分钟昼夜循环：缓冲150kW×36min需约1.9吨纯PCM，不可行

---

## 发射成本：45年下降272倍（1981→2026）

| 运载器 | 年代 | $/kg to LEO |
|--------|------|------------|
| Space Shuttle | 1981-2011 | ~$54,500 |
| Falcon 9（复用） | 2017至今 | ~$2,400 |
| Falcon Heavy | 2018至今 | ~$1,400-2,350 |
| Starship V3目标 | 2026+ | $100-200 |
| 物理地板 | — | ~$20-30/kg |

Wright's Law学习率85%，R²=0.37。2030年基准估计$200/kg

---

## 马斯克"300-500 GW/年"声明验证

- FAA当前上限：**69次/年**（Boca Chica 25 + KSC 44）
- 每次Starship可部署约 4.8 MW 等效算力
- 69次/年 × 4.8MW = **331 MW/年** → 仅声称的约 0.1%

达到300GW/年需要约 **62,500次/年（每天171次发射）**

**结论**：偏差约3个数量级。该数字更可能描述"年产10,000艘×复用100次"的终极理论极限，而非近期可操作目标

---

## GPU能效 vs 绝对功耗：一对悖论

| 架构 | 年份 | TDP(W) | TFLOPS/W |
|------|------|--------|----------|
| Volta V100 | 2017 | 300 | 0.42 |
| Ampere A100 | 2020 | 400 | 0.78 |
| Hopper H100 | 2022 | 700 | 2.83 |
| Blackwell B200 | 2024 | 1,200 | 7.5 |
| Rubin R100 | 2026 | ~2,300 | ~21.7 |

**TFLOPS/W 8年提升52倍，但绝对功耗同步飙升10倍**

Dennard缩放已失效。能效提升改善每瓦产出，而非每芯片散热需求——对轨道散热瓶颈缓解有限

---

## TCO：轨道 vs 地面多情景对比（10年，1MW IT）

| 情景 | 轨道TCO | 地面中位 | 比值 |
|------|---------|---------|------|
| 乐观（$50/kg，2.5x溢价，7年寿命） | $261M | $64.6M | 4.3x |
| 基准（$200/kg，3.5x溢价，5年寿命） | $681M | $64.6M | 10.5x |
| 悲观（$500/kg，5x溢价，3年寿命） | $1,220M | $64.6M | 17.7x |

**关键发现**：即使发射<$100/kg + 溢价<3x + 寿命>7年，TCO仍为$408M（6.3x地面）

---

## 轨道TCO成本构成（基准情景 $681M）

| 成本项 | 金额 | 占比 |
|--------|------|------|
| 光伏+储能 | $300M | 44% |
| 硬件替换（含二次发射） | $258M | 38% |
| 地面运维 | $50M | 7% |
| 计算硬件（抗辐射加固） | $34M | 5% |
| 发射成本 | $2M | <1% |

**最大成本项是光伏+储能，不是发射**。发射成本下降本身不足以解决经济性问题

---

## 静态（2026）vs 近未来（2030）对比

| 维度 | 2026静态 | 2030近未来 |
|------|---------|-----------|
| 发射成本 | $500-2,700/kg | $50-200/kg |
| GPU能效 | ~7.5 TFLOPS/W | ~100-150 TFLOPS/W |
| 散热密度 | ~1,400 W/m² | 1,500-2,000 W/m² |
| 硬件寿命 | 3-5年（估计） | 可能5-7年 |
| 轨道TCO vs 地面 | **10.5x** | **乐观4.3x，仍高于地面** |

地面数据中心同样在进步——不是静止参照系

---

## 翻转条件：四参数必须同时达标

| 组合 | 发射($/kg) | GPU(TF/W) | 散热(W/m²) |
|------|-----------|-----------|-----------|
| A 最乐观 (<10%) | <$50 | >150 | >2,500 |
| B 乐观可行 (15-25%) | <$100 | >100 | >2,000 |
| C 临界可行 (25-40%) | <$200 | >80 | >1,800 |

所有组合需满足：硬件寿命>5年、硬件溢价<4x地面

**无单一参数突破可使太空算力翻转——需四参数同步改善，综合概率<$25%**

---

## 三层面综合评估

| 层面 | 当前可行？ | 核心约束 |
|------|-----------|---------|
| 物理 | 是 | 1GW需~0.7km²散热面积，物理上不否定 |
| 工程 | 脆弱 | GPU轨道故障率5-15%/年，维修不可行 |
| 商业 | 否 | TCO为地面10.5倍，翻转概率<$25% |

分歧本质不是"做不做"，而是"多快能做"和"瓶颈在哪里"
黄仁勋从芯片工程视角看到多参数耦合难度
马斯克从文明能源视角假设参数同步改善

---

<!-- _class: center-statement -->

# 结论

**物理成立。工程脆弱。商业不可行。**

黄仁勋"务实保留"在工程层面更站得住脚

最可能路径：2026-28原型验证 → 2028-30有限军事部署
→ 2030-35条件性扩张（如果四参数同步达标）
