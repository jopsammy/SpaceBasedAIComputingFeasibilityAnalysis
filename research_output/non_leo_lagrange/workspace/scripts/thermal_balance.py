#!/usr/bin/env python3
"""
M3: 各轨道热平衡模型 (Thermal Balance Model)
==============================================
基于斯特藩-玻尔兹曼定律，代入各轨道实际热输入，计算：
  - 各轨道单位面积有效散热能力
  - 跨轨道对比表
  - 1 MW 算力所需散热面积

参数:
  - 太阳常数: 1,361 W/m² (全轨道相同)
  - 地球红外 / 反照: 按轨道变化
  - 食占比: 按轨道变化
  - ε = 0.85 (双面辐射), T_panel = 300-373K

数据来源: .trae/specs/research-non-leo-lagrange/current-note.md Phase 1
"""

import os, sys, json, csv

# ============================================================
# 解析输出目录
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 物理常数
# ============================================================
SIGMA = 5.670374419e-8          # 斯特藩-玻尔兹曼常数 W/(m²·K⁴)
SOLAR_CONSTANT = 1361.0         # W/m²
EMISSIVITY = 0.85               # 双面辐射 ε

# ============================================================
# 输入参数 (来源: Phase 1 note)
# ============================================================

# 热环境数据: {orbit: (Earth_IR, Earth_Albedo, eclipse_fraction, notes)}
THERMAL_DATA = {
    "LEO (SSO 600km)": {
        "earth_ir": 240.0,
        "earth_albedo": 480.0,
        "eclipse_fraction": 0.40,
        "solar_constant": SOLAR_CONSTANT,
        "note": "高 IR+反照，高频食，散热最受限",
    },
    "MEO (~20,200 km)": {
        "earth_ir": 14.0,
        "earth_albedo": 2.5,
        "eclipse_fraction": 0.05,
        "solar_constant": SOLAR_CONSTANT,
        "note": "IR/反照大幅衰减，低食",
    },
    "GEO (~35,786 km)": {
        "earth_ir": 5.0,
        "earth_albedo": 1.0,
        "eclipse_fraction": 0.02,  # 全年 <2% 时间在食中
        "solar_constant": SOLAR_CONSTANT,
        "note": "IR/反照可忽略，食极少",
    },
    "HEO (Molniya)": {
        "earth_ir": None,           # 变化: 远地点~4-5, 近地点~150-200
        "earth_albedo": None,
        "eclipse_fraction": 0.15,   # 中等（近地点穿越阴影）
        "solar_constant": SOLAR_CONSTANT,
        "note": "近地点高IR+反照，远地点可忽略。按近地点主导保守估计",
    },
    "地日 L1": {
        "earth_ir": 0.0,
        "earth_albedo": 0.0,
        "eclipse_fraction": 0.0,
        "solar_constant": SOLAR_CONSTANT,
        "note": "无地球IR/反照，连续日照",
    },
    "地日 L2": {
        "earth_ir": 0.0,
        "earth_albedo": 0.0,
        "eclipse_fraction": 0.0,
        "solar_constant": SOLAR_CONSTANT,
        "note": "无地球IR/反照，连续日照。JWST 实测: 热侧 85°C / 冷侧 -233°C",
    },
    "地月 L4/L5": {
        "earth_ir": 0.003,         # 384,400km 处 ~1/r² 衰减
        "earth_albedo": 0.001,
        "eclipse_fraction": 0.0,
        "solar_constant": SOLAR_CONSTANT,
        "note": "地球IR/反照可忽略，几乎无食",
    },
    "地月 L1": {
        "earth_ir": 0.01,
        "earth_albedo": 0.005,
        "eclipse_fraction": 0.02,
        "solar_constant": SOLAR_CONSTANT,
        "note": "月球+地球IR均大幅衰减",
    },
    "地月 L2": {
        "earth_ir": 0.005,
        "earth_albedo": 0.002,
        "eclipse_fraction": 0.02,
        "solar_constant": SOLAR_CONSTANT,
        "note": "月球+地球IR均大幅衰减",
    },
}

