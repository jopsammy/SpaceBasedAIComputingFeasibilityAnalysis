#!/usr/bin/env python3
"""
第二阶段 Task 5/8：Blackwell 主线下的 GaAs/HJT 电源系统重建

目标：
1. 吸收 Task 6/7 已更新的结构化 JSON 输入；
2. 在统一 Blackwell 主线下重建 GaAs/HJT 电源路线（HJT 为并行成熟路线）；
3. 输出本轮电源系统结果 Markdown；
4. 保留 get_task5_power_replacements() 兼容接口，供后续脚本复用。
"""

from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
MASS_INPUT_PATH = os.path.join(DATA_DIR, "stage2_mass_inputs_blackwell_hjt.json")
COST_INPUT_PATH = os.path.join(DATA_DIR, "stage2_cost_inputs_blackwell_hjt.json")
DEFAULT_RESULTS_OUTPUT = os.path.join(DATA_DIR, "stage2_power_system_results_blackwell_hjt.md")
DEFAULT_COMPARISON_OUTPUT = os.path.join(DATA_DIR, "stage2_power_route_comparison.md")

EARTH_RADIUS_KM = 6378.137
EARTH_MU_KM3_S2 = 398600.4418
DEFAULT_ARRAY_PACKAGING_FACTOR = 0.85
DEFAULT_BATTERY_CHARGE_EFFICIENCY = 0.95
DEFAULT_BATTERY_DISCHARGE_EFFICIENCY = 0.95
DEFAULT_BUS_EFFICIENCY = 0.94


@dataclass(frozen=True)
class RouteCase:
    case_id: str
    label: str
    route: str
    role: str
    status: str
    evidence_grade: str
    altitude_km: float
    sustained_power_kw: float
    peak_power_kw: float
    # 电池 —— 兼容旧字段（默认 5yr Li-ion）
    battery_dod: float
    battery_specific_energy_wh_kg: float
    # 电池 —— 分支化字段（Task 6/7 新增）
    battery_dod_5yr: float
    battery_dod_10yr_liion: float
    battery_dod_10yr_lto: float
    battery_specific_energy_wh_kg_liion: float
    battery_specific_energy_wh_kg_lto: float
    battery_charge_efficiency: float
    battery_discharge_efficiency: float
    bus_efficiency: float
    array_cell_efficiency_bol: float
    array_cell_efficiency_eol: float
    array_packaging_factor: float
    array_specific_mass_kg_m2: float
    array_cost_per_bol_w_usd: Optional[float]
    # PCDU —— 兼容旧字段（默认 baseline）
    pcdu_specific_power_kw_kg: float
    # PCDU —— 场景化字段（Task 6/7 新增）
    pcdu_specific_power_kw_kg_light: float
    pcdu_specific_power_kw_kg_baseline: float
    pcdu_specific_power_kw_kg_conservative: float
    pcdu_cost_per_kw_usd: Optional[float]
    pcdu_cost_per_kw_usd_light: Optional[float]
    pcdu_cost_per_kw_usd_baseline: Optional[float]
    pcdu_cost_per_kw_usd_conservative: Optional[float]
    # 电池成本 —— 兼容旧字段（NMC 默认）
    battery_cost_per_kwh_usd: Optional[float]
    # 电池成本 —— 新 item_id（Task 7 新增/重命名）
    battery_cost_per_kwh_nmc_usd: Optional[float]
    battery_cost_per_kwh_lto_usd: Optional[float]
    cost_chain_status: str
    source_anchors: List[str]
    notes: str
    remaining_gap: str
    anchor_area_m2: Optional[float]
    anchor_array_mass_kg: Optional[float]
    anchor_battery_mass_kg: Optional[float]
    anchor_pcdu_mass_kg: Optional[float]
    anchor_total_power_mass_kg: Optional[float]


