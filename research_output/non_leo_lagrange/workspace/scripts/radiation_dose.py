#!/usr/bin/env python3
"""
M2: 辐射剂量对比模型 (Radiation Dose Comparison Model)
======================================================
基于 Phase 1 的 TID 数据和 SEU 相对率，计算：
  - 各轨道 TID 累积曲线（5年/10年/15年）
  - 各轨道所需辐射加固等级（相对 LEO 的倍数）
  - 硬件寿命预期（基于 TID 失效阈值 100 krad 假设）
  - 辐射威胁综合排序

数据来源: .trae/specs/research-non-leo-lagrange/current-note.md Phase 1
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
# 输入参数 (来源: Phase 1 note)
# ============================================================

# TID 数据: (min, max) krad(Si)/年，带屏蔽
# 注意: L1/L2 的 TID 在屏蔽后仅为 2-5 krad/年（低于 LEO！）
TID_DATA = {
    "LEO (SSO 600km)":     (10, 30),
    "MEO (~20,200 km)":    (5, 15),
    "GEO (~35,786 km)":    (3, 10),
    "HEO (Molniya)":       (50, 200),
    "地日 L1":             (2, 5),
    "地日 L2":             (2, 5),
    "地月 L4/L5":          (5, 15),    # 估计值，置信度较低
    "地月 L1":             (5, 15),    # 估计值
    "地月 L2":             (5, 15),    # 估计值
}

# SEU 相对率 (以 LEO = 1x 为基准)
SEU_RELATIVE = {
    "LEO (SSO 600km)":     1,
    "MEO (~20,200 km)":    1e5,        # 10^5x
    "GEO (~35,786 km)":    5.5,        # ~1-10x 取几何中值 sqrt(10) ≈ 3.16, 偏向保守取 5.5
    "HEO (Molniya)":       3.16e5,     # 10^5-10^6x 取几何中值 sqrt(10)*1e5 ≈ 3.16e5
    "地日 L1":             316,        # 100-1000x 取几何中值 sqrt(100*1000) ≈ 316
    "地日 L2":             316,
    "地月 L4/L5":          22.4,       # 10-50x 取几何中值 sqrt(10*50) ≈ 22.4
    "地月 L1":             22.4,
    "地月 L2":             22.4,
}

# 辐射威胁权重
TID_WEIGHT = 0.4
SEU_WEIGHT = 0.6

# TID 失效阈值假设
TID_FAILURE = 100.0  # krad(Si) — 典型抗辐射加固器件阈值

# ============================================================
# 计算函数
# ============================================================

def tid_at_year(tid_range, year):
    """返回第 year 年的 TID 累积区间"""
    tid_min, tid_max = tid_range
    return (tid_min * year, tid_max * year)


def tid_hardening_factor(tid_range, leo_tid_range, threshold=TID_FAILURE):
    """计算所需辐射加固等级 = 该轨道 TID / LEO TID"""
    tid_mid = (tid_range[0] + tid_range[1]) / 2.0
    leo_mid = (leo_tid_range[0] + leo_tid_range[1]) / 2.0
    return tid_mid / leo_mid


def expected_lifetime(tid_range, threshold=TID_FAILURE):
    """基于 TID 失效阈值估算硬件寿命（年）"""
    tid_mid = (tid_range[0] + tid_range[1]) / 2.0
    if tid_mid == 0:
        return float("inf")
    return threshold / tid_mid


def has_reversed_tid(tid_range, leo_range):
    """检查该轨道 TID 是否低于 LEO（悖论：深空 TID 更低）"""
    return tid_range[1] < leo_range[0]


def threat_score(tid_range, seu_rel, leo_tid_range):
    """综合辐射威胁评分 (0-100)，越高越危险"""
    # TID 评分: 相对 LEO 的比例映射到 0-50
    tid_mid = (tid_range[0] + tid_range[1]) / 2.0
    leo_mid = (leo_tid_range[0] + leo_tid_range[1]) / 2.0
    tid_score = min(50, (tid_mid / leo_mid) * 25)

    # SEU 评分: 对数映射到 0-50
    if seu_rel <= 1:
        seu_score = 0
    else:
        seu_score = min(50, math.log10(seu_rel) * 10)

    return round(tid_score * TID_WEIGHT + seu_score * SEU_WEIGHT, 1)


def main():
    print("=" * 72)
    print("M2: 辐射剂量对比模型")
    print("=" * 72)

    orbits = list(TID_DATA.keys())
    leo_tid = TID_DATA["LEO (SSO 600km)"]

    results = []
    for orbit in orbits:
        tid = TID_DATA[orbit]
        seu = SEU_RELATIVE[orbit]

        # TID 累积
        tid_5yr = tid_at_year(tid, 5)
        tid_10yr = tid_at_year(tid, 10)
        tid_15yr = tid_at_year(tid, 15)

        # 加固等级
        hf = tid_hardening_factor(tid, leo_tid)

        # 硬件寿命
        lifetime = expected_lifetime(tid, TID_FAILURE)

        # 是否 TID 悖论
        reversed_tid = has_reversed_tid(tid, leo_tid)

        # 威胁评分
        ts = threat_score(tid, seu, leo_tid)

        results.append({
            "orbit": orbit,
            "tid_min_krad_yr": tid[0],
            "tid_max_krad_yr": tid[1],
            "tid_mid_krad_yr": round((tid[0] + tid[1]) / 2, 1),
            "seu_relative": seu,
            "seu_log10": round(math.log10(seu) if seu > 0 else 0, 2),
            "tid_5yr_min_krad": tid_5yr[0],
            "tid_5yr_max_krad": tid_5yr[1],
            "tid_10yr_min_krad": tid_10yr[0],
            "tid_10yr_max_krad": tid_10yr[1],
            "tid_15yr_min_krad": tid_15yr[0],
            "tid_15yr_max_krad": tid_15yr[1],
            "tid_vs_leo_factor": round(hf, 2),
            "expected_lifetime_yr": round(lifetime, 1) if lifetime != float("inf") else ">1000",
            "tid_below_leo": reversed_tid,
            "threat_score_100": ts,
        })

    # -------- 排序: 威胁从高到低 --------
    results.sort(key=lambda r: r["threat_score_100"], reverse=True)

    # -------- 输出 --------
    print(f"\n{'轨道':<22s} {'TID中值':>8s} {'SEU(log10)':>11s} "
          f"{'TIDvsLEO':>9s} {'寿命(yr)':>8s} {'TID<LEO':>7s} {'威胁分':>7s}")
    print("-" * 78)
    for r in results:
        print(f"{r['orbit']:<22s} {r['tid_mid_krad_yr']:>7.1f} k "
              f"{r['seu_log10']:>9.2f} "
              f"{r['tid_vs_leo_factor']:>8.2f}x "
              f"{str(r['expected_lifetime_yr']):>8s} "
              f"{'是' if r['tid_below_leo'] else '否':>6s} "
              f"{r['threat_score_100']:>6.1f}")

    print(f"\n--- TID 累积曲线 (krad) ---")
    print(f"{'轨道':<22s} {'5yr':>12s} {'10yr':>12s} {'15yr':>12s} {'超阈值?':>8s}")
    print("-" * 70)
    for r in results:
        over = "是" if isinstance(r['expected_lifetime_yr'], str) else (
            "是" if r['expected_lifetime_yr'] < 15 else "否"
        )
        print(f"{r['orbit']:<22s} "
              f"{r['tid_5yr_min_krad']:.0f}-{r['tid_5yr_max_krad']:.0f} "
              f"{r['tid_10yr_min_krad']:.0f}-{r['tid_10yr_max_krad']:.0f} "
              f"{r['tid_15yr_min_krad']:.0f}-{r['tid_15yr_max_krad']:.0f} "
              f"{over:>7s}")

    print(f"\nTID 失效阈值假设: {TID_FAILURE} krad(Si)")
    print(f"辐射威胁评分: TID 权重={TID_WEIGHT}, SEU 权重={SEU_WEIGHT}")

    print(f"\n--- TID 悖论说明 ---")
    paradox_orbits = [r for r in results if r["tid_below_leo"]]
    if paradox_orbits:
        for r in paradox_orbits:
            print(f"  {r['orbit']}: TID({r['tid_min_krad_yr']}-{r['tid_max_krad_yr']} krad/年) "
                  f"< LEO({leo_tid[0]}-{leo_tid[1]} krad/年)")
        print(f"\n  解释: 深空无 SAA 捕获质子贡献 TID，屏蔽后剂量反而更低。")
        print(f"  但这不意味深空对电子器件更友好——SEU 高出 2-6 个数量级。")

    # -------- 保存 --------
    csv_path = os.path.join(DATA_DIR, "m2_radiation_dose.csv")
    json_path = os.path.join(DATA_DIR, "m2_radiation_dose.json")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[INFO] 结果已保存: {csv_path}")
    print(f"[INFO] 结果已保存: {json_path}")
    print("[INFO] M2 完成。")
    return results


if __name__ == "__main__":
    main()
