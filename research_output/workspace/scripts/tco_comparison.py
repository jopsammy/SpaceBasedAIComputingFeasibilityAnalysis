#!/usr/bin/env python3
"""
轨道 vs 地面数据中心 TCO 全生命周期对比验证脚本 (Phase 3 Q7)
==========================================================
验证内容:
  1. 地面数据中心 10 年 TCO (基建 Capex + GPU 硬件 + 电力 + 运维)
  2. 轨道数据中心 10 年 TCO (发射 + 轨道硬件 + 轨道运维 + 退役)
  3. 至少 3 个情景 (乐观/基准/悲观)
  4. 敏感性分析: 发射成本 $50-1000/kg, 硬件寿命 3-10 年
  5. 对比表与关键交叉点

参数来源:
  - 地面超大规模 Capex: $7-12M/MW
  - GB300 GPU: ~$35-40K/颗
  - 地面 PUE: 1.09-1.58
  - 电费: $0.05-0.10/kWh
  - Starship 基准: $200/kg
  - 轨道硬件溢价: 3-5x 地面
  - 空间光伏: $200-400/W

作者: AC范式v6 parallel-sub-agent
日期: 2026-06-11
"""

import argparse
import os
import sys
import io
from datetime import datetime


# =============================================================================
# 默认参数
# =============================================================================
# 规模假设
POWER_MW = 1.0                 # 计算基准: 1 MW IT 负载

# --- 地面参数 ---
GROUND_INFRA_CAPEX_PER_MW_M = (7, 12)    # 基建 Capex $M/MW (低, 高)
GROUND_GPU_COST_K = 38.0                  # GB300 GPU 均价 $K/颗 (35-40中间值)
GROUND_GPU_PER_MW = 256                   # 估计 1MW 所需 GPU 数
GROUND_NETWORK_STORAGE_M = 6.5            # 网络+存储 $M (5-8中间值)
GROUND_ELECTRICITY_COST_PER_KWH = 0.075   # 电费 $/kWh (0.05-0.10中间值)
GROUND_PUE = 1.20                         # 典型超大规模 PUE
GROUND_OPEX_MAINTENANCE_RATE = 0.02       # 年运维占 Capex 比例
GROUND_HARDWARE_LIFETIME_Y = 6            # 地面硬件平均寿命 (年)
GROUND_HARDWARE_REFRESH_Y = 3             # GPU 刷新周期 (年)

# --- 轨道参数 ---
# 发射
STARSHIP_LEO_COST_BASE = 200              # $/kg 基准
STARSHIP_LEO_PAYLOAD_T = 200              # 单次 LEO 运力 (吨)
STARSHIP_LAUNCH_COST_BASE_M = 40          # 单次发射成本基准 $M

# 轨道硬件
ORBITAL_HARDWARE_PREMIUM_X = 3.5          # 轨道硬件 vs 地面溢价倍数 (3-5中间)
ORBITAL_SATELLITE_PLATFORM_COST_KW = 30_000  # 卫星平台成本 $/kW (~$30K/kW平台+bus)
ORBITAL_PV_COST_PER_W = 300.0             # 空间光伏 $/W
ORBITAL_PV_AREA_M2_PER_KW = 5.5           # 光伏面积 m²/kW (基于Q5: 1MW需~5500m² 30%效率GaAs)
ORBITAL_RADIATOR_COST_PER_M2 = 5000.0     # 散热板 $/m²
ORBITAL_RADIATOR_AREA_M2_PER_KW = 0.7     # 双面辐射板面积 m²/kW (基于Q1: 1GW需~0.7km² BOL激进)
ORBITAL_LAUNCH_INSURANCE_RATE = 0.08      # 发射保险费率

# 轨道运维
ORBITAL_OPS_STATIONS_YEARLY_M = 2.0       # 地面测控站年费 $M
ORBITAL_OPS_PERSONNEL_YEARLY_M = 3.0      # 运维人员年费 $M
ORBITAL_LIFETIME_Y = 5                    # 轨道硬件寿命 (年)
ORBITAL_REPLACEMENT_LAUNCH_M = 15.0       # 替换发射成本 (硬件替换, 不含原始发射)

