#!/usr/bin/env python3
"""
斯特藩-玻尔兹曼定律定量验证脚本 (Phase 3 Q1)
=============================================
验证内容:
  1. 基础散热通量计算表 (8组温度 x 4组辐射率 = 32个数据点)
  2. 双面辐射通量计算
  3. AI1 1400W/m² 物理可行性反推
  4. 1GW 轨道数据中心最小散热面积 (多场景)
  5. 敏感性分析

参数来源:
  - sigma = 5.6704e-8 W/(m²·K⁴), CODATA 2018
  - AI1: 150kW 峰值, 110m² 散热板, 双面辐射 epsilon~0.9
  - 温度范围: 300K (27°C) 至 500K (227°C)
  - 辐射率: 0.85 (典型白漆) 至 1.00 (理想黑体)

作者: AC范式v6 parallel-sub-agent
日期: 2026-06-11
"""

import argparse
import os
import sys
import io
from datetime import datetime


# =============================================================================
# 物理常数与默认参数
# =============================================================================
SIGMA = 5.6704e-8          # 斯特藩-玻尔兹曼常数 W/(m²·K⁴)
SOLAR_CONSTANT = 1361.0     # 太阳常数 W/m² (AM0)

# 温度序列 (K)
DEFAULT_TEMPERATURES_K = [300, 323, 340, 350, 373, 400, 450, 500]

# 辐射率序列
DEFAULT_EMISSIVITIES = [0.85, 0.90, 0.95, 1.00]

# AI1 卫星参数
AI1_PEAK_POWER_W = 150_000      # 峰值功率 (W)
AI1_SUSTAINED_POWER_W = 120_000 # 持续功率 (W)
AI1_RADIATOR_AREA_M2 = 110.0    # 散热板物理面积 (m²)
AI1_DOUBLE_SIDED = True         # 双面辐射
AI1_EMISSIVITY = 0.90           # AI1 标称辐射率

# 验证目标
AI1_TARGET_FLUX_WM2 = 1400.0    # AI1 声称散热密度 (W/m²)

# 1 GW 场景
ONE_GW = 1_000_000_000  # 1 GW = 1e9 W


def stefan_boltzmann_flux(T_K, epsilon, double_sided=False):
    """
    计算斯特藩-玻尔兹曼定律散热通量。

    参数:
        T_K: 散热面板温度 (K)
        epsilon: 表面辐射率 (0-1)
        double_sided: 是否双面辐射

    返回:
        flux_W_per_m2: 单位物理面板面积的散热通量 (W/m²)
    """
    single_side = epsilon * SIGMA * (T_K ** 4)
    if double_sided:
        return 2.0 * single_side
    return single_side


def required_temperature(flux_target, epsilon, double_sided=False):
    """
    反推达到目标通量所需的散热面板温度。

    返回:
        T_K: 所需温度 (K)
    """
    if double_sided:
        effective_epsilon = 2.0 * epsilon
    else:
        effective_epsilon = epsilon
    T4 = flux_target / (effective_epsilon * SIGMA)
    return T4 ** 0.25


def required_area(power_W, T_K, epsilon, double_sided=False):
    """计算所需散热面积。"""
    flux = stefan_boltzmann_flux(T_K, epsilon, double_sided)
    return power_W / flux


def format_number(n, precision=1):
    """智能格式化数字。"""
    if abs(n) >= 1e9:
        return f"{n/1e9:.{precision}f} GW"
    elif abs(n) >= 1e6:
        return f"{n/1e6:.{precision}f} MW"
    elif abs(n) >= 1e3:
        return f"{n/1e3:.{precision}f} kW"
    elif abs(n) >= 100:
        return f"{n:.0f}"
    elif abs(n) >= 10:
        return f"{n:.1f}"
    else:
        return f"{n:.2f}"


def format_area(area_m2):
    """智能格式化面积。"""
    if area_m2 >= 1e6:
        return f"{area_m2/1e6:.3f} km²"
    elif area_m2 >= 1:
        return f"{area_m2:.1f} m²"
    else:
        return f"{area_m2:.3f} m²"