# HEO 的等效值: 按轨道时间加权平均
# 近地点~1-2h/圈 有 LEO 等效 IR/反照，远地点~10h/圈 可忽略
# 加权: 近地点 IR ~175, 反照 ~300 (低于 LEO 因高度~1000km)
HEO_EQUIV_IR = 175 * (2 / 12) + 5 * (10 / 12)   # ≈ 33.3 W/m²
HEO_EQUIV_ALBEDO = 300 * (2 / 12) + 1 * (10 / 12) # ≈ 50.8 W/m²

# ============================================================
# 计算函数
# ============================================================

def stefan_boltzmann_radiated_power(T, epsilon=EMISSIVITY):
    """斯特藩-玻尔兹曼辐射功率密度 P = εσT⁴"""
    return epsilon * SIGMA * T ** 4


def effective_cooling_capacity(orbit_data, T_panel, solar_absorptance=0.3):
    """
    计算单位面积有效散热能力 (W/m²)
    散热能力 = 辐射出的功率 - 吸收的功率

    散热器假设: 仅向深空一面散热（单面），另一面隔热。
    对于 LEO: 地球 IR 和反照会加热散热器面
    对于深空: 仅太阳方向加热，散热器可指向深空方向

    简化模型: 假设散热器指向深空方向，接收:
      - 太阳常数 × (1-日照占比) × 太阳能吸收率 ≈ 仅食时吸收少
      - 实际吸热 = solar × absorptance × sun_fraction + earth_ir + earth_albedo
    """
    sun_frac = 1.0 - orbit_data["eclipse_fraction"]

    # 散热器接收的热输入
    solar_input = SOLAR_CONSTANT * solar_absorptance * sun_frac
    earth_ir = orbit_data["earth_ir"] if orbit_data["earth_ir"] is not None else HEO_EQUIV_IR
    earth_albedo = orbit_data["earth_albedo"] if orbit_data["earth_albedo"] is not None else HEO_EQUIV_ALBEDO

    # 若是 HEO 特殊处理
    if orbit_data.get("_heo_ir") is not None:
        earth_ir = orbit_data["_heo_ir"]
    if orbit_data.get("_heo_albedo") is not None:
        earth_albedo = orbit_data["_heo_albedo"]

    total_heat_input = solar_input + earth_ir + earth_albedo

    # 散热器辐射出去的功率 (假设双面辐射，两面均向深空)
    # 实际设计中散热器通常为单面辐射，但此处按双面计算以接近实际
    radiated = 2 * stefan_boltzmann_radiated_power(T_panel, EMISSIVITY)

    net_cooling = radiated - total_heat_input
    return net_cooling, radiated, total_heat_input, solar_input, earth_ir, earth_albedo


def area_for_heat_load(heat_load_w, net_cooling_w_m2):
    """计算散发指定热负荷所需的散热面积"""
    if net_cooling_w_m2 <= 0:
        return float("inf")
    return heat_load_w / net_cooling_w_m2