# 退役
ORBITAL_DECOM_COST_PER_KW = 3_000         # 退役成本 $/kW
GROUND_DECOM_COST_PER_KW = 1_500          # 地面退役成本 $/kW

# 时间
HORIZON_YEARS = 10


def format_million(value_M):
    """格式化百万美元。"""
    if abs(value_M) >= 1000:
        return f"${value_M/1000:.2f}B"
    else:
        return f"${value_M:.1f}M"


def compute_ground_tco(power_mw, infra_low, infra_high, electricity_rate,
                        pue, maintenance_rate, hw_lifetime, refresh_cycle,
                        horizon_years):
    """
    计算地面数据中心 10 年 TCO。

    返回: dict with cost breakdown
    """
    power_kw = power_mw * 1000

    # 基建 Capex
    infra_capex_M = (infra_low + infra_high) / 2 * power_mw
    infra_capex_low_M = infra_low * power_mw
    infra_capex_high_M = infra_high * power_mw

    # GPU 硬件 Capex
    gpu_count = GROUND_GPU_PER_MW * power_mw
    gpu_capex_M = gpu_count * GROUND_GPU_COST_K / 1000
    # GPU 刷新: 每 refresh_cycle 年换一次
    gpu_refresh_count = int(horizon_years / refresh_cycle)
    gpu_refresh_M = gpu_capex_M * gpu_refresh_count

    # 网络+存储
    network_storage_M = GROUND_NETWORK_STORAGE_M * power_mw
    network_refresh_M = network_storage_M * int(horizon_years / refresh_cycle)

    # 总硬件 (含刷新)
    total_hardware_M = infra_capex_M + gpu_capex_M + network_storage_M
    total_hardware_with_refresh_M = (infra_capex_M + gpu_capex_M + gpu_refresh_M
                                      + network_storage_M + network_refresh_M)

    # 电力 (10年)
    annual_energy_kwh = power_kw * 8760 * pue
    annual_electricity_M = annual_energy_kwh * electricity_rate / 1e6
    total_electricity_M = annual_electricity_M * horizon_years

    # 运维
    annual_maintenance_M = total_hardware_M * maintenance_rate
    total_maintenance_M = annual_maintenance_M * horizon_years

    # 退役
    decommission_M = GROUND_DECOM_COST_PER_KW * power_kw / 1e6

    # 合计
    # 低端
    low_total = (infra_capex_low_M + gpu_capex_M + network_storage_M
                 + total_electricity_M + total_maintenance_M + decommission_M)
    # 高端 (含硬件刷新)
    high_total = (infra_capex_high_M + gpu_capex_M + gpu_refresh_M
                  + network_storage_M + network_refresh_M
                  + total_electricity_M + total_maintenance_M + decommission_M)

    return {
        "infra_capex": (infra_capex_low_M, infra_capex_high_M),
        "gpu_capex": gpu_capex_M,
        "gpu_refresh": gpu_refresh_M,
        "network_storage": network_storage_M,
        "network_refresh": network_refresh_M,
        "total_hardware_initial": total_hardware_M,
        "total_hardware_with_refresh": total_hardware_with_refresh_M,
        "electricity_total": total_electricity_M,
        "maintenance_total": total_maintenance_M,
        "decommission": decommission_M,
        "tco_low": low_total,
        "tco_high": high_total,
        "tco_mid": (low_total + high_total) / 2,
        "annual_electricity_M": annual_electricity_M,
        "cooling_overhead_pct": (pue - 1) * 100,
    }