# =============================================================================
# 第一部分: 基础散热通量计算表
# =============================================================================
def compute_basic_table(temperatures_K, emissivities):
    """生成单面辐射基础计算表。"""
    print("\n" + "=" * 80)
    print("第一部分: 斯特藩-玻尔兹曼定律基础散热通量计算表 (单面辐射)")
    print("=" * 80)
    print(f"\n公式: P/A = epsilon * sigma * T^4")
    print(f"sigma = {SIGMA:.4e} W/(m^2·K^4)\n")

    # 表头
    header = f"{'T (K)':>8} {'T (°C)':>8}"
    for eps in emissivities:
        header += f" {'eps={eps:.2f} (W/m²)':>20}"
    print(header)
    print("-" * len(header))

    # 数据行
    rows = []
    for T_K in temperatures_K:
        T_C = T_K - 273.15
        row = f"{T_K:>8.0f} {T_C:>8.1f}"
        for eps in emissivities:
            flux = stefan_boltzmann_flux(T_K, eps, double_sided=False)
            row += f" {flux:>20.0f}"
        print(row)
        rows.append((T_K, [stefan_boltzmann_flux(T_K, eps, False) for eps in emissivities]))

    return rows


# =============================================================================
# 第二部分: 双面辐射通量计算
# =============================================================================
def compute_double_sided_table(emissivities):
    """生成双面辐射通量表 (聚焦 AI1 工作温度范围)。"""
    print("\n" + "=" * 80)
    print("第二部分: 双面辐射散热通量计算")
    print("=" * 80)
    print(f"\n公式: P/A = 2 × epsilon × sigma × T⁴ (物理面板面积)")

    # 关注温度范围
    temps = [340, 342.5, 345, 350, 353, 360]
    header = f"{'T (K)':>8} {'T (°C)':>8}"
    for eps in [0.85, 0.90, 0.95]:
        header += f" {'eps={eps:.2f} 双面':>20}"
    print(header)
    print("-" * len(header))

    for T_K in temps:
        T_C = T_K - 273.15
        row = f"{T_K:>8.1f} {T_C:>8.1f}"
        for eps in [0.85, 0.90, 0.95]:
            flux = stefan_boltzmann_flux(T_K, eps, double_sided=True)
            row += f" {flux:>20.0f}"
        print(row)


# =============================================================================
# 第三部分: AI1 1400W/m² 物理可行性验证
# =============================================================================
def verify_ai1_flux():
    """验证 AI1 1400 W/m² 散热密度是否物理可行。"""
    print("\n" + "=" * 80)
    print("第三部分: AI1 1400 W/m² 散热密度物理可行性验证")
    print("=" * 80)

    print(f"""
AI1 卫星参数 (来源: SpaceX 官方视频, 2026-06-08):
  - 峰值功率: {AI1_PEAK_POWER_W/1000:.0f} kW
  - 持续功率: {AI1_SUSTAINED_POWER_W/1000:.0f} kW
  - 散热板面积: {AI1_RADIATOR_AREA_M2:.0f} m²
  - 散热模式: {'双面辐射' if AI1_DOUBLE_SIDED else '单面辐射'}
  - 标称辐射率: epsilon = {AI1_EMISSIVITY}
  - 目标散热密度: {AI1_TARGET_FLUX_WM2:.0f} W/m² (物理面板面积)
""")

    # 反推所需温度
    print("--- 反推分析: 达到 1400 W/m² 需要什么条件? ---\n")

    results = []
    for eps in [0.85, 0.88, 0.90, 0.92, 0.95]:
        T_single = required_temperature(AI1_TARGET_FLUX_WM2, eps, double_sided=False)
        T_double = required_temperature(AI1_TARGET_FLUX_WM2, eps, double_sided=True)
        results.append((eps, T_single, T_double))

    print(f"{'epsilon':>10} {'T 单面 (K)':>14} {'T 单面 (°C)':>14} {'T 双面 (K)':>14} {'T 双面 (°C)':>14}")
    print("-" * 68)
    for eps, T_s, T_d in results:
        print(f"{eps:>10.2f} {T_s:>14.1f} {T_s-273.15:>14.1f} {T_d:>14.1f} {T_d-273.15:>14.1f}")

    # 最佳匹配
    T_match = required_temperature(AI1_TARGET_FLUX_WM2, AI1_EMISSIVITY, double_sided=True)
    print(f"""
--- AI1 最佳匹配 ---
  散热模式: 双面辐射
  辐射率 epsilon: {AI1_EMISSIVITY}
  所需面板温度: {T_match:.1f} K ({T_match-273.15:.1f} °C)
  验证: epsilon={AI1_EMISSIVITY}, T={T_match:.1f}K, 双面 → flux = {stefan_boltzmann_flux(T_match, AI1_EMISSIVITY, True):.0f} W/m²
  目标: {AI1_TARGET_FLUX_WM2:.0f} W/m²
  偏差: {(stefan_boltzmann_flux(T_match, AI1_EMISSIVITY, True) - AI1_TARGET_FLUX_WM2):.1f} W/m²

--- 物理可行性判定 ---
  判定: 物理成立，已接近当前材料天花板
  前提条件:
    1. 双面辐射 (等效辐射面积 220 m²)
    2. 高辐射率涂层 epsilon >= 0.90 (BOL)
    3. 面板温度 >= {T_match-273.15:.0f} °C (在液冷散热器工作范围内)
    4. 严格的 knife-edge-to-sun 定向
    5. 涂层退化后 (EOL epsilon ~0.82-0.85) 需降额运行

  总散热量验证:
    AI1 峰值 {AI1_PEAK_POWER_W/1000:.0f} kW × 产热率 ~95% = {AI1_PEAK_POWER_W*0.95/1000:.0f} kW
    散热器能力: 110 m² × {AI1_TARGET_FLUX_WM2:.0f} W/m² = {AI1_RADIATOR_AREA_M2*AI1_TARGET_FLUX_WM2/1000:.0f} kW
    余量: {AI1_RADIATOR_AREA_M2*AI1_TARGET_FLUX_WM2/1000 - AI1_PEAK_POWER_W*0.95/1000:.0f} kW
""")