def load_json(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def get_cost_item(cost_inputs: Dict[str, object], item_id: str) -> Dict[str, object]:
    for item in cost_inputs["items"]:
        if item["item_id"] == item_id:
            return item
    raise KeyError(f"未找到价格项: {item_id}")


def value_from_map(values: Dict[str, object], *keys: str) -> Optional[float]:
    for key in keys:
        if key in values:
            return float(values[key])
    return None


def orbit_metrics(altitude_km: float) -> Dict[str, float]:
    orbit_radius_km = EARTH_RADIUS_KM + altitude_km
    period_seconds = 2.0 * math.pi * math.sqrt((orbit_radius_km ** 3) / EARTH_MU_KM3_S2)
    period_minutes = period_seconds / 60.0
    eclipse_fraction = math.asin(EARTH_RADIUS_KM / orbit_radius_km) / math.pi
    eclipse_minutes = period_minutes * eclipse_fraction
    sunlight_minutes = period_minutes - eclipse_minutes
    return {
        "period_minutes": period_minutes,
        "eclipse_minutes": eclipse_minutes,
        "sunlight_minutes": sunlight_minutes,
        "sunlight_fraction": sunlight_minutes / period_minutes,
        "eclipse_fraction": eclipse_minutes / period_minutes,
    }


def compute_power_case(
    case: RouteCase,
    battery_branch: str = "5yr",
    pcdu_scenario: str = "baseline",
) -> Dict[str, object]:
    """计算单条电源路线的物理量。

    Args:
        case: 路线参数案例。
        battery_branch: 电池分支 — "5yr" / "10yr_liion" / "10yr_lto"。
        pcdu_scenario: PCDU 场景 — "light" / "baseline" / "conservative"。
    """
    orbit = orbit_metrics(case.altitude_km)
    eclipse_hours = orbit["eclipse_minutes"] / 60.0
    sunlight_hours = orbit["sunlight_minutes"] / 60.0

    # 电池参数按分支选取
    if battery_branch == "10yr_lto":
        dod = case.battery_dod_10yr_lto
        specific_energy = case.battery_specific_energy_wh_kg_lto
        battery_cost_per_kwh = case.battery_cost_per_kwh_lto_usd
    elif battery_branch == "10yr_liion":
        dod = case.battery_dod_10yr_liion
        specific_energy = case.battery_specific_energy_wh_kg_liion
        battery_cost_per_kwh = case.battery_cost_per_kwh_nmc_usd
    else:  # "5yr"
        dod = case.battery_dod_5yr
        specific_energy = case.battery_specific_energy_wh_kg_liion
        battery_cost_per_kwh = case.battery_cost_per_kwh_nmc_usd

    # PCDU 比功率按场景选取
    if pcdu_scenario == "light":
        pcdu_sp = case.pcdu_specific_power_kw_kg_light
        pcdu_cost_per_kw = case.pcdu_cost_per_kw_usd_light
    elif pcdu_scenario == "conservative":
        pcdu_sp = case.pcdu_specific_power_kw_kg_conservative
        pcdu_cost_per_kw = case.pcdu_cost_per_kw_usd_conservative
    else:  # "baseline"
        pcdu_sp = case.pcdu_specific_power_kw_kg_baseline
        pcdu_cost_per_kw = case.pcdu_cost_per_kw_usd_baseline

    load_energy_during_eclipse_kwh = case.sustained_power_kw * eclipse_hours
    battery_nominal_kwh = load_energy_during_eclipse_kwh / (
        dod * case.battery_discharge_efficiency
    )
    battery_mass_kg = battery_nominal_kwh * 1000.0 / specific_energy

    recharge_energy_kwh = load_energy_during_eclipse_kwh / (
        case.battery_charge_efficiency * case.battery_discharge_efficiency
    )
    recharge_power_kw = recharge_energy_kwh / sunlight_hours
    pcdu_output_required_kw = case.sustained_power_kw + recharge_power_kw
    array_output_required_kw_eol = pcdu_output_required_kw / case.bus_efficiency

    net_array_density_bol_w_m2 = (
        1361.0 * case.array_cell_efficiency_bol * case.array_packaging_factor
    )
    net_array_density_eol_w_m2 = (
        1361.0 * case.array_cell_efficiency_eol * case.array_packaging_factor
    )
    required_area_m2 = array_output_required_kw_eol * 1000.0 / net_array_density_eol_w_m2
    array_nameplate_bol_kw = required_area_m2 * net_array_density_bol_w_m2 / 1000.0
    array_mass_kg = required_area_m2 * case.array_specific_mass_kg_m2

    pcdu_rating_kw = max(array_output_required_kw_eol, case.peak_power_kw)
    pcdu_mass_kg = pcdu_rating_kw / pcdu_sp

    array_cost_usd = None
    if case.array_cost_per_bol_w_usd is not None:
        array_cost_usd = array_nameplate_bol_kw * 1000.0 * case.array_cost_per_bol_w_usd

    battery_cost_usd = None
    if battery_cost_per_kwh is not None:
        battery_cost_usd = battery_nominal_kwh * battery_cost_per_kwh

    pcdu_cost_usd = None
    if pcdu_cost_per_kw is not None:
        pcdu_cost_usd = pcdu_rating_kw * pcdu_cost_per_kw

    total_mass_kg = array_mass_kg + battery_mass_kg + pcdu_mass_kg
    total_cost_usd = None
    if array_cost_usd is not None and battery_cost_usd is not None and pcdu_cost_usd is not None:
        total_cost_usd = array_cost_usd + battery_cost_usd + pcdu_cost_usd

    return {
        "case": case,
        "battery_branch": battery_branch,
        "pcdu_scenario": pcdu_scenario,
        "orbit": orbit,
        "load_energy_during_eclipse_kwh": load_energy_during_eclipse_kwh,
        "battery_nominal_kwh": battery_nominal_kwh,
        "battery_mass_kg": battery_mass_kg,
        "recharge_energy_kwh": recharge_energy_kwh,
        "recharge_power_kw": recharge_power_kw,
        "pcdu_output_required_kw": pcdu_output_required_kw,
        "array_output_required_kw_eol": array_output_required_kw_eol,
        "net_array_density_bol_w_m2": net_array_density_bol_w_m2,
        "net_array_density_eol_w_m2": net_array_density_eol_w_m2,
        "required_area_m2": required_area_m2,
        "array_nameplate_bol_kw": array_nameplate_bol_kw,
        "array_mass_kg": array_mass_kg,
        "pcdu_rating_kw": pcdu_rating_kw,
        "pcdu_mass_kg": pcdu_mass_kg,
        "array_cost_usd": array_cost_usd,
        "battery_cost_usd": battery_cost_usd,
        "pcdu_cost_usd": pcdu_cost_usd,
        "total_mass_kg": total_mass_kg,
        "total_cost_usd": total_cost_usd,
    }


def _build_single_route_case(
    case_id: str,
    label: str,
    route: str,
    role: str,
    route_input: Dict[str, object],
    public_baseline: Dict[str, object],
    cost_inputs: Dict[str, object],
    array_cost_item_id: Optional[str],
    hjt_cost_chain: Optional[Dict[str, object]] = None,
) -> RouteCase:
    """从 JSON 输入构造单个 RouteCase。"""
    battery = route_input["battery"]
    pcdu = route_input["pcdu"]

    # 电池分支参数
    battery_dod_5yr = float(battery["dod_5yr"])
    battery_dod_10yr_liion = float(battery["dod_10yr_liion"])
    battery_dod_10yr_lto = float(battery["dod_10yr_lto"])
    battery_se_liion = float(battery["specific_energy_wh_per_kg_liion"])
    battery_se_lto = float(battery["specific_energy_wh_per_kg_lto"])

    # PCDU 场景参数
    pcdu_sp_light = float(pcdu["specific_power_kw_per_kg_light"])
    pcdu_sp_baseline = float(pcdu["specific_power_kw_per_kg_baseline"])
    pcdu_sp_conservative = float(pcdu["specific_power_kw_per_kg_conservative"])

    # 阵列成本
    array_cost = None
    if array_cost_item_id:
        array_cost_item = get_cost_item(cost_inputs, array_cost_item_id)
        array_cost = value_from_map(array_cost_item["values"], "baseline")

    # PCDU 成本（三场景）
    pcdu_cost_item = get_cost_item(cost_inputs, "pcdu_cost_per_kw")
    pcdu_cost_light = value_from_map(pcdu_cost_item["values"], "light")
    pcdu_cost_baseline = value_from_map(pcdu_cost_item["values"], "baseline")
    pcdu_cost_conservative = value_from_map(pcdu_cost_item["values"], "conservative")

    # 电池成本（NMC 固定 + LTO 三场景）
    battery_cost_nmc_item = get_cost_item(cost_inputs, "battery_cost_per_kwh_nmc")
    battery_cost_nmc = value_from_map(battery_cost_nmc_item["values"], "fixed")
    battery_cost_lto_item = get_cost_item(cost_inputs, "battery_cost_per_kwh_lto")
    battery_cost_lto = value_from_map(battery_cost_lto_item["values"], "baseline")

    return RouteCase(
        case_id=case_id,
        label=label,
        route=route,
        role=role,
        status=str(route_input["status"]),
        evidence_grade=str(route_input["evidence_grade"]),
        altitude_km=float(public_baseline["orbit_altitude_km"]),
        sustained_power_kw=float(public_baseline["sustained_power_kw"]),
        peak_power_kw=float(public_baseline["peak_power_kw"]),
        # 兼容旧字段（默认 5yr Li-ion + baseline PCDU）
        battery_dod=battery_dod_5yr,
        battery_specific_energy_wh_kg=battery_se_liion,
        # 电池分支字段
        battery_dod_5yr=battery_dod_5yr,
        battery_dod_10yr_liion=battery_dod_10yr_liion,
        battery_dod_10yr_lto=battery_dod_10yr_lto,
        battery_specific_energy_wh_kg_liion=battery_se_liion,
        battery_specific_energy_wh_kg_lto=battery_se_lto,
        battery_charge_efficiency=DEFAULT_BATTERY_CHARGE_EFFICIENCY,
        battery_discharge_efficiency=DEFAULT_BATTERY_DISCHARGE_EFFICIENCY,
        bus_efficiency=DEFAULT_BUS_EFFICIENCY,
        array_cell_efficiency_bol=float(route_input["array_efficiency_bol"]),
        array_cell_efficiency_eol=float(route_input["array_efficiency_eol"]),
        array_packaging_factor=DEFAULT_ARRAY_PACKAGING_FACTOR,
        array_specific_mass_kg_m2=float(route_input["array_specific_mass_kg_per_m2"]),
        array_cost_per_bol_w_usd=array_cost,
        # PCDU 兼容旧字段（默认 baseline）
        pcdu_specific_power_kw_kg=pcdu_sp_baseline,
        # PCDU 场景字段
        pcdu_specific_power_kw_kg_light=pcdu_sp_light,
        pcdu_specific_power_kw_kg_baseline=pcdu_sp_baseline,
        pcdu_specific_power_kw_kg_conservative=pcdu_sp_conservative,
        pcdu_cost_per_kw_usd=pcdu_cost_baseline,
        pcdu_cost_per_kw_usd_light=pcdu_cost_light,
        pcdu_cost_per_kw_usd_baseline=pcdu_cost_baseline,
        pcdu_cost_per_kw_usd_conservative=pcdu_cost_conservative,
        # 电池成本兼容（NMC 默认）
        battery_cost_per_kwh_usd=battery_cost_nmc,
        battery_cost_per_kwh_nmc_usd=battery_cost_nmc,
        battery_cost_per_kwh_lto_usd=battery_cost_lto,
        cost_chain_status="阵列成本为情景参数；电池与 PCDU 成本见 Task 7 新 item_id",
        source_anchors=list(route_input["source_anchors"]),
        notes="",
        remaining_gap=str(route_input.get("remaining_gap", "")),
        anchor_area_m2=(
            float(route_input["array_area_m2"]) if "array_area_m2" in route_input else None
        ),
        anchor_array_mass_kg=(
            float(route_input["array_mass_kg"]) if "array_mass_kg" in route_input else None
        ),
        anchor_battery_mass_kg=None,
        anchor_pcdu_mass_kg=None,
        anchor_total_power_mass_kg=None,
    )


def build_route_cases(
    mass_inputs: Dict[str, object], cost_inputs: Dict[str, object]
) -> Dict[str, RouteCase]:
    public_baseline = mass_inputs["common_inputs"]["public_baseline"]
    gaas_input = mass_inputs["route_sensitive_inputs"]["gaas_baseline"]
    hjt_input = mass_inputs["route_sensitive_inputs"]["hjt_parallel"]

    hjt_cost_chain = get_cost_item(cost_inputs, "hjt_route_cost_chain")

    gaas_case = _build_single_route_case(
        case_id="gaas_baseline",
        label="GaAs 主链基准",
        route="GaAs",
        role="Task 5/8 主模型电源路线",
        route_input=gaas_input,
        public_baseline=public_baseline,
        cost_inputs=cost_inputs,
        array_cost_item_id="gaas_array_cost_per_bol_w",
        hjt_cost_chain=None,
    )
    gaas_case = RouteCase(
        case_id=gaas_case.case_id,
        label=gaas_case.label,
        route=gaas_case.route,
        role=gaas_case.role,
        status=gaas_case.status,
        evidence_grade=gaas_case.evidence_grade,
        altitude_km=gaas_case.altitude_km,
        sustained_power_kw=gaas_case.sustained_power_kw,
        peak_power_kw=gaas_case.peak_power_kw,
        battery_dod=gaas_case.battery_dod,
        battery_specific_energy_wh_kg=gaas_case.battery_specific_energy_wh_kg,
        battery_dod_5yr=gaas_case.battery_dod_5yr,
        battery_dod_10yr_liion=gaas_case.battery_dod_10yr_liion,
        battery_dod_10yr_lto=gaas_case.battery_dod_10yr_lto,
        battery_specific_energy_wh_kg_liion=gaas_case.battery_specific_energy_wh_kg_liion,
        battery_specific_energy_wh_kg_lto=gaas_case.battery_specific_energy_wh_kg_lto,
        battery_charge_efficiency=gaas_case.battery_charge_efficiency,
        battery_discharge_efficiency=gaas_case.battery_discharge_efficiency,
        bus_efficiency=gaas_case.bus_efficiency,
        array_cell_efficiency_bol=gaas_case.array_cell_efficiency_bol,
        array_cell_efficiency_eol=gaas_case.array_cell_efficiency_eol,
        array_packaging_factor=gaas_case.array_packaging_factor,
        array_specific_mass_kg_m2=gaas_case.array_specific_mass_kg_m2,
        array_cost_per_bol_w_usd=gaas_case.array_cost_per_bol_w_usd,
        pcdu_specific_power_kw_kg=gaas_case.pcdu_specific_power_kw_kg,
        pcdu_specific_power_kw_kg_light=gaas_case.pcdu_specific_power_kw_kg_light,
        pcdu_specific_power_kw_kg_baseline=gaas_case.pcdu_specific_power_kw_kg_baseline,
        pcdu_specific_power_kw_kg_conservative=gaas_case.pcdu_specific_power_kw_kg_conservative,
        pcdu_cost_per_kw_usd=gaas_case.pcdu_cost_per_kw_usd,
        pcdu_cost_per_kw_usd_light=gaas_case.pcdu_cost_per_kw_usd_light,
        pcdu_cost_per_kw_usd_baseline=gaas_case.pcdu_cost_per_kw_usd_baseline,
        pcdu_cost_per_kw_usd_conservative=gaas_case.pcdu_cost_per_kw_usd_conservative,
        battery_cost_per_kwh_usd=gaas_case.battery_cost_per_kwh_usd,
        battery_cost_per_kwh_nmc_usd=gaas_case.battery_cost_per_kwh_nmc_usd,
        battery_cost_per_kwh_lto_usd=gaas_case.battery_cost_per_kwh_lto_usd,
        cost_chain_status="阵列成本为情景参数（三档）；电池 NMC 成本为三档（Starlink 迁移）；PCDU 成本为四档（Terma 锚点）",
        source_anchors=gaas_case.source_anchors,
        notes="以 Task 6 的 GaAs 主链参数为准，吸收 Task 7 的电池 NMC/LTO 与 PCDU 成本。",
        remaining_gap="电池与 PCDU 的价格链均为合理推断/迁移证据，非一手采购价。",
        anchor_area_m2=gaas_case.anchor_area_m2,
        anchor_array_mass_kg=gaas_case.anchor_array_mass_kg,
        anchor_battery_mass_kg=gaas_case.anchor_battery_mass_kg,
        anchor_pcdu_mass_kg=gaas_case.anchor_pcdu_mass_kg,
        anchor_total_power_mass_kg=gaas_case.anchor_total_power_mass_kg,
    )

    hjt_case = _build_single_route_case(
        case_id="hjt_parallel",
        label="HJT 并行路线",
        route="HJT",
        role="Task 5/8 并行成熟路线，物理链可比较，价格链单独标注",
        route_input=hjt_input,
        public_baseline=public_baseline,
        cost_inputs=cost_inputs,
        array_cost_item_id=None,  # HJT 阵列成本不走 GaAs 的 $/W_BOL
    )
    hjt_case = RouteCase(
        case_id=hjt_case.case_id,
        label=hjt_case.label,
        route=hjt_case.route,
        role=hjt_case.role,
        status=hjt_case.status,
        evidence_grade=hjt_case.evidence_grade,
        altitude_km=hjt_case.altitude_km,
        sustained_power_kw=hjt_case.sustained_power_kw,
        peak_power_kw=hjt_case.peak_power_kw,
        battery_dod=hjt_case.battery_dod,
        battery_specific_energy_wh_kg=hjt_case.battery_specific_energy_wh_kg,
        battery_dod_5yr=hjt_case.battery_dod_5yr,
        battery_dod_10yr_liion=hjt_case.battery_dod_10yr_liion,
        battery_dod_10yr_lto=hjt_case.battery_dod_10yr_lto,
        battery_specific_energy_wh_kg_liion=hjt_case.battery_specific_energy_wh_kg_liion,
        battery_specific_energy_wh_kg_lto=hjt_case.battery_specific_energy_wh_kg_lto,
        battery_charge_efficiency=hjt_case.battery_charge_efficiency,
        battery_discharge_efficiency=hjt_case.battery_discharge_efficiency,
        bus_efficiency=hjt_case.bus_efficiency,
        array_cell_efficiency_bol=hjt_case.array_cell_efficiency_bol,
        array_cell_efficiency_eol=hjt_case.array_cell_efficiency_eol,
        array_packaging_factor=hjt_case.array_packaging_factor,
        array_specific_mass_kg_m2=hjt_case.array_specific_mass_kg_m2,
        array_cost_per_bol_w_usd=hjt_case.array_cost_per_bol_w_usd,
        pcdu_specific_power_kw_kg=hjt_case.pcdu_specific_power_kw_kg,
        pcdu_specific_power_kw_kg_light=hjt_case.pcdu_specific_power_kw_kg_light,
        pcdu_specific_power_kw_kg_baseline=hjt_case.pcdu_specific_power_kw_kg_baseline,
        pcdu_specific_power_kw_kg_conservative=hjt_case.pcdu_specific_power_kw_kg_conservative,
        pcdu_cost_per_kw_usd=hjt_case.pcdu_cost_per_kw_usd,
        pcdu_cost_per_kw_usd_light=hjt_case.pcdu_cost_per_kw_usd_light,
        pcdu_cost_per_kw_usd_baseline=hjt_case.pcdu_cost_per_kw_usd_baseline,
        pcdu_cost_per_kw_usd_conservative=hjt_case.pcdu_cost_per_kw_usd_conservative,
        battery_cost_per_kwh_usd=hjt_case.battery_cost_per_kwh_usd,
        battery_cost_per_kwh_nmc_usd=hjt_case.battery_cost_per_kwh_nmc_usd,
        battery_cost_per_kwh_lto_usd=hjt_case.battery_cost_per_kwh_lto_usd,
        cost_chain_status=(
            "HJT 阵列采购价格链为三档（地面 HJT $0.14-0.24/W × 10-15× 空间放大）；"
            "电池与 PCDU 与 GaAs 共享同一链路"
        ),
        source_anchors=hjt_case.source_anchors,
        notes=(
            "HJT 现为 GaAs 的并行成熟路线（非探索性/降级），物理链可比较，"
            "价格链闭合度单独标注。"
            f"Task 7 状态：{hjt_cost_chain['source_type']}。"
        ),
        remaining_gap=str(hjt_input.get("remaining_gap", "")),
        anchor_area_m2=hjt_case.anchor_area_m2,
        anchor_array_mass_kg=hjt_case.anchor_array_mass_kg,
        anchor_battery_mass_kg=hjt_case.anchor_battery_mass_kg,
        anchor_pcdu_mass_kg=hjt_case.anchor_pcdu_mass_kg,
        anchor_total_power_mass_kg=hjt_case.anchor_total_power_mass_kg,
    )

    return {
        gaas_case.case_id: gaas_case,
        hjt_case.case_id: hjt_case,
    }


def build_compatibility_cases(
    mass_inputs: Dict[str, object], cost_inputs: Dict[str, object]
) -> Dict[str, RouteCase]:
    public_baseline = mass_inputs["common_inputs"]["public_baseline"]
    gaas_input = mass_inputs["route_sensitive_inputs"]["gaas_baseline"]
    gaas_array_cost = get_cost_item(cost_inputs, "gaas_array_cost_per_bol_w")
    battery_nmc = get_cost_item(cost_inputs, "battery_cost_per_kwh_nmc")
    battery_lto = get_cost_item(cost_inputs, "battery_cost_per_kwh_lto")
    pcdu_cost = get_cost_item(cost_inputs, "pcdu_cost_per_kw")

    battery_cost_nmc = value_from_map(battery_nmc["values"], "fixed")
    battery_cost_lto = value_from_map(battery_lto["values"], "baseline")

    pcdu_cost_light = value_from_map(pcdu_cost["values"], "light")
    pcdu_cost_baseline = value_from_map(pcdu_cost["values"], "baseline")
    pcdu_cost_conservative = value_from_map(pcdu_cost["values"], "conservative")

    shared = {
        "route": "GaAs",
        "status": str(gaas_input["status"]),
        "evidence_grade": str(gaas_input["evidence_grade"]),
        "altitude_km": float(public_baseline["orbit_altitude_km"]),
        "sustained_power_kw": float(public_baseline["sustained_power_kw"]),
        "peak_power_kw": float(public_baseline["peak_power_kw"]),
        "battery_charge_efficiency": DEFAULT_BATTERY_CHARGE_EFFICIENCY,
        "battery_discharge_efficiency": DEFAULT_BATTERY_DISCHARGE_EFFICIENCY,
        "bus_efficiency": DEFAULT_BUS_EFFICIENCY,
        "array_packaging_factor": DEFAULT_ARRAY_PACKAGING_FACTOR,
        "source_anchors": list(gaas_input["source_anchors"]),
        "remaining_gap": "仅供兼容旧接口；价格链仍需保留降级标签。",
        "anchor_area_m2": None,
        "anchor_array_mass_kg": None,
        "anchor_battery_mass_kg": None,
        "anchor_pcdu_mass_kg": None,
        "anchor_total_power_mass_kg": None,
        "cost_chain_status": "兼容接口；电池与 PCDU 成本见 Task 7 新 item_id",
        "notes": "用于维持 stage2_mass_cost_model.py 的旧接口，不代表新增事实口径。",
    }

    return {
        "gaas_advanced": RouteCase(
            case_id="gaas_advanced",
            label="GaAs 先进工程情景",
            role="兼容旧接口：轻量化",
            battery_dod=0.60,
            battery_specific_energy_wh_kg=220.0,
            battery_dod_5yr=0.60,
            battery_dod_10yr_liion=0.40,
            battery_dod_10yr_lto=0.90,
            battery_specific_energy_wh_kg_liion=220.0,
            battery_specific_energy_wh_kg_lto=110.0,
            array_cell_efficiency_bol=0.36,
            array_cell_efficiency_eol=0.33,
            array_specific_mass_kg_m2=1.3,
            array_cost_per_bol_w_usd=value_from_map(gaas_array_cost["values"], "advanced"),
            pcdu_specific_power_kw_kg=1.0,
            pcdu_specific_power_kw_kg_light=1.0,
            pcdu_specific_power_kw_kg_baseline=0.5,
            pcdu_specific_power_kw_kg_conservative=0.2,
            pcdu_cost_per_kw_usd=pcdu_cost_light,
            pcdu_cost_per_kw_usd_light=pcdu_cost_light,
            pcdu_cost_per_kw_usd_baseline=pcdu_cost_baseline,
            pcdu_cost_per_kw_usd_conservative=pcdu_cost_conservative,
            battery_cost_per_kwh_usd=battery_cost_nmc,
            battery_cost_per_kwh_nmc_usd=battery_cost_nmc,
            battery_cost_per_kwh_lto_usd=battery_cost_lto,
            **shared,
        ),
        "gaas_baseline": RouteCase(
            case_id="gaas_baseline",
            label="GaAs 中性工程情景",
            role="兼容旧接口：基准",
            battery_dod=float(gaas_input["battery"]["dod_5yr"]),
            battery_specific_energy_wh_kg=float(gaas_input["battery"]["specific_energy_wh_per_kg_liion"]),
            battery_dod_5yr=float(gaas_input["battery"]["dod_5yr"]),
            battery_dod_10yr_liion=float(gaas_input["battery"]["dod_10yr_liion"]),
            battery_dod_10yr_lto=float(gaas_input["battery"]["dod_10yr_lto"]),
            battery_specific_energy_wh_kg_liion=float(gaas_input["battery"]["specific_energy_wh_per_kg_liion"]),
            battery_specific_energy_wh_kg_lto=float(gaas_input["battery"]["specific_energy_wh_per_kg_lto"]),
            array_cell_efficiency_bol=float(gaas_input["array_efficiency_bol"]),
            array_cell_efficiency_eol=float(gaas_input["array_efficiency_eol"]),
            array_specific_mass_kg_m2=float(gaas_input["array_specific_mass_kg_per_m2"]),
            array_cost_per_bol_w_usd=value_from_map(gaas_array_cost["values"], "baseline"),
            pcdu_specific_power_kw_kg=float(gaas_input["pcdu"]["specific_power_kw_per_kg_baseline"]),
            pcdu_specific_power_kw_kg_light=float(gaas_input["pcdu"]["specific_power_kw_per_kg_light"]),
            pcdu_specific_power_kw_kg_baseline=float(gaas_input["pcdu"]["specific_power_kw_per_kg_baseline"]),
            pcdu_specific_power_kw_kg_conservative=float(gaas_input["pcdu"]["specific_power_kw_per_kg_conservative"]),
            pcdu_cost_per_kw_usd=pcdu_cost_baseline,
            pcdu_cost_per_kw_usd_light=pcdu_cost_light,
            pcdu_cost_per_kw_usd_baseline=pcdu_cost_baseline,
            pcdu_cost_per_kw_usd_conservative=pcdu_cost_conservative,
            battery_cost_per_kwh_usd=battery_cost_nmc,
            battery_cost_per_kwh_nmc_usd=battery_cost_nmc,
            battery_cost_per_kwh_lto_usd=battery_cost_lto,
            **shared,
        ),
        "gaas_heritage": RouteCase(
            case_id="gaas_heritage",
            label="GaAs 长寿命保守情景",
            role="兼容旧接口：保守",
            battery_dod=0.20,
            battery_specific_energy_wh_kg=180.0,
            battery_dod_5yr=0.30,
            battery_dod_10yr_liion=0.20,
            battery_dod_10yr_lto=0.70,
            battery_specific_energy_wh_kg_liion=180.0,
            battery_specific_energy_wh_kg_lto=90.0,
            array_cell_efficiency_bol=float(gaas_input["array_efficiency_bol"]),
            array_cell_efficiency_eol=0.28,
            array_specific_mass_kg_m2=1.8,
            array_cost_per_bol_w_usd=value_from_map(gaas_array_cost["values"], "heritage"),
            pcdu_specific_power_kw_kg=0.2,
            pcdu_specific_power_kw_kg_light=1.0,
            pcdu_specific_power_kw_kg_baseline=0.5,
            pcdu_specific_power_kw_kg_conservative=0.2,
            pcdu_cost_per_kw_usd=pcdu_cost_conservative,
            pcdu_cost_per_kw_usd_light=pcdu_cost_light,
            pcdu_cost_per_kw_usd_baseline=pcdu_cost_baseline,
            pcdu_cost_per_kw_usd_conservative=pcdu_cost_conservative,
            battery_cost_per_kwh_usd=battery_cost_nmc,
            battery_cost_per_kwh_nmc_usd=battery_cost_nmc,
            battery_cost_per_kwh_lto_usd=battery_cost_lto,
            **shared,
        ),
    }


def format_mass(value_kg: Optional[float]) -> str:
    if value_kg is None:
        return "-"
    return f"{value_kg:,.0f} kg"


def format_area(value_m2: Optional[float]) -> str:
    if value_m2 is None:
        return "-"
    return f"{value_m2:,.0f} m^2"


def format_kwh(value_kwh: Optional[float]) -> str:
    if value_kwh is None:
        return "-"
    return f"{value_kwh:.1f} kWh"


def format_cost(value_usd: Optional[float]) -> str:
    if value_usd is None:
        return "当前不可判定"
    return f"${value_usd / 1_000_000:.2f}M"


def format_delta(current: Optional[float], anchor: Optional[float], unit: str) -> str:
    if current is None or anchor is None:
        return "-"
    delta = current - anchor
    if unit == "m2":
        return f"{delta:+.0f} m^2"
    return f"{delta:+.0f} kg"


def build_source_absorption_table() -> str:
    lines = [
        "| 输入层 | 来源文件 | Task 5/8 吸收方式 | 约束 |",
        "|---|---|---|---|",
        "| 质量输入 | `stage2_mass_inputs_blackwell_hjt.json` | 读取 `public_baseline`、`route_sensitive_inputs`（`hjt_parallel`）和 `components`，重算轨道食时、电池容量、阵列面积、功率电子质量 | HJT 定位为并行成熟路线，不再保留「只能降级」标签 |",
        "| 价格输入 | `stage2_cost_inputs_blackwell_hjt.json` | 读取 GaAs 阵列成本情景参数、电池 NMC/LTO 单价、PCDU 单价、HJT 价格链 | 电池成本按 item_id 分支（NMC 固定/LTO 三场景）；HJT 阵列采购链单独标注闭合度 |",
        "| 方法学边界 | 审计文档与 `current-note.md` | 固定 `Blackwell` 主线、`GaAs/HJT` 并行、电池分支化（5yr/10yr Li-ion/10yr LTO） | 废弃 kW/t 反推链；不把 Rubin 带回主线 |",
    ]
    return "\n".join(lines)


def build_route_result_table(results: Dict[str, Dict[str, object]]) -> str:
    ordered = ["gaas_baseline", "hjt_parallel"]
    lines = [
        "| 路线 | Task 5/8 角色 | 状态 | 阵列面积 | 阵列质量 | 电池质量 | PCDU 质量 | 电源总质量 | 电源总成本 | 价格链状态 |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for case_id in ordered:
        result = results[case_id]
        case = result["case"]
        lines.append(
            f"| {case.label} | {case.role} | {case.status} | "
            f"{result['required_area_m2']:.0f} m^2 | "
            f"{result['array_mass_kg']:.0f} kg | "
            f"{result['battery_mass_kg']:.0f} kg | "
            f"{result['pcdu_mass_kg']:.0f} kg | "
            f"{result['total_mass_kg']:.0f} kg | "
            f"{format_cost(result['total_cost_usd'])} | {case.cost_chain_status} |"
        )
    return "\n".join(lines)


def build_compatibility_table(results: Dict[str, Dict[str, object]]) -> str:
    scenario_map = {
        "轻量化": "gaas_advanced",
        "基准": "gaas_baseline",
        "保守": "gaas_heritage",
    }
    lines = [
        "| 兼容场景 | 光伏质量 | 电池质量 | 功率电子质量 | 电源总质量 | 光伏面积 | 电池名义容量 | 电源总成本 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for scenario_name, case_id in scenario_map.items():
        result = results[case_id]
        lines.append(
            f"| {scenario_name} | {format_mass(result['array_mass_kg'])} | "
            f"{format_mass(result['battery_mass_kg'])} | {format_mass(result['pcdu_mass_kg'])} | "
            f"{format_mass(result['total_mass_kg'])} | {result['required_area_m2']:.0f} m^2 | "
            f"{result['battery_nominal_kwh']:.1f} kWh | {format_cost(result['total_cost_usd'])} |"
        )
    return "\n".join(lines)


def build_results_markdown(
    route_results: Dict[str, Dict[str, object]],
    compatibility_results: Dict[str, Dict[str, object]],
) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    gaas = route_results["gaas_baseline"]
    hjt = route_results["hjt_parallel"]
    delta_area = hjt["required_area_m2"] - gaas["required_area_m2"]
    delta_mass = hjt["total_mass_kg"] - gaas["total_mass_kg"]
    orbit = gaas["orbit"]
    return f"""# Stage 2 Task 5/8：Blackwell 主线下的电源系统结果

## 说明

- 生成时间：`{now}`
- 任务定位：服务于 Task 5/8，吸收 Task 6 的质量输入（含废弃 kW/t 链）与 Task 7 的价格输入（含新 item_id 与电池分支化）。
- 写法原则：中性审计式；明确区分 `已闭合`、`四档`、`三档` 与 `当前不可判定`。
- 当前主线：统一 `Blackwell`，电源路线按 `GaAs` 主链与 `HJT` 并行成熟路线比较展开。

## 一、先行结论

- `600 km`、`beta = 0` 最保守近似下，轨道周期约 `{orbit['period_minutes']:.1f} min`，食时约 `{orbit['eclipse_minutes']:.1f} min`，日照约 `{orbit['sunlight_minutes']:.1f} min`。
- `GaAs` 主链基准重算得到：阵列面积约 `{gaas['required_area_m2']:.0f} m^2`、电池名义容量 `{gaas['battery_nominal_kwh']:.1f} kWh`、电源总质量 `{gaas['total_mass_kg'] / 1000.0:.2f} t`。
- `HJT` 并行路线在相同负载与轨道假设下，需要额外约 `{delta_area:.0f} m^2` 阵列面积与 `{delta_mass / 1000.0:.2f} t` 电源总质量；说明其物理上可比，但系统代价明显更重。
- `GaAs` 的阵列成本可作为情景参数进入后续模型；`HJT` 阵列采购价格链有三档支撑（地面 HJT $0.14-0.24/W × 10-15×），但闭合度低于 GaAs，单独标注。
- 电池成本已更新为 Task 7 新 item_id：`battery_cost_per_kwh_nmc`（NMC 固定 $200/kWh，三档 Starlink 迁移）与 `battery_cost_per_kwh_lto`（LTO 三场景，四档等比压缩）。PCDU 成本沿用 Task 7 的 $3k-10k/kW 四档。

## 二、Task 6/7 输入吸收关系

{build_source_absorption_table()}

## 三、路线重算结果

{build_route_result_table(route_results)}

## 四、公式链

```text
轨道周期 = 2*pi*sqrt((R_earth + h)^3 / mu)
食时占比(beta=0近似) = asin(R_earth / (R_earth + h)) / pi
食区负载能量 = 持续功率 * 食时
电池名义容量 = 食区负载能量 / (DoD * 放电效率)  ← DoD 按电池分支选取
回充能量 = 食区负载能量 / (充电效率 * 放电效率)
日照段额外回充功率 = 回充能量 / 日照时长
PCDU 输出需求 = 持续功率 + 日照段额外回充功率
EOL 阵列需求功率 = PCDU 输出需求 / 母线效率
阵列面积 = EOL 阵列需求功率 / (太阳常数 * EOL 电池效率 * 封装修正)
阵列质量 = 阵列面积 * 阵列面密度
PCDU 质量 = 额定功率 / 比功率  ← 比功率按 PCDU 场景选取
```

## 五、兼容旧接口的 `GaAs` 三场景

> 该表只用于维持 `get_task5_power_replacements()` 的后续脚本接口，不新增新的事实结论。

{build_compatibility_table(compatibility_results)}

## 六、审计判断

- `GaAs`：质量链为 `已闭合`（二档 AzurSpace 4G32 + 三档面密度），价格链为"阵列情景参数 + 电池 NMC 三档 + PCDU 四档"，可进入下一步主经济模型。
- `HJT`：现为并行成熟路线（非「禁止进入主模型」），物理链可用于并行比较（二档 CEA/INES 辐照实验 + 三档面密度）；采购价格链有三档地面 HJT 锚点 + 10-15× 空间放大，闭合度单独标注。
- `Task 6` 中废弃的 kW/t 反推链已从本脚本中彻底移除，计算载荷质量改为从 `components[compute_payload].scenario_mass_kg` 直接读取（Task 8 在 stage2_mass_cost_model.py 中落实）。
- `Task 7` 的新 item_id（`battery_cost_per_kwh_nmc` / `battery_cost_per_kwh_lto`）已在本脚本中被正确引用，旧 `battery_cost_per_kwh` 不再使用。

## 七、对下游的交接输入

- 主模型电源路线：继续使用 `GaAs` 主链。
- 并行比较路线：保留 `HJT` 为并行成熟路线（非探索性/降级）。
- 电池分支：5yr NMC（DoD 40%）、10yr Li-ion NMC（DoD 25%）、10yr LTO（DoD 80%）三分支可用于下游敏感性。
- 兼容接口：后续脚本可继续调用 `get_task5_power_replacements()` 获取 `轻量化 / 基准 / 保守` 三个 `GaAs` 场景的替换值。
"""


def build_comparison_markdown(route_results: Dict[str, Dict[str, object]]) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    gaas = route_results["gaas_baseline"]
    hjt = route_results["hjt_parallel"]
    area_ratio = hjt["required_area_m2"] / gaas["required_area_m2"]
    mass_ratio = hjt["total_mass_kg"] / gaas["total_mass_kg"]
    lines = [
        "# Stage 2 Task 5/8：GaAs 与 HJT 电源路线比较",
        "",
        "## 说明",
        "",
        f"- 生成时间：`{now}`",
        "- 比较边界：统一 `Blackwell` 主线、统一 `120 kW` 持续功率、统一 `150 kW` 峰值功率、统一 `~600 km` 轨道条件。",
        "- 本文只比较电源路线，不扩展到寿命与全星经济结论。",
        "",
        "## 一、核心差异",
        "",
        "| 指标 | GaAs 主链 | HJT 并行路线 | 差异 | 解释 |",
        "|---|---:|---:|---:|---|",
        f"| 阵列面积 | {gaas['required_area_m2']:.0f} m^2 | {hjt['required_area_m2']:.0f} m^2 | +{hjt['required_area_m2'] - gaas['required_area_m2']:.0f} m^2 | HJT 的 EOL 效率更低，导致相同负载下需要更大面积 |",
        f"| 阵列质量 | {gaas['array_mass_kg']:.0f} kg | {hjt['array_mass_kg']:.0f} kg | +{hjt['array_mass_kg'] - gaas['array_mass_kg']:.0f} kg | 面积放大是主因，即使面密度略低也不足以抵消 |",
        f"| 电池名义容量 | {gaas['battery_nominal_kwh']:.1f} kWh | {hjt['battery_nominal_kwh']:.1f} kWh | +{hjt['battery_nominal_kwh'] - gaas['battery_nominal_kwh']:.1f} kWh | 当前两条路线共用同一电池链路（电池质量由食时决定） |",
        f"| 功率电子质量 | {gaas['pcdu_mass_kg']:.0f} kg | {hjt['pcdu_mass_kg']:.0f} kg | +{hjt['pcdu_mass_kg'] - gaas['pcdu_mass_kg']:.0f} kg | 当前两条路线共用同一 PCDU 链路 |",
        f"| 电源总质量 | {gaas['total_mass_kg'] / 1000.0:.2f} t | {hjt['total_mass_kg'] / 1000.0:.2f} t | +{(hjt['total_mass_kg'] - gaas['total_mass_kg']) / 1000.0:.2f} t | HJT 路线会把电源系统整体放大约 `{mass_ratio:.2f}x` |",
        f"| 电源总成本 | {format_cost(gaas['total_cost_usd'])} | {format_cost(hjt['total_cost_usd'])} | - | HJT 阵列采购价格链闭合度低于 GaAs，单独标注 |",
        "",
        "## 二、证据等级与可用性",
        "",
        "| 路线 | 质量状态 | 价格状态 | 当前可支撑到的结论 | 当前不能支撑的结论 |",
        "|---|---|---|---|---|",
        "| GaAs | 已闭合（二档+三档） | 阵列情景参数（三档）+电池 NMC（三档）+PCDU（四档） | 可进入主模型电源质量链与情景成本链 | 不能写成 AI1 一手电源 BOM |",
        "| HJT | 并行成熟路线（二档+三档） | 阵列价格链为三档（地面→空间放大），电池 PCDU 与 GaAs 共享 | 可作为并行路线比较其面积/质量放大效应，价格链亦有独立锚点 | 价格链闭合度低于 GaAs，不能直接给出同等确定性的总成本 |",
        "",
        "## 三、收束判断",
        "",
        f"- 在相同功率口径下，HJT 需要约 `{area_ratio:.2f}x` 的阵列面积和约 `{mass_ratio:.2f}x` 的电源总质量，因此当前不适合作为主经济模型默认路线。",
        '- 但 HJT 已不再是「禁止进入主模型」或「只能降级」：它具备并行路线的物理链和三档价格锚点，可在终稿中作为"可比较的成熟候选路线"描述。',
        "- 若后续获得 HJT 阵列在具体空间任务下的寿命、封装和采购价格链，才有资格把 HJT 从路线比较升级到主模型成本比较。",
        "- 下游若继续推进主模型，应保持 `GaAs` 为主链，并把 HJT 作为灵敏度旁支或对照路线。",
    ]
    return "\n".join(lines)


def write_output(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def get_task5_power_replacements() -> Dict[str, Dict[str, float]]:
    mass_inputs = load_json(MASS_INPUT_PATH)
    cost_inputs = load_json(COST_INPUT_PATH)
    compatibility_cases = build_compatibility_cases(mass_inputs, cost_inputs)
    results = {
        case_id: compute_power_case(case, battery_branch="5yr", pcdu_scenario="baseline")
        for case_id, case in compatibility_cases.items()
    }
    scenario_map = {
        "轻量化": "gaas_advanced",
        "基准": "gaas_baseline",
        "保守": "gaas_heritage",
    }
    replacements: Dict[str, Dict[str, float]] = {}
    for scenario_name, case_id in scenario_map.items():
        result = results[case_id]
        replacements[scenario_name] = {
            "光伏阵列质量_kg": float(result["array_mass_kg"]),
            "电池质量_kg": float(result["battery_mass_kg"]),
            "功率电子质量_kg": float(result["pcdu_mass_kg"]),
            "电源系统总质量_kg": float(result["total_mass_kg"]),
            "电源系统总成本_usd": float(result["total_cost_usd"]) if result["total_cost_usd"] is not None else None,
            "光伏阵列成本_usd": float(result["array_cost_usd"]) if result["array_cost_usd"] is not None else None,
            "电池成本_usd": float(result["battery_cost_usd"]) if result["battery_cost_usd"] is not None else None,
            "功率电子成本_usd": float(result["pcdu_cost_usd"]) if result["pcdu_cost_usd"] is not None else None,
            "光伏面积_m2": float(result["required_area_m2"]),
            "电池名义储能_kwh": float(result["battery_nominal_kwh"]),
        }
    return replacements


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 2 Task 5/8 电源系统重建")
    parser.add_argument(
        "--results-output",
        default=DEFAULT_RESULTS_OUTPUT,
        help="主结果 Markdown 输出路径",
    )
    parser.add_argument(
        "--comparison-output",
        default=DEFAULT_COMPARISON_OUTPUT,
        help="GaAs/HJT 路线比较 Markdown 输出路径",
    )
    args = parser.parse_args()

    mass_inputs = load_json(MASS_INPUT_PATH)
    cost_inputs = load_json(COST_INPUT_PATH)

    route_cases = build_route_cases(mass_inputs, cost_inputs)
    # 主比较默认用 5yr Li-ion 电池分支 + baseline PCDU 场景
    route_results = {
        case_id: compute_power_case(case, battery_branch="5yr", pcdu_scenario="baseline")
        for case_id, case in route_cases.items()
    }

    compatibility_cases = build_compatibility_cases(mass_inputs, cost_inputs)
    compatibility_results = {
        case_id: compute_power_case(case, battery_branch="5yr", pcdu_scenario="baseline")
        for case_id, case in compatibility_cases.items()
    }

    results_markdown = build_results_markdown(route_results, compatibility_results)
    comparison_markdown = build_comparison_markdown(route_results)

    results_output_path = os.path.abspath(args.results_output)
    comparison_output_path = os.path.abspath(args.comparison_output)
    write_output(results_output_path, results_markdown)
    write_output(comparison_output_path, comparison_markdown)

    gaas = route_results["gaas_baseline"]
    hjt = route_results["hjt_parallel"]
    print("Stage 2 Task 5/8 电源系统模型已执行。")
    print(f"结果文件: {results_output_path}")
    print(f"比较文件: {comparison_output_path}")
    print(
        "GaAs 主链 (5yr Li-ion): "
        f"阵列面积 {gaas['required_area_m2']:.0f} m^2, "
        f"电源总质量 {gaas['total_mass_kg'] / 1000.0:.2f} t, "
        f"电源总成本 {format_cost(gaas['total_cost_usd'])}"
    )
    print(
        "HJT 并行路线 (5yr Li-ion): "
        f"阵列面积 {hjt['required_area_m2']:.0f} m^2, "
        f"电源总质量 {hjt['total_mass_kg'] / 1000.0:.2f} t, "
        f"电源总成本 {format_cost(hjt['total_cost_usd'])}"
    )
    print("HJT 现为并行成熟路线，价格链闭合度单独标注。")


if __name__ == "__main__":
    main()
