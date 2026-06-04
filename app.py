import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Employee Attrition", layout="wide")

# colors
DARK   = "#353b98"
ACCENT = "#8a91f2"
DANGER = "#ff6b6b"
GREEN  = "#43d9a0"
TEXT   = "#1a1d3a"

# ── load data ─────────────────────────────────────────────
df = pd.read_csv("combined.csv")

# ── sidebar filters ───────────────────────────────────────
st.sidebar.image("kayfa_logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.title("Filters")

roles = ["All"] + sorted(df["job_role"].unique().tolist())
sel_role = st.sidebar.selectbox("Job Role", roles)

levels = ["All"] + sorted(df["job_level"].unique().tolist())
sel_level = st.sidebar.selectbox("Job Level", levels)

sizes = ["All"] + sorted(df["company_size"].unique().tolist())
sel_size = st.sidebar.selectbox("Company Size", sizes)

remote_opts = ["All", "Yes", "No"]
sel_remote = st.sidebar.selectbox("Remote Work", remote_opts)

age_min = int(df["age"].min())
age_max = int(df["age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

# ── apply filters ─────────────────────────────────────────
if sel_role   != "All": df = df[df["job_role"]     == sel_role]
if sel_level  != "All": df = df[df["job_level"]    == sel_level]
if sel_size   != "All": df = df[df["company_size"] == sel_size]
if sel_remote != "All": df = df[df["remote_work"]  == sel_remote]
df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

# ── KPIs ──────────────────────────────────────────────────
total      = len(df)
left_n     = int(df["attrition"].sum())
stayed_n   = total - left_n
rate       = round(left_n / total * 100, 1) if total > 0 else 0
avg_income = round(df["monthly_income"].mean(), 0)
months_mapping = {"Entry": 6, "Mid": 12, "Senior": 24}

cost_total = 0
for level, months in months_mapping.items():
    level_df_cost = df[df["job_level"] == level]
    if len(level_df_cost) == 0:
        continue
    cost_total += level_df_cost["attrition"].sum() * level_df_cost["monthly_income"].mean() * months

if cost_total >= 1e9:
    cost_label = f"${round(cost_total / 1e9, 2)}B"
else:
    cost_label = f"${round(cost_total / 1e6, 1)}M"

# ── header ────────────────────────────────────────────────
st.title("Employee Attrition Analytics")
st.markdown("**What 3 decisions should HR make today to stop attrition?**")
st.divider()

# ── KPI row ───────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Employees",      f"{total:,}")
k2.metric("Attrition Rate",       f"{rate}%")
k3.metric("Retention Rate",       f"{round(100 - rate, 1)}%")
k4.metric("Avg Monthly Income",   f"${avg_income:,.0f}")
k5.metric("Est. Replacement Cost", cost_label)

st.divider()

# ── 3 decisions ───────────────────────────────────────────
st.subheader("The 3 Decisions")

sr = round(df[(df["job_level"]=="Senior") & (df["remote_work"]=="Yes")]["attrition"].mean() * 100, 1)
sp = round(df[(df["job_level"]=="Senior") & (df["number_of_promotions"]>=3)]["attrition"].mean() * 100, 1)
el = round(df[df["job_level"]=="Entry"]["attrition"].mean() * 100, 1)

d1, d2, d3 = st.columns(3)

with d1:
    st.markdown("#### 01 — Mandate Hybrid for Senior Employees")
    st.markdown(f"Remote Senior employees leave at **{sr}%**. Senior roles need visibility and collaboration that remote work removes.")
    st.info("Action: 3 days/week on-site for Senior level. Offer relocation support.")

with d2:
    st.markdown("#### 02 — Redesign the Senior Career Path")
    st.markdown(f"Senior employees with 3+ promotions leave at **{sp}%**. They have hit a ceiling with nowhere left to grow.")
    st.info("Action: Create Principal and Distinguished tracks above Senior.")

with d3:
    st.markdown("#### 03 — Protect Entry-Level Employees Early")
    st.markdown(f"Entry-level employees leave at only **{el}%** — the most retainable group.")
    st.info("Action: Launch mentorship and flexible hours to prevent early burnout.")

st.divider()

# ── charts ────────────────────────────────────────────────
st.subheader("What Drives Attrition?")

col1, col2 = st.columns(2)

# chart 1 — by job level
with col1:
    level_df = df.groupby("job_level", observed=True)["attrition"].mean().reset_index()
    level_df["rate"] = (level_df["attrition"] * 100).round(1)
    level_df["job_level"] = pd.Categorical(level_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    level_df = level_df.sort_values("job_level")

    fig = px.bar(level_df, x="job_level", y="rate", text="rate",
                 color="rate", color_continuous_scale=[[0, ACCENT],[1, DARK]],
                 title="Attrition by Job Level",
                 labels={"job_level":"Job Level","rate":"Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color=TEXT)
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0,100])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# chart 2 — remote x job level
with col2:
    remote_df = df.groupby(["job_level","remote_work"], observed=True)["attrition"].mean().reset_index()
    remote_df["rate"] = (remote_df["attrition"] * 100).round(1)
    remote_df["job_level"] = pd.Categorical(remote_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    remote_df = remote_df.sort_values("job_level")

    fig = px.bar(remote_df, x="job_level", y="rate", color="remote_work",
                 barmode="group", text="rate",
                 color_discrete_map={"No": DARK, "Yes": DANGER},
                 title="Remote Work x Job Level",
                 labels={"job_level":"Job Level","rate":"Attrition Rate (%)","remote_work":"Remote"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color=TEXT)
    fig.update_yaxes(range=[0,115])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

# chart 3 — promotions heatmap
with col3:
    promo_df = df[df["number_of_promotions"] <= 4].groupby(
        ["job_level","number_of_promotions"], observed=True)["attrition"].mean().reset_index()
    promo_df["rate"] = (promo_df["attrition"] * 100).round(1)
    promo_df["job_level"] = pd.Categorical(promo_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    promo_df["number_of_promotions"] = promo_df["number_of_promotions"].astype(str) + " promos"

    fig = px.density_heatmap(promo_df, x="number_of_promotions", y="job_level", z="rate",
                             color_continuous_scale=[[0,"#eef0ff"],[0.5, ACCENT],[1, DARK]],
                             text_auto=True,
                             title="Promotions x Job Level — Career Ceiling",
                             labels={"number_of_promotions":"Promotions","job_level":"Job Level","rate":"Attrition %"})
    fig.update_traces(textfont_color=TEXT)
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

# chart 4 — work life balance
with col4:
    wlb_order = ["Poor","Fair","Good","Excellent"]
    wlb_df = df.groupby("work_life_balance", observed=True)["attrition"].mean().reset_index()
    wlb_df["rate"] = (wlb_df["attrition"] * 100).round(1)
    wlb_df["work_life_balance"] = pd.Categorical(wlb_df["work_life_balance"], categories=wlb_order, ordered=True)
    wlb_df = wlb_df.sort_values("work_life_balance")

    fig = px.bar(wlb_df, x="work_life_balance", y="rate", text="rate",
                 color="rate", color_continuous_scale=[[0, GREEN],[0.5, ACCENT],[1, DANGER]],
                 title="Work-Life Balance vs Attrition",
                 labels={"work_life_balance":"Work-Life Balance","rate":"Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color=TEXT)
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0,80])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2)

# chart 5 — by department
with col5:
    role_df = df.groupby("job_role")["attrition"].mean().reset_index()
    role_df["rate"] = (role_df["attrition"] * 100).round(1)
    role_df = role_df.sort_values("rate", ascending=True)

    fig = px.bar(role_df, x="rate", y="job_role", orientation="h", text="rate",
                 color="rate", color_continuous_scale=[[0, ACCENT],[1, DARK]],
                 title="Attrition by Department",
                 labels={"job_role":"","rate":"Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color=TEXT)
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(range=[0,65])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# chart 6 — income distribution
with col6:
    income_df = df[["monthly_income","attrition"]].copy()
    income_df["Status"] = income_df["attrition"].map({0:"Stayed", 1:"Left"})

    fig = px.histogram(income_df, x="monthly_income", color="Status",
                       barmode="overlay", nbins=40, opacity=0.75,
                       color_discrete_map={"Stayed": ACCENT, "Left": DANGER},
                       title="Monthly Income — Stayed vs Left",
                       labels={"monthly_income":"Monthly Income ($)"})
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# chart 7 — cost by level
st.subheader("Financial Impact")

months_per_level = {"Entry": 6, "Mid": 12, "Senior": 24}
cost_df = df.groupby("job_level", observed=True).apply(
    lambda x: round(x["attrition"].sum() * x["monthly_income"].mean() * months_per_level.get(x.name, 6) / 1e6, 1)
).reindex(["Entry","Mid","Senior"]).reset_index()
cost_df.columns = ["job_level","cost_M"]

fig = px.bar(cost_df, x="job_level", y="cost_M", text="cost_M",
             color="job_level",
             color_discrete_map={"Entry": ACCENT, "Mid": DARK, "Senior": DANGER},
             title="Estimated Replacement Cost by Job Level ($M)",
             labels={"job_level":"Job Level","cost_M":"Cost ($M)"})
fig.update_traces(texttemplate="$%{text}M", textposition="outside", textfont_color=TEXT)
fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Kayfa — AI & Data Analytics Internship Program · Month 1 Week 1 · Synthetic HR dataset · 44,686 records")