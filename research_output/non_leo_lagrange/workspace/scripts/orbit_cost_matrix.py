#!/usr/bin/env python3
"""
M5: 跨轨道成本综合对比 (Cross-Orbit Cost Matrix)
==================================================
整合 M1-M4 结果，产出：
  - 各轨道 vs LEO 成本差异矩阵
  - 每轨道主要成本驱动因子
  - "可行性翻转"临界值分析（发射成本/辐射加固/散热密度/硬件寿命四参数）

数据来源: M1-M4 计算结果
"""

import os, sys, json, csv, math

# ============================================================
# 解析输出目录
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 加载 M1-M4 结果
# ============================================================

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_csv_to_dict(name, key_field="orbit"):
    path = os.path.join(DATA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row[key_field]: row for row in reader}


def main():
    print("=" * 72)
    print("M5: 跨轨道成本综合对比矩阵")
    print("=" * 72)

    # 加载各模型结果
    m1 = {r["orbit"]: r for r in load_json("m1_delta_v_cost.json")}
    m2 = {r["orbit"]: r for r in load_json("m2_radiation_dose.json")}
    m3_all = load_json("m3_thermal_balance.json")
    m4 = {r["orbit"]: r for r in load_json("m4_solar_power.json")}

    # M3 提取 350K 情景（更现实的工况）
    m3 = {}
    for r in m3_all:
        if r["T_panel_K"] == 350.0:
            m3[r["orbit"]] = r

    orbits = list(m1.keys())
    leo_key = "LEO (SSO 600km)"

    # ============================================================
    # Part A: 成本差异矩阵 (LEO = 1.00x)
    # ============================================================
    print(f"\n{'='*50}")
    print(f"  PART A: 各轨道 vs LEO 成本差异矩阵 (LEO = 1.00x 基准)")
    print(f"{'='*50}")

    leo_vals = {
        "launch_1mw": float(m1[leo_key]["launch_1mw_base_M"]),
        "thermal_area": float(m3[leo_key]["area_1mw_heat_m2"]),
        "pv_area": float(m4[leo_key]["pv_area_bol_m2"]),
        "storage_kwh": float(m4[leo_key]["storage_kwh"]),
        "threat_score": float(m2[leo_key]["threat_score_100"]),
        "lifetime_yr": float(m2[leo_key]["expected_lifetime_yr"]),
    }

    matrix = []
    for orbit in orbits:
        row = {"orbit": orbit}

        # 发射成本比
        launch_1mw = float(m1[orbit]["launch_1mw_base_M"])
        launch_vs_leo = launch_1mw / leo_vals["launch_1mw"]

        # 散热面积比
        th_area = float(m3[orbit]["area_1mw_heat_m2"])
        th_vs_leo = th_area / leo_vals["thermal_area"] if leo_vals["thermal_area"] > 0 else float("inf")

        # 光伏面积比
        pv_area = float(m4[orbit]["pv_area_bol_m2"])
        pv_vs_leo = pv_area / leo_vals["pv_area"]

        # 储能比
        storage = float(m4[orbit]["storage_kwh"])
        storage_vs_leo = storage / leo_vals["storage_kwh"] if leo_vals["storage_kwh"] > 0 else (0 if storage == 0 else float("inf"))

        # 辐射威胁比
        threat = float(m2[orbit]["threat_score_100"])
        threat_vs_leo = threat / leo_vals["threat_score"]

        # 寿命比
        lifetime = float(m2[orbit]["expected_lifetime_yr"]) if m2[orbit]["expected_lifetime_yr"] != ">1000" else 1000
        lifetime_vs_leo = lifetime / leo_vals["lifetime_yr"]

        # 综合成本指数 (加权平均)
        # 权重: 发射 30%, 散热 20%, 光伏 15%, 辐射 25%, 寿命 10%
        weights = {"launch": 0.30, "thermal": 0.20, "pv": 0.15, "rad": 0.25, "life": 0.10}

        # 对于"越大越优"的指标（寿命）取倒数
        composite = (
            weights["launch"] * launch_vs_leo
            + weights["thermal"] * th_vs_leo
            + weights["pv"] * pv_vs_leo
            + weights["rad"] * threat_vs_leo
            + weights["life"] * (1.0 / lifetime_vs_leo)
        )

        row.update({
            "launch_1mw_M": round(launch_1mw, 1),
            "launch_vs_leo": round(launch_vs_leo, 2),
            "thermal_area_m2": round(th_area, 0),
            "thermal_vs_leo": round(th_vs_leo, 2),
            "pv_area_m2": round(pv_area, 0),
            "pv_vs_leo": round(pv_vs_leo, 2),
            "storage_kwh": round(storage, 0),
            "storage_vs_leo": round(storage_vs_leo, 2) if storage_vs_leo != float("inf") else "inf",
            "threat_score": round(threat, 1),
            "threat_vs_leo": round(threat_vs_leo, 2),
            "lifetime_yr": round(lifetime, 1),
            "lifetime_vs_leo": round(lifetime_vs_leo, 2),
            "composite_index": round(composite, 3),
        })
        matrix.append(row)

    # 排序：综合指数低→高
    matrix.sort(key=lambda r: r["composite_index"])

    print(f"\n{'轨道':<22s} {'发射':>6s} {'散热':>6s} {'光伏':>6s} "
          f"{'储能':>6s} {'辐射':>6s} {'寿命':>6s} {'综合':>7s}")
    print("-" * 72)
    for r in matrix:
        print(f"{r['orbit']:<22s} {r['launch_vs_leo']:>5.2f}x "
              f"{r['thermal_vs_leo']:>5.2f}x {r['pv_vs_leo']:>5.2f}x "
              f"{str(r['storage_vs_leo']):>6s} {r['threat_vs_leo']:>5.2f}x "
              f"{r['lifetime_vs_leo']:>5.2f}x {r['composite_index']:>6.2f}")

    # ============================================================
    # Part B: 各轨道主要成本驱动因子
    # ============================================================
    print(f"\n{'='*50}")
    print(f"  PART B: 各轨道主要成本驱动因子分析")
    print(f"{'='*50}")

    driver_labels = ["launch_vs_leo", "thermal_vs_leo", "pv_vs_leo", "threat_vs_leo"]
    driver_names = {"launch_vs_leo": "发射成本", "thermal_vs_leo": "散热面积",
                    "pv_vs_leo": "光伏面积", "threat_vs_leo": "辐射威胁"}

    print(f"\n{'轨道':<22s} {'#1 驱动':>12s} {'值':>7s} {'#2 驱动':>12s} {'值':>7s}")
    print("-" * 66)
    for r in matrix:
        vals = [(k, r[k]) for k in driver_labels]
        vals.sort(key=lambda x: x[1], reverse=True)
        print(f"{r['orbit']:<22s} {driver_names[vals[0][0]]:>12s} "
              f"{vals[0][1]:>6.2f}x {driver_names[vals[1][0]]:>12s} {vals[1][1]:>6.2f}x")

    # ============================================================
    # Part C: "可行性翻转"临界值分析
    # ============================================================
    print(f"\n{'='*50}")
    print(f"  PART C: 可行性翻转临界值分析")
    print(f"{'='*50}")

    print(f"""
基于四参数（发射成本/辐射加固/散热密度/硬件寿命），分析各参数需改善到何种程度
才能使该轨道在综合成本上"翻转为优于 LEO"（综合指数 < 1.0）。

LEO 基准参数:
  发射成本: ${leo_vals['launch_1mw']:.1f}M / 1 MW
  散热面积: {leo_vals['thermal_area']:.0f} m² @ 350K
  光伏面积: {leo_vals['pv_area']:.0f} m²
  辐射威胁分: {leo_vals['threat_score']:.1f}/100
  硬件寿命: {leo_vals['lifetime_yr']:.1f} 年
""")

    # 对每个非 LEO 轨道，计算使其 composite_index ≈ 1.0 所需的参数改善
    for r in matrix:
        if r["orbit"] == leo_key:
            continue

        ci = r["composite_index"]
        if ci <= 1.0:
            print(f"  {r['orbit']}: 已优于或等于 LEO (综合指数={ci:.2f})")
            continue

        # 需改善的百分比
        improvement_needed = (ci - 1.0) / ci * 100

        print(f"  {r['orbit']} (综合指数={ci:.2f}):")
        print(f"    需综合改善 ~{improvement_needed:.0f}% 以翻转为优于 LEO")

        # 各维度的临界值
        if r["launch_vs_leo"] > 1.0:
            target_launch = leo_vals["launch_1mw"] / r["launch_vs_leo"] * ci
            print(f"    发射成本: 需从 ${r['launch_1mw_M']:.1f}M 降至 "
                  f"${leo_vals['launch_1mw']:.1f}M (LEO 水平) 以翻平")
        if r["threat_vs_leo"] > 1.0:
            target_threat = leo_vals["threat_score"]
            print(f"    辐射威胁: 需从 {r['threat_score']:.0f}/100 降至 "
                  f"{leo_vals['threat_score']:.0f}/100 (LEO 水平)")

    # ============================================================
    # Part D: 综合排名与推荐
    # ============================================================
    print(f"\n{'='*50}")
    print(f"  PART D: 综合排名")
    print(f"{'='*50}")

    print(f"\n{'排名':<5s} {'轨道':<22s} {'综合指数':>8s} {'评级':>6s}")
    print("-" * 46)
    for i, r in enumerate(matrix, 1):
        if r["composite_index"] < 1.2:
            grade = "A"
        elif r["composite_index"] < 1.8:
            grade = "B"
        elif r["composite_index"] < 3.0:
            grade = "C"
        else:
            grade = "D"
        print(f"{i:<5d} {r['orbit']:<22s} {r['composite_index']:>7.2f}  {grade:>5s}")

    # Extra: 非 LEO 最优
    non_leo_first = [r for r in matrix if r["orbit"] != leo_key][0]
    print(f"\n  非 LEO 最优轨道: {non_leo_first['orbit']} "
          f"(综合指数={non_leo_first['composite_index']:.2f})")

    # ============================================================
    # 保存结果
    # ============================================================
    csv_path = os.path.join(DATA_DIR, "m5_orbit_cost_matrix.csv")
    json_path = os.path.join(DATA_DIR, "m5_orbit_cost_matrix.json")

    matrix_fields = [
        "orbit", "launch_1mw_M", "launch_vs_leo", "thermal_area_m2", "thermal_vs_leo",
        "pv_area_m2", "pv_vs_leo", "storage_kwh", "storage_vs_leo",
        "threat_score", "threat_vs_leo", "lifetime_yr", "lifetime_vs_leo", "composite_index"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=matrix_fields)
        writer.writeheader()
        writer.writerows([{k: r[k] for k in matrix_fields} for r in matrix])

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(matrix, f, ensure_ascii=False, indent=2)

    print(f"\n[INFO] 结果已保存: {csv_path}")
    print(f"[INFO] 结果已保存: {json_path}")
    print("[INFO] M5 完成。")
    return matrix


if __name__ == "__main__":
    main()
