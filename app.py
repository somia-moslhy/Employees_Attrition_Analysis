import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Employee Attrition — Kayfa Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK    = "#353b98"
ACCENT  = "#8a91f2"
WHITE   = "#ffffff"
BG      = "#f7f8ff"
MUTED   = "#a0a6c8"
DANGER  = "#ff6b6b"
SUCCESS = "#43d9a0"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {BG};
    color: #1a1d3a;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARK} 0%, #1e2260 100%);
    border-right: none;
}}
[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {{
    color: {ACCENT} !important;
    font-weight: 600;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}}

.main .block-container {{
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

.kpi-card {{
    background: {WHITE};
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 16px rgba(53,59,152,0.08);
    border-left: 4px solid {DARK};
}}
.kpi-card.danger {{ border-left-color: {DANGER}; }}
.kpi-card.success {{ border-left-color: {SUCCESS}; }}
.kpi-card.accent  {{ border-left-color: {ACCENT}; }}
.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {MUTED};
    margin-bottom: 0.4rem;
}}
.kpi-value {{
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #1a1d3a;
    line-height: 1;
}}
.kpi-sub {{ font-size: 0.8rem; color: {MUTED}; margin-top: 0.3rem; }}

.decision-card {{
    background: {WHITE};
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 4px 20px rgba(53,59,152,0.1);
    border-top: 4px solid {DARK};
    margin-bottom: 1rem;
    height: 100%;
}}
.decision-number {{
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: {ACCENT};
    opacity: 0.4;
    line-height: 1;
}}
.decision-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: {DARK};
    margin-bottom: 0.5rem;
}}
.decision-insight {{ font-size: 0.88rem; color: #4a5080; line-height: 1.6; }}
.decision-action {{
    background: linear-gradient(135deg, {DARK}18, {ACCENT}18);
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: {DARK};
    border-left: 3px solid {ACCENT};
}}

.section-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: {DARK};
    margin-bottom: 0.2rem;
    margin-top: 1.2rem;
}}
.section-sub {{ font-size: 0.83rem; color: {MUTED}; margin-bottom: 1rem; }}

.custom-divider {{
    height: 2px;
    background: linear-gradient(90deg, {DARK}, {ACCENT}, transparent);
    border: none;
    margin: 1.5rem 0;
    border-radius: 2px;
}}
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("combined.csv")

df_full = load_data()


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-family:'Syne',sans-serif; font-size:2rem; font-weight:800;
                    color:#fff; letter-spacing:0.05em;">kayfa</div>
        <div style="font-size:0.7rem; color:{ACCENT}; letter-spacing:0.15em;
                    text-transform:uppercase; margin-top:0.2rem;">Analytics Dashboard</div>
    </div>
    <div style="height:1px; background:rgba(255,255,255,0.12); margin-bottom:1.5rem;"></div>
    """, unsafe_allow_html=True)

    st.markdown("**FILTERS**")

    roles = ["All"] + sorted(df_full["job_role"].unique().tolist())
    sel_role = st.selectbox("Job Role", roles)

    levels = ["All"] + sorted(df_full["job_level"].unique().tolist())
    sel_level = st.selectbox("Job Level", levels)

    sizes = ["All"] + sorted(df_full["company_size"].unique().tolist())
    sel_size = st.selectbox("Company Size", sizes)

    remote_opts = ["All", "Yes", "No"]
    sel_remote = st.selectbox("Remote Work", remote_opts)

    age_range = st.slider("Age Range", int(df_full["age"].min()), int(df_full["age"].max()), (18, 60))

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.75rem; color:{ACCENT}; line-height:1.8;">
        Filters apply to all charts<br>
        Dataset: 44,686 employees<br>
        Focus: Business Decisions
    </div>
    """, unsafe_allow_html=True)


