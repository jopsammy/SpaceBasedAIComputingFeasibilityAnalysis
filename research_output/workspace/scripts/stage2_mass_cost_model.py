#!/usr/bin/env python3
"""
第二阶段 Task 6/8：Blackwell 主线三分支经济模型

目标：
1. 在统一 Blackwell 口径下建立 `5年-GaAs`、`5年-HJT`、`10年-GaAs` 三分支；
2. 吸收 Task 6/7 的更新 JSON（质量输入含 component，价格输入含新 item_id 与分寿命分支）；
3. 输出三分支结果文档与上一轮结果映射文档；
4. 废弃 kW/t 反推链，直接从 components 读取计算载荷质量；
5. 电池分支化（5yr NMC / 10yr Li-ion NMC / 10yr LTO），LTO 作为额外敏感性分支。
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from stage2_power_system_model import (
    build_route_cases,
    compute_power_case,
    load_json,
)


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")
MASS_INPUT_PATH = os.path.join(DATA_DIR, "stage2_mass_inputs_blackwell_hjt.json")
COST_INPUT_PATH = os.path.join(DATA_DIR, "stage2_cost_inputs_blackwell_hjt.json")
DEFAULT_BRANCH_OUTPUT = os.path.join(DATA_DIR, "stage2_economic_branches_blackwell.md")
DEFAULT_MAPPING_OUTPUT = os.path.join(DATA_DIR, "stage2_branch_mapping_from_previous_round.md")

TARGET_IT_LOAD_KW = 1000.0
HORIZON_YEARS = 10
ANNUAL_OPS_COST_USD = 5_000_000.0
DEORBIT_COST_PER_CONSTELLATION_USD = 3_000_000.0
LAUNCH_INSURANCE_RATE = 0.08
LAUNCH_COST_PER_KG_USD = {
    "light": 100.0,
    "baseline": 200.0,
    "conservative": 500.0,
}

PREVIOUS_ROUND_BASELINE = {
    "per_satellite_mass_kg": 7_570.0,
    "per_satellite_cost_usd": 68_940_000.0,
    "manufacturing_plus_launch_usd": 587_100_000.0,
    "orbital_tco_usd": 681_000_000.0,
    "rubin_manufacturing_plus_launch_usd": 203_000_000.0,
    "ground_mid_tco_usd": 64_600_000.0,
}


@dataclass(frozen=True)
class PowerSnapshot:
    label: str
    route: str
    status: str
    evidence_grade: str
    required_area_m2: float
    battery_nominal_kwh: float
    array_mass_kg: float
    battery_mass_kg: float
    pcdu_mass_kg: float
    total_power_mass_kg: float
    array_cost_usd: Optional[float]
    battery_cost_usd: Optional[float]
    pcdu_cost_usd: Optional[float]
    total_power_cost_usd: Optional[float]
    cost_chain_status: str
    remaining_gap: str
    battery_branch: str = "5yr"
    pcdu_scenario: str = "baseline"


@dataclass(frozen=True)
class BranchConfig:
    branch_id: str
    label: str
    route: str
    lifetime_years: int
    power_key: str
    battery_branch: str
    branch_role: str


@dataclass
class BranchResult:
    config: BranchConfig
    satellites_per_generation: float
    generations: int
    replacements: int
    per_satellite_mass_kg: float
    per_satellite_cost_usd: Optional[float]
    per_satellite_cost_floor_usd: float
    total_mass_per_generation_kg: float
    total_launch_cost_usd: float
    total_launch_insurance_usd: float
    total_manufacturing_cost_usd: Optional[float]
    total_manufacturing_cost_floor_usd: float
    total_ops_usd: float
    total_deorbit_usd: float
    total_lifecycle_cost_usd: Optional[float]
    total_lifecycle_cost_floor_usd: float
    missing_cost_items: List[str]
    mass_breakdown: Dict[str, float]
    cost_breakdown: Dict[str, Optional[float]]
    known_cost_breakdown: Dict[str, float]
    power: PowerSnapshot
    launch_cost_per_kg_usd: float


BRANCHES = [
    BranchConfig(
        branch_id="5y_gaas",
        label="5年-GaAs",
        route="GaAs",
        lifetime_years=5,
        power_key="gaas_baseline",
        battery_branch="5yr",
        branch_role="主模型分支；5年寿命后自动坠毁并按同口径重射一次。电池用 NMC Li-ion（DoD 40%）。",
    ),
    BranchConfig(
        branch_id="5y_hjt",
        label="5年-HJT",
        route="HJT",
        lifetime_years=5,
        power_key="hjt_parallel",
        battery_branch="5yr",
        branch_role="并行成熟路线分支；保留质量/发射账，完整成本单独标注闭合度。电池用 NMC Li-ion（DoD 40%）。",
    ),
    BranchConfig(
        branch_id="10y_gaas",
        label="10年-GaAs",
        route="GaAs",
        lifetime_years=10,
        power_key="gaas_baseline",
        battery_branch="10yr_liion",
        branch_role="主模型分支；10年寿命内不做整星重射。电池用 Li-ion NMC（DoD 25%）；LTO 为额外敏感性分支。",
    ),
]


def get_cost_item(cost_inputs: Dict[str, object], item_id: str) -> Dict[str, object]:
    for item in cost_inputs["items"]:
        if item["item_id"] == item_id:
            return item
    raise KeyError(f"未找到价格项: {item_id}")


def get_cost_value(
    cost_inputs: Dict[str, object],
    item_id: str,
    preferred_key: str = "baseline",
    fallback_keys: Tuple[str, ...] = (),
    branch: Optional[str] = None,
) -> Optional[float]:
    """读取成本项的值。支持分寿命分支（branches 字段）。"""
    item = get_cost_item(cost_inputs, item_id)
    if branch and "branches" in item:
        values = item["branches"][branch]["values"]
    else:
        values = item["values"]
    keys = (preferred_key,) + fallback_keys
    for key in keys:
        if key in values:
            return float(values[key])
    return None


def get_component_mass(
    mass_inputs: Dict[str, object],
    component_id: str,
    scenario_key: str = "baseline",
) -> float:
    """从 mass_inputs['components'] 中按 scenario_key 读取组件质量（替代废弃的 kW/t 链）。"""
    for comp in mass_inputs["components"]:
        if comp["id"] == component_id:
            return float(comp["scenario_mass_kg"][scenario_key])
    raise KeyError(f"未找到组件: {component_id}")


def format_t(value_kg: float) -> str:
    return f"{value_kg / 1000.0:.2f} t"


def format_musd(value_usd: float) -> str:
    return f"${value_usd / 1_000_000:.2f}M"


def format_cost_or_unknown(value_usd: Optional[float]) -> str:
    if value_usd is None:
        return "当前不可判定"
    return format_musd(value_usd)


def format_floor_or_exact(exact_value: Optional[float], floor_value: float) -> str:
    if exact_value is not None:
        return format_musd(exact_value)
    return f">= {format_musd(floor_value)}"


def compute_branch(
    config: BranchConfig,
    mass_inputs: Dict[str, object],
    scalars: Dict[str, object],
    cost_inputs: Dict[str, object],
    route_cases: Dict[str, object],
    launch_cost_per_kg_usd: float,
) -> BranchResult:
    """计算单条经济分支。

    Args:
        config: 分支配置（含 battery_branch）。
        mass_inputs: 质量输入 JSON。
        scalars: 场景标量（按寿命分支选取 scenario_scalars 或 scenario_scalars_10yr）。
        cost_inputs: 价格输入 JSON。
        route_cases: build_route_cases 的返回值。
        launch_cost_per_kg_usd: 发射单价。
    """
    public_baseline = mass_inputs["common_inputs"]["public_baseline"]
    sustained_power_kw = float(public_baseline["sustained_power_kw"])
    radiator_area_m2 = float(public_baseline["radiator_area_m2"])

    # 电源计算（带电池分支）
    route_case = route_cases[config.power_key]
    power_result = compute_power_case(route_case, battery_branch=config.battery_branch)

    power = PowerSnapshot(
        label=route_case.label,
        route=route_case.route,
        status=route_case.status,
        evidence_grade=route_case.evidence_grade,
        required_area_m2=float(power_result["required_area_m2"]),
        battery_nominal_kwh=float(power_result["battery_nominal_kwh"]),
        array_mass_kg=float(power_result["array_mass_kg"]),
        battery_mass_kg=float(power_result["battery_mass_kg"]),
        pcdu_mass_kg=float(power_result["pcdu_mass_kg"]),
        total_power_mass_kg=float(power_result["total_mass_kg"]),
        array_cost_usd=power_result["array_cost_usd"],
        battery_cost_usd=power_result["battery_cost_usd"],
        pcdu_cost_usd=power_result["pcdu_cost_usd"],
        total_power_cost_usd=power_result["total_cost_usd"],
        cost_chain_status=route_case.cost_chain_status,
        remaining_gap=route_case.remaining_gap,
        battery_branch=config.battery_branch,
    )

    # 计算载荷质量 —— 从 components 直接读取（替代废弃的 kW/t 链）
    compute_mass_kg = get_component_mass(mass_inputs, "compute_payload", "baseline")

    # 质量链（除计算载荷外，其余仍从 scalars 读取）
    thermal_mass_kg = radiator_area_m2 * float(scalars["radiator_specific_mass_kg_per_m2"])
    platform_mass_kg = (
        compute_mass_kg + thermal_mass_kg + power.total_power_mass_kg
    ) * float(scalars["platform_ratio"])
    propulsion_mass_kg = float(scalars["propulsion_mass_kg"])
    comms_mass_kg = float(scalars["comms_mass_kg"])
    subtotal_without_margin_kg = (
        compute_mass_kg
        + thermal_mass_kg
        + power.total_power_mass_kg
        + platform_mass_kg
        + propulsion_mass_kg
        + comms_mass_kg
    )
    # AIT 裕量 —— 按寿命分支选取（5yr 用 scenario_scalars，10yr 用 scenario_scalars_10yr）
    ait_margin_mass_kg = subtotal_without_margin_kg * float(scalars["ait_margin_ratio"])
    per_satellite_mass_kg = subtotal_without_margin_kg + ait_margin_mass_kg

    # 成本链 —— 使用新 item_id
    lifetime_branch_key = f"{config.lifetime_years}yr"

    compute_cost_usd = sustained_power_kw * float(
        get_cost_value(cost_inputs, "compute_payload_cost_per_kw", "baseline") or 0.0
    )
    thermal_cost_usd = radiator_area_m2 * float(
        get_cost_value(cost_inputs, "thermal_cost_per_m2", "baseline") or 0.0
    )
    platform_cost_usd = platform_mass_kg * float(
        get_cost_value(cost_inputs, "platform_structure_cost_per_kg", "baseline") or 0.0
    )
    propulsion_cost_usd = float(
        get_cost_value(cost_inputs, "propulsion_total_cost_per_sat", "baseline",
                       branch=lifetime_branch_key) or 0.0
    )
    comms_cost_usd = float(
        get_cost_value(cost_inputs, "comms_total_cost_per_sat", "baseline") or 0.0
    )
    ait_cost_ratio = float(
        get_cost_value(cost_inputs, "ait_cost_ratio", "baseline",
                       branch=lifetime_branch_key) or 0.0
    )

    # 电源成本已知项求和
    known_power_cost_usd = sum(
        value for value in [power.array_cost_usd, power.battery_cost_usd, power.pcdu_cost_usd]
        if value is not None
    )
    missing_cost_items: List[str] = []
    if power.array_cost_usd is None:
        missing_cost_items.append(f"{power.route} 阵列采购价格链")
    if power.battery_cost_usd is None:
        missing_cost_items.append(f"电池采购价（{config.battery_branch}）")
    if power.pcdu_cost_usd is None:
        missing_cost_items.append("空间级 PCDU 采购价")

    subtotal_known_cost_usd = (
        compute_cost_usd
        + thermal_cost_usd
        + known_power_cost_usd
        + platform_cost_usd
        + propulsion_cost_usd
        + comms_cost_usd
    )
    ait_cost_floor_usd = subtotal_known_cost_usd * ait_cost_ratio
    per_satellite_cost_floor_usd = subtotal_known_cost_usd + ait_cost_floor_usd

    per_satellite_cost_usd: Optional[float] = None
    if not missing_cost_items and power.total_power_cost_usd is not None:
        subtotal_full_cost_usd = (
            compute_cost_usd
            + thermal_cost_usd
            + power.total_power_cost_usd
            + platform_cost_usd
            + propulsion_cost_usd
            + comms_cost_usd
        )
        per_satellite_cost_usd = subtotal_full_cost_usd + subtotal_full_cost_usd * ait_cost_ratio

    satellites_per_generation = TARGET_IT_LOAD_KW / sustained_power_kw
    generations = int(math.ceil(HORIZON_YEARS / config.lifetime_years))
    replacements = generations - 1

    total_mass_per_generation_kg = per_satellite_mass_kg * satellites_per_generation
    total_launch_cost_usd = total_mass_per_generation_kg * launch_cost_per_kg_usd * generations
    total_launch_insurance_usd = total_launch_cost_usd * LAUNCH_INSURANCE_RATE
    total_manufacturing_cost_floor_usd = per_satellite_cost_floor_usd * satellites_per_generation * generations
    total_manufacturing_cost_usd = (
        None
        if per_satellite_cost_usd is None
        else per_satellite_cost_usd * satellites_per_generation * generations
    )
    total_ops_usd = ANNUAL_OPS_COST_USD * HORIZON_YEARS
    total_deorbit_usd = DEORBIT_COST_PER_CONSTELLATION_USD * generations
    total_lifecycle_cost_floor_usd = (
        total_manufacturing_cost_floor_usd
        + total_launch_cost_usd
        + total_launch_insurance_usd
        + total_ops_usd
        + total_deorbit_usd
    )
    total_lifecycle_cost_usd = (
        None
        if total_manufacturing_cost_usd is None
        else total_manufacturing_cost_usd
        + total_launch_cost_usd
        + total_launch_insurance_usd
        + total_ops_usd
        + total_deorbit_usd
    )

    mass_breakdown = {
        "计算载荷": compute_mass_kg,
        "散热系统": thermal_mass_kg,
        "光伏阵列": power.array_mass_kg,
        "电池": power.battery_mass_kg,
        "功率电子/配电": power.pcdu_mass_kg,
        "平台/结构": platform_mass_kg,
        "推进": propulsion_mass_kg,
        "通信/激光链路": comms_mass_kg,
        "集成测试/冗余": ait_margin_mass_kg,
    }
    cost_breakdown: Dict[str, Optional[float]] = {
        "计算载荷": compute_cost_usd,
        "散热系统": thermal_cost_usd,
        "光伏阵列": power.array_cost_usd,
        "电池": power.battery_cost_usd,
        "功率电子/配电": power.pcdu_cost_usd,
        "平台/结构": platform_cost_usd,
        "推进": propulsion_cost_usd,
        "通信/激光链路": comms_cost_usd,
        "集成测试/冗余": (
            None
            if missing_cost_items
            else (
                per_satellite_cost_usd  # type: ignore[operator]
                - compute_cost_usd
                - thermal_cost_usd
                - (power.total_power_cost_usd or 0.0)
                - platform_cost_usd
                - propulsion_cost_usd
                - comms_cost_usd
            )
        ),
    }
    known_cost_breakdown = {
        "计算载荷": compute_cost_usd,
        "散热系统": thermal_cost_usd,
        "光伏阵列": power.array_cost_usd or 0.0,
        "电池": power.battery_cost_usd or 0.0,
        "功率电子/配电": power.pcdu_cost_usd or 0.0,
        "平台/结构": platform_cost_usd,
        "推进": propulsion_cost_usd,
        "通信/激光链路": comms_cost_usd,
        "集成测试/冗余": ait_cost_floor_usd,
    }

    return BranchResult(
        config=config,
        satellites_per_generation=satellites_per_generation,
        generations=generations,
        replacements=replacements,
        per_satellite_mass_kg=per_satellite_mass_kg,
        per_satellite_cost_usd=per_satellite_cost_usd,
        per_satellite_cost_floor_usd=per_satellite_cost_floor_usd,
        total_mass_per_generation_kg=total_mass_per_generation_kg,
        total_launch_cost_usd=total_launch_cost_usd,
        total_launch_insurance_usd=total_launch_insurance_usd,
        total_manufacturing_cost_usd=total_manufacturing_cost_usd,
        total_manufacturing_cost_floor_usd=total_manufacturing_cost_floor_usd,
        total_ops_usd=total_ops_usd,
        total_deorbit_usd=total_deorbit_usd,
        total_lifecycle_cost_usd=total_lifecycle_cost_usd,
        total_lifecycle_cost_floor_usd=total_lifecycle_cost_floor_usd,
        missing_cost_items=missing_cost_items,
        mass_breakdown=mass_breakdown,
        cost_breakdown=cost_breakdown,
        known_cost_breakdown=known_cost_breakdown,
        power=power,
        launch_cost_per_kg_usd=launch_cost_per_kg_usd,
    )


def build_branch_summary_table(results: Dict[str, BranchResult]) -> str:
    lines = [
        "| 分支 | 路线 | 电池分支 | 生命周期 | 代数 | 单星总质量 | 单星制造成本 | 10年总制造成本 | 10年总发射成本 | 10年总成本 | 备注 |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    order = ["5y_gaas", "5y_hjt", "10y_gaas"]
    for branch_id in order:
        result = results[branch_id]
        lines.append(
            f"| {result.config.label} | {result.config.route} | "
            f"{result.config.battery_branch} | "
            f"{result.config.lifetime_years} 年 | "
            f"{result.generations} | {format_t(result.per_satellite_mass_kg)} | "
            f"{format_floor_or_exact(result.per_satellite_cost_usd, result.per_satellite_cost_floor_usd)} | "
            f"{format_floor_or_exact(result.total_manufacturing_cost_usd, result.total_manufacturing_cost_floor_usd)} | "
            f"{format_musd(result.total_launch_cost_usd)} | "
            f"{format_floor_or_exact(result.total_lifecycle_cost_usd, result.total_lifecycle_cost_floor_usd)} | "
            f"{result.config.branch_role} |"
        )
    return "\n".join(lines)


def build_branch_assumption_table(results: Dict[str, BranchResult]) -> str:
    lines = [
        "| 分支 | 单代卫星当量 | 更替次数 | 电源路线状态 | 电池分支 | 发射单价 | 关键边界 |",
        "|---|---:|---:|---|---:|---:|---|",
    ]
    order = ["5y_gaas", "5y_hjt", "10y_gaas"]
    for branch_id in order:
        result = results[branch_id]
        lines.append(
            f"| {result.config.label} | {result.satellites_per_generation:.2f} | {result.replacements} | "
            f"{result.power.status} / {result.power.cost_chain_status} | "
            f"{result.config.battery_branch} | "
            f"${result.launch_cost_per_kg_usd:.0f}/kg | {result.power.remaining_gap} |"
        )
    return "\n".join(lines)


def build_single_satellite_tables(results: Dict[str, BranchResult]) -> str:
    blocks: List[str] = []
    order = ["5y_gaas", "5y_hjt", "10y_gaas"]
    for branch_id in order:
        result = results[branch_id]
        lines = [
            f"### {result.config.label}（电池分支：{result.config.battery_branch}）",
            "",
            "| 子系统 | 质量 | 制造成本 |",
            "|---|---:|---:|",
        ]
        for key in [
            "计算载荷",
            "散热系统",
            "光伏阵列",
            "电池",
            "功率电子/配电",
            "平台/结构",
            "推进",
            "通信/激光链路",
            "集成测试/冗余",
        ]:
            lines.append(
                f"| {key} | {result.mass_breakdown[key]:,.0f} kg | "
                f"{format_cost_or_unknown(result.cost_breakdown[key])} |"
            )
        lines.append(
            f"| 合计 | {result.per_satellite_mass_kg:,.0f} kg | "
            f"{format_floor_or_exact(result.per_satellite_cost_usd, result.per_satellite_cost_floor_usd)} |"
        )
        if result.missing_cost_items:
            lines.extend(
                [
                    "",
                    f"- 缺口项：`{'`、`'.join(result.missing_cost_items)}`。",
                    f"- 当前只可给出制造成本下界 `{format_musd(result.per_satellite_cost_floor_usd)}`，不能给出完整总额。",
                ]
            )
        else:
            lines.extend(
                [
                    "",
                    f"- 当前路线质量链状态：`{result.power.status}`；完整制造成本可用于后续总账。",
                ]
            )
        # HJT 特殊说明
        if branch_id == "5y_hjt":
            lines.append(
                "- HJT 现为并行成熟路线（非「禁止进入主模型」），物理链可比较，价格链闭合度单独标注。"
            )
        if branch_id == "10y_gaas":
            lines.append(
                "- 与 `5年-GaAs` 的单星物理配置保持一致（除电池分支与 AIT 裕量外），"
                "不额外假设新的 Rubin 或 HJT 参数。"
                " LTO 电池（DoD 80%）为额外敏感性分支，未纳入主模型。"
            )
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def build_launch_sensitivity_table(results: Dict[str, BranchResult]) -> str:
    lines = [
        "| 分支 | `$100/kg` | `$200/kg` | `$500/kg` | 说明 |",
        "|---|---:|---:|---:|---|",
    ]
    order = ["5y_gaas", "5y_hjt", "10y_gaas"]
    for branch_id in order:
        result = results[branch_id]
        per_generation_mass = result.total_mass_per_generation_kg
        generations = result.generations
        values = []
        for key in ["light", "baseline", "conservative"]:
            launch_total = per_generation_mass * LAUNCH_COST_PER_KG_USD[key] * generations
            values.append(format_musd(launch_total))
        lines.append(
            f"| {result.config.label} | {values[0]} | {values[1]} | {values[2]} | "
            f"总质量按 `{format_t(per_generation_mass)}`/代计算，共 `{generations}` 代 |"
        )
    return "\n".join(lines)


def build_branch_delta_table(results: Dict[str, BranchResult]) -> str:
    baseline = results["10y_gaas"]
    lines = [
        "| 分支 | 相对 `10年-GaAs` 的总制造成本差异 | 相对 `10年-GaAs` 的总发射成本差异 | 相对 `10年-GaAs` 的总成本差异 | 差异来源 |",
        "|---|---:|---:|---:|---|",
    ]
    for branch_id in ["5y_gaas", "5y_hjt"]:
        result = results[branch_id]
        manufacturing_delta = None
        if result.total_manufacturing_cost_usd is not None and baseline.total_manufacturing_cost_usd is not None:
            manufacturing_delta = result.total_manufacturing_cost_usd - baseline.total_manufacturing_cost_usd
        lifecycle_delta = None
        if result.total_lifecycle_cost_usd is not None and baseline.total_lifecycle_cost_usd is not None:
            lifecycle_delta = result.total_lifecycle_cost_usd - baseline.total_lifecycle_cost_usd
        lines.append(
            f"| {result.config.label} | "
            f"{format_cost_or_unknown(manufacturing_delta)} | "
            f"{format_musd(result.total_launch_cost_usd - baseline.total_launch_cost_usd)} | "
            f"{format_cost_or_unknown(lifecycle_delta)} | "
            f"{'寿命缩短导致整星重射一次' if result.config.route == 'GaAs' else 'HJT 额外质量放大发射账'}"
        )
    return "\n".join(lines)


def build_branch_markdown(results: Dict[str, BranchResult]) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    baseline = results["10y_gaas"]
    gaas_5y = results["5y_gaas"]
    hjt_5y = results["5y_hjt"]
    return f"""# Stage 2 Task 6/8：Blackwell 主线三分支经济模型