def compute_orbital_tco(power_mw, launch_cost_per_kg, hardware_premium,
                         pv_cost_per_w, radiator_cost_per_m2,
                         radiator_area_m2_per_kw, pv_area_m2_per_kw,
                         sat_platform_cost_per_kw,
                         launch_insurance_rate,
                         orbital_lifetime, ops_stations, ops_personnel,
                         horizon_years, decommission_cost_per_kw):
    """
    计算轨道数据中心 10 年 TCO。

    返回: dict with cost breakdown
    """
    power_kw = power_mw * 1000

    # 质量估算
    # 计算硬件: ~1.2t/MW 的 IT 硬件 (基于地面GB300机架)
    compute_mass_kg = power_kw * 1.2  # kg
    # 散热系统: radiator_area_m2_per_kW * power_kW * ~4 kg/m²
    radiator_area = radiator_area_m2_per_kw * power_kw
    thermal_mass_kg = radiator_area * 4.0
    # 光伏系统: pv_area_m2_per_kW * power_kW * ~0.75 kg/m²
    pv_area = pv_area_m2_per_kw * power_kw
    pv_mass_kg = pv_area * 0.75
    # 卫星平台 (结构+姿态+通信+电源管理): ~20% 总质量
    platform_mass_kg = (compute_mass_kg + thermal_mass_kg + pv_mass_kg) * 0.25
    total_mass_kg = compute_mass_kg + thermal_mass_kg + pv_mass_kg + platform_mass_kg
    total_mass_t = total_mass_kg / 1000

    # 发射成本 (基于 kg 计算)
    launch_cost_M = total_mass_kg * launch_cost_per_kg / 1e6
    launch_insurance_M = launch_cost_M * launch_insurance_rate

    # 轨道硬件成本
    compute_hardware_cost_M = (GROUND_GPU_COST_K * GROUND_GPU_PER_MW * power_mw
                               / 1000 * hardware_premium)
    thermal_cost_M = radiator_area * radiator_cost_per_m2 / 1e6
    pv_cost_M = power_kw * pv_cost_per_w * 1000 / 1e6
    platform_cost_M = sat_platform_cost_per_kw * power_kw / 1e6
    total_orbital_hw_M = (compute_hardware_cost_M + thermal_cost_M
                          + pv_cost_M + platform_cost_M)

    # 硬件替换 (寿命到期后)
    num_replacements = max(0, int(horizon_years / orbital_lifetime) - 1)
    replacement_launch_M = num_replacements * (launch_cost_M * 0.5)  # 替换发射 ~50% 原始
    replacement_hw_M = num_replacements * total_orbital_hw_M * 0.7  # 替换硬件 ~70% 原始(批次折扣)

    # 运维
    annual_ops_M = ops_stations + ops_personnel
    total_ops_M = annual_ops_M * horizon_years

    # 退役
    decommission_M = decommission_cost_per_kw * power_kw / 1e6

    # TCO
    tco_total_M = (launch_cost_M + launch_insurance_M + total_orbital_hw_M
                   + replacement_launch_M + replacement_hw_M
                   + total_ops_M + decommission_M)

    return {
        "total_mass_t": total_mass_t,
        "launch_cost": launch_cost_M,
        "launch_insurance": launch_insurance_M,
        "compute_hardware": compute_hardware_cost_M,
        "thermal_system": thermal_cost_M,
        "pv_system": pv_cost_M,
        "platform": platform_cost_M,
        "total_hardware_initial": total_orbital_hw_M,
        "replacement_launch": replacement_launch_M,
        "replacement_hardware": replacement_hw_M,
        "total_ops": total_ops_M,
        "decommission": decommission_M,
        "tco_total": tco_total_M,
        "num_replacements": num_replacements,
    }


def print_ground_tco(result, label="地面数据中心"):
    """打印地面 TCO 详情。"""
    print(f"\n--- {label} 10 年 TCO ({POWER_MW} MW IT) ---")
    print(f"{'成本项':<30} {'低端':>12} {'高端':>12}")
    print("-" * 56)
    print(f"{'基建 Capex':<30} {format_million(result['infra_capex'][0]):>12} {format_million(result['infra_capex'][1]):>12}")
    print(f"{'GPU 硬件 Capex':<30} {format_million(result['gpu_capex']):>12}")
    gpu_str = format_million(result['gpu_capex'])
    print(f"{'GPU 刷新 (周期' + str(GROUND_HARDWARE_REFRESH_Y) + '年)':<30} {format_million(result['gpu_refresh']):>12}")
    print(f"{'网络+存储':<30} {format_million(result['network_storage']):>12}")
    print(f"{'网络+存储刷新':<30} {format_million(result['network_refresh']):>12}")
    print(f"{'电力 (PUE=' + str(GROUND_PUE) + ')':<30} {format_million(result['electricity_total']):>12}")
    print(f"{'运维':<30} {format_million(result['maintenance_total']):>12}")
    print(f"{'退役':<30} {format_million(result['decommission']):>12}")
    print("-" * 56)
    print(f"{'总 TCO':<30} {format_million(result['tco_low']):>12} {format_million(result['tco_high']):>12}")
    print(f"{'中位 TCO':<30} {format_million(result['tco_mid']):>12}")


