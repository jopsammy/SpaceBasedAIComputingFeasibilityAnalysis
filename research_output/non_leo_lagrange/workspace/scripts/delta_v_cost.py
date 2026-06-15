#!/usr/bin/env python3
"""
M1: Delta-v 成本模型 (Delta-v Cost Model)
==========================================
基于 Phase 1 的 delta-v 数据，计算：
  - 各轨道 delta-v 预算表（地面→轨道、LEO→轨道）
  - 各轨道 $/kg 估算（按 delta-v 比例）
  - 部署 1 MW 算力到各轨道的发射成本
  - 相对 LEO 的成本倍数

数据来源: .trae/specs/research-non-leo-lagrange/current-note.md Phase 1
"""

import os, sys, json, csv
import math

# ============================================================
# 解析输出目录
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)  # workspace/
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 输入参数 (来源: Phase 1 note)
# ============================================================

# 各轨道 delta-v (km/s)
DV_GROUND_TO_ORBIT = {
    "LEO (SSO 600km)":     9.4,
    "MEO (~20,200 km)":    12.3,
    "GEO (~35,786 km)":    14.0,
    "HEO (Molniya)":       14.5,
    "地日 L1":             12.7,
    "地日 L2":             12.7,
    "地月 L4/L5":          13.1,
    "地月 L1":             12.8,
    "地月 L2":             13.0,
}

# LEO → 目标轨道 delta-v (km/s)
DV_LEO_TO_ORBIT = {
    "LEO (SSO 600km)":     0.0,
    "MEO (~20,200 km)":    3.6,
    "GEO (~35,786 km)":    3.9,
    "HEO (Molniya)":       5.1,
    "地日 L1":             3.3,
    "地日 L2":             3.3,
    "地月 L4/L5":          3.7,
    "地月 L1":             3.4,
    "地月 L2":             3.6,
}

# Starship LEO 基准成本
LEO_COST_BASE = 150.0          # $/kg (基准: $100-200 中值)
LEO_COST_LOW = 100.0           # 乐观
LEO_COST_HIGH = 200.0          # 保守
ELASTIC_LOW = 50.0             # 弹性下界
ELASTIC_HIGH = 500.0           # 弹性上界

# 1 MW 算力质量假设
# 假设: 每 kW 算力约 15-25 kg (含散热/电源/结构/屏蔽)
# 使用 20 kg/kW 作为基准，由此 1 MW = 20,000 kg
MASS_PER_KW = 20.0             # kg/kW
POWER_MW = 1.0                 # MW
PAYLOAD_MASS_KG = POWER_MW * 1000 * MASS_PER_KW  # 20,000 kg

# 站位保持 Δv (m/s/年)
STATION_KEEPING = {
    "LEO (SSO 600km)":     0.0,      # 大气阻力补偿，不计入发射成本
    "MEO (~20,200 km)":    0.0,      # MEO 稳定
    "GEO (~35,786 km)":    1.0,      # 南北站位保持
    "HEO (Molniya)":       0.0,
    "地日 L1":             3.0,      # 约 1-5 m/s/年，取中值 3
    "地日 L2":             3.0,      # 约 2-4 m/s/年，取中值 3
    "地月 L4/L5":          0.5,      # 理论上零，太阳摄动极小
    "地月 L1":             66.0,     # 传统 halo 12天周期
    "地月 L2":             28.0,     # 传统 halo 14天周期
}

# ============================================================
# 计算函数
# ============================================================

def calc_cost_per_kg(dv_ratio, leo_base):
    """按 delta-v 比例计算 $/kg，考虑非线性因素（火箭方程指数效应）"""
    # 简单线性比例，但为高 Δv 轨道加指数修正
    linear_cost = leo_base * dv_ratio
    # 对 Δv > 1.3x LEO 的情况加 ~5% 非线性修正
    if dv_ratio > 1.3:
        linear_cost *= (1 + 0.05 * (dv_ratio - 1.3) / 0.3)
    return linear_cost


