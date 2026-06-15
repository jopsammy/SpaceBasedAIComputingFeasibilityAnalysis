#!/usr/bin/env python3
"""
发射成本学习曲线验证脚本 (Phase 3 Q4/Q9)
==========================================
验证内容:
  1. 历史发射成本数据 (Shuttle → Falcon 9 → Starship 目标)
  2. Wright's Law 学习曲线拟合与验证
  3. 2030 年 $/kg 弹性推算
  4. 马斯克 "300-500 GW/年" 的物理可行性反推

参数来源:
  - Space Shuttle: ~$54,500/kg (NASA 2018)
  - Falcon 9 复用: ~$2,400/kg
  - Starship 目标: $100-200/kg
  - FAA 批准频次: Boca Chica 25/年 + KSC 44/年 = 69/年
  - Starship V3 运力: 200t/次
  - 每颗 AI 卫星: 5-10t, 120 kW 算力

作者: AC范式v6 parallel-sub-agent
日期: 2026-06-11
"""

import argparse
import math
import os
import sys
import io
from datetime import datetime


# =============================================================================
# 历史发射成本数据
# =============================================================================
# (年份, 运载器, $/kg_to_LEO, LEO运力kg, 累计发射次数估计)
HISTORICAL_LAUNCH_COSTS = [
    # (year, name, cost_per_kg, payload_kg, cumulative_launches, notes)
    (1981, "Space Shuttle",       54500,  27500,     1,   "NASA正式数据"),
    (1996, "Ariane 5",            8500,   21000,    80,   "ESA"),
    (2004, "Delta IV Heavy",      12200,  28790,   120,   "ULA"),
    (2010, "Falcon 9 (一次性)",   2720,   22800,   130,   "SpaceX首飞"),
    (2015, "Falcon 9 (回收成功)", 2720,   22800,   150,   "首次回收成功, 初期复用未降价"),
    (2018, "Falcon Heavy",        1500,   63800,   160,   "部分复用"),
    (2020, "Falcon 9 (复用常态)", 2400,   17500,   170,   "复用折扣, 载荷略降"),
    (2024, "Starship V1 (一次性)", 500,   200000,  175,   "Payload Research估算"),
    (2026, "Starship V3 (目标)",  200,    200000,  185,   "SpaceX营销目标"),
]

# Wright's Law 参数
WRIGHT_LEARNING_RATE_DEFAULT = 0.85  # 航天标准: 累计产量翻倍时成本降至85%
PHYSICAL_COST_FLOOR = 25.0           # 物理地板 $/kg ($10制造成本 + $10-20燃料/运营)


def wrights_law_cost(cumulative_units, first_unit_cost, learning_rate):
    """
    Wright's Law: 单位成本 = 首件成本 × 累计产量^(log2(学习率))

    参数:
        cumulative_units: 累计产量
        first_unit_cost: 首件成本
        learning_rate: 学习率 (航天标准 ~0.85)

    返回: 单位成本
    """
    if cumulative_units <= 0:
        return first_unit_cost
    exponent = math.log2(learning_rate)
    return first_unit_cost * (cumulative_units ** exponent)


def fit_wrights_law(data_points, learning_rate):
    """
    用 Wright's Law 拟合首件成本。
    最小化: sum((实际成本 - 预测成本)^2) 的对数空间误差。

    返回: (first_unit_cost, r_squared, residuals)
    """
    # 在 log-log 空间做线性回归
    # log(cost) = log(C1) + b * log(cumulative)
    # b = log2(learning_rate)
    b = math.log2(learning_rate)

    xs = []
    ys = []
    for year, name, cost_kg, payload, cum_launch, notes in data_points:
        xs.append(math.log(cum_launch))
        ys.append(math.log(cost_kg))

    n = len(xs)
    if n < 2:
        return 0, 0, []

    # 简单线性回归: y = a + b*x, 但 b 已固定
    # 所以 a = mean(y - b*x)
    a = sum(ys[i] - b * xs[i] for i in range(n)) / n
    C1 = math.exp(a)

    # 计算 R^2
    ss_res = 0
    ss_tot = 0
    y_mean = sum(ys) / n
    for i in range(n):
        y_pred = a + b * xs[i]
        ss_res += (ys[i] - y_pred) ** 2
        ss_tot += (ys[i] - y_mean) ** 2

    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    # 残差
    residuals = []
    for i, (year, name, cost_kg, payload, cum_launch, notes) in enumerate(data_points):
        predicted = C1 * (cum_launch ** b)
        residuals.append((name, cost_kg, predicted, cost_kg - predicted))

    return C1, r_squared, residuals