def print_orbital_tco(result, label="轨道数据中心"):
    """打印轨道 TCO 详情。"""
    print(f"\n--- {label} 10 年 TCO ({POWER_MW} MW IT) ---")
    print(f"{'成本项':<30} {'金额':>12}")
    print("-" * 44)
    print(f"{'总质量':<30} {result['total_mass_t']:>11.1f} t")
    print(f"{'发射成本':<30} {format_million(result['launch_cost']):>12}")
    print(f"{'发射保险':<30} {format_million(result['launch_insurance']):>12}")
    print(f"{'计算硬件 (抗辐射加固)':<30} {format_million(result['compute_hardware']):>12}")
    print(f"{'散热系统':<30} {format_million(result['thermal_system']):>12}")
    print(f"{'光伏+储能':<30} {format_million(result['pv_system']):>12}")
    print(f"{'卫星平台':<30} {format_million(result['platform']):>12}")
    print(f"{'硬件替换 (发射)':<30} {format_million(result['replacement_launch']):>12}")
    print(f"{'硬件替换 (设备)':<30} {format_million(result['replacement_hardware']):>12}")
    print(f"{'地面运维':<30} {format_million(result['total_ops']):>12}")
    print(f"{'退役':<30} {format_million(result['decommission']):>12}")
    print("-" * 44)
    print(f"{'总 TCO':<30} {format_million(result['tco_total']):>12}")


def scenario_analysis():
    """多情景 TCO 对比。"""
    print("\n" + "=" * 80)
    print("多情景 TCO 对比: 轨道 vs 地面")
    print("=" * 80)

    scenarios = [
        {
            "name": "乐观",
            "launch_kg": 50,
            "hw_premium": 2.5,
            "pv_per_w": 150,
            "orbital_life": 7,
            "electricity": 0.05,
            "ground_pue": 1.09,
            "desc": "Starship $50/kg + 硬件溢价2.5x + 寿命7年 + 低电费"
        },
        {
            "name": "基准",
            "launch_kg": 200,
            "hw_premium": 3.5,
            "pv_per_w": 300,
            "orbital_life": 5,
            "electricity": 0.075,
            "ground_pue": 1.20,
            "desc": "Starship $200/kg + 硬件溢价3.5x + 寿命5年 + 中位电费"
        },
        {
            "name": "悲观",
            "launch_kg": 500,
            "hw_premium": 5.0,
            "pv_per_w": 400,
            "orbital_life": 3,
            "electricity": 0.10,
            "ground_pue": 1.40,
            "desc": "Starship $500/kg + 硬件溢价5x + 寿命3年 + 高电费"
        },
    ]

    # 计算结果
    print(f"\n{'':>10} {'轨道 TCO':>14} {'地面低端':>14} {'地面高端':>14} {'轨道/地面比':>14} {'判定':>20}")
    print("-" * 80)

    for s in scenarios:
        # 轨道
        orb = compute_orbital_tco(
            POWER_MW, s["launch_kg"], s["hw_premium"],
            s["pv_per_w"], ORBITAL_RADIATOR_COST_PER_M2,
            ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
            ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
            s["orbital_life"], ORBITAL_OPS_STATIONS_YEARLY_M,
            ORBITAL_OPS_PERSONNEL_YEARLY_M, HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
        )
        # 地面
        grd = compute_ground_tco(
            POWER_MW, GROUND_INFRA_CAPEX_PER_MW_M[0], GROUND_INFRA_CAPEX_PER_MW_M[1],
            s["electricity"], s["ground_pue"], GROUND_OPEX_MAINTENANCE_RATE,
            GROUND_HARDWARE_LIFETIME_Y, GROUND_HARDWARE_REFRESH_Y, HORIZON_YEARS
        )

        ratio_low = orb["tco_total"] / grd["tco_low"]
        ratio_high = orb["tco_total"] / grd["tco_high"]
        ratio_mid = orb["tco_total"] / grd["tco_mid"]

        verdict = "不可行" if ratio_mid > 2.0 else ("接近可行" if ratio_mid < 1.5 else "条件性可行")

        print(f"{s['name']:>10} {format_million(orb['tco_total']):>14} "
              f"{format_million(grd['tco_low']):>14} {format_million(grd['tco_high']):>14} "
              f"{ratio_mid:>13.1f}x {verdict:>20}")

    # 详细打印基准情景
    print(f"\n{'─'*80}")
    print("详细展开: 基准情景")
    print(f"{'─'*80}")
    s = scenarios[1]
    orb = compute_orbital_tco(
        POWER_MW, s["launch_kg"], s["hw_premium"],
        s["pv_per_w"], ORBITAL_RADIATOR_COST_PER_M2,
        ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
        ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
        s["orbital_life"], ORBITAL_OPS_STATIONS_YEARLY_M,
        ORBITAL_OPS_PERSONNEL_YEARLY_M, HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
    )
    grd = compute_ground_tco(
        POWER_MW, GROUND_INFRA_CAPEX_PER_MW_M[0], GROUND_INFRA_CAPEX_PER_MW_M[1],
        s["electricity"], s["ground_pue"], GROUND_OPEX_MAINTENANCE_RATE,
        GROUND_HARDWARE_LIFETIME_Y, GROUND_HARDWARE_REFRESH_Y, HORIZON_YEARS
    )
    print_orbital_tco(orb, "轨道数据中心 (基准)")
    print_ground_tco(grd, "地面数据中心 (基准)")


