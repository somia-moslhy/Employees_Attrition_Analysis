import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.append('..')
from utils import load_data, DARK, ACCENT, DANGER, GREEN, WHITE, TEXT, CHART, WLB_ORDER, JS_ORDER

st.set_page_config(page_title="Segmentation", layout="wide")
st.sidebar.image("kayfa_logo.png", use_container_width=True)

df = load_data()
avg_rate = df['attrition'].mean() * 100

st.title("Comparison & Segmentation")
st.markdown("Q4 · Q5 · Q6 · Q7 — Who leaves, when, and what are the warning signs?")
st.divider()

# ── Q4 ────────────────────────────────────────────────────
st.subheader("Q4 — Pay Fairness: Does Higher Pay Reduce Attrition Within the Same Level?")

pay_rows = []
for level in ['Entry', 'Mid', 'Senior']:
    sub = df[df['job_level'] == level].copy()
    sub['income_quartile'] = pd.qcut(sub['monthly_income'], q=4,
                                      labels=['Q1 Low', 'Q2', 'Q3', 'Q4 High'])
    t = sub.groupby('income_quartile', observed=True)['attrition'].mean().reset_index()
    t['rate'] = (t['attrition'] * 100).round(1)
    t['Job Level'] = level
    pay_rows.append(t)

pay_df = pd.concat(pay_rows)
pay_df['Job Level'] = pd.Categorical(pay_df['Job Level'], categories=['Entry','Mid','Senior'], ordered=True)

fig = px.bar(pay_df, x="income_quartile", y="rate", color="Job Level",
             barmode="group", text="rate",
             color_discrete_map={"Entry": DANGER, "Mid": ACCENT, "Senior": GREEN},
             title="Attrition by Income Quartile within Each Job Level",
             labels={"income_quartile": "Income Quartile", "rate": "Attrition Rate (%)"})
fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
fig.update_yaxes(range=[0, 80])
fig.update_layout(**CHART, legend=dict(orientation="h", y=-0.2))
st.plotly_chart(fig, use_container_width=True)

st.info("**Insight:** Within every job level, income quartile moves attrition by at most 2 percentage points. Pay is not the driver — job level is. Entry sits at 63% regardless of salary. **Action:** Stop trying to retain Entry employees with pay rises alone. Invest in faster, clearer promotion paths to Mid level.")
st.divider()

# ── Q5 ────────────────────────────────────────────────────
st.subheader("Q5 — The Retention Timeline: At What Point Do Employees Leave?")

tenure_df = df.groupby("tenure_group", observed=True)["attrition"].mean().reset_index()
tenure_df["rate"] = (tenure_df["attrition"] * 100).round(1)

fig = px.line(tenure_df, x="tenure_group", y="rate", markers=True, text="rate",
              title="Attrition Rate by Years at Company",
              labels={"tenure_group": "Years at Company", "rate": "Attrition Rate (%)"},
              color_discrete_sequence=[DARK])
fig.update_traces(textposition="top center", textfont_color="#ffffff", line_width=3, marker_size=10)
fig.add_hline(y=avg_rate, line_dash="dash", line_color=DANGER,
              annotation_text=f"Company Average {avg_rate:.1f}%",
              annotation_position="top right")
fig.update_yaxes(range=[38, 60])
fig.update_layout(**CHART)
st.plotly_chart(fig, use_container_width=True)

st.info("**Insight:** Attrition peaks at years 3–5 (53.1%). Employees survive onboarding, gain experience, then leave when growth stalls. After 11 years loyalty rises sharply to 44%. **Action:** Focus retention resources on employees in years 3–10. A mid-career growth conversation at year 3 is the single most cost-effective HR intervention.")
st.divider()

# ── Q6 ────────────────────────────────────────────────────
st.subheader("Q6 — Engagement Warning Signs: Job Satisfaction + Work-Life Balance")

combo_df = df.groupby(['job_satisfaction','work_life_balance'], observed=True)['attrition'].mean().reset_index()
combo_df['rate'] = (combo_df['attrition'] * 100).round(1)

fig = px.density_heatmap(combo_df, x="work_life_balance", y="job_satisfaction", z="rate",
                          color_continuous_scale=[[0, GREEN],[0.5, ACCENT],[1, DANGER]],
                          text_auto=True,
                          title="Attrition Rate by Job Satisfaction and Work-Life Balance",
                          labels={"work_life_balance": "Work-Life Balance",
                                  "job_satisfaction": "Job Satisfaction",
                                  "rate": "Attrition %"})
fig.update_traces(textfont_color="#ffffff")
fig.update_layout(**CHART)
st.plotly_chart(fig, use_container_width=True)

st.info("**Insight:** Low Satisfaction + Poor WLB = 67% attrition — the highest combination. Work-Life Balance is the stronger lever: Poor WLB pushes attrition above 55% regardless of satisfaction level. **Action:** Any employee reporting Poor or Fair WLB should trigger an immediate manager conversation, even if they express satisfaction with the job itself.")
st.divider()

# ── Q7 ────────────────────────────────────────────────────
st.subheader("Q7 — Life Stage: Age, Marital Status, and Who Is Most at Risk")

c1, c2 = st.columns(2)

with c1:
    marital_df = df.groupby("marital_status")["attrition"].mean().reset_index()
    marital_df["rate"] = (marital_df["attrition"] * 100).round(1)
    marital_df = marital_df.sort_values("rate", ascending=False)
    fig = px.bar(marital_df, x="marital_status", y="rate", text="rate",
                 color="marital_status",
                 color_discrete_map={"Single": DANGER, "Divorced": ACCENT, "Married": GREEN},
                 title="Attrition by Marital Status",
                 labels={"marital_status": "Marital Status", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
    fig.update_yaxes(range=[0, 80])
    fig.update_layout(**CHART, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    age_df = df.groupby("age_group", observed=True)["attrition"].mean().reset_index()
    age_df["rate"] = (age_df["attrition"] * 100).round(1)
    fig = px.bar(age_df, x="age_group", y="rate", text="rate",
                 color="rate",
                 color_continuous_scale=[[0, GREEN],[0.5, ACCENT],[1, DANGER]],
                 title="Attrition by Age Group",
                 labels={"age_group": "Age Group", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0, 65])
    fig.update_layout(**CHART, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

single_young = df[(df['marital_status']=='Single') & (df['age_group']=='18-25')]
st.info(f"**Insight:** Single employees leave at 66.8% — nearly double married (36%). Single aged 18–25 hit **{single_young['attrition'].mean()*100:.1f}%** — the highest life-stage group in the dataset. **Action:** Design retention specifically for early-career single staff: mentorship, fast career tracks, and community belonging — not family-focused benefits.")