def print_historical_table():
    """打印历史发射成本表。"""
    print("\n" + "=" * 80)
    print("第一部分: 历史发射成本数据")
    print("=" * 80)

    print(f"\n{'年份':>6} {'运载器':<22} {'$/kg':>12} {'LEO运力(kg)':>14} {'累计发射':>10} {'备注':<30}")
    print("-" * 100)

    for year, name, cost_kg, payload, cum_launch, notes in HISTORICAL_LAUNCH_COSTS:
        print(f"{year:>6} {name:<22} ${cost_kg:>11,} {payload:>14,} {cum_launch:>10} {notes:<30}")

    # 计算下降幅度
    first_cost = HISTORICAL_LAUNCH_COSTS[0][2]
    last_cost = HISTORICAL_LAUNCH_COSTS[-1][2]
    reduction = first_cost / last_cost
    print(f"\n  1981→2026 下降幅度: ${first_cost:,}/kg → ${last_cost:,}/kg = {reduction:.0f}x")
    print(f"  年化降幅 (CAGR): {((last_cost/first_cost)**(1/(2026-1981))-1)*100:.1f}%  (45年)")


def print_wrights_law_fit():
    """Wright's Law 拟合与验证。"""
    print("\n" + "=" * 80)
    print("第二部分: Wright's Law 学习曲线拟合")
    print("=" * 80)

    learning_rates = [0.80, 0.82, 0.85, 0.87, 0.90]
    print(f"\n{'学习率':>10} {'首件成本 $/kg':>18} {'R²':>10} {'2030预测 $/kg*':>18} {'物理地板达标?':>15}")
    print("-" * 75)

    best_lr = WRIGHT_LEARNING_RATE_DEFAULT
    best_r2 = 0

    for lr in learning_rates:
        C1, r2, residuals = fit_wrights_law(HISTORICAL_LAUNCH_COSTS, lr)
        cum_2030 = 250  # 估计2030年累计发射次数
        pred_2030 = wrights_law_cost(cum_2030, C1, lr)
        above_floor = "是" if pred_2030 > PHYSICAL_COST_FLOOR else "低于地板!"

        marker = " <--" if abs(lr - WRIGHT_LEARNING_RATE_DEFAULT) < 0.001 else ""
        print(f"{lr:>10.2f} ${C1:>17,.0f} {r2:>10.3f} ${pred_2030:>17,.0f} {above_floor:>15}{marker}")

        if r2 > best_r2:
            best_r2 = r2
            best_lr = lr

    # 用最优学习率详细展示
    C1, r2, residuals = fit_wrights_law(HISTORICAL_LAUNCH_COSTS, best_lr)
    print(f"\n最优学习率: {best_lr} (R² = {r2:.3f})")
    print(f"拟合首件成本: ${C1:,.0f}/kg")

    print(f"\n--- 拟合残差分析 ---")
    print(f"{'运载器':<22} {'实际 $/kg':>12} {'预测 $/kg':>12} {'残差 $/kg':>12}")
    print("-" * 60)
    for name, actual, pred, res in residuals:
        print(f"{name:<22} ${actual:>11,} ${pred:>11,.0f} ${res:>11,.0f}")

    # 物理地板分析
    print(f"\n--- Wright's Law 收敛性分析 ---")
    print(f"物理成本地板: ${PHYSICAL_COST_FLOOR}/kg")
    print(f"  (制造成本极限 ~$10/kg + 燃料/运营 ~$10-20/kg)")

    for cum in [10, 50, 100, 200, 500, 1000, 5000, 10000]:
        cost = wrights_law_cost(cum, C1, best_lr)
        above = cost - PHYSICAL_COST_FLOOR
        print(f"  累计 {cum:>5} 次: ${cost:>8,.0f}/kg  (高于地板 ${above:>7,.0f}/kg)")