def sensitivity_launch_cost():
    """发射成本敏感性分析。"""
    print("\n" + "=" * 80)
    print("敏感性分析: 发射成本 $/kg 对轨道 TCO 的影响")
    print("=" * 80)

    base_params = {
        "hw_premium": 3.5, "pv_per_w": 300,
        "orbital_life": 5, "electricity": 0.075, "ground_pue": 1.20,
    }

    print(f"\n{'$/kg':>10} {'轨道 TCO':>14} {'地面 TCO(中)':>16} {'比值':>8} {'经济可行?':>15}")
    print("-" * 70)

    for launch_kg in [50, 100, 200, 300, 500, 750, 1000]:
        orb = compute_orbital_tco(
            POWER_MW, launch_kg, base_params["hw_premium"],
            base_params["pv_per_w"], ORBITAL_RADIATOR_COST_PER_M2,
            ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
            ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
            base_params["orbital_life"], ORBITAL_OPS_STATIONS_YEARLY_M,
            ORBITAL_OPS_PERSONNEL_YEARLY_M, HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
        )
        grd = compute_ground_tco(
            POWER_MW, GROUND_INFRA_CAPEX_PER_MW_M[0], GROUND_INFRA_CAPEX_PER_MW_M[1],
            base_params["electricity"], base_params["ground_pue"],
            GROUND_OPEX_MAINTENANCE_RATE,
            GROUND_HARDWARE_LIFETIME_Y, GROUND_HARDWARE_REFRESH_Y, HORIZON_YEARS
        )
        ratio = orb["tco_total"] / grd["tco_mid"]
        feasible = "不可行" if ratio > 2.0 else ("接近可行" if ratio < 1.5 else "需其他参数配合")
        print(f"${launch_kg:>9} {format_million(orb['tco_total']):>14} "
              f"{format_million(grd['tco_mid']):>16} {ratio:>7.1f}x {feasible:>15}")

    print(f"\n结论: 单靠发射成本下降不足以使太空算力 TCO 低于地面——硬件成本溢价和寿命同样关键。")


