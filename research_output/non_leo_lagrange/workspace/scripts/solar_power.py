#!/usr/bin/env python3
"""
M4: 太阳能可用性模型 (Solar Power Availability Model)
======================================================
基于各轨道日照占比和光伏效率，计算：
  - 各轨道年有效发电小时数
  - 各轨道 1 MW 持续算力所需光伏面积
  - 储能需求（如有食周期）
  - 轨道太阳能 vs 地面光伏对比

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
# 输入参数
# ============================================================
SOLAR_CONSTANT = 1361.0          # W/m²
PV_EFFICIENCY = 0.30             # 空间级 GaAs 三结 30%
PV_DEGRADATION = 0.02            # 年均衰减 (2%/年 典型值，辐射环境更劣)
HOURS_PER_YEAR = 8766.0          # 小时/年

# 各轨道日照占比 (1 - eclipse_fraction)
# LEO 约 60% 日照; MEO 95%; GEO 98%; HEO 85%; L1/L2 100%; EM L4/L5 100%
SUNLIGHT_FRACTION = {
    "LEO (SSO 600km)":     0.60,   # 40% 食
    "MEO (~20,200 km)":    0.95,   # ~5% 食
    "GEO (~35,786 km)":    0.98,   # <2% 食
    "HEO (Molniya)":       0.85,   # ~15% 食
    "地日 L1":             1.00,   # 连续日照
    "地日 L2":             1.00,   # 连续日照
    "地月 L4/L5":          1.00,   # 几乎无食
    "地月 L1":             0.98,   # 偶尔食
    "地月 L2":             0.98,   # 偶尔食
}

# 典型食持续时间 (minutes) 和轨道周期
ECLIPSE_DATA = {
    "LEO (SSO 600km)":     {"duration_min": 36, "period_min": 90, "cycles_per_day": 16},
    "MEO (~20,200 km)":    {"duration_min": 0, "period_min": 720, "cycles_per_day": 2,
                             "note": "高β角可连续数周无食"},
    "GEO (~35,786 km)":    {"duration_min": 72, "period_min": 24*60, "cycles_per_day": 1,
                             "note": "仅在春/秋分，全年<2%时间"},
    "HEO (Molniya)":       {"duration_min": 60, "period_min": 720, "cycles_per_day": 2},
    "地日 L1":             {"duration_min": 0, "period_min": 0, "cycles_per_day": 0,
                             "note": "无食"},
    "地日 L2":             {"duration_min": 0, "period_min": 0, "cycles_per_day": 0,
                             "note": "无食"},
    "地月 L4/L5":          {"duration_min": 0, "period_min": 0, "cycles_per_day": 0,
                             "note": "几乎无食"},
    "地月 L1":             {"duration_min": 30, "period_min": 12*60, "cycles_per_day": 2,
                             "note": "月球阴影偶尔遮挡"},
    "地月 L2":             {"duration_min": 30, "period_min": 12*60, "cycles_per_day": 2,
                             "note": "月球阴影偶尔遮挡"},
}

# 地面光伏参考 (基准对比)
GROUND_PV_DATA = {
    "capacity_factor": 0.18,       # 全球平均 ~18%
    "peak_sun_hours_day": 5.0,     # 等效峰值日照小时/天
    "irradiance_peak": 1000.0,     # W/m² AM1.5 标准
    "efficiency": 0.22,            # 商业级单晶硅 22%
    "note": "地面光伏有昼夜+天气+大气衰减",
}

# 1 MW 持续算力功耗假设
COMPUTE_POWER_W = 1_000_000       # 1 MW
SYSTEM_OVERHEAD = 1.30            # 含散热/电源转换/通信 30% 开销
TOTAL_POWER_NEEDED = COMPUTE_POWER_W * SYSTEM_OVERHEAD  # 1.3 MW

# 电池储能效率
BATTERY_EFFICIENCY = 0.90         # 充放电效率
BATTERY_DOD = 0.80                # 放电深度
BATTERY_SPECIFIC_ENERGY = 250.0   # Wh/kg (锂离子空间级)


def main():
    print("=" * 72)
    print("M4: 太阳能可用性模型")
    print("=" * 72)

    orbits = list(SUNLIGHT_FRACTION.keys())

    results = []
    for orbit in orbits:
        sun_frac = SUNLIGHT_FRACTION[orbit]
        ecl = ECLIPSE_DATA[orbit]

        # 年等效日照小时
        sun_hours_per_year = sun_frac * HOURS_PER_YEAR

        # 光伏输出功率密度 (W/m²) = 太阳常数 × 效率 × 日照占比
        pv_output_density = SOLAR_CONSTANT * PV_EFFICIENCY * sun_frac

        # 考虑 5 年后衰减的等效输出
        pv_output_5yr = pv_output_density * (1 - PV_DEGRADATION) ** 5

        # 1 MW 持续算力所需光伏面积
        # 需要注意: 在食期间电池需要充电，因此光伏需额外功率充电
        if sun_frac < 1.0:
            # 光伏需在日照期间同时供电 + 充电
            charge_ratio = (1.0 / sun_frac)  # 充电因子
            pv_area_m2 = TOTAL_POWER_NEEDED * charge_ratio / pv_output_density
        else:
            pv_area_m2 = TOTAL_POWER_NEEDED / pv_output_density

        # 考虑衰减后的面积 (设计为寿命末期仍满足需求)
        pv_area_eol_m2 = TOTAL_POWER_NEEDED / pv_output_5yr if sun_frac > 0 else float("inf")
        if sun_frac < 1.0:
            charge_ratio_5yr = 1.0 / (sun_frac * (1 - PV_DEGRADATION) ** 5)
            pv_area_eol_m2 = TOTAL_POWER_NEEDED * charge_ratio_5yr / pv_output_density

        # 储能需求
        if ecl.get("duration_min", 0) > 0 and ecl.get("cycles_per_day", 0) > 0:
            # 最长连续食期间需储能供电
            eclipse_hours = ecl["duration_min"] / 60.0
            storage_kwh = TOTAL_POWER_NEEDED / 1000 * eclipse_hours / (BATTERY_EFFICIENCY * BATTERY_DOD)
            storage_mass_kg = storage_kwh * 1000 / BATTERY_SPECIFIC_ENERGY
        else:
            storage_kwh = 0.0
            storage_mass_kg = 0.0

        # vs 地面光伏
        ground_pv_output = GROUND_PV_DATA["irradiance_peak"] * GROUND_PV_DATA["efficiency"] * GROUND_PV_DATA["capacity_factor"]
        vs_ground_ratio = pv_output_density / ground_pv_output if ground_pv_output > 0 else float("inf")

        results.append({
            "orbit": orbit,
            "sunlight_fraction": sun_frac,
            "sun_hours_per_year": round(sun_hours_per_year, 0),
            "pv_output_density_W_m2": round(pv_output_density, 1),
            "pv_output_5yr_degraded_W_m2": round(pv_output_5yr, 1),
            "pv_area_bol_m2": round(pv_area_m2, 0),
            "pv_area_eol_m2": round(pv_area_eol_m2, 0) if pv_area_eol_m2 != float("inf") else "inf",
            "storage_kwh": round(storage_kwh, 1),
            "storage_mass_kg": round(storage_mass_kg, 0),
            "max_eclipse_min": ecl.get("duration_min", 0),
            "vs_ground_pv_ratio": round(vs_ground_ratio, 2),
            "orbit_note": ecl.get("note", ""),
        })

    # -------- 输出 --------
    print(f"\n{'轨道':<22s} {'日照%':>7s} {'年日照h':>8s} "
          f"{'PV密度':>8s} {'PV面积':>9s} {'储能kWh':>9s} {'储能kg':>9s} {'vs地面':>7s}")
    print("-" * 88)
    for r in results:
        area_str = f"{r['pv_area_bol_m2']:>8.0f}" if isinstance(r['pv_area_bol_m2'], (int, float)) else "     inf"
        print(f"{r['orbit']:<22s} {r['sunlight_fraction']:>6.0%} "
              f"{r['sun_hours_per_year']:>7.0f} h "
              f"{r['pv_output_density_W_m2']:>7.0f} W "
              f"{area_str} m² "
              f"{r['storage_kwh']:>8.0f} "
              f"{r['storage_mass_kg']:>8.0f} "
              f"{r['vs_ground_pv_ratio']:>6.1f}x")

    print(f"\n假设:")
    print(f"  光伏效率: {PV_EFFICIENCY*100:.0f}% (空间级 GaAs 三结)")
    print(f"  年均衰减: {PV_DEGRADATION*100:.0f}%/年")
    print(f"  系统开销: {SYSTEM_OVERHEAD*100-100:.0f}% (散热/电源/通信)")
    print(f"  1 MW 持续算力总功耗: {TOTAL_POWER_NEEDED/1e6:.2f} MW")
    print(f"  电池: 效率{BATTERY_EFFICIENCY*100:.0f}%, DoD{BATTERY_DOD*100:.0f}%, "
          f"能量密度{BATTERY_SPECIFIC_ENERGY:.0f} Wh/kg")
    print(f"  地面光伏参考: 容量系数{GROUND_PV_DATA['capacity_factor']*100:.0f}%, "
          f"效率{GROUND_PV_DATA['efficiency']*100:.0f}%")

    # 特别标注无食轨道
    no_eclipse = [r for r in results if r["storage_kwh"] == 0 and r["sunlight_fraction"] >= 0.99]
    print(f"\n--- 零储能需求轨道 (连续日照) ---")
    for r in no_eclipse:
        print(f"  {r['orbit']}: 无储能需求, PV面积 {r['pv_area_bol_m2']:.0f} m²")

    # -------- 保存 --------
    csv_path = os.path.join(DATA_DIR, "m4_solar_power.csv")
    json_path = os.path.join(DATA_DIR, "m4_solar_power.json")

    # 处理 inf 值
    clean_results = []
    for r in results:
        cr = dict(r)
        for k, v in cr.items():
            if v == float("inf"):
                cr[k] = "inf"
        clean_results.append(cr)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=clean_results[0].keys())
        writer.writeheader()
        writer.writerows(clean_results)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)

    print(f"\n[INFO] 结果已保存: {csv_path}")
    print(f"[INFO] 结果已保存: {json_path}")
    print("[INFO] M4 完成。")
    return results


if __name__ == "__main__":
    main()