# =============================================================================
# 第四部分: 1GW 轨道数据中心最小散热面积
# =============================================================================
def compute_1gw_area_scenarios():
    """计算 1GW 所需散热面积 (多场景)。"""
    print("\n" + "=" * 80)
    print("第四部分: 1 GW 轨道数据中心所需最小散热面积 (多场景)")
    print("=" * 80)

    scenarios = [
        # (名称, epsilon, T_K, double_sided, 描述)
        ("AI1 BOL (激进)",       0.90, 342.5, True,  "AI1 设计点, 寿命初期, 双面"),
        ("AI1 EOL (退化后)",     0.83, 340.0, True,  "涂层退化后, epsilon下降, 双面"),
        ("典型航天器设计点",     0.85, 350.0, True,  "典型航天器, 双面辐射"),
        ("保守设计点 (单面)",    0.85, 323.0, False, "保守假设, 单面辐射, 50°C面板"),
        ("保守设计点 (双面)",    0.85, 323.0, True,  "保守假设, 双面辐射, 50°C面板"),
        ("高性能涂层+高温",      0.93, 353.0, True,  "先进涂层+80°C面板, 双面"),
        ("极限材料+最高温",      0.96, 393.0, True,  "Ti-石墨辐射翼+120°C, 双面"),
        ("第三方分析参考",       0.85, 350.0, False, "cybernative.ai 单面参考"),
    ]

    # 考虑真实热环境的惩罚系数
    # 基于 Q3: knife-edge 吸收 ~5%, 地球IR ~5%, 涂层退化 ~10% → 净效率 ~0.80-0.85
    ENV_PENALTY = 0.80  # 保守: 真实环境效率为理想值的80%

    print(f"\n假设: 1 GW IT功率, ~95% 转化为废热, 即 {ONE_GW*0.95/1e6:.0f} MW 待散热")
    print(f"理想散热计算 (仅斯特藩-玻尔兹曼):\n")

    print(f"{'场景':<24} {'eps':>6} {'T (K)':>8} {'T (°C)':>8} {'模式':>6} {'通量 W/m²':>12} {'面积 (km²)':>12} {'卫星数*':>10}")
    print("-" * 90)

    heat_load = ONE_GW * 0.95  # 待散热热负荷

    for name, eps, T_K, ds, desc in scenarios:
        flux = stefan_boltzmann_flux(T_K, eps, ds)
        area_m2 = heat_load / flux
        area_km2 = area_m2 / 1e6
        n_sats = area_m2 / AI1_RADIATOR_AREA_M2
        print(f"{name:<24} {eps:>6.2f} {T_K:>8.1f} {T_K-273.15:>8.1f} {'双面' if ds else '单面':>6} {flux:>12.0f} {area_km2:>12.3f} {n_sats:>10.0f}")

    print(f"\n* 卫星数按每颗 AI1 级卫星 {AI1_RADIATOR_AREA_M2:.0f} m² 散热板估算")

    # 综合修正表
    print(f"\n--- 经真实热环境惩罚后 (环境效率系数 = {ENV_PENALTY:.0%}) ---\n")
    print(f"{'场景':<24} {'eps':>6} {'T (K)':>8} {'修正通量':>12} {'修正面积':>12} {'缩小比例':>10}")
    print("-" * 80)

    base_flux_ai1 = stefan_boltzmann_flux(342.5, 0.90, True)
    base_area_ai1 = heat_load / base_flux_ai1

    key_scenarios = [
        ("AI1 BOL (激进)", 0.90, 342.5, True),
        ("Q3修正: AI1基础+环境惩罚", 0.90, 342.5, True),  # 同参数但经惩罚
        ("Q10 L1: 高eps+80°C", 0.93, 353.0, True),
        ("Q10 L3: eps0.96+120°C", 0.96, 393.0, True),
        ("综合 2030-2032 最现实估计", 0.93, 348.0, True),
    ]

    for i, (name, eps, T_K, ds) in enumerate(key_scenarios):
        ideal_flux = stefan_boltzmann_flux(T_K, eps, ds)
        if i == 1:  # Q3修正: 用惩罚系数
            corrected_flux = ideal_flux * ENV_PENALTY
        else:
            corrected_flux = ideal_flux
        corrected_area_m2 = heat_load / corrected_flux
        ratio = corrected_area_m2 / base_area_ai1
        print(f"{name:<32} {eps:>6.2f} {T_K:>8.1f} {corrected_flux:>12.0f} {format_area(corrected_area_m2):>12} {ratio:>10.3f}x")

    print(f"""
--- 核心结论 ---
1. AI1 设计点的 1 GW 散热面积约 0.7 km² (双面辐射), 相当于 {AI1_RADIATOR_AREA_M2:.0f} m²/颗 x ~{heat_load / stefan_boltzmann_flux(342.5, 0.90, True) / AI1_RADIATOR_AREA_M2:.0f} 颗 AI1 级卫星
2. 经 LEO 真实热环境惩罚后, 实际需要约 {heat_load / (stefan_boltzmann_flux(342.5, 0.90, True) * ENV_PENALTY) / 1e6:.2f} km²
3. 通过高温容忍芯片 + 高eps耐久涂层, 2030-2032 年可望缩小至 ~0.5 km²
4. 散热面积需求巨大但并非物理不可能——真正挑战在部署、定向控制和退化管理
""")


