# 第二阶段证据链路由手册

> 创建时间：2026-06-14
> 对应轮次：close-stage-two-evidence-gaps（第三轮）
> 用途：人类阅读的证据追溯速查表

## 一、路由原则

本手册使任何人（包括未来的你或协作者）能通过文件名追溯到每个关键结论的原始支撑证据。追溯路径为五层：

```text
最终结论（根目录交付物或结果文档）
  → 审计文档（缺口解除状态、逐条审计）
    → 结构化 JSON 输入（模型可读参数值）
      → V 裁决记录（current-note.md §Task V2，含 AskUserQuestion 裁决、来源 URL、推导链）
        → 原始来源 URL / 物理公式
```

使用方式：在表中找到你要查的结论 → 从左到右依次打开对应列的文件 → 每一层都精确指向更原始的支撑证据。最右列给出最终的 URL 或公式，可独立核验。

## 二、关键结论速查路由

> 绝对路径前缀统一为 `D:\2024备份和迁移\2024备份和迁移\f复旭文件\h彗星计划相关\其他资料\凯瑞甘的texmarp项链孵化池\黄仁勋发言调研\`，下表中为节省列宽省略此前缀以 `…\` 表示。完整路径请自行拼接。

| 结论 | 值 | 证据档位 | 第一落点（结果文档） | 第二落点（审计文档） | 第三落点（JSON输入） | 第四落点（V裁决） | 第五落点（URL/公式） |
|------|-----|---------|---------------------|---------------------|---------------------|-------------------|---------------------|
| 功率轨道基线 | 峰值 150 kW / 持续 120 kW / 轨道 600 km | 二档（多源交叉验证） | `…\第二阶段差异分析初步研究.md` §1.3 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七 | 不适用（脚本常量） | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V1-V3 | Inkl/Tom's Hardware `inkl.com` / Knightli `knightli.com` / Indexbox `indexbox.io` 三家一致 |
| 计算载荷质量（基准） | 1,500 kg | 二档 + 三档 | `…\第二阶段差异分析初步研究.md` §5.2 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §三 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §components[compute_payload] | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V30 | GB300 NVL72 计算托盘 29 kg — [Lenovo LP2357](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai)；HGX B200 32 kg — [NVIDIA PCF](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf)；DGX B200 142.4 kg — [NVIDIA User Guide](https://docs.nvidia.com/dgx/dgxb200-user-guide/introduction-to-dgxb200.html) |
| GaAs 效率 BOL | 32% | 二档（权威产品规格） | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` §三 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §route_sensitive_inputs | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V4 | [AzurSpace 4G32 产品页](https://www.azurspace.com/en/products/space-products/) — 32% class 三结 GaAs 空间级电池 |
| GaAs 效率 EOL | 29% | 二档（文献退化率） | 同上 §三 | 同上 §七 | 同上 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V5 | BOL 32% × (1 − 9.4%) ≈ 29%；退化率来自 NASA NEPP 报告数据库 III-V 空间电池 LEO 10 年统计 |
| HJT 效率 BOL | 22% | 二档（多锚点交叉+AM0 修正） | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` §三 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §四 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §route_sensitive_inputs.hjt_parallel | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V6 | [华晟](https://www.huasunsolar.com/) 量产 >26%；[东方日升](https://www.prnewswire.com/news-releases/risen-energy-achieves-26-61-efficiency-for-hjt-solar-cell-302390000.html) 26.61%；[隆基](https://www.longi.com/) 27.81%；AM0 修正 0.85 → 保守取 22% |
| HJT 效率 EOL | 14% | 二档（独立辐照实验） | 同上 §三 | 同上 §四 | 同上 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V7 | [CEA/INES](https://www.cea.fr/cea-tech/liten/english/Pages/Medias/News/2025/major-breakthrough-for-photovoltaic-technology-space.aspx)：>14% after 10¹⁴ e⁻/cm² 1MeV；[ISFH Caltec](https://ines-solaire.org/) 独立验证 97% self-curing recovery |
| GaAs 阵列面密度 | 1.5 kg/m²（panel-only） | 三档（可迁移证据） | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` §三 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §route_sensitive_inputs | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V8 | 行业区间 1.5–2.5 kg/m²（空间级刚性 GaAs 面板，含 cells+cover glass+interconnects+honeycomb），取区间低端 |
| HJT 阵列面密度 | 1.8 kg/m²（panel-only） | 三档（Starlink V2 Mini 迁移） | 同上 §三（HJT 行） | 同上 §四 | 同上 §route_sensitive_inputs.hjt_parallel | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V9 | Starlink V2 Mini 面板级反推 ~1.7–2.6 kg/m²（116m² / 740kg 整星）；[33FG Research](https://research.33fg.com/analysis/starlink-v2-mini-optimized-lighter-satellites-more-bandwidth-per-launch) 硅基阵列区间 1.0–3.0 |
| 电池 DOD（三分支） | 5yr NMC 40% / 10yr Li-ion 25% / 10yr LTO 80% | 三档（Starlink 迁移）+ 四档（LTO 等比） | `…\第二阶段差异分析初步研究.md` §8.2 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §五 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §battery | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V10 | Ray Barsa（SpaceX 首席电池工程师）[演讲](https://ciclibattery.com/battery-power-online-space-batteries-how-spacex-designs-batteries-for-satellites/)：max DOD ~50%、5,000 等效全循环；[Saft LTO](https://saft.com/en/horizon-new-lithium-based-technology-satellite-batteries-improving-mission-performance)：80–90% DOD |
| 电池比能量 | Li-ion NMC 190 Wh/kg / LTO 100 Wh/kg | 三档 | 同上 §8.2 | 同上 §五 | 同上 §battery | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V11 | Starlink pack 230 Wh/kg（cell→pack 降额 ~12%→190）；Saft LTO 比 Li-ion 低 30–50%→100 Wh/kg 保守 |
| 散热器面密度 | 4.0 / 5.0 / 6.5 kg/m² | 四档（合理推断） | `…\第二阶段差异分析初步研究.md` §4.3 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §三（空间化增量） | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — 通过 script 读取 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V20 | 航天器热控结构面密度 3–8 kg/m²；ISS 840 m² / 1,000 kg≈1.2 为展开式轻量设计不适用刚性面板 |
| 平台系数 | 0.25 / 0.35 / 0.45 | 四档（Starlink V2 Mini 迁移） | `…\第二阶段差异分析初步研究.md` §4.3 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七（V21 修正） | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — ratio 字段 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V21 | Starlink V2 Mini 质量粗拆：整星 740 kg − 光伏 197 − 电池 48 − 推进 40 − 通信 170 = 结构/热控/线束 ~285 kg → ratio ~0.38 |
| 推进质量 | 200 / 350 / 500 kg | 四档（Starlink 比例外推） | `…\第二阶段差异分析初步研究.md` §12.1 | 同上 §七（V22 修正） | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — components[propulsion] | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V22 | Starlink V2 Mini 推进 ~5–6% 整星质量（SpaceX 自研氩霍尔 170 mN/台）；AI1 6,000–8,000 kg 级→5–8%→300–640 kg |
| 通信质量 | 200 / 300 / 450 kg | 四档（Google Suncatcher 推断） | `…\第二阶段差异分析初步研究.md` §4.3 | 同上 §七（V23 修正） | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — components[communication] | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V23+V28 | [Google Suncatcher](https://arxiv.org/html/2511.19468v1)（2025 arXiv）：天基 AI 集群需 tens of Tbps ISL；Starlink V2 Mini 通信系统 ~170–250 kg 为下界 |
| PCDU 比功率 | 1.0 / 0.5 / 0.2 kW/kg | 四档（Terma 飞行产品锚点） | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` §三 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七（V25 修正） | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — 通过 script 读取 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V25 | [Terma PCDU 飞行产品](https://satsearch.co/products/terma-power-conditioning-distribution-unit)：15 kW / 28 kg = 0.54 kW/kg；Starlink "simplified power electronics" 改善 |
| 计算载荷成本 | $38k / $60k / $100k / kW | 三档（3 轮搜索 + SpaceX COTS 策略） | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md` §四 | 同上 §七（V12） | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V12 | GB300 NVL72 地面 $25–33k/kW — [awesomeagents.ai](https://awesomeagents.ai/hardware/nvidia-gb300-nvl72/)；H100 空间原型 17–33× — [culled.org](https://culled.org/articles/ai-in-space-satellite-h100-beginning/)；SpaceX COTS 策略 1.5–3× |
| GaAs 阵列成本 | $180 / $200 / $250 / W_BOL | 三档（多锚点交叉） | 同上 §四（光伏阵列行） | 同上 §七（V14） | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V14 | AzurSpace 产品存在 + 旧口径 200–400 USD/W + satsearch 零售面板三锚点 |
| 电池 NMC 成本 | $200/kWh（固定） | 三档（Starlink 直接迁移） | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md` §四（电池行） | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §五 | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` §battery_cost_per_kwh_nmc | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V36 | Ray Barsa 演讲 + Starlink 亿颗级 Panasonic 21700 采购；零溢价原则——Starlink pack 本身就是空间电池 |
| 电池 LTO 成本 | $260 / $350 / $400 / kWh | 四档（等比压缩法） | 同上 §八 | 同上 §五 | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` §battery_cost_per_kwh_lto | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V37 | 地面 LTO/NMC 价格比 1.3–1.5×；V36 NMC $200/kWh × 1.3–2.0 = $260–400/kWh |
| PCDU 成本 | $3k / $5k / $10k / kW | 四档（Terma 锚点但无公开价格） | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md` §四（功率电子行） | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七（V26） | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V25+V26 | Terma BepiColombo MTM PCDU 飞行产品存在（[satnow.com](https://www.satnow.com/products/power-conditioning-and-distribution-units/terma/134-1195-bepicolombo-mtm-pcdu)），但价格未公开 |
| 推进成本 | 5yr：$500k/$800k/$1.2M；10yr：$800k/$1.3M/$2.4M | 四档（0.6 次方缩放 + 寿命分支） | 同上 §四（推进行） | 同上 §七（V27） | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V27 | Starlink 推进成本雪球分析 $125–250k；0.6 次方法则：10× 推力 → 10^0.6 ≈ 4× 成本；用户纠正线性缩放错误 |
| 通信成本 | $1.5M / $2.5M / $4.0M per 卫星 | 四档（Google Suncatcher 推断） | 同上 §四（通信行） | 同上 §七（V28） | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V28 | [Google Suncatcher](https://arxiv.org/html/2511.19468v1)：tens of Tbps ISL；Starlink V2 Mini 通信系统 ~$1–2M 为下界 |
| 10年-GaAs 总成本 | $764.98M | 一档+二档+三档+四档（多档混合） | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md` §三 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §六 | 全部 JSON 输入的综合输出 | 不适用（模型计算值，非单参数裁决） | 计算公式：制造成本 + 发射成本 + 保险(8%) + 运维($5M/年×10) + 退役($3M/代×1)；`stage2_mass_cost_model.py` 实跑 exit code 0 |
| 废弃的 kW/t 链 | 70/55/45 kW/t → 永久废弃 | 已废弃 | `…\第二阶段差异分析初步研究.md` §5.1 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §三 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` — deprecated_notice 字段 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §Task 2 | 废弃原因：分母来源 B1 级二手转述、定义域根本性歧义（整星 vs 载荷）、循环引用风险 |

## 三、文件类型与职能

| 文件类型 | 职能 | 谁读 | 实例 |
|---------|------|------|------|
| 根目录交付物 | 最终结论汇总，全文人类可读 | 人类决策者、paper 作者 | `…\第二阶段差异分析初步研究.md` |
| 审计包 | 全量缺口解除状态，逐 Task 审计 | 审查者 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` |
| 证据包 | 单主题深度证据（含 URL、推导链） | 技术审查 | `…\research_output\workspace\data\stage2_hjt_evidence_pack.md` |
| 审计文档 | 单领域逐条审计 | 技术审查 | `…\research_output\workspace\data\stage2_bom_mass_support_audit.md`（BOM 质量）；`…\research_output\workspace\data\stage2_power_boundary_and_formula_audit.md`（电源边界）；`…\research_output\workspace\data\stage2_procurement_price_sources.md`（采购价格链） |
| JSON 输入 | 模型可读的结构化参数 | 脚本 + 人工核对 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json`；`…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` |
| Python 脚本 | 计算逻辑实现 | 开发者 + 验证者 | `…\research_output\workspace\scripts\stage2_mass_cost_model.py`；`…\research_output\workspace\scripts\stage2_power_system_model.py` |
| 结果文档 | 脚本自动产出（含先行结论+拆解表） | 结论使用者 | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md`；`…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` |
| Spec 三件套 | 过程约束（spec/tasks/checklist） | 执行者 | `…\.trae\specs\close-stage-two-evidence-gaps\spec.md`；`…\.trae\specs\close-stage-two-evidence-gaps\tasks.md`；`…\.trae\specs\close-stage-two-evidence-gaps\checklist.md` |
| Note | V1-V37 跨 Task 裁决记录 | 追溯者 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` |

## 四、Paper 更新路线

如果你要更新 paper 的某个章节，应依次读取以下文件：

| Paper 章节 | 先读这个 | 再读这个 | 最后核对 |
|-----------|---------|---------|---------|
| 计算载荷 / 单星质量 | `…\research_output\workspace\data\stage2_blackwell_payload_mass_bottom_up.md` | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §components | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V30 |
| 光伏 / 电源系统 | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §route_sensitive_inputs | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V4–V9, V25 |
| 电池 / 储能 | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §五 | `…\research_output\workspace\data\stage2_mass_inputs_blackwell_hjt.json` §battery | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V10–V11, V36–V37 |
| 制造成本 / 经济模型 | `…\research_output\workspace\data\stage2_economic_branches_blackwell.md` | `…\research_output\workspace\data\stage2_cost_inputs_blackwell_hjt.json` | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V12–V15, V26–V29 |
| HJT 路线 | `…\research_output\workspace\data\stage2_hjt_evidence_pack.md` | `…\research_output\workspace\data\stage2_power_system_results_blackwell_hjt.md` §三（HJT 行） | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §V6–V7, V9, V16 |
| 参数准入 / 缺口状态 | `…\research_output\workspace\data\stage2_parameter_admission_registry.md` | `…\research_output\workspace\data\stage2_gap_closure_verification.md` §七/九 | `…\.trae\specs\close-stage-two-evidence-gaps\current-note.md` §Task V2 |
| 旧轮→本轮映射 | `…\research_output\workspace\data\stage2_branch_mapping_from_previous_round.md` | — | — |

## 五、废弃清单

| 废弃项 | 替代项 | 说明 |
|--------|--------|------|
| `70/55/45 kW/t` 反推链 | V30 bottom-up（GB300 NVL72 地面硬件 + 三项空间化增量） | 分母来源 B1 级二手转述，定义域存在根本性歧义（整星 vs 载荷），存在循环引用风险（Task 2 裁决） |
| `compute_specific_power_kw_per_t` 所有引用 | `components[compute_payload].scenario_mass_kg` 直接读取 | 脚本中已完全移除 kW/t 中间量（`stage2_mass_cost_model.py` 实跑确认） |
| HJT "只能降级" / "禁止进入主模型" | "并行成熟路线" | Task 3 V6–V9 裁决：HJT 现为与 GaAs 并列的成熟技术路线，物理链可比较，价格链闭合度单独标注 |
| 旧 `battery_cost_per_kwh` item_id | `battery_cost_per_kwh_nmc` + `battery_cost_per_kwh_lto` | 电池分裂为 NMC（三档固定 $200/kWh）和 LTO（四档 $260/350/400/kWh）两独立 item_id |
| `stage2_mass_cost_results.md` | `stage2_economic_branches_blackwell.md` | 旧聚合模型结果文档，已移入 `_deprecated/`（若存在） |
| `stage2_power_system_results.md` | `stage2_power_system_results_blackwell_hjt.md` | 旧版电源系统结果文档，已由 Blackwell+HJT 并行版替代 |
| `stage2_architecture_reconciliation.md` | 无直接替代（Rubin 已降级为支线留痕） | Rubin 主线已废弃，仅保留支线留痕；不再进入主模型 |

## 六、四档证据体系速查

| 档位 | 入模条件 | 标签 | 参数数 | 典型参数 |
|------|---------|------|--------|---------|
| 一档 | 直接入模，写清公式/输入/单位/边界 | 物理推导 | 5 | 太阳常数(1361.0 W/m²)、散热面积(110 m², S-B 推导)、阵列面积（物理公式推导）、电池名义容量（186.4 kWh） |
| 二档 | 首次引用即 AskUserQuestion | 权威资料 | 7 | 峰值功率(150 kW)、持续功率(120 kW)、轨道高度(600 km)、GaAs BOL/EOL(32%/29%)、HJT BOL/EOL(22%/14%) |
| 三档 | 首次引用即 AskUserQuestion | 可迁移证据 | 17 | GaAs/HJT 面密度、DoD、比能量、计算载荷成本、GaAs 阵列成本、HJT 价格链等 |
| 四档 | 首次引用即 AskUserQuestion | 合理推断 | 14 | 散热器面密度、平台系数、推进质量/成本、通信质量/成本、AIT 裕量/成本、PCDU 比功率/成本等 |
| 禁止 | 永不入模 | 无支撑 | 1 | 旧电池成本 $400/kWh（与 satsearch 空间级列表价存在约 225 倍数量级矛盾） |
| 废弃 | 已替换 | — | 3 | kW/t 反推链(70/55/45)、旧计算载荷质量(2,143/2,727/3,333 kg)、HJT"禁止进入主模型"标签 |

> 统计来源：`…\research_output\workspace\data\stage2_parameter_admission_registry.md`（47 参数逐条重分级清单）；`…\research_output\workspace\data\stage2_gap_closure_verification.md` §七。