def main():
    print("=" * 72)
    print("M1: Delta-v 成本模型")
    print("=" * 72)

    orbits = list(DV_GROUND_TO_ORBIT.keys())
    dv_leo = DV_GROUND_TO_ORBIT["LEO (SSO 600km)"]

    results = []
    for orbit in orbits:
        dv_ground = DV_GROUND_TO_ORBIT[orbit]
        dv_leo_to = DV_LEO_TO_ORBIT[orbit]
        dv_ratio = dv_ground / dv_leo
        sk = STATION_KEEPING.get(orbit, 0.0)

        # $/kg 三种情景
        cost_opt = calc_cost_per_kg(dv_ratio, LEO_COST_LOW)
        cost_base = calc_cost_per_kg(dv_ratio, LEO_COST_BASE)
        cost_con = calc_cost_per_kg(dv_ratio, LEO_COST_HIGH)

        # 部署 1 MW 发射成本
        launch_cost_base = cost_base * PAYLOAD_MASS_KG / 1e6  # $M
        launch_cost_range = (
            f"${cost_opt * PAYLOAD_MASS_KG / 1e6:.1f}M - "
            f"${cost_con * PAYLOAD_MASS_KG / 1e6:.1f}M"
        )

        # 10 年站位保持额外 Δv 成本（简化：按比例增加推进剂质量）
        # 假设 Isp=300s 化学推进，每年 Δv 需要推进剂质量比 exp(Δv/(g0*Isp))-1
        g0 = 9.80665
        isp = 300.0
        sk_total = sk * 10.0  # m/s over 10 years
        prop_mass_ratio = math.exp(sk_total / (g0 * isp)) - 1.0
        sk_extra_cost_base = cost_base * PAYLOAD_MASS_KG * prop_mass_ratio / 1e6  # $M

        results.append({
            "orbit": orbit,
            "dv_ground_km_s": dv_ground,
            "dv_leo_to_orbit_km_s": dv_leo_to,
            "dv_ratio_vs_leo": round(dv_ratio, 3),
            "cost_per_kg_base": round(cost_base, 1),
            "cost_per_kg_optimistic": round(cost_opt, 1),
            "cost_per_kg_conservative": round(cost_con, 1),
            "launch_1mw_base_M": round(launch_cost_base, 1),
            "launch_1mw_range": launch_cost_range,
            "station_keeping_m_s_yr": sk,
            "sk_extra_10yr_M": round(sk_extra_cost_base, 2),
            "total_1mw_10yr_base_M": round(launch_cost_base + sk_extra_cost_base, 1),
            "cost_multiplier_vs_leo": round(cost_base / LEO_COST_BASE, 2),
        })

    # -------- 输出到控制台 --------
    print(f"\n{'轨道':<22s} {'地面Δv':>8s} {'LEO→':>7s} {'Δv比':>6s} "
          f"{'$/kg基':>8s} {'1MW发射':>10s} {'成本倍':>7s}")
    print("-" * 72)
    for r in results:
        print(f"{r['orbit']:<22s} {r['dv_ground_km_s']:>7.1f} "
              f"{r['dv_leo_to_orbit_km_s']:>6.1f} {r['dv_ratio_vs_leo']:>5.2f}x "
              f"${r['cost_per_kg_base']:>6.0f} "
              f"${r['launch_1mw_base_M']:>7.1f}M "
              f"{r['cost_multiplier_vs_leo']:>6.2f}x")

    print(f"\n假设: 1 MW = {PAYLOAD_MASS_KG:,.0f} kg (按 {MASS_PER_KW:.0f} kg/kW)")
    print(f"LEO 基准 Starship: ${LEO_COST_LOW:.0f}-${LEO_COST_HIGH:.0f}/kg "
          f"(弹性区间 ${ELASTIC_LOW:.0f}-${ELASTIC_HIGH:.0f})")

    print(f"\n--- 含 10 年站位保持总成本 ---")
    print(f"{'轨道':<22s} {'发射':>9s} {'站位保持':>9s} {'合计10年':>10s}")
    print("-" * 54)
    for r in results:
        print(f"{r['orbit']:<22s} ${r['launch_1mw_base_M']:>7.1f}M "
              f"${r['sk_extra_10yr_M']:>7.2f}M "
              f"${r['total_1mw_10yr_base_M']:>8.1f}M")

    # -------- 保存结果 --------
    csv_path = os.path.join(DATA_DIR, "m1_delta_v_cost.csv")
    json_path = os.path.join(DATA_DIR, "m1_delta_v_cost.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[INFO] 结果已保存: {csv_path}")
    print(f"[INFO] 结果已保存: {json_path}")
    print("[INFO] M1 完成。")
    return results


if __name__ == "__main__":
    main()