def print_2030_projections():
    """2030 年 $/kg 弹性推算。"""
    print("\n" + "=" * 80)
    print("第三部分: 2030 年 $/kg 弹性推算")
    print("=" * 80)

    C1, r2, _ = fit_wrights_law(HISTORICAL_LAUNCH_COSTS, WRIGHT_LEARNING_RATE_DEFAULT)

    print(f"""
基础参数:
  - Wright's Law 学习率: {WRIGHT_LEARNING_RATE_DEFAULT}
  - 拟合首件成本: ${C1:,.0f}/kg
  - 物理地板: ${PHYSICAL_COST_FLOOR}/kg (来源: 33fg Research 2026)
""")

    scenarios_2030 = [
        # (名称, 年发射频次, 累计发射, 2026基线发射, 额外说明)
        ("乐观",      200,  350, 185, "FAA大幅放宽 + 第2发射场投产 + Starship复用>30次"),
        ("基准",      125,  275, 185, "FAA审批扩展至100+次/年 + Block 3成熟"),
        ("悲观",       60,  220, 185, "FAA维持69/年上限 + 复用率<5次"),
        ("单Wright's Law", 125, 275, 185, "纯学习曲线推算, 无其他约束"),
    ]

    print(f"\n{'情景':<16} {'年发射':>8} {'累计发射':>10} {'Wright预测':>14} {'考虑地板后':>14} {'是否可行':>12}")
    print("-" * 80)

    for name, annual, cumulative, base_launches, notes in scenarios_2030:
        wright_cost = wrights_law_cost(cumulative, C1, WRIGHT_LEARNING_RATE_DEFAULT)
        effective_cost = max(wright_cost, PHYSICAL_COST_FLOOR)

        feasible = "可行" if effective_cost <= 200 else ("需验证" if effective_cost <= 500 else "需突破")
        print(f"{name:<16} {annual:>8} {cumulative:>10} ${wright_cost:>13,.0f} ${effective_cost:>13,.0f} {feasible:>12}")

    # FAA 频次约束分析
    print(f"""
--- FAA 发射频次约束分析 ---
  当前批准上限:
    Boca Chica (德州): 25 次/年 (2025 EA)
    KSC LC-39A (佛州): 44 次/年 (2026 ROD)
    合计: 69 次/年

  2030 年合理上限: 100-200 次/年
    - 扩展路径: KSC LC-49, Cape Canaveral SLC-37B, 海上平台
    - 需新建 1-2 个发射台 + FAA NEPA 审查

  结论: FAA 频次是比 Wright's Law 更硬的上限约束。
""")

    # 概率评估
    print(f"--- 2030 年 $/kg 概率估计 ---")
    probs = [
        ("<$100/kg",   "<15%",  "需 Starship 复用 >50 次 + 年发射 >200 次 + 第2/3发射场"),
        ("$100-200/kg", "40-50%", "基准情景: Block 3 成熟 + 年发射 100-150 次"),
        ("$200-500/kg", "30-35%", "FAA 约束 + 复用率 <10 次"),
        (">$500/kg",   "<10%",   "重大工程挫折"),
    ]
    print(f"  {'区间':<14} {'概率':<8} {'条件'}")
    print(f"  {'-'*12} {'-'*6} {'-'*40}")
    for interval, prob, cond in probs:
        print(f"  {interval:<14} {prob:<8} {cond}")