def main():
    print("=" * 72)
    print("M3: 各轨道热平衡模型")
    print("=" * 72)

    # HEO 特殊值
    THERMAL_DATA["HEO (Molniya)"]["_heo_ir"] = HEO_EQUIV_IR
    THERMAL_DATA["HEO (Molniya)"]["_heo_albedo"] = HEO_EQUIV_ALBEDO

    # 两个面板温度情景
    T_scenarios = {
        "T=300K (27°C)": 300.0,
        "T=350K (77°C)": 350.0,
    }

    total_results = []

    for scenario_name, T_panel in T_scenarios.items():
        print(f"\n{'='*50}")
        print(f"  散热面板温度: {scenario_name}")
        print(f"{'='*50}")

        results = []
        for orbit, od in THERMAL_DATA.items():
            net_cool, rad, heat_in, solar_in, e_ir, e_alb = \
                effective_cooling_capacity(od, T_panel)

            # 1 MW 算力 → 假设 ~40% 效率 → 60% 作为废热 = 1.5 MW
            heat_per_mw_compute = 1e6 / 0.40 * 0.60  # 1.5 MW
            area_req = area_for_heat_load(heat_per_mw_compute, net_cool)

            results.append({
                "orbit": orbit,
                "T_panel_K": T_panel,
                "net_cooling_W_m2": round(net_cool, 1),
                "radiated_W_m2": round(rad, 1),
                "heat_input_W_m2": round(heat_in, 1),
                "solar_input_W_m2": round(solar_in, 1),
                "earth_ir_W_m2": round(e_ir, 1),
                "earth_albedo_W_m2": round(e_alb, 1),
                "area_1mw_heat_m2": round(area_req, 1) if area_req != float("inf") else "inf",
                "eclipse_fraction": od["eclipse_fraction"],
                "note": od["note"],
            })

        # 按散热能力排序 (高→低)
        results.sort(key=lambda r: r["net_cooling_W_m2"], reverse=True)

        print(f"\n{'轨道':<22s} {'散热能力':>9s} {'辐射':>8s} {'热输入':>8s} "
              f"{'IR':>7s} {'反照':>7s} {'面积/1MW':>10s}")
        print("-" * 78)
        for r in results:
            area_str = f"{r['area_1mw_heat_m2']:>9.0f}" if isinstance(r['area_1mw_heat_m2'], (int, float)) else "      inf"
            print(f"{r['orbit']:<22s} {r['net_cooling_W_m2']:>8.0f} W "
                  f"{r['radiated_W_m2']:>7.0f} "
                  f"{r['heat_input_W_m2']:>7.0f} "
                  f"{r['earth_ir_W_m2']:>6.0f} "
                  f"{r['earth_albedo_W_m2']:>6.0f} "
                  f"{area_str} m²")

        total_results.extend(results)

    # -------- 跨温度对比 --------
    print(f"\n{'='*50}")
    print(f"  散热能力跨温度对比")
    print(f"{'='*50}")

    orbits = list(THERMAL_DATA.keys())
    print(f"\n{'轨道':<22s} {'300K散热':>10s} {'350K散热':>10s} {'提升':>7s} "
          f"{'LEO比值300K':>11s}")
    print("-" * 68)
    leo_300k = None
    leo_350k = None
    for r in total_results:
        if r["orbit"] == "LEO (SSO 600km)" and r["T_panel_K"] == 300:
            leo_300k = r["net_cooling_W_m2"]
        if r["orbit"] == "LEO (SSO 600km)" and r["T_panel_K"] == 350:
            leo_350k = r["net_cooling_W_m2"]

    orbit_summary = {}
    for r in total_results:
        o = r["orbit"]
        if o not in orbit_summary:
            orbit_summary[o] = {}
        orbit_summary[o][int(r["T_panel_K"])] = r

    for orbit in orbits:
        r300 = orbit_summary[orbit][300]
        r350 = orbit_summary[orbit][350]
        ratio = r350["net_cooling_W_m2"] / r300["net_cooling_W_m2"]
        leo_ratio = r300["net_cooling_W_m2"] / leo_300k if leo_300k else 1
        print(f"{orbit:<22s} {r300['net_cooling_W_m2']:>9.0f} W "
              f"{r350['net_cooling_W_m2']:>9.0f} W "
              f"{ratio:>6.2f}x "
              f"{leo_ratio:>10.2f}x")

    print(f"\n假设: ε={EMISSIVITY}, 双面辐射, 太阳吸收率=0.3")
    print(f"斯特藩-玻尔兹曼常数 σ = {SIGMA:.4e} W/(m²·K⁴)")
    if leo_300k:
        print(f"LEO 300K 基准散热能力: {leo_300k:.0f} W/m²")

    # -------- 保存 --------
    csv_path = os.path.join(DATA_DIR, "m3_thermal_balance.csv")
    json_path = os.path.join(DATA_DIR, "m3_thermal_balance.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=total_results[0].keys())
        writer.writeheader()
        writer.writerows(total_results)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(total_results, f, ensure_ascii=False, indent=2)

    print(f"\n[INFO] 结果已保存: {csv_path}")
    print(f"[INFO] 结果已保存: {json_path}")
    print("[INFO] M3 完成。")
    return total_results


if __name__ == "__main__":
    main()
