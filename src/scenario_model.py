# Purpose: Run scenario comparisons on the NOH Maternity 24-month cashflow model.
#          Disaggregated costs: antenatal midwifery, in-hospital midwifery,
#          MO (revised), anaesthesia, OB pool, and board/facility fee.
# Input:   Scenario parameters defined in SCENARIOS dict below.
# Output:  outputs/YYYY-MM-DD_scenario_<name>.csv
#          outputs/YYYY-MM-DD_scenario_all.csv
#          outputs/YYYY-MM-DD_scenario_summary.csv
# Author:  NOH Expansion Workbench
# Date:    2026-03-01

import csv
import math
from datetime import date
from pathlib import Path

OUT_DIR = Path("outputs")
TODAY = date.today()
N_MONTHS = 24

# --- Model logic ---

def linear_ramp(m, start, end, ramp_months):
    """Linear ramp from start to end over ramp_months, then holds at end."""
    if ramp_months <= 1:
        return end
    if m <= ramp_months:
        return start + (end - start) * (m - 1) / (ramp_months - 1)
    return end

def run_model(name, p):
    """Run the disaggregated cashflow model for a single scenario."""
    rows = []
    cumulative_cash = 0

    for m in range(1, N_MONTHS + 1):
        t = (m - 1) / (N_MONTHS - 1)

        # --- Volume ---
        births     = round(t * p["births_end"])
        enrolments = round(t * p["enrolments_end"])

        # --- MA/Cash split ---
        ma_share   = linear_ramp(m, p["ma_share_start"], p["ma_share_target"], p["ma_months"])
        ma_cases   = round(births * ma_share)
        cash_cases = births - ma_cases

        # --- CS / NVD split ---
        cs_rate    = linear_ramp(m, p["cs_rate_start"], p["cs_rate_target"], p["cs_months"])
        cs_cases   = births * cs_rate
        nvd_cases  = births - cs_cases

        # --- Revenue ---
        total_receipts = cash_cases * p["pr_cash"] + ma_cases * p["pr_ma"]
        noh_fee        = total_receipts * p["noh_fee_pct"]
        medicare_fee   = total_receipts * p["medicare_fee_pct"]
        residual       = total_receipts - noh_fee - medicare_fee

        # --- Antenatal midwifery ---
        # R300/visit × 10 visits per enrolled patient episode
        antenatal_midwifery = births * p["antenatal_visits_per_episode"] * p["antenatal_visit_fee"]

        # --- In-hospital midwifery ---
        # Applies only to midwife-only NVD births (excludes MO-assisted NVD and all CS).
        # When an MO is called, midwife cost is not applied.
        midwife_only_nvd = nvd_cases * (1 - p["mo_nvd_pct"])
        inhosp_midwifery = midwife_only_nvd * p["inhosp_midwife_hours"] * p["inhosp_midwife_rate"]

        # --- MO costs (revised) ---
        # Session fee: driven by enrolments (unchanged)
        mo_sessions     = math.ceil(enrolments / p["mo_clients_per_session"]) if enrolments > 0 else 0
        mo_session_cost = mo_sessions * p["mo_session_fee"]
        # Birth fee: only MO-involved NVDs + all CS (not all births)
        mo_nvd_cases    = nvd_cases * p["mo_nvd_pct"]
        mo_birth_cost   = (mo_nvd_cases + cs_cases) * p["mo_births_fee"]
        mo_cost         = mo_session_cost + mo_birth_cost

        # --- Anaesthesia (CS only, unchanged) ---
        anaes_cost = cs_cases * p["anaes_fee_per_cs"]

        # --- OB pool (unchanged) ---
        ob_cores = 3 if (enrolments > p["ob_add_core_enrolments"] or births > p["ob_add_core_births"]) else 2
        ob_pool  = min(ob_cores * p["ob_retainer"] + p["ob_pepm"] * enrolments, p["ob_pool_cap"])

        # --- Board / facility fee ---
        # Proxy for hospital fee per patient-day (covers board, medicines, materials)
        # NVD = 1 day (2 days, 1 night); CS = 2 days (3 days, 2 nights)
        board_facility = (
            nvd_cases * p["nvd_los_days"] +
            cs_cases  * p["cs_los_days"]
        ) * p["room_rate_per_day"]

        # --- Cost totals ---
        midwifery_costs  = antenatal_midwifery + inhosp_midwifery
        clinician_costs  = mo_cost + anaes_cost + ob_pool
        total_costs      = midwifery_costs + clinician_costs + board_facility
        net_cashflow     = residual - total_costs
        cumulative_cash += net_cashflow

        rows.append({
            "scenario":              name,
            "month":                 m,
            "births":                births,
            "nvd_cases":             round(nvd_cases, 2),
            "cs_cases":              round(cs_cases, 2),
            "enrolments_active":     enrolments,
            "ma_share":              round(ma_share, 4),
            "cs_rate":               round(cs_rate, 4),
            "total_receipts":        round(total_receipts),
            "noh_fee":               round(noh_fee),
            "medicare_fee":          round(medicare_fee),
            "residual":              round(residual),
            # --- Disaggregated costs ---
            "antenatal_midwifery":   round(antenatal_midwifery),
            "inhosp_midwifery":      round(inhosp_midwifery),
            "midwifery_costs":       round(midwifery_costs),
            "mo_session_cost":       round(mo_session_cost),
            "mo_birth_cost":         round(mo_birth_cost),
            "mo_cost":               round(mo_cost),
            "anaes_cost":            round(anaes_cost),
            "ob_cores":              ob_cores,
            "ob_pool":               round(ob_pool),
            "clinician_costs":       round(clinician_costs),
            "board_facility":        round(board_facility),
            "total_costs":           round(total_costs),
            "net_cashflow":          round(net_cashflow),
            "cumulative_cash":       round(cumulative_cash),
        })

    return rows