# ── APPLY FILTERS ────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_role   != "All": df = df[df["job_role"]    == sel_role]
if sel_level  != "All": df = df[df["job_level"]   == sel_level]
if sel_size   != "All": df = df[df["company_size"] == sel_size]
if sel_remote != "All": df = df[df["remote_work"]  == sel_remote]
df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,{DARK} 0%,#5058c8 100%);
     border-radius:16px; padding:2rem 2.5rem; margin-bottom:1.5rem;
     display:flex; align-items:center; justify-content:space-between;
     box-shadow:0 8px 32px rgba(53,59,152,0.25);">
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                color:#fff;margin:0;">Employee Attrition Analytics</div>
    <div style="color:{ACCENT};font-size:0.9rem;margin-top:0.3rem;">
        What 3 decisions should HR make today to stop attrition?
    </div>
  </div>
  <div style="background:rgba(255,255,255,0.12);border-radius:12px;
       padding:0.6rem 1.2rem;font-family:'Syne',sans-serif;font-weight:800;
       font-size:1.5rem;color:#fff;border:1px solid rgba(255,255,255,0.2);">
    kayfa
  </div>
</div>
""", unsafe_allow_html=True)


# ── KPIs ─────────────────────────────────────────────────────────────────────
total      = len(df)
left_n     = int(df["attrition"].sum())
stayed_n   = total - left_n
attr_rate  = left_n / total * 100 if total > 0 else 0
avg_income = df["monthly_income"].mean()
cost_est   = left_n * avg_income * 6

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Employees</div><div class="kpi-value">{total:,}</div><div class="kpi-sub">in filtered view</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card danger"><div class="kpi-label">Attrition Rate</div><div class="kpi-value" style="color:{DANGER};">{attr_rate:.1f}%</div><div class="kpi-sub">{left_n:,} employees left</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card success"><div class="kpi-label">Retention Rate</div><div class="kpi-value" style="color:{SUCCESS};">{100-attr_rate:.1f}%</div><div class="kpi-sub">{stayed_n:,} stayed</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi-card accent"><div class="kpi-label">Avg Monthly Income</div><div class="kpi-value">${avg_income:,.0f}</div><div class="kpi-sub">across all employees</div></div>', unsafe_allow_html=True)
with c5:
    st.markdown(f'<div class="kpi-card danger"><div class="kpi-label">Est. Replacement Cost</div><div class="kpi-value" style="color:{DANGER};font-size:1.6rem;">${cost_est/1e6:.1f}M</div><div class="kpi-sub">at 6x monthly salary</div></div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ── 3 DECISIONS ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">The 3 Decisions</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Each decision is backed by a clear pattern in the data</div>', unsafe_allow_html=True)

d1, d2, d3 = st.columns(3)

sr = df[(df["job_level"]=="Senior") & (df["remote_work"]=="Yes")]["attrition"].mean()*100
sp = df[(df["job_level"]=="Senior") & (df["number_of_promotions"]>=3)]["attrition"].mean()*100
el = df[df["job_level"]=="Entry"]["attrition"].mean()*100

with d1:
    st.markdown(f"""
    <div class="decision-card">
        <div class="decision-number">01</div>
        <div class="decision-title">Mandate Hybrid for Senior Employees</div>
        <div class="decision-insight">
            Remote Senior employees leave at <strong style="color:{DANGER};">{sr:.0f}%</strong>.
            Senior roles need visibility, mentorship, and collaboration that remote work eliminates.
        </div>
        <div class="decision-action">
            Action: 3 days/week on-site for Senior level. Offer relocation support for those far from office.
        </div>
    </div>""", unsafe_allow_html=True)

with d2:
    st.markdown(f"""
    <div class="decision-card">
        <div class="decision-number">02</div>
        <div class="decision-title">Redesign the Senior Career Path</div>
        <div class="decision-insight">
            Senior employees with 3+ promotions leave at <strong style="color:{DANGER};">{sp:.0f}%</strong>.
            They have climbed the ladder and hit a ceiling — high performers with nowhere to go.
        </div>
        <div class="decision-action">
            Action: Create Principal and Distinguished tracks above Senior. Add leadership project ownership.
        </div>
    </div>""", unsafe_allow_html=True)

with d3:
    st.markdown(f"""
    <div class="decision-card">
        <div class="decision-number">03</div>
        <div class="decision-title">Protect Entry-Level Employees Early</div>
        <div class="decision-insight">
            Entry-level employees leave at only <strong style="color:{SUCCESS};">{el:.0f}%</strong> — 
            the most retainable group. Invest in their experience before they become a mid/senior flight risk.
        </div>
        <div class="decision-action">
            Action: Launch Entry-level mentorship and flexible hours program to prevent early burnout.
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ── CHARTS ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Deep Dive: What Drives Attrition?</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Breakdown by key factors</div>', unsafe_allow_html=True)