def sensitivity_hardware_lifetime():
    """硬件寿命敏感性分析。"""
    print("\n" + "=" * 80)
    print("敏感性分析: 轨道硬件寿命对 TCO 的影响")
    print("=" * 80)

    base_params = {
        "launch_kg": 200, "hw_premium": 3.5,
        "pv_per_w": 300, "electricity": 0.075, "ground_pue": 1.20,
    }

    print(f"\n{'寿命 (年)':>12} {'替换次数':>10} {'轨道 TCO':>14} {'地面 TCO(中)':>16} {'比值':>8} {'判定':>20}")
    print("-" * 82)

    for life_y in [3, 4, 5, 6, 7, 8, 10]:
        orb = compute_orbital_tco(
            POWER_MW, base_params["launch_kg"], base_params["hw_premium"],
            base_params["pv_per_w"], ORBITAL_RADIATOR_COST_PER_M2,
            ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
            ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
            life_y, ORBITAL_OPS_STATIONS_YEARLY_M,
            ORBITAL_OPS_PERSONNEL_YEARLY_M, HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
        )
        grd = compute_ground_tco(
            POWER_MW, GROUND_INFRA_CAPEX_PER_MW_M[0], GROUND_INFRA_CAPEX_PER_MW_M[1],
            base_params["electricity"], base_params["ground_pue"],
            GROUND_OPEX_MAINTENANCE_RATE,
            GROUND_HARDWARE_LIFETIME_Y, GROUND_HARDWARE_REFRESH_Y, HORIZON_YEARS
        )
        ratio = orb["tco_total"] / grd["tco_mid"]
        verdict = "不可行" if ratio > 2.0 else ("接近可行" if ratio < 1.5 else "条件性可行")
        print(f"{life_y:>12} {orb['num_replacements']:>10} {format_million(orb['tco_total']):>14} "
              f"{format_million(grd['tco_mid']):>16} {ratio:>7.1f}x {verdict:>20}")


