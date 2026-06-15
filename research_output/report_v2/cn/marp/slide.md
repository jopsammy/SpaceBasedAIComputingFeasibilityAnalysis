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

# 太空算力：物理可行，工程脆弱，商业远距

基于 Space Solar 与 NVIDIA 架构的三层独立验证

---

## 分歧定性：不是做不做，是多快做

黄仁勋（保守审慎）vs 马斯克（极度乐观），分歧不在"谁算错了"

- 时间窗、功率口径、系统边界——三项变量不同，结论自然分化
- 核心判断：不是做不做，而是**多快做**

---

<!-- _class: section-divider -->

## 三层分析总览

物理可行 —— S-B 定律与辐射散热自洽

工程脆弱 —— 质量链与制造边界紧张

商业远距 —— TCO 与地面差 **11.8×**

---

## 散热可行：S-B 定律与 1,400 W/m² 工作点

斯特藩-玻尔兹曼定律：

$$
\frac{P}{A} = 2\varepsilon\sigma T^4
$$

$$
\sigma = 5.6704\times10^{-8}\;{\rm W\cdot m^{-2}\cdot K^{-4}}
$$

AI1：取 $\varepsilon\approx0.90$、$T\approx342.5\;{\rm K}$（69.5°C），得 **~1,400 W/m²**

物理自洽，但已逼近涂层 EOL 退化裕度

---

## LEO 不是冷库：食影与热环境约束

三热源叠加：太阳直射 **1,361 W/m²** + 地球反照 **~122 W/m²** + 地球红外 **~240 W/m²**

- 净散热能力比理想真空低 **15–40%**
- 食影 **35.5 min** / 周期 **96.7 min**，需电池 **71.0 kWh**

结论：LEO 不是无限冷沉

---

## 整星成本拆解：$83.61M 去了哪里

9 子系统，整星 **8.48 t**

- 光伏阵列 **$46.27M（55.3%）** — 最大单项
- 系统裕量/冗余 **$18.29M（21.9%）**
- 单星总制造成本 **$83.61M**
- 发射成本仅占 TCO 的 **~1.8%**

---

## 三数字矛盾：120 / 150 / ~210 kW

- **120 kW** — 持续 IT 负载声明
- **150 kW** — GPU 峰值功率
- **~210 kW** — 根据 LEO 昼食周期推算的阵列 EOL 物理需求：日食段电池充电 + 光照段 IT+散热持续供电，闭合后需 **~210 kW**

结论：120 kW 声明值与 150 kW 峰值功率均与轨道能量平衡的 **~210 kW** 物理需求存在 **1.4× 偏差**，存在物理学上的矛盾

---

## 发射规模现实检验：300 GW/年 vs FAA 上限 69 次/年

马斯克声称 **300–500 GW/年** 部署能力

- FAA 批准 Starship 年发射上限：**69 次**
- 按 10 颗/发、120 kW/颗计算：**~0.083 GW/年**
- 差距约 **3,600 倍（3 个数量级）**

即使大幅放宽 FAA 上限，三个参数的组合改善也无法闭合量级差距

---

## 寿命杠杆：5年HJT×2 反超 10年砷化镓

- 10年-GaAs（单代）：**$764.98M**
- 5年-HJT×2（需重射）：**~$1,005M（+31.4%）**
- HJT 电池虽便宜 70–100×，但 **2× 重射** 代价反超
- 轨道 GPU AFR **5–15%/年**，维修不可行

结论：在轨寿命是比电池成本更重要的经济杠杆

---

## 三分支 TCO 对比：地面 vs 太空

| 场景 | 10年总成本 | 与地面差距 |
|------|-----------|-----------|
| **地面 IDC** | **$64.6M** | **1×（基准）** |
| 10年-GaAs（主链） | $764.98M | 11.8× |
| 5年-HJT×2（补齐估计） | ~$1,005M | 15.6× |
| 5年-GaAs×2（对照） | $1,341M | 20.8× |

制造端（特别是光伏阵列）是 TCO 的核心驱动

---

<!-- _class: section-divider -->

## 商业远距：$765M vs $65M = 11.8×

10年-GaAs **$764.98M** vs 地面 **$64.6M**

差距 = **11.8×**

---

## 成本解剖：发射仅占 1.8%

- 制造成本 **91.1%** 绝对主导
- 光伏阵列 **50.4%**，系统裕量 **20.0%**
- 发射仅 **1.8%** — 每 $100 中不到 $2 用于发射

方向性杠杆在制造端，不在发射端

---

## 翻转条件：四参数同步概率 < 25%

四参数同步达标：寿命≥7年 + 光伏<$50/W_BOL + AIT Starlink 级 + 发射<$100/kg

- 独立联合概率 **~8.4%**，正相关调整后 **<25%**

结论：可能但不确定，不足以支撑明确商业承诺

---

## 时间线：2026 → 2028 → 2030 → 2035

| 阶段 | 时间 | 判断 |
|------|------|------|
| 原型验证 | 2026–2028 | 商业不可行，技术验证有意义 |
| 利基部署 | 2028–2030 | 军事/低延迟推理场景 |
| 条件性扩张 | 2030–2035 | 四条件同步概率 **<25%** |

---

<!-- _class: center-statement -->

# 总结

**已知事实** · **可计算链** · **当前不可判定**

物理基础坚实，商业承诺不宜提前