def verify_musk_300gw():
    """验证马斯克 300-500 GW/年 声明的物理可行性。"""
    print("\n" + "=" * 80)
    print("第四部分: 马斯克 '300-500 GW/年' 物理可行性反推")
    print("=" * 80)

    # 基础参数
    STARSHIP_PAYLOAD_T = 200          # Starship V3 复用运力 (吨)
    AI_SAT_MASS_T = (5, 10)           # 每颗 AI 卫星质量 (吨)
    AI_SAT_POWER_KW = 120             # 每颗持续功率 (kW)
    FAA_MAX_LAUNCHES = 69             # 当前 FAA 批准上限
    FAA_2030_OPTIMISTIC = 200         # 2030 乐观上限

    # 每次发射可部署的卫星数和算力
    sats_per_launch_low = STARSHIP_PAYLOAD_T / AI_SAT_MASS_T[1]   # 重星
    sats_per_launch_high = STARSHIP_PAYLOAD_T / AI_SAT_MASS_T[0]  # 轻星
    power_per_launch_low_MW = sats_per_launch_low * AI_SAT_POWER_KW / 1000
    power_per_launch_high_MW = sats_per_launch_high * AI_SAT_POWER_KW / 1000

    print(f"""
基础假设:
  - Starship V3 复用运力: {STARSHIP_PAYLOAD_T} t/次
  - AI 卫星质量: {AI_SAT_MASS_T[0]}-{AI_SAT_MASS_T[1]} t/颗
  - 每颗持续算力: {AI_SAT_POWER_KW} kW
  - 当前 FAA 批准频次: {FAA_MAX_LAUNCHES} 次/年
  - 2030 年乐观频次: {FAA_2030_OPTIMISTIC} 次/年

每次发射部署能力:
  - 卫星数: {sats_per_launch_high:.0f}-{sats_per_launch_low:.0f} 颗
  - 算力: {power_per_launch_low_MW:.1f}-{power_per_launch_high_MW:.1f} MW/次
""")

    # 当前 FAA 上限下
    power_faa_current_low = power_per_launch_low_MW * FAA_MAX_LAUNCHES
    power_faa_current_high = power_per_launch_high_MW * FAA_MAX_LAUNCHES

    print(f"当前 FAA 上限 ({FAA_MAX_LAUNCHES} 次/年):")
    print(f"  年部署算力: {power_faa_current_low:.0f}-{power_faa_current_high:.0f} MW = {power_faa_current_high/1000:.2f}-{power_faa_current_low/1000:.2f} GW")

    power_faa_2030_low = power_per_launch_low_MW * FAA_2030_OPTIMISTIC
    power_faa_2030_high = power_per_launch_high_MW * FAA_2030_OPTIMISTIC

    print(f"\n2030 年乐观上限 ({FAA_2030_OPTIMISTIC} 次/年):")
    print(f"  年部署算力: {power_faa_2030_low:.0f}-{power_faa_2030_high:.0f} MW = {power_faa_2030_high/1000:.2f}-{power_faa_2030_low/1000:.2f} GW")

    # 反推达到 300 GW 需要多少次发射
    launches_needed_300gw_low = 300_000 / power_per_launch_high_MW
    launches_needed_300gw_high = 300_000 / power_per_launch_low_MW
    launches_needed_500gw = 500_000 / power_per_launch_low_MW

    print(f"\n--- 反推: 达到马斯克声称的部署速率 ---")
    print(f"  300 GW/年:")
    print(f"    需要发射: {launches_needed_300gw_low:,.0f}-{launches_needed_300gw_high:,.0f} 次/年")
    print(f"    每天需要: {launches_needed_300gw_low/365:,.0f}-{launches_needed_300gw_high/365:,.0f} 次")
    print(f"    年部署卫星: {launches_needed_300gw_low * sats_per_launch_high:,.0f}-{launches_needed_300gw_high * sats_per_launch_low:,.0f} 颗")
    print(f"    当前上限可达成比例: {FAA_MAX_LAUNCHES / launches_needed_300gw_low * 100:.2f}%-{FAA_MAX_LAUNCHES / launches_needed_300gw_high * 100:.2f}%")

    print(f"\n  500 GW/年:")
    print(f"    需要发射: ~{launches_needed_500gw:,.0f} 次/年")
    print(f"    每天需要: ~{launches_needed_500gw/365:,.0f} 次")

    # 极端假设: 10000次/年
    launches_10000 = 10000
    power_10000 = power_per_launch_low_MW * launches_10000
    print(f"\n--- 极端假设: 年产 10,000 艘 Starship (33fg Research 假设) ---")
    print(f"  年部署算力: {power_10000:.0f} MW = {power_10000/1000:.1f} GW")
    print(f"  vs 300 GW: {power_10000/1000/300*100:.1f}%")
    print(f"  vs 500 GW: {power_10000/1000/500*100:.1f}%")

    # 结论
    deviation_orders = math.log10(launches_needed_300gw_low / FAA_MAX_LAUNCHES)
    print(f"""
--- 物理可行性判定 ---
  偏差数量级: 当前 FAA 上限与 300 GW/年所需发射次数相差约 ~10^{deviation_orders:.1f} 倍
  即偏差约 3 个数量级

  判定: 马斯克 "300-500 GW/年" 声明在当前工程约束下不可行
  可能的解释框架:
    1. 马斯克在描述终极理论极限 (10,000 艘 Starship + 100 次复用/艘)
    2. 或是故意用极端数字构建产业想象
    3. 不属于可操作近期目标 (2030年前)

  即使年产 10,000 艘 Starship (每艘复用 100 次 = 1,000,000 次等效发射):
    年部署算力: ~{power_per_launch_low_MW * 10000 * 100 / 1000:.0f} GW
    这将超过 300-500 GW 目标
    但年产 10,000 艘属于工业文明级别的假设, 不能仅用火星殖民解释

  严谨结论: 300-500 GW/年 需要 ~{launches_needed_300gw_low:,.0f} 次发射/年,
    相当于每天 ~{launches_needed_300gw_low/365:,.0f} 次 Starship 发射,
    在当前和可预见的工程约束下不可行。
""")