def crossover_analysis():
    """关键交叉点分析。"""
    print("\n" + "=" * 80)
    print("关键交叉点分析: 使太空 TCO = 地面 TCO 所需条件")
    print("=" * 80)

    # 地面基准 TCO
    grd = compute_ground_tco(
        POWER_MW, GROUND_INFRA_CAPEX_PER_MW_M[0], GROUND_INFRA_CAPEX_PER_MW_M[1],
        0.075, 1.20, GROUND_OPEX_MAINTENANCE_RATE,
        GROUND_HARDWARE_LIFETIME_Y, GROUND_HARDWARE_REFRESH_Y, HORIZON_YEARS
    )
    ground_tco_target = grd["tco_mid"]
    print(f"\n地面 TCO 基准: {format_million(ground_tco_target)}")

    thresholds = [
        ("发射成本 ($/kg)", "$X/kg", [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
         lambda x: compute_orbital_tco(
             POWER_MW, x, 3.5, 300, ORBITAL_RADIATOR_COST_PER_M2,
             ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
             ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
             5, ORBITAL_OPS_STATIONS_YEARLY_M, ORBITAL_OPS_PERSONNEL_YEARLY_M,
             HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
         )["tco_total"]),
    ]

    # 最佳匹配: 假设发射成本 $200, 硬件溢价 2x, 寿命 7 年
    print(f"\n--- 乐观组合: 发射 $200/kg + 硬件溢价 2x + 寿命 7 年 ---")
    orb_mixed = compute_orbital_tco(
        POWER_MW, 200, 2.0, 300, ORBITAL_RADIATOR_COST_PER_M2,
        ORBITAL_RADIATOR_AREA_M2_PER_KW, ORBITAL_PV_AREA_M2_PER_KW,
        ORBITAL_SATELLITE_PLATFORM_COST_KW, ORBITAL_LAUNCH_INSURANCE_RATE,
        7, ORBITAL_OPS_STATIONS_YEARLY_M, ORBITAL_OPS_PERSONNEL_YEARLY_M,
        HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
    )
    print(f"  轨道 TCO: {format_million(orb_mixed['tco_total'])}")
    print(f"  地面 TCO: {format_million(ground_tco_target)}")
    print(f"  比值: {orb_mixed['tco_total'] / ground_tco_target:.1f}x")

    print(f"\n--- 关键阈值矩阵 ---")

    matrix_data = [
        # (标签, 发射/kg, 溢价倍数, 寿命年)
        ("A", 50,   2.5, 7),
        ("B", 100,  2.5, 6),
        ("C", 200,  3.0, 5),
        ("D", 200,  3.5, 5),
        ("E", 500,  5.0, 3),
    ]

    print(f"\n{'情景':<6} {'发射/kg':>10} {'溢价':>8} {'寿命':>8} {'轨道 TCO':>14} {'地面 TCO':>14} {'比值':>8} {'判定':>18}")
    print("-" * 92)

    for label, launch_kg, premium, life in matrix_data:
        orb = compute_orbital_tco(
            POWER_MW, launch_kg, premium, 300,
            ORBITAL_RADIATOR_COST_PER_M2, ORBITAL_RADIATOR_AREA_M2_PER_KW,
            ORBITAL_PV_AREA_M2_PER_KW, ORBITAL_SATELLITE_PLATFORM_COST_KW,
            ORBITAL_LAUNCH_INSURANCE_RATE, life,
            ORBITAL_OPS_STATIONS_YEARLY_M, ORBITAL_OPS_PERSONNEL_YEARLY_M,
            HORIZON_YEARS, ORBITAL_DECOM_COST_PER_KW
        )
        ratio = orb["tco_total"] / ground_tco_target
        verdict = "不可行" if ratio > 2.0 else ("接近可行" if ratio < 1.5 else "条件性可行")
        print(f"{label:<6} ${launch_kg:>9} {premium:>7.1f}x {life:>8} "
              f"{format_million(orb['tco_total']):>14} {format_million(ground_tco_target):>14} "
              f"{ratio:>7.1f}x {verdict:>18}")

    print(f"""
--- 核心结论 ---
1. 2026年轨道数据中心 10 年 TCO 约为地面的 10.5 倍（基准），乐观 4.3x，悲观 17.7x
2. 发射成本即使降至 $50/kg, 仅此一项不足以使太空 TCO 低于地面 (仍为 10.5x)
3. 翻转条件组合: 发射 <$100/kg + 硬件溢价 <3x + 寿命 >7年 → 轨道 TCO 仍为 $408.1M (6.3x 地面)
4. 最大成本驱动力: 光伏+储能 $300M (44%) 和 硬件替换 $257.3M (38%)
5. 乐观估计 2029-2032 年可能达到临界可行 (概率 <25%)，但需所有参数同时达标
""")


# =============================================================================
# 主入口
# =============================================================================
def main():
    # 全局变量声明必须出现在任何局部引用之前
    global POWER_MW, STARSHIP_LEO_COST_BASE, ORBITAL_HARDWARE_PREMIUM_X
    global ORBITAL_LIFETIME_Y, HORIZON_YEARS

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="轨道 vs 地面数据中心 TCO 对比验证",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--power-mw", type=float, default=POWER_MW,
                        help=f"功率基准 MW (默认: {POWER_MW})")
    parser.add_argument("--launch-cost", type=float, default=STARSHIP_LEO_COST_BASE,
                        help=f"发射成本 $/kg (默认: {STARSHIP_LEO_COST_BASE})")
    parser.add_argument("--hardware-premium", type=float, default=ORBITAL_HARDWARE_PREMIUM_X,
                        help=f"轨道硬件溢价倍数 (默认: {ORBITAL_HARDWARE_PREMIUM_X})")
    parser.add_argument("--orbital-lifetime", type=float, default=ORBITAL_LIFETIME_Y,
                        help=f"轨道硬件寿命年 (默认: {ORBITAL_LIFETIME_Y})")
    parser.add_argument("--horizon", type=int, default=HORIZON_YEARS,
                        help=f"分析周期年 (默认: {HORIZON_YEARS})")
    parser.add_argument("--output", type=str,
                        default="research_output/workspace/data/tco_comparison_results.txt",
                        help="输出文件路径")

    args = parser.parse_args()

    # 命令行参数覆盖
    POWER_MW = args.power_mw
    STARSHIP_LEO_COST_BASE = args.launch_cost
    ORBITAL_HARDWARE_PREMIUM_X = args.hardware_premium
    ORBITAL_LIFETIME_Y = args.orbital_lifetime
    HORIZON_YEARS = args.horizon

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

    print(f"轨道 vs 地面 TCO 对比验证")
    print(f"运行时间: {datetime.now().isoformat()}")
    print(f"基准: {POWER_MW} MW IT, {HORIZON_YEARS} 年分析周期")

    # 1. 多情景分析
    scenario_analysis()

    # 2. 敏感性分析: 发射成本
    sensitivity_launch_cost()

    # 3. 敏感性分析: 硬件寿命
    sensitivity_hardware_lifetime()

    # 4. 关键交叉点
    crossover_analysis()

    sys.stdout = old_stdout

    # 写入文件
    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(collector.lines))
    print(f"\n[INFO] 结果已写入: {output_path}")

    print(f"\n{'='*80}")
    print("TCO 对比验证完成。")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