## 说明

- 生成时间：`{now}`
- 任务定位：服务于 Task 6/8，吸收 Task 6 的质量输入（含废弃 kW/t 链、新 component 结构）与 Task 7 的价格输入（含新 item_id、电池 NMC/LTO 成本、分寿命 branch 字段）。
- 三个允许分支：`5年-GaAs`、`5年-HJT`、`10年-GaAs`。
- 生命周期口径：以 `1 MW` 持续 IT 负载、`10 年` 总窗口为共同分母；其中 `5年` 分支显式执行"5 年服役后自动坠毁并重射一次"的规则。
- 电池分支：5yr NMC Li-ion（DoD 40%，$200/kWh）、10yr Li-ion NMC（DoD 25%，$200/kWh）。LTO（DoD 80%，$350/kWh）为额外敏感性分支。
- 边界约束：`Rubin` 不重新进入主模型；`HJT` 现为并行成熟路线（非「禁止进入主模型」），价格链闭合度单独标注。
- **废弃项**：计算载荷质量不再使用 kW/t 反推链（70/55/45 kW/t 已废弃），改为从 `components[compute_payload].scenario_mass_kg` 直接读取（V30 bottom-up 拆解）。

## 一、先行结论

- `10年-GaAs`（电池 10yr Li-ion NMC）当前是三分支里唯一可完整给出 10 年总成本的单代主链，其基线总成本约为 `{format_musd(baseline.total_lifecycle_cost_usd or 0.0)}`。
- `5年-GaAs`（电池 5yr NMC）在同一 `1 MW / 10年` 分母下，需要整星重射一次，导致总制造成本与总发射成本近似翻倍，基线总成本抬升到 `{format_musd(gaas_5y.total_lifecycle_cost_usd or 0.0)}`。
- `5年-HJT`（电池 5yr NMC）的单星质量高于 `GaAs`，因此发射账更重；HJT 阵列采购价格链有三档地面 HJT 锚点 + 10-15× 空间放大，但闭合度低于 GaAs。当前可给出总成本下界 `{format_musd(hjt_5y.total_lifecycle_cost_floor_usd)}`。
- 与上一轮 `统一 Blackwell 基准` 相比，本轮最大的结构变化：① 废弃 kW/t 反推链；② 电池分支化（5yr/10yr Li-ion/LTO）；③ 成本 item_id 更新（`battery_cost_per_kwh_nmc` / `battery_cost_per_kwh_lto`）；④ 推进与 AIT 成本按寿命分支选取。

