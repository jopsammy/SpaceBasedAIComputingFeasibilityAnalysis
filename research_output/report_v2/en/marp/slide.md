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
    font-size: 28px;
    padding: 60px 80px;
    line-height: 1.45;
    word-break: break-word;
    overflow-wrap: break-word;
  }
  h1, h2 { color: var(--color-heading); font-weight: bold; margin-top: 0; }
  h1 { font-size: 2.2em; margin-bottom: 0.5em; }
  h2 { font-size: 1.6em; margin-bottom: 0.6em; }
  h3 {
    font-size: 1.2em;
    color: var(--color-text);
    border-left: 6px solid var(--color-accent);
    padding-left: 15px;
  }
  strong { color: var(--color-heading); font-weight: 800; }
  em { color: var(--color-accent); font-style: normal; font-weight: bold; }
  ul { padding-left: 1em; }
  li { margin-bottom: 0.4em; }
  section.center-statement {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
  }
  section.center-statement h1 { font-size: 2.8em; line-height: 1.2; }
  section.center-statement p { font-size: 1.3em; color: var(--color-text); opacity: 0.8; }
  section.section-divider {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background-color: #f5f5f5;
  }
  section.section-divider h2 { font-size: 2em; }
  table { border-collapse: collapse; width: 100%; font-size: 0.6em; margin: 0 auto; table-layout: fixed; }
  th, td { border: 1px solid var(--color-border); padding: 6px 8px; text-align: left; word-break: break-word; overflow-wrap: break-word; }
  th { background-color: #f6f8fa; font-weight: bold; }
  img { display: block; margin: 0 auto; max-width: 100%; max-height: 60vh; }
---

<!-- _class: center-statement -->

# Space-Based AI Computing: Physically Feasible, Engineering-Fragile, Commercially Distant

Three-Tier Independent Verification Based on Space Solar and NVIDIA Architecture

---

## Characterizing the Disagreement: It's Not About Whether, It's About How Fast

Jensen Huang (conservative &amp; prudent) vs. Elon Musk (extremely optimistic)&mdash;the disagreement is not about "who miscalculated"

- Time window, power sizing, system boundary&mdash;three variables differ, conclusions naturally diverge
- Core judgment: it's not about whether, but **how fast**

---

<!-- _class: section-divider -->

## Three-Tier Analysis Overview

Physically Feasible&mdash;S-B Law and radiative heat dissipation self-consistent

Engineering-Fragile&mdash;mass chain and manufacturing margins tight

Commercially Distant&mdash;TCO gap vs. ground: **11.8&times;**

---

## Heat Dissipation Feasible: S-B Law and 1,400 W/m&sup2; Operating Point

Stefan-Boltzmann law:

$$
\frac{P}{A} = 2\varepsilon\sigma T^4
$$

$$
\sigma = 5.6704\times10^{-8}\;{\rm W\cdot m^{-2}\cdot K^{-4}}
$$

AI1: Using &epsilon;&asymp;0.90, T&asymp;342.5 K (69.5&deg;C), yields **~1,400 W/m&sup2;**

Physically self-consistent, but approaching coating EOL degradation margin

---

## LEO Is Not a Cold Sink: Eclipse and Thermal Environment Constraints

Three heat sources combined: direct solar **1,361 W/m&sup2;** + Earth albedo **~122 W/m&sup2;** + Earth IR **~240 W/m&sup2;**

- Net heat dissipation capacity **15&ndash;40%** lower than ideal vacuum
- Eclipse **35.5 min** / orbit **96.7 min**, requires **71.0 kWh** battery

Conclusion: LEO is not an infinite cold sink

---

## Satellite Cost Breakdown: Where the $83.61M Goes

9 subsystems, satellite **8.48 t**

- Photovoltaic array **$46.27M (55.3%)**&mdash;largest single item
- System margin/redundancy **$18.29M (21.9%)**
- Per-satellite manufacturing cost **$83.61M**
- Launch cost only **~1.8%** of TCO

---

## Three-Number Contradiction: 120 / 150 / ~210 kW

- **120 kW**&mdash;claimed sustained IT load
- **150 kW**&mdash;GPU peak power
- **~210 kW**&mdash;array EOL physical requirement<br>derived from LEO day-night cycle:<br>eclipse-segment battery charging + sunlit-segment IT +<br>heat dissipation continuous power&mdash;closes at **~210 kW**

Conclusion: Both the 120 kW claimed value and 150 kW peak power<br>exhibit a **1.4&times; deviation** from the **~210 kW** physical requirement<br>of orbital energy balance&mdash;a physics-level contradiction

---

## Launch Scale Reality Check: 300 GW/yr vs. FAA Cap of 69 Launches/yr

Musk claims **300&ndash;500 GW/yr** deployment capacity

- FAA-approved Starship annual launch cap: **69 launches**
- At 10 satellites/launch, 120 kW/satellite: **~0.083 GW/yr**
- Gap: **~3,600&times; (3 orders of magnitude)**

Even with substantial FAA cap relaxation,<br>combined improvement of all three parameters<br>cannot close the order-of-magnitude gap

---

## Lifetime Leverage: 5yr HJT&times;2 Outweighs 10yr GaAs

- 10yr-GaAs (single generation): **$764.98M**
- 5yr-HJT&times;2 (requires re-launch): **~$1,005M (+31.4%)**
- HJT cells are 70&ndash;100&times; cheaper, but **2&times; re-launch** cost outweighs
- Orbital GPU AFR **5&ndash;15%/yr**, maintenance infeasible

Conclusion: On-orbit lifetime is a more important economic lever than cell cost

---

## Three-Branch TCO Comparison: Ground vs. Space

| Scenario | 10yr Total Cost | Gap vs. Ground |
|------|-----------|-----------|
| **Ground IDC** | **$64.6M** | **1&times; (baseline)** |
| 10yr-GaAs (primary) | $764.98M | 11.8&times; |
| 5yr-HJT&times;2 (gap-filling estimate) | ~$1,005M | 15.6&times; |
| 5yr-GaAs&times;2 (control) | $1,341M | 20.8&times; |

Manufacturing (especially photovoltaic array) is the core TCO driver

---

<!-- _class: section-divider -->

## Commercially Distant: $765M vs. $65M = 11.8&times;

10yr-GaAs **$764.98M** vs. ground **$64.6M**

Gap = **11.8&times;**

---

## Cost Anatomy: Launch Is Only 1.8%

- Manufacturing cost **91.1%**&mdash;absolutely dominant
- Photovoltaic array **50.4%**, system margin **20.0%**
- Launch only **1.8%**&mdash;less than $2 out of every $100 goes to launch

Directional leverage is in manufacturing, not launch

---

## Reversal Conditions: Four-Parameter Joint Probability &lt; 25%

Four parameters met simultaneously:<br>lifetime &ge;7yr + PV &lt;$50/W<sub>BOL</sub> + AIT Starlink-class + launch &lt;$100/kg

- Independent joint probability **~8.4%**, after positive-correlation adjustment **&lt;25%**

Conclusion: possible but uncertain,<br>insufficient to support a definitive commercial commitment

---

## Timeline: 2026 &rarr; 2028 &rarr; 2030 &rarr; 2035

| Phase | Time | Assessment |
|------|------|------|
| Prototype Verification | 2026&ndash;2028 | Commercially infeasible, technology validation meaningful |
| Niche Deployment | 2028&ndash;2030 | Military / low-latency inference scenarios |
| Conditional Expansion | 2030&ndash;2035 | Four-condition joint probability **&lt;25%** |

---

<!-- _class: center-statement -->

# Summary

**Known Facts** &middot; **Computable Chains** &middot; **Currently Undecidable**

Physical foundation is solid; commercial commitment should not be made prematurely