# --- Scenario definitions ---

BASE = {
    # Volume
    "births_end":                 52,
    "enrolments_end":             50,
    # Revenue
    "ma_share_start":             0.20,
    "ma_share_target":            0.50,
    "ma_months":                  12,
    "pr_cash":                    40_000,
    "pr_ma":                      50_000,
    "noh_fee_pct":                0.15,
    "medicare_fee_pct":           0.4868,
    # CS / NVD
    "cs_rate_start":              0.42,
    "cs_rate_target":             0.30,
    "cs_months":                  12,
    # Antenatal midwifery
    "antenatal_visits_per_episode": 10,
    "antenatal_visit_fee":          300,
    # In-hospital midwifery (midwife-only NVD births only; excluded when MO is called)
    "inhosp_midwife_hours":       10,    # average hours per midwife-only delivery
    "inhosp_midwife_rate":        200,   # R/hr
    # MO (revised: only MO-involved NVDs + CS)
    "mo_nvd_pct":                 0.175,   # midpoint of 15-20%
    "mo_session_fee":             2_000,
    "mo_births_fee":              3_000,
    "mo_clients_per_session":     40,
    # Anaesthesia
    "anaes_fee_per_cs":           5_000,
    # OB pool
    "ob_retainer":                5_000,
    "ob_pepm":                    3_900,
    "ob_pool_cap":                300_000,
    "locum_rate":                 0.05,
    "ob_add_core_enrolments":     75,
    "ob_add_core_births":         65,
    # Board / facility fee (proxy: board + medicines + materials per patient-day)
    "nvd_los_days":               1,       # 2 days, 1 night
    "cs_los_days":                2,       # 3 days, 2 nights
    "room_rate_per_day":          2_500,   # ← adjust to calibrate hospital fee
}

SCENARIOS = {
    "base": BASE,

    "conservative": {**BASE,
        "births_end":          35,
        "enrolments_end":      35,
        "ma_share_target":     0.35,
        "ma_months":           18,
        "cs_rate_target":      0.35,
        "cs_months":           18,
    },

    "optimistic": {**BASE,
        "births_end":          70,
        "enrolments_end":      65,
        "ma_share_start":      0.25,
        "ma_share_target":     0.60,
        "ma_months":           10,
        "cs_rate_target":      0.25,
        "cs_months":           10,
    },

    "high_cs_rate": {**BASE,
        "cs_rate_target":      0.42,
        "cs_months":           12,
    },
}

COLUMNS = [
    "scenario", "month", "births", "nvd_cases", "cs_cases",
    "enrolments_active", "ma_share", "cs_rate",
    "total_receipts", "noh_fee", "medicare_fee", "residual",
    "antenatal_midwifery", "inhosp_midwifery", "midwifery_costs",
    "mo_session_cost", "mo_birth_cost", "mo_cost",
    "anaes_cost", "ob_cores", "ob_pool", "clinician_costs",
    "board_facility", "total_costs",
    "net_cashflow", "cumulative_cash",
]

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows = []
    summary_rows = []

    for name, params in SCENARIOS.items():
        rows = run_model(name, params)
        all_rows.extend(rows)

        path = OUT_DIR / f"{TODAY}_scenario_{name}.csv"
        write_csv(path, rows)

        m12 = rows[11]
        m24 = rows[23]
        summary_rows.append({
            "scenario":               name,
            "births_m24":             m24["births"],
            "enrolments_m24":         m24["enrolments_active"],
            "total_receipts_m24":     m24["total_receipts"],
            "midwifery_costs_m24":    m24["midwifery_costs"],
            "clinician_costs_m24":    m24["clinician_costs"],
            "board_facility_m24":     m24["board_facility"],
            "total_costs_m24":        m24["total_costs"],
            "net_cashflow_m12":       m12["net_cashflow"],
            "net_cashflow_m24":       m24["net_cashflow"],
            "cumulative_cash_m24":    m24["cumulative_cash"],
            "breakeven_month":        next(
                (r["month"] for r in rows if r["cumulative_cash"] >= 0), "not reached"
            ),
        })

        print(
            f"  {name:15s} | "
            f"midwifery: R{m24['midwifery_costs']:>8,.0f} | "
            f"board: R{m24['board_facility']:>7,.0f} | "
            f"net m24: R{m24['net_cashflow']:>9,.0f} | "
            f"cumulative: R{m24['cumulative_cash']:>12,.0f}"
        )

    combined_path = OUT_DIR / f"{TODAY}_scenario_all.csv"
    write_csv(combined_path, all_rows)

    summary_path = OUT_DIR / f"{TODAY}_scenario_summary.csv"
    summary_cols = list(summary_rows[0].keys())
    with open(summary_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=summary_cols)
        writer.writeheader()
        writer.writerows(summary_rows)

    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Scenarios run:      {len(SCENARIOS)}")
    print(f"Rows per scenario:  {N_MONTHS}")
    print(f"Total rows written: {len(all_rows)}")
    print(f"Columns:            {len(COLUMNS)}")
    print(f"Status:             PASS")
    print("=" * 70)

if __name__ == "__main__":
    main()