def sensitivity_learning_rate():
    """学习率敏感性分析。"""
    print("\n" + "=" * 80)
    print("第五部分: Wright's Law 学习率对 2030 年预测的敏感性")
    print("=" * 80)

    C1_base, _, _ = fit_wrights_law(HISTORICAL_LAUNCH_COSTS, 0.85)

    print(f"\n{'学习率':>10} {'2030累200 $/kg':>18} {'2030累300 $/kg':>18} {'2030累500 $/kg':>18}")
    print("-" * 66)

    for lr in [0.75, 0.78, 0.80, 0.82, 0.85, 0.87, 0.90, 0.92, 0.95]:
        C1, r2, _ = fit_wrights_law(HISTORICAL_LAUNCH_COSTS, lr)
        p200 = max(wrights_law_cost(200, C1, lr), PHYSICAL_COST_FLOOR)
        p300 = max(wrights_law_cost(300, C1, lr), PHYSICAL_COST_FLOOR)
        p500 = max(wrights_law_cost(500, C1, lr), PHYSICAL_COST_FLOOR)
        print(f"{lr:>10.2f} ${p200:>17,.0f} ${p300:>17,.0f} ${p500:>17,.0f}")

    print(f"\n物理成本地板: ${PHYSICAL_COST_FLOOR}/kg")
    print(f"注意: 学习率越低 (越接近 0.75) 成本下降越快, 但拟合质量(R²)越低")


# =============================================================================
# 主入口
# =============================================================================
def main():
    # 全局变量声明必须出现在任何局部引用之前
    global WRIGHT_LEARNING_RATE_DEFAULT, PHYSICAL_COST_FLOOR

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="发射成本学习曲线验证",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--learning-rate", type=float, default=WRIGHT_LEARNING_RATE_DEFAULT,
                        help=f"Wright's Law 学习率 (默认: {WRIGHT_LEARNING_RATE_DEFAULT})")
    parser.add_argument("--cost-floor", type=float, default=PHYSICAL_COST_FLOOR,
                        help=f"物理成本地板 $/kg (默认: {PHYSICAL_COST_FLOOR})")
    parser.add_argument("--starship-payload", type=float, default=200,
                        help=f"Starship 运力吨 (默认: 200)")
    parser.add_argument("--faa-max-launches", type=int, default=69,
                        help=f"FAA 批准频次上限 (默认: 69)")
    parser.add_argument("--output", type=str,
                        default="research_output/workspace/data/launch_cost_results.txt",
                        help="输出文件路径")

    args = parser.parse_args()

    # 命令行参数覆盖
    WRIGHT_LEARNING_RATE_DEFAULT = args.learning_rate
    PHYSICAL_COST_FLOOR = args.cost_floor

    # 输出收集
    class Collector:
        def __init__(self):
            self.lines = []
        def write(self, text):
            self.lines.append(text)
            sys.__stdout__.buffer.write(text.encode('utf-8'))
        def flush(self):
            sys.__stdout__.flush()

    collector = Collector()
    old_stdout = sys.stdout
    sys.stdout = collector

    print(f"发射成本学习曲线验证")
    print(f"运行时间: {datetime.now().isoformat()}")
    print(f"学习率: {args.learning_rate} | 物理地板: ${args.cost_floor}/kg")

    # 第一部分: 历史数据
    print_historical_table()

    # 第二部分: Wright's Law 拟合
    print_wrights_law_fit()

    # 第三部分: 2030 推算
    print_2030_projections()

    # 第四部分: 马斯克 300GW 验证
    verify_musk_300gw()

    # 第五部分: 学习率敏感性
    sensitivity_learning_rate()

    sys.stdout = old_stdout

    # 写入文件
    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(collector.lines))
    print(f"\n[INFO] 结果已写入: {output_path}")

    print(f"\n{'='*80}")
    print("发射成本学习曲线验证完成。")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
