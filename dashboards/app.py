# NOH Maternity Cashflow Dashboard
# Run: streamlit run dashboards/app.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scenario_model import run_model, BASE

st.set_page_config(page_title="NOH Maternity Cashflow", layout="wide")

st.title("NOH Maternity Programme — 24-Month Cashflow Model")
st.caption("Disaggregated costs: antenatal midwifery · in-hospital midwifery · clinicians · board/facility · Rustenburg · Prices escalate at CPI")

OUT_DIR = Path("outputs")

SCENARIO_COLORS = {
    "base":          "#599591",
    "optimistic":    "#2e6b68",
    "conservative":  "#f3bdc4",
    "high_cs_rate":  "#d4878f",
    "price_stress":  "#e8c07a",
    "custom":        "#7b5ea7",
}

SCENARIO_LABELS = {
    "base":          "Base (6% CPI)",
    "optimistic":    "Optimistic",
    "conservative":  "Conservative",
    "high_cs_rate":  "High CS Rate",
    "price_stress":  "Price Stress (4% CPI floor)",
    "custom":        "Live Negotiation",
}

# --- Load pre-computed data (always picks the latest dated files) ---
@st.cache_data
def load_scenarios():
    files = sorted(OUT_DIR.glob("*_scenario_all.csv"))
    if not files:
        st.error("Missing scenario_all.csv. Run src/scenario_model.py first.")
        st.stop()
    return pd.read_csv(files[-1])

@st.cache_data
def load_summary():
    files = sorted(OUT_DIR.glob("*_scenario_summary.csv"))
    if not files:
        st.error("Missing scenario_summary.csv. Run src/scenario_model.py first.")
        st.stop()
    return pd.read_csv(files[-1])

df      = load_scenarios()
summary = load_summary()

# --- Sidebar: scenario filter ---
st.sidebar.header("Scenarios")
all_scenarios = df["scenario"].unique().tolist() + ["custom"]
selected = st.sidebar.multiselect(
    "Show scenarios",
    options=all_scenarios,
    format_func=lambda s: SCENARIO_LABELS.get(s, s),
    default=all_scenarios,
)

# --- Sidebar: live negotiation sliders ---
st.sidebar.divider()
st.sidebar.header("Live Negotiation")
st.sidebar.caption("Adjust assumptions to model different partnership terms.")

custom_births      = st.sidebar.slider("Birth volume target (Month 24)", 20, 120, int(BASE["births_end"]), step=1)
custom_nvd_rate    = st.sidebar.slider("NVD per diem (R/day)", 1_000, 6_000, int(BASE["nvd_room_rate"]), step=100)
custom_cs_rate_bd  = st.sidebar.slider("CS per diem (R/day)", 2_000, 10_000, int(BASE["cs_room_rate"]), step=100)
custom_cs_rate     = st.sidebar.slider("CS rate target (%)", 20, 55, int(BASE["cs_rate_target"] * 100)) / 100
custom_ma_share    = st.sidebar.slider("MA share target (%)", 20, 80, int(BASE["ma_share_target"] * 100)) / 100
custom_noh_fee     = st.sidebar.slider("NOH fee (%)", 5, 25, int(BASE["noh_fee_pct"] * 100)) / 100

# --- Compute live custom scenario (runs on every slider change) ---
custom_params = {**BASE,
    "births_end":       custom_births,
    "enrolments_end":   max(1, round(custom_births * (BASE["enrolments_end"] / BASE["births_end"]))),
    "nvd_room_rate":    custom_nvd_rate,
    "cs_room_rate":     custom_cs_rate_bd,
    "cs_rate_target":   custom_cs_rate,
    "ma_share_target":  custom_ma_share,
    "noh_fee_pct":      custom_noh_fee,
}
custom_rows   = run_model("custom", custom_params)
df_custom     = pd.DataFrame(custom_rows)
custom_m12    = custom_rows[11]
custom_m24    = custom_rows[23]
custom_summary = pd.DataFrame([{
    "scenario":            "custom",
    "births_m24":          custom_m24["births"],
    "enrolments_m24":      custom_m24["enrolments_active"],
    "total_receipts_m24":  custom_m24["total_receipts"],
    "midwifery_costs_m24": custom_m24["midwifery_costs"],
    "clinician_costs_m24": custom_m24["clinician_costs"],
    "board_facility_m24":  custom_m24["board_facility"],
    "total_costs_m24":     custom_m24["total_costs"],
    "net_cashflow_m12":    custom_m12["net_cashflow"],
    "net_cashflow_m24":    custom_m24["net_cashflow"],
    "cumulative_cash_m24": custom_m24["cumulative_cash"],
    "breakeven_month":     next(
        (r["month"] for r in custom_rows if r["cumulative_cash"] >= 0), "not reached"
    ),
}])

# --- Live readout in sidebar ---
st.sidebar.divider()
st.sidebar.markdown("**Live scenario result**")
st.sidebar.metric("Cumulative cash M24", f"R {custom_m24['cumulative_cash']:,.0f}")
st.sidebar.metric("Net cashflow M24", f"R {custom_m24['net_cashflow']:,.0f}")
st.sidebar.metric("Break-even month", str(custom_summary.iloc[0]["breakeven_month"]))

# --- Merge custom into working dataframes ---
df_all      = pd.concat([df, df_custom], ignore_index=True)
summary_all = pd.concat([summary, custom_summary], ignore_index=True)

df_f        = df_all[df_all["scenario"].isin(selected)]
summary_f   = summary_all[summary_all["scenario"].isin(selected)]

# --- KPI cards ---
st.subheader("Month 24 Summary")
if selected:
    cols = st.columns(len(selected))
    for i, scen in enumerate(selected):
        row = summary_all[summary_all["scenario"] == scen].iloc[0]
        cols[i].metric(
            label=SCENARIO_LABELS.get(scen, scen),
            value=f"R {row['cumulative_cash_m24']:,.0f}",
            delta=f"Net M24: R {row['net_cashflow_m24']:,.0f}",
        )

st.divider()

# --- Row 1: Cashflow ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cumulative Cashflow")
    fig = px.line(
        df_f, x="month", y="cumulative_cash", color="scenario",
        color_discrete_map=SCENARIO_COLORS, markers=True,
        labels={"cumulative_cash": "Cumulative Cash (R)", "month": "Month"},
    )
    fig.add_hline(y=0, line_dash="dash", line_color="grey", annotation_text="Break-even")
    fig.update_layout(legend_title="Scenario", hovermode="x unified")
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("Net Cashflow per Month")
    fig2 = px.bar(
        df_f, x="month", y="net_cashflow", color="scenario",
        color_discrete_map=SCENARIO_COLORS, barmode="group",
        labels={"net_cashflow": "Net Cashflow (R)", "month": "Month"},
    )
    fig2.add_hline(y=0, line_dash="dash", line_color="grey")
    fig2.update_layout(legend_title="Scenario", hovermode="x unified")
    st.plotly_chart(fig2, width='stretch')

st.divider()

# --- Row 2: Cost breakdown ---
st.subheader("Cost Breakdown — Month 24")

ref_scen = "custom" if "custom" in selected else ("base" if "base" in selected else selected[0]) if selected else None

col3, col4 = st.columns(2)

with col3:
    if ref_scen:
        ref_m24 = df_f[(df_f["scenario"] == ref_scen) & (df_f["month"] == 24)].iloc[0]
        st.markdown(f"**{SCENARIO_LABELS.get(ref_scen, ref_scen)} — Month 24 cost stack**")
        cost_labels = [
            "Antenatal Midwifery",
            "In-Hospital Midwifery",
            "MO Sessions",
            "MO Birth Fees",
            "Anaesthesia",
            "OB Pool",
            "Board / Facility",
        ]
        cost_values = [
            ref_m24["antenatal_midwifery"],
            ref_m24["inhosp_midwifery"],
            ref_m24["mo_session_cost"],
            ref_m24["mo_birth_cost"],
            ref_m24["anaes_cost"],
            ref_m24["ob_pool"],
            ref_m24["board_facility"],
        ]
        fig3 = go.Figure(go.Bar(
            x=cost_values,
            y=cost_labels,
            orientation="h",
            marker_color=[
                "#f3bdc4", "#d4878f",
                "#599591", "#2e6b68", "#3a8582",
                "#a8d5d3",
                "#e8c07a",
            ],
            text=[f"R {v:,.0f}" for v in cost_values],
            textposition="outside",
        ))
        fig3.add_vline(x=ref_m24["residual"], line_dash="dash", line_color="#599591",
                       annotation_text="Residual", annotation_position="top right")
        fig3.update_layout(xaxis_title="R", yaxis_title="", margin=dict(l=160))
        st.plotly_chart(fig3, width='stretch')