## 二、分支假设

{build_branch_assumption_table(results)}

## 三、分支总览

{build_branch_summary_table(results)}

## 四、单星基线拆解

{build_single_satellite_tables(results)}

## 五、10 年窗口总账差异

{build_branch_delta_table(results)}

## 六、发射单价敏感性

{build_launch_sensitivity_table(results)}

## 七、计算链

```text
计算载荷质量 = components[compute_payload].scenario_mass_kg[baseline]  ← 新：替代废弃的 kW/t 链
单代卫星当量 = 目标持续 IT 负载 / 单星持续 IT 负载
总代数 = ceil(10 年窗口 / 分支寿命)
总制造成本 = 单星制造成本 * 单代卫星当量 * 总代数
总发射成本 = 单星总质量 * 单代卫星当量 * 发射单价 * 总代数
总保险 = 总发射成本 * 8%
总运维 = 5 MUSD/年 * 10 年
总退役/再入 = 3 MUSD/代 * 总代数
10 年总成本 = 总制造成本 + 总发射成本 + 总保险 + 总运维 + 总退役/再入
```

## 八、当前不可判定项

- `5年-HJT` 的完整总成本当前不可判定（HJT 阵列采购价格链有三档锚点但闭合度低于 GaAs，不是无证据）。
- `10年-GaAs` 当前只把"寿命延长后不重射"写入总账，没有额外假定公开可证实的 10 年寿命增重或增价因子；这属于保守占位，而不是已证实硬件事实。
- LTO 电池分支为额外敏感性（四档等比压缩法），未纳入主模型默认值。
- 电池与 `PCDU` 单价继续沿用合理推断/迁移证据（三档/四档），因此所有分支的成本链仍需保留"非一手采购价"的降级标签。