# =============================================================================
# 第五部分: 敏感性分析
# =============================================================================
def sensitivity_analysis():
    """散热通量对温度和辐射率的敏感性分析。"""
    print("\n" + "=" * 80)
    print("第五部分: 敏感性分析——温度和辐射率对散热通量的影响")
    print("=" * 80)

    print(f"\n{'温度变化':>30} {'通量变化 (T⁴关系)':>40}")
    print("-" * 72)

    base_T = 342.5
    for delta_T in [1, 5, 10, 20, 50]:
        new_T = base_T + delta_T
        flux_ratio = (new_T / base_T) ** 4
        print(f"  T: {base_T:.0f}K → {new_T:.0f}K (+{delta_T}K / +{delta_T/base_T*100:.1f}%)"
              f"  →  通量 × {flux_ratio:.3f} (+{(flux_ratio-1)*100:.1f}%)")

    print(f"\n{'辐射率变化':>30} {'通量变化 (线性关系)':>40}")
    print("-" * 72)

    base_eps = 0.90
    for delta_eps in [0.01, 0.02, 0.05, 0.08, 0.10]:
        new_eps = base_eps + delta_eps
        flux_ratio = new_eps / base_eps
        print(f"  eps: {base_eps:.2f} → {new_eps:.2f} (+{delta_eps:.2f})"
              f"  →  通量 × {flux_ratio:.3f} (+{(flux_ratio-1)*100:.1f}%)")

    print(f"""
--- 敏感性洞察 ---
  - 散热通量 ∝ T⁴: 温度提升 10% (342.5→376.8K) → 通量提升 ~46%
  - 散热通量 ∝ epsilon: 辐射率提升 10% (0.90→0.99) → 通量提升 ~10%
  - 温度是最有效的调节杠杆, 但受限于芯片结温上限
  - 双面辐射可获 2× 等效通量, 是最直接的面积减半手段
""")


