import streamlit as st
import pandas as pd

DARK   = "#353b98"
ACCENT = "#8a91f2"
DANGER = "#ff6b6b"
GREEN  = "#43d9a0"
WHITE  = "#ffffff"
TEXT   = "#ffffff"

WLB_ORDER   = ['Poor', 'Fair', 'Good', 'Excellent']
JS_ORDER    = ['Low', 'Medium', 'High', 'Very High']
LEVEL_ORDER = ['Entry', 'Mid', 'Senior']

CHART = dict(
    plot_bgcolor  = "rgba(0,0,0,0)",
    paper_bgcolor = "rgba(0,0,0,0)",
    font_color    = "#e8eaf6",
    margin        = dict(t=50, b=40, l=40, r=30),
    height        = 420,
)

@st.cache_data
def load_data():
    df = pd.read_csv("combined.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    df['attrition'] = df['attrition'].map({'Left': 1, 'Stayed': 0})
    df['attrition_label'] = df['attrition'].map({1: 'Left', 0: 'Stayed'})
    df['work_life_balance'] = pd.Categorical(df['work_life_balance'], categories=WLB_ORDER, ordered=True)
    df['job_satisfaction']  = pd.Categorical(df['job_satisfaction'],  categories=JS_ORDER,  ordered=True)
    df['job_level']         = pd.Categorical(df['job_level'],         categories=LEVEL_ORDER, ordered=True)
    df['tenure_group'] = pd.cut(df['years_at_company'],
        bins=[0, 2, 5, 10, 20, 100],
        labels=['0-2 yrs', '3-5 yrs', '6-10 yrs', '11-20 yrs', '20+ yrs'])
    df['age_group'] = pd.cut(df['age'],
        bins=[17, 25, 35, 45, 60],
        labels=['18-25', '26-35', '36-45', '46-60'])
    return df


def render_sidebar(df):
    """Renders filters in sidebar and returns filtered dataframe."""
    st.sidebar.image("kayfa_logo.png", width='stretch')
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")

    roles = ["All"] + sorted(df["job_role"].unique().tolist())
    sel_role = st.sidebar.selectbox("Job Role", roles)

    levels = ["All"] + sorted(df["job_level"].unique().tolist())
    sel_level = st.sidebar.selectbox("Job Level", levels)

    remote_opts = ["All", "Yes", "No"]
    sel_remote = st.sidebar.selectbox("Remote Work", remote_opts)

    age_min = int(df["age"].min())
    age_max = int(df["age"].max())
    age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

    st.sidebar.markdown("---")
    st.sidebar.caption("Kayfa · AI & Data Analytics · Month 1 Week 1")

    # apply filters
    filtered = df.copy()
    if sel_role   != "All": filtered = filtered[filtered["job_role"]   == sel_role]
    if sel_level  != "All": filtered = filtered[filtered["job_level"]  == sel_level]
    if sel_remote != "All": filtered = filtered[filtered["remote_work"] == sel_remote]
    filtered = filtered[(filtered["age"] >= age_range[0]) & (filtered["age"] <= age_range[1])]

    return filtered