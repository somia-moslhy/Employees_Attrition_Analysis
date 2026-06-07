import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, DARK, ACCENT, DANGER, GREEN, TEXT

st.set_page_config(page_title="HR Attrition Analytics", layout="wide")

# ── chart colors that work on dark AND light backgrounds ──
# use transparent backgrounds so chart inherits page theme
CHART_BASE = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font_color    = "#e8eaf6",
    margin        = dict(t=50, b=40, l=40, r=30),
    height        = 380,
)

df = load_data()
avg_rate = df['attrition'].mean() * 100

# ── sidebar ───────────────────────────────────────────────
col_side_logo, _ = st.sidebar.columns([3, 1])
with col_side_logo:
    st.sidebar.image("kayfa_logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.caption("Kayfa · AI & Data Analytics · Month 1 Week 1")

# ── header row: title left, logo right ───────────────────
h1, h2 = st.columns([5, 1])
with h1:
    st.markdown("##### KAYFA — AI & DATA ANALYTICS INTERNSHIP PROGRAM")
    st.title("Week 1 Task: Who Is Leaving and Why?")
    st.markdown("**Employee Attrition Analytics — From raw data to decisions an HR leader can act on.**")
with h2:
    st.image("kayfa_logo.png", use_container_width=True)

st.divider()

# ── KPIs ─────────────────────────────────────────────────
total    = len(df)
left_n   = int(df['attrition'].sum())
stayed_n = total - left_n
rate     = round(df['attrition'].mean() * 100, 1)
avg_inc  = df['monthly_income'].mean()

months_map = {'Entry': 6, 'Mid': 12, 'Senior': 24}
cost_total = sum(
    df[df['job_level'] == lvl]['attrition'].sum() *
    df[df['job_level'] == lvl]['monthly_income'].mean() * mo
    for lvl, mo in months_map.items()
    if len(df[df['job_level'] == lvl]) > 0
)
cost_label = f"${round(cost_total/1e9,2)}B" if cost_total >= 1e9 else f"${round(cost_total/1e6,1)}M"

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Employees",       f"{total:,}")
k2.metric("Attrition Rate",        f"{rate}%")
k3.metric("Retention Rate",        f"{round(100-rate,1)}%")
k4.metric("Avg Monthly Income",    f"${avg_inc:,.0f}")
k5.metric("Est. Replacement Cost", cost_label)

st.divider()

# ── 3 key decisions ───────────────────────────────────────
st.subheader("The 3 Decisions HR Should Make Today")

d1, d2, d3 = st.columns(3)

remote_rate  = round(df[df['remote_work']=='No']['attrition'].mean()*100, 1)
remote_saved = round(df[df['remote_work']=='Yes']['attrition'].mean()*100, 1)
promo_stuck  = round(df[df['number_of_promotions']==0]['attrition'].mean()*100, 1)
promo_free   = round(df[df['number_of_promotions']>=3]['attrition'].mean()*100, 1)
single_rate  = round(df[df['marital_status']=='Single']['attrition'].mean()*100, 1)

with d1:
    st.markdown("#### 01 — Expand Remote Work")
    st.markdown(f"On-site employees leave at **{remote_rate}%**. Remote employees leave at only **{remote_saved}%** — a 28 pp gap, the largest single lever in the data.")
    st.info("Action: Run a remote-eligibility pilot for feasible roles next quarter.")

with d2:
    st.markdown("#### 02 — Fix the Promotion Path")
    st.markdown(f"Employees with 0 promotions leave at **{promo_stuck}%**. Three or more promotions drops that to **{promo_free}%**. The first two promotions alone do not retain.")
    st.info("Action: Ensure every employee has a clear, timed path to their third promotion.")

with d3:
    st.markdown("#### 03 — Retain Single Early-Career Employees")
    st.markdown(f"Single employees leave at **{single_rate}%** — nearly double married staff. Single aged 18–25 hit 72%. They are mobile and need a reason to stay.")
    st.info("Action: Launch mentorship and fast career tracks for early-career single employees.")

st.divider()

# ── summary charts on home ────────────────────────────────
st.subheader("Key Findings at a Glance")

c1, c2 = st.columns(2)

# chart 1 — overall donut
with c1:
    donut_df = pd.DataFrame({
        "Status": ["Stayed", "Left"],
        "Count":  [stayed_n, left_n]
    })
    fig = px.pie(donut_df, names="Status", values="Count", hole=0.6,
                 color="Status",
                 color_discrete_map={"Stayed": ACCENT, "Left": DANGER},
                 title="Overall Attrition Rate")
    fig.update_traces(textfont_color="#ffffff")
    fig.update_layout(**CHART_BASE)
    st.plotly_chart(fig, use_container_width=True)

# chart 2 — top drivers
with c2:
    drivers_df = pd.DataFrame({
        "Driver": [
            "Remote Work (No to Yes)",
            "Work-Life Balance (Poor to Excellent)",
            "Promotions (0 to 3+)",
            "Overtime (Yes to No)",
            "Leadership Opp. (No to Yes)",
        ],
        "Impact": [
            round(df[df['remote_work']=='No']['attrition'].mean()*100 - df[df['remote_work']=='Yes']['attrition'].mean()*100, 1),
            round(df[df['work_life_balance']=='Poor']['attrition'].mean()*100 - df[df['work_life_balance']=='Excellent']['attrition'].mean()*100, 1),
            round(df[df['number_of_promotions']==0]['attrition'].mean()*100 - df[df['number_of_promotions']>=3]['attrition'].mean()*100, 1),
            round(df[df['overtime']=='Yes']['attrition'].mean()*100 - df[df['overtime']=='No']['attrition'].mean()*100, 1),
            round(df[df['leadership_opportunities']=='No']['attrition'].mean()*100 - df[df['leadership_opportunities']=='Yes']['attrition'].mean()*100, 1),
        ]
    }).sort_values("Impact", ascending=True)

    fig = px.bar(drivers_df, x="Impact", y="Driver", orientation="h",
                 text="Impact",
                 color="Impact",
                 color_continuous_scale=[[0, ACCENT],[1, "#ff6b6b"]],
                 title="Top Attrition Drivers — Impact if Improved (pp)",
                 labels={"Driver": "", "Impact": "Attrition Reduction (pp)"})
    fig.update_traces(texttemplate="-%{text} pp", textposition="outside",
                      textfont_color="#ffffff")
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(range=[0, 35])
    fig.update_layout(**CHART_BASE, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

# chart 3 — remote vs onsite
with c3:
    rw_df = df.groupby("remote_work")["attrition"].mean().reset_index()
    rw_df["rate"] = (rw_df["attrition"] * 100).round(1)
    rw_df["remote_work"] = rw_df["remote_work"].map({"No": "On-site", "Yes": "Remote"})
    fig = px.bar(rw_df, x="remote_work", y="rate", text="rate",
                 color="remote_work",
                 color_discrete_map={"On-site": "#ff6b6b", "Remote": "#43d9a0"},
                 title="Remote Work vs On-site Attrition",
                 labels={"remote_work": "", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside",
                      textfont_color="#ffffff")
    fig.update_yaxes(range=[0, 65])
    fig.update_layout(**CHART_BASE, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# chart 4 — marital status
with c4:
    ms_df = df.groupby("marital_status")["attrition"].mean().reset_index()
    ms_df["rate"] = (ms_df["attrition"] * 100).round(1)
    ms_df = ms_df.sort_values("rate", ascending=False)
    fig = px.bar(ms_df, x="marital_status", y="rate", text="rate",
                 color="marital_status",
                 color_discrete_map={"Single": "#ff6b6b", "Divorced": ACCENT, "Married": "#43d9a0"},
                 title="Attrition by Marital Status",
                 labels={"marital_status": "", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside",
                      textfont_color="#ffffff")
    fig.update_yaxes(range=[0, 80])
    fig.update_layout(**CHART_BASE, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Kayfa · AI & Data Analytics Internship · Month 1 Week 1 · Synthetic HR dataset · 74,498 records · Exploratory analysis only")