chart_layout = dict(
    plot_bgcolor=WHITE,
    paper_bgcolor=WHITE,
    font_family="DM Sans, sans-serif",
    title_font=dict(size=14, color=DARK, family="Syne, sans-serif"),
    margin=dict(t=50, b=40, l=40, r=20),
    height=360,
)

col1, col2 = st.columns(2)

# Chart 1 — Attrition by Job Level
with col1:
    level_df = df.groupby("job_level", observed=True)["attrition"].mean().reset_index()
    level_df["rate"] = (level_df["attrition"] * 100).round(1)
    level_df["job_level"] = pd.Categorical(level_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    level_df = level_df.sort_values("job_level")

    fig = px.bar(
        level_df, x="job_level", y="rate",
        text="rate",
        color="rate",
        color_continuous_scale=[[0, ACCENT], [1, DARK]],
        title="Attrition Rate by Job Level",
        labels={"job_level": "Job Level", "rate": "Attrition Rate (%)"},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#1a1d3a")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0, 100], gridcolor="#f0f0f8")
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

# Chart 2 — Remote Work x Job Level
with col2:
    remote_df = df.groupby(["job_level", "remote_work"], observed=True)["attrition"].mean().reset_index()
    remote_df["rate"] = (remote_df["attrition"] * 100).round(1)
    remote_df["job_level"] = pd.Categorical(remote_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    remote_df = remote_df.sort_values("job_level")

    fig = px.bar(
        remote_df, x="job_level", y="rate",
        color="remote_work", barmode="group",
        text="rate",
        color_discrete_map={"No": DARK, "Yes": DANGER},
        title="Remote Work x Job Level — Highest Risk Combination",
        labels={"job_level": "Job Level", "rate": "Attrition Rate (%)", "remote_work": "Remote Work"},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#1a1d3a")
    fig.update_yaxes(range=[0, 115], gridcolor="#f0f0f8")
    fig.update_layout(**chart_layout, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

# Chart 3 — Promotions Heatmap
with col3:
    promo_df = df[df["number_of_promotions"] <= 4].groupby(
        ["job_level", "number_of_promotions"], observed=True
    )["attrition"].mean().reset_index()
    promo_df["rate"] = (promo_df["attrition"] * 100).round(1)
    promo_df["job_level"] = pd.Categorical(promo_df["job_level"], categories=["Entry","Mid","Senior"], ordered=True)
    promo_df["number_of_promotions"] = promo_df["number_of_promotions"].astype(str) + " promos"

    fig = px.density_heatmap(
        promo_df, x="number_of_promotions", y="job_level", z="rate",
        color_continuous_scale=[[0, "#eef0ff"], [0.5, ACCENT], [1, DARK]],
        title="Promotions x Job Level — The Career Ceiling",
        labels={"number_of_promotions": "Promotions", "job_level": "Job Level", "rate": "Attrition %"},
        text_auto=True,
    )
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

# Chart 4 — Work Life Balance
with col4:
    wlb_order = ["Poor", "Fair", "Good", "Excellent"]
    wlb_df = df.groupby("work_life_balance", observed=True)["attrition"].mean().reset_index()
    wlb_df["rate"] = (wlb_df["attrition"] * 100).round(1)
    wlb_df["work_life_balance"] = pd.Categorical(wlb_df["work_life_balance"], categories=wlb_order, ordered=True)
    wlb_df = wlb_df.sort_values("work_life_balance")

    fig = px.bar(
        wlb_df, x="work_life_balance", y="rate",
        text="rate",
        color="rate",
        color_continuous_scale=[[0, SUCCESS], [0.5, ACCENT], [1, DANGER]],
        title="Work-Life Balance vs Attrition — The Paradox",
        labels={"work_life_balance": "Work-Life Balance", "rate": "Attrition Rate (%)"},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#1a1d3a")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0, 80], gridcolor="#f0f0f8")
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

col5, col6 = st.columns(2)

# Chart 5 — Attrition by Department
with col5:
    role_df = df.groupby("job_role")["attrition"].mean().reset_index()
    role_df["rate"] = (role_df["attrition"] * 100).round(1)
    role_df = role_df.sort_values("rate", ascending=True)

    fig = px.bar(
        role_df, x="rate", y="job_role",
        orientation="h",
        text="rate",
        color="rate",
        color_continuous_scale=[[0, ACCENT], [1, DARK]],
        title="Attrition Rate by Department",
        labels={"job_role": "", "rate": "Attrition Rate (%)"},
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#1a1d3a")
    fig.update_coloraxes(showscale=False)
    fig.update_xaxes(range=[0, 65], gridcolor="#f0f0f8")
    fig.update_layout(**chart_layout)
    st.plotly_chart(fig, use_container_width=True)

# Chart 6 — Income Distribution
with col6:
    income_df = df[["monthly_income", "attrition"]].copy()
    income_df["Status"] = income_df["attrition"].map({0: "Stayed", 1: "Left"})

    fig = px.histogram(
        income_df, x="monthly_income", color="Status",
        barmode="overlay", nbins=40,
        color_discrete_map={"Stayed": ACCENT, "Left": DANGER},
        opacity=0.75,
        title="Monthly Income — Stayed vs Left",
        labels={"monthly_income": "Monthly Income ($)", "count": "Employees"},
    )
    fig.update_yaxes(gridcolor="#f0f0f8")
    fig.update_layout(**chart_layout, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ── COST CHART ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Financial Impact</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Estimated replacement cost per segment at 6x monthly salary</div>', unsafe_allow_html=True)

cost_df = df.groupby("job_level", observed=True).apply(
    lambda x: round(x["attrition"].sum() * x["monthly_income"].mean() * 6 / 1e6, 1)
).reindex(["Entry", "Mid", "Senior"]).reset_index()
cost_df.columns = ["job_level", "cost_M"]

fig = px.bar(
    cost_df, x="job_level", y="cost_M",
    text="cost_M",
    color="job_level",
    color_discrete_map={"Entry": ACCENT, "Mid": DARK, "Senior": DANGER},
    title="Replacement Cost by Job Level ($M)",
    labels={"job_level": "Job Level", "cost_M": "Estimated Cost ($M)"},
)
fig.update_traces(texttemplate="$%{text}M", textposition="outside", textfont_color="#1a1d3a")
fig.update_yaxes(gridcolor="#f0f0f8")
fig.update_layout(
    plot_bgcolor=WHITE, paper_bgcolor=WHITE,
    font_family="DM Sans, sans-serif",
    title_font=dict(size=14, color=DARK, family="Syne, sans-serif"),
    showlegend=False,
    margin=dict(t=50, b=40, l=40, r=20),
    height=360,
)
st.plotly_chart(fig, use_container_width=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center; padding:2rem 0 1rem; margin-top:2rem;
            border-top:1px solid #e8eaff;">
    <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                color:{DARK};letter-spacing:0.05em;">kayfa</div>
    <div style="font-size:0.75rem;color:{MUTED};margin-top:0.3rem;letter-spacing:0.1em;">
        AI & DATA ANALYTICS INTERNSHIP PROGRAM · MONTH 1 · WEEK 1
    </div>
    <div style="font-size:0.72rem;color:{MUTED};margin-top:0.2rem;">
        Dataset: Synthetic HR Attrition · 44,686 records · Exploratory analysis only
    </div>
</div>
""", unsafe_allow_html=True)