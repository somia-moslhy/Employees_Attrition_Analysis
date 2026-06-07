import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.append('..')
from utils import load_data, DARK, ACCENT, DANGER, GREEN, WHITE, TEXT, CHART

st.set_page_config(page_title="Foundations", layout="wide")
st.sidebar.image("kayfa_logo.png", use_container_width=True)

df = load_data()
avg_rate = df['attrition'].mean() * 100

st.title("Foundations")
st.markdown("Q1 · Q2 · Q3 — The headline numbers every HR leader needs first.")
st.divider()

# ── Q1 ────────────────────────────────────────────────────
st.subheader("Q1 — The Headline: Overall Attrition and Where It Hits Hardest")

c1, c2 = st.columns(2)

with c1:
    donut_df = pd.DataFrame({
        "Status": ["Stayed", "Left"],
        "Count":  [int((df['attrition']==0).sum()), int(df['attrition'].sum())]
    })
    fig = px.pie(donut_df, names="Status", values="Count", hole=0.6,
                 color="Status", color_discrete_map={"Stayed": ACCENT, "Left": DANGER},
                 title="Overall Attrition Rate")
    fig.update_traces(textfont_color="#ffffff")
    fig.update_layout(**CHART)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    role_df = df.groupby("job_role")["attrition"].mean().reset_index()
    role_df["rate"] = (role_df["attrition"] * 100).round(1)
    role_df = role_df.sort_values("rate", ascending=True)
    fig = px.bar(role_df, x="rate", y="job_role", orientation="h", text="rate",
                 color="rate", color_continuous_scale=[[0, ACCENT],[1, DARK]],
                 title="Attrition Rate by Department",
                 labels={"job_role": "", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(range=[0, 60])
    fig.update_layout(**CHART, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.info("**Insight:** All departments sit within 2 percentage points of each other (46.8%–48.8%). This is not a department problem — it is a company-wide structural issue. Any solution must be applied at company level, not targeted at one team.")
st.divider()

# ── Q2 ────────────────────────────────────────────────────
st.subheader("Q2 — Overtime: Does Working Extra Hours Lead to Leaving?")

ot_df = df.groupby("overtime")["attrition"].mean().reset_index()
ot_df["rate"] = (ot_df["attrition"] * 100).round(1)
ot_df["overtime"] = ot_df["overtime"].map({"No": "No Overtime", "Yes": "Overtime"})

fig = px.bar(ot_df, x="overtime", y="rate", text="rate",
             color="overtime",
             color_discrete_map={"No Overtime": ACCENT, "Overtime": DANGER},
             title="Attrition Rate: Overtime vs No Overtime",
             labels={"overtime": "", "rate": "Attrition Rate (%)"})
fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
fig.update_yaxes(range=[0, 65])
fig.update_layout(**CHART, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

ot_gap = round(ot_df[ot_df['overtime']=='Overtime']['rate'].values[0] - ot_df[ot_df['overtime']=='No Overtime']['rate'].values[0], 1)
ot_pct = round(df[df['overtime']=='Yes'].shape[0] / len(df) * 100, 1)
st.info(f"**Insight:** Overtime employees leave at 51.5% vs 45.5% — a {ot_gap} pp gap. Only {ot_pct}% of staff work overtime, so this affects a defined segment. **Action:** Audit teams with consistently high overtime and redistribute workload before burnout leads to resignation.")
st.divider()

# ── Q3 ────────────────────────────────────────────────────
st.subheader("Q3 — Remote Work: The Strongest Single Signal in the Dataset")

rw_df = df.groupby("remote_work")["attrition"].mean().reset_index()
rw_df["rate"] = (rw_df["attrition"] * 100).round(1)
rw_df["remote_work"] = rw_df["remote_work"].map({"No": "On-site", "Yes": "Remote"})

fig = px.bar(rw_df, x="remote_work", y="rate", text="rate",
             color="remote_work",
             color_discrete_map={"On-site": DANGER, "Remote": GREEN},
             title="Attrition Rate: Remote vs On-site",
             labels={"remote_work": "", "rate": "Attrition Rate (%)"})
fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
fig.update_yaxes(range=[0, 65])
fig.update_layout(**CHART, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

remote_pct = round(df[df['remote_work']=='Yes'].shape[0] / len(df) * 100, 1)
st.info(f"**Insight:** Remote = 24.7% vs On-site = 52.8% — a 28 pp gap, the largest single factor in the dataset. **Caveat:** Only {remote_pct}% of staff work remotely, so this finding reflects a small and possibly self-selected group. **Action:** Run a structured remote-eligibility pilot for roles where it is feasible and measure attrition impact after 6 months.")