## 九、对下游的交接输入

- 主终稿应优先引用 `10年-GaAs`（电池 10yr Li-ion NMC）作为当前最完整主链结果，并将 `5年-GaAs` 作为寿命敏感性对照。
- `5年-HJT` 应写成"已形成物理链和发射账、但完整成本未闭合"的并行成熟分支。
- LTO 电池分支预留为敏感性分析支线。
- 上一轮映射关系已单独写入 `stage2_branch_mapping_from_previous_round.md`，便于终稿保留继承链。
"""


def build_mapping_table(results: Dict[str, BranchResult]) -> str:
    baseline = results["10y_gaas"]
    gaas_5y = results["5y_gaas"]
    hjt_5y = results["5y_hjt"]
    current_mfg_launch = (
        (baseline.total_manufacturing_cost_usd or 0.0)
        + baseline.total_launch_cost_usd
    )
    gaas_5y_mfg_launch = (
        (gaas_5y.total_manufacturing_cost_usd or 0.0)
        + gaas_5y.total_launch_cost_usd
    )
    return "\n".join(
        [
            "| 上一轮资产/数字 | 来源文件 | 本轮映射去向 | 当前关系 | 说明 |",
            "|---|---|---|---|---|",
            f"| 单星基准 `7.57 t / 68.94 MUSD` | `stage2_mass_cost_results.md` | `10年-GaAs` 单星基线 | 近似继承 | 当前脚本已切换到新 component 结构（计算载荷 1,500 kg）和 Task 7 新 item_id，基线单星制造成本更新为 `{format_musd(baseline.per_satellite_cost_usd or 0.0)}`。 |",
            f"| 统一 `Blackwell` 基准 `587.1 MUSD`（制造+发射） | `stage2_architecture_reconciliation.md` | `10年-GaAs` 10 年制造+发射总账 | 直接映射并微调 | 当前值为 `{format_musd(current_mfg_launch)}`，差异主要来自 component 结构、新电池成本 item_id 和寿命分支化。 |",
            f"| 原 paper 当前 `681.0 MUSD / MW / 10年` | `tco_comparison_results.txt` | `10年-GaAs` 全生命周期总账 | 可比但不完全同模 | 当前 `10年-GaAs` 全生命周期约 `{format_musd(baseline.total_lifecycle_cost_usd or 0.0)}`；两者同属 `Blackwell` 主线，但旧模型使用的是更粗颗粒的轨道 TCO 聚合式假设。 |",
            f"| 上一轮未显式展开的 5 年寿命假设 | `第二阶段差异与验证思路.md` | `5年-GaAs` | 本轮新增显式分支 | 当前 `5年-GaAs` 的 10 年制造+发射总账为 `{format_musd(gaas_5y_mfg_launch)}`，比 `10年-GaAs` 高出一次整星重射成本。 |",
            f"| `Rubin` 统一复算基准 `203.0 MUSD`（制造+发射） | `stage2_architecture_reconciliation.md` | 不进入 Task 6/8 主模型 | 降级保留 | 本轮只保留其支线审计作用，不再参与三分支主计算。 |",
            f"| 上一轮无 HJT 主经济分支 | 无直接对应 | `5年-HJT` | 本轮新增并行成熟分支 | 当前可映射到 `{format_musd(hjt_5y.total_launch_cost_usd)}` 级别的发射账与 `{format_musd(hjt_5y.total_lifecycle_cost_floor_usd)}` 的总成本下界；HJT 现为并行成熟路线。 |",
        ]
    )


def build_branch_vs_previous_table(results: Dict[str, BranchResult]) -> str:
    baseline = results["10y_gaas"]
    gaas_5y = results["5y_gaas"]
    hjt_5y = results["5y_hjt"]
    lines = [
        "| 当前分支 | 相对上一轮 `统一 Blackwell 基准` 制造+发射差异 | 相对上一轮 `681.0 MUSD` TCO 差异 | 当前解释 |",
        "|---|---:|---:|---|",
        f"| 10年-GaAs | {format_musd(((baseline.total_manufacturing_cost_usd or 0.0) + baseline.total_launch_cost_usd) - PREVIOUS_ROUND_BASELINE['manufacturing_plus_launch_usd'])} | {format_musd((baseline.total_lifecycle_cost_usd or 0.0) - PREVIOUS_ROUND_BASELINE['orbital_tco_usd'])} | 基本承接上一轮 Blackwell 基准，差异主要来自 component 结构、电池分支化与成本 item_id 更新。 |",
        f"| 5年-GaAs | {format_musd(((gaas_5y.total_manufacturing_cost_usd or 0.0) + gaas_5y.total_launch_cost_usd) - PREVIOUS_ROUND_BASELINE['manufacturing_plus_launch_usd'])} | {format_musd((gaas_5y.total_lifecycle_cost_usd or 0.0) - PREVIOUS_ROUND_BASELINE['orbital_tco_usd'])} | 差异主要来自寿命缩短导致的整星重造与重射。 |",
        f"| 5年-HJT | 当前不可判定 | 当前不可判定 | HJT 阵列采购链闭合度低于 GaAs，只能确认发射账与总成本下界。 |",
    ]
    return "\n".join(lines)


def build_mapping_markdown(results: Dict[str, BranchResult]) -> str:
    now = datetime.now().isoformat(timespec="seconds")
    return f"""# Stage 2 Task 6/8：与上一轮结果的分支映射

## 说明

- 生成时间：`{now}`
- 文档定位：说明 `Task 6/8` 的三分支结果如何承接上一轮 `Blackwell/Rubin`、`质量/制造成本` 与 `TCO` 结果，避免前后两轮断链。
- 写法边界：只做映射与差异说明，不把上一轮支线结果重新升格为本轮主模型。

## 一、映射总表

{build_mapping_table(results)}

## 二、当前分支对上一轮数字的影响

{build_branch_vs_previous_table(results)}

## 三、收束判断

- 上一轮 `统一 Blackwell 基准` 最自然地映射到本轮 `10年-GaAs`，因为二者都代表"Blackwell 主线 + GaAs 主链 + 10 年窗口"。
- 本轮真正新增的不是新的架构主线，而是：① 废弃 kW/t 链改为 component 直读；② 电池分支化；③ 成本 item_id 更新与分支化。
- `Rubin` 继续只保留为支线留痕。
- `HJT` 现为并行成熟路线（非「禁止进入主模型」），其映射关系到"质量/发射账 + 已知成本下界"。

## 四、仍需在终稿保留的提示

- 当根目录终稿回写结果时，应明确写出：`10年-GaAs` 承接上一轮主链，`5年-GaAs` 是寿命敏感性放大分支，`5年-HJT` 为未闭合成本的并行成熟路线。
- 若需要引用上一轮 `681.0 MUSD`，必须同时说明它来自旧的聚合式轨道 TCO 模型，而本轮已经改成 Task 6/7 驱动的分项链。
"""


def write_output(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stage 2 Task 6/8 三分支经济模型")
    parser.add_argument(
        "--branch-output",
        default=DEFAULT_BRANCH_OUTPUT,
        help="三分支结果 Markdown 输出路径",
    )
    parser.add_argument(
        "--mapping-output",
        default=DEFAULT_MAPPING_OUTPUT,
        help="上一轮结果映射 Markdown 输出路径",
    )
    args = parser.parse_args()

    mass_inputs = load_json(MASS_INPUT_PATH)
    cost_inputs = load_json(COST_INPUT_PATH)

    route_cases = build_route_cases(mass_inputs, cost_inputs)

    results: Dict[str, BranchResult] = {}
    for config in BRANCHES:
        # 按寿命分支选取合适的 scalars（AIT 裕量不同）
        if config.lifetime_years == 5:
            scalars = mass_inputs["common_inputs"]["scenario_scalars"]["baseline"]
        else:
            scalars = mass_inputs["common_inputs"]["scenario_scalars_10yr"]["baseline"]

        results[config.branch_id] = compute_branch(
            config=config,
            mass_inputs=mass_inputs,
            scalars=scalars,
            cost_inputs=cost_inputs,
            route_cases=route_cases,
            launch_cost_per_kg_usd=LAUNCH_COST_PER_KG_USD["baseline"],
        )

    branch_markdown = build_branch_markdown(results)
    mapping_markdown = build_mapping_markdown(results)

    branch_output_path = os.path.abspath(args.branch_output)
    mapping_output_path = os.path.abspath(args.mapping_output)
    write_output(branch_output_path, branch_markdown)
    write_output(mapping_output_path, mapping_markdown)

    baseline = results["10y_gaas"]
    gaas_5y = results["5y_gaas"]
    hjt_5y = results["5y_hjt"]
    print("Stage 2 Task 6/8 三分支经济模型已执行。")
    print(f"三分支结果文件: {branch_output_path}")
    print(f"上一轮映射文件: {mapping_output_path}")
    print(f"10年-GaAs 基线总成本: {format_musd(baseline.total_lifecycle_cost_usd or 0.0)}")
    print(f"5年-GaAs 基线总成本: {format_musd(gaas_5y.total_lifecycle_cost_usd or 0.0)}")
    print(f"5年-HJT 当前总成本下界: {format_musd(hjt_5y.total_lifecycle_cost_floor_usd)}")
    print(f"计算载荷质量（components 直读）: {get_component_mass(mass_inputs, 'compute_payload', 'baseline'):,.0f} kg")
    print("HJT 现为并行成熟路线，价格链闭合度单独标注。")
    print("kW/t 反推链已废弃，不再使用。")


if __name__ == "__main__":
    main()