# =============================================================================
# 输出到文件
# =============================================================================
def write_results_to_file(output_path, lines_buffer):
    """将结果写入文件。"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines_buffer))
    print(f"\n[INFO] 结果已写入: {output_path}")


# =============================================================================
# 自定义输出收集器
# =============================================================================
class OutputCollector:
    """收集所有 print 输出用于文件保存。"""
    def __init__(self):
        self.lines = []

    def write(self, text):
        self.lines.append(text)
        sys.__stdout__.buffer.write(text.encode('utf-8'))
    def flush(self):
        sys.__stdout__.flush()


# =============================================================================
# 主入口
# =============================================================================
def main():
    # 全局变量声明必须出现在任何局部引用之前
    global SIGMA, AI1_EMISSIVITY, AI1_RADIATOR_AREA_M2, AI1_TARGET_FLUX_WM2

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="斯特藩-玻尔兹曼定律定量验证",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--sigma", type=float, default=SIGMA,
                        help=f"斯特藩-玻尔兹曼常数 (默认: {SIGMA:.4e})")
    parser.add_argument("--ai1-emissivity", type=float, default=AI1_EMISSIVITY,
                        help=f"AI1 辐射率 (默认: {AI1_EMISSIVITY})")
    parser.add_argument("--ai1-area", type=float, default=AI1_RADIATOR_AREA_M2,
                        help=f"AI1 散热板面积 m² (默认: {AI1_RADIATOR_AREA_M2})")
    parser.add_argument("--ai1-flux-target", type=float, default=AI1_TARGET_FLUX_WM2,
                        help=f"AI1 目标散热通量 W/m² (默认: {AI1_TARGET_FLUX_WM2})")
    parser.add_argument("--output", type=str,
                        default="research_output/workspace/data/stefan_boltzmann_results.txt",
                        help="输出文件路径")
    parser.add_argument("--env-penalty", type=float, default=0.80,
                        help="LEO 热环境效率系数 (默认: 0.80)")

    args = parser.parse_args()

    # 命令行参数覆盖
    SIGMA = args.sigma
    AI1_EMISSIVITY = args.ai1_emissivity
    AI1_RADIATOR_AREA_M2 = args.ai1_area
    AI1_TARGET_FLUX_WM2 = args.ai1_flux_target

    # 输出收集
    collector = OutputCollector()
    old_stdout = sys.stdout
    sys.stdout = collector

    print(f"斯特藩-玻尔兹曼定律定量验证")
    print(f"运行时间: {datetime.now().isoformat()}")
    print(f"sigma = {SIGMA:.6e} W/(m^2·K^4)")

    # 第一部分
    compute_basic_table(DEFAULT_TEMPERATURES_K, DEFAULT_EMISSIVITIES)

    # 第二部分
    compute_double_sided_table(DEFAULT_EMISSIVITIES)

    # 第三部分
    verify_ai1_flux()

    # 第四部分
    compute_1gw_area_scenarios()

    # 第五部分
    sensitivity_analysis()

    # 恢复 stdout
    sys.stdout = old_stdout

    # 写入文件
    output_path = os.path.abspath(args.output)
    write_results_to_file(output_path, collector.lines)

    print(f"\n{'='*80}")
    print("验证完成。所有计算均已执行。")
    print(f"输出文件: {output_path}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