with col4:
    st.subheader("Midwifery vs Clinician vs Board")
    cost_df = df_f[["scenario", "month", "midwifery_costs", "clinician_costs", "board_facility"]].copy()
    cost_melt = cost_df.melt(
        id_vars=["scenario", "month"],
        value_vars=["midwifery_costs", "clinician_costs", "board_facility"],
        var_name="cost_type", value_name="amount"
    )
    cost_melt["cost_type"] = cost_melt["cost_type"].map({
        "midwifery_costs":  "Midwifery",
        "clinician_costs":  "Clinicians",
        "board_facility":   "Board / Facility",
    })
    fig4 = px.area(
        cost_melt,
        x="month", y="amount", color="cost_type",
        facet_col="scenario", facet_col_wrap=2,
        color_discrete_map={
            "Midwifery":        "#f3bdc4",
            "Clinicians":       "#599591",
            "Board / Facility": "#e8c07a",
        },
        labels={"amount": "R", "month": "Month", "cost_type": "Cost"},
    )
    fig4.update_layout(hovermode="x unified")
    st.plotly_chart(fig4, width='stretch')

st.divider()

# --- Row 3: Revenue vs Total Costs + Births ---
col5, col6 = st.columns(2)

with col5:
    st.subheader("Residual vs Total Costs")
    fig5 = px.line(
        df_f, x="month", y=["residual", "total_costs"], color="scenario",
        color_discrete_map=SCENARIO_COLORS,
        labels={"value": "R", "month": "Month", "variable": ""},
        line_dash="variable",
    )
    fig5.update_layout(legend_title="Scenario / Line", hovermode="x unified")
    st.plotly_chart(fig5, width='stretch')

with col6:
    ref_births_scen = "custom" if "custom" in selected else "base"
    births_df = df_all[df_all["scenario"] == ref_births_scen].copy()
    st.subheader(f"Births by Type — {SCENARIO_LABELS.get(ref_births_scen, ref_births_scen)}")
    mo_nvd_pct = custom_params["mo_nvd_pct"] if ref_births_scen == "custom" else BASE["mo_nvd_pct"]
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(name="NVD (midwife-only)", x=births_df["month"],
                          y=(births_df["nvd_cases"] * (1 - mo_nvd_pct)).round(1),
                          marker_color="#f3bdc4"))
    fig6.add_trace(go.Bar(name="NVD (MO-assisted)", x=births_df["month"],
                          y=(births_df["nvd_cases"] * mo_nvd_pct).round(1),
                          marker_color="#599591"))
    fig6.add_trace(go.Bar(name="CS", x=births_df["month"],
                          y=births_df["cs_cases"].round(1),
                          marker_color="#2e6b68"))
    fig6.update_layout(barmode="stack", xaxis_title="Month", yaxis_title="Cases",
                       legend_title="Birth Type", hovermode="x unified")
    st.plotly_chart(fig6, width='stretch')

st.divider()

# --- Summary table ---
st.subheader("Scenario Comparison Table")
fmt = {
    "total_receipts_m24":   "R {:,.0f}",
    "midwifery_costs_m24":  "R {:,.0f}",
    "clinician_costs_m24":  "R {:,.0f}",
    "board_facility_m24":   "R {:,.0f}",
    "total_costs_m24":      "R {:,.0f}",
    "net_cashflow_m12":     "R {:,.0f}",
    "net_cashflow_m24":     "R {:,.0f}",
    "cumulative_cash_m24":  "R {:,.0f}",
}
st.dataframe(
    summary_f.set_index("scenario").style.format(fmt),
    width='stretch',
)

# --- Raw data ---
with st.expander("Raw scenario data"):
    st.dataframe(df_f, width='stretch')
