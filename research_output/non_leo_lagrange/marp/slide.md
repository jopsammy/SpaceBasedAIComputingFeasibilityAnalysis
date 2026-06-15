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

# 非 LEO 轨道与拉格朗日点太空算力可行性

基于七维度的系统性工程评估

---

## LEO 基准回顾

- **散热瓶颈**：地球 IR（~240 W/m²）+ 反照（~480 W/m²），净回载 ~720 W/m²，散热器等效温度 >300 K
- **TCO 2-6x 地面**：5 年硬件寿命导致频繁替换；航天级抗辐射硬件溢价 5-10x
- **热循环**：5,840 次/年，导致材料疲劳与焊点失效风险

---

## 轨道环境全景

| 维度 | LEO | MEO | GEO | 地日L1/L2 |
|------|-----|-----|-----|-----------|
| TID (krad/yr) | 10-30 | 5-15 | 3-10 | **2-5** |
| SEU (vs LEO) | 1x | 10⁵x | 1-10x | 100-1000x |
| RTT | 5-10ms | 135ms | 500ms | 10,000ms |
| 350K散热(W/m²) | 482 | 1,040 | 1,040 | 1,038 |

HEO 与地月 L4/L5 见后续专题页；*地月 L4/L5 辐射数据置信度较低

---

## 关键发现：TID 悖论

地日 L1/L2 在 2.5mm Al 屏蔽后年 TID 仅 **2-5 krad/yr**，低于穿越 SAA 的 LEO 轨道（10-30 krad/yr）。

- LEO 的 TID 由 SAA 区域捕获质子贡献，深空无此来源
- 但 SEU 率高出 **100-1000 倍**——GCR 重离子全通量，无地磁场偏转
- **"猝死"（SEE）比"慢死"（TID）更难应对**

---

## MEO：SEE 主导的辐射难题

- SEU 率 ~10⁵ 倍于 LEO——外辐射带核心区域
- TMR + EDAC + 秒级 scrubbing 开销可能"吃掉"大部分有效算力
- TID 与 LEO 可比的假象（5-15 krad/yr）被 SEE 风暴掩盖
- 缺少独特应用价值：GNSS 星上 AI 增强市场规模有限

**综合指数 1.47，评级 B——不推荐独立部署**

---

## GEO：综合最优轨道

- **TID 仅 3-10 krad/yr**（低于 LEO），SEU 仅 1-10x LEO
- **热环境近乎理想**：地球 IR/反照可忽略，<2% 时间在食中，散热 2.2x LEO
- **固定覆盖 1/3 地球**：光伏面积比 LEO 少 ~40%，RTT 500ms 可本地规避
- **发射成本 1.54x LEO**：Starship 在轨加注可缩至 1.1-1.3x

---

## GEO：在轨维护的战略优势

- **MEV-1/2 已成功**：2020-2021 年对接 Intelsat 卫星延寿 5 年以上
- **DARPA RSGS 即将就位**：机器人有效载荷已完成 TVAC 测试（2024），预计 2027-2028 首飞
- **15 年已验证寿命** + 在轨服务 → 全生命周期折旧成本下降 3-4x
- **最可能场景**：通信卫星"搭载"AI 推理载荷，下行数据预处理压缩

**综合指数 0.83，比 LEO 优 17%（排名第一）**

---

## HEO：不推荐——双杀轨道

- **TID 50-200 krad/yr**（5-7x LEO）——所有轨道最高
- **SEU 10⁵-10⁶ x LEO**——所有轨道最高
- 每圈穿越辐射带 4 次，无法通过单一屏蔽厚度应对
- 发射成本 1.60x LEO（最高），RTT 跨度 37x 极度不稳定

**综合指数 2.52，评级 C——不推荐任何太空算力部署**

---

## 拉格朗日点：地日 L2

- **连续日照 + 40K 天然冷端**：JWST 已验证，散热效率 ~1,700 W/m²
- **RTT ~10s**：排除交互式推理，仅适用批处理式计算
- **SEU 100-1000x LEO**：TMR + scrubbing 综合开销 200-300% 面积
- **唯一利基**：量子-经典协同计算——40K 被动预冷大幅降低稀释制冷机功耗

---

## 拉格朗日点：地月 L4/L5

- **引力稳定**：理论上零站位保持燃料（实际 ~0-1 m/s/年）
- **RTT ~2.6s**：4x 优于地日 L1/L2，256-512x LEO
- **零热循环 + 零储能**：连续日照，地球 IR/反照 ~0
- **战略定位**：Artemis/LunaNet 深空通信导航骨干计算节点

**综合指数 0.94——最具长期战略价值的深空平台**

---

## 综合成本排名 — 上半（M5 模型）

| 排名 | 轨道 | 综合指数 | 评级 |
|------|------|----------|------|
| **1** | **GEO** | **0.83** | A |
| 2 | 地月L1 | 0.94 | A |
| 3 | 地月L4/L5 | 0.94 | A |
| 4 | 地月L2 | 0.95 | A |
| 5 | 地日L1 | 0.99 | A |

加权：发射30% + 散热20% + 光伏15% + 辐射25% + 寿命10%

---

## 综合成本排名 — 下半（M5 模型）

| 排名 | 轨道 | 综合指数 | 评级 |
|------|------|----------|------|
| 6 | 地日L2 | 0.99 | A |
| 7 | LEO(基准) | 1.00 | A |
| 8 | MEO | 1.47 | B |
| 9 | HEO | 2.52 | C |

**GEO 最优（比 LEO 优 17%），MEO/HEO 不推荐**

---

## 翻转阈值与演进路径

| 轨道 | 发射临界 | 硬件溢价临界 | 寿命临界 | 翻转概率(2035) |
|------|---------|------------|---------|---------------|
| LEO | <$100/kg | <3x 地面 | >7 年 | 中低 25-40% |
| GEO | <$120/kg | <3x 地面 | >5 年 | 中低 20-35% |
| L1/L2 | <$100/kg | <2.5x 地面 | >8 年 | 低 10-20% |
| L4/L5 | <$100/kg | <2.5x 地面 | >7 年 | 低 15-25% |

**降低硬件抗辐射溢价——而非发射成本——是关键杠杆**

---

<!-- _class: center-statement -->

# GEO 先行 → L4/L5 跟随 → L2 利基

**GEO (2028-2035)**：通信卫星搭载 AI 载荷
**L4/L5 (2032-2040)**：Artemis/LunaNet 深空骨干
**L2 (2035+)**：量子-经典协同计算

MEO 和 HEO 不推荐
