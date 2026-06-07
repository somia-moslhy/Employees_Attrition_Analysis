import streamlit as st
import pandas as pd
import plotly.express as px
import sys
sys.path.append('..')
from utils import load_data, DARK, ACCENT, DANGER, GREEN, WHITE, TEXT, CHART

st.set_page_config(page_title="Decisions", layout="wide")
st.sidebar.image("kayfa_logo.png", use_container_width=True)

df = load_data()
avg_rate = df['attrition'].mean() * 100

st.title("Synthesis & Decision-Making")
st.markdown("Q8 · Q9 · Q10 — The hardest questions. The most valuable answers.")
st.divider()

# ── Q8 ────────────────────────────────────────────────────
st.subheader("Q8 — Career Stagnation: Does Feeling Stuck Drive Attrition?")

c1, c2 = st.columns(2)

with c1:
    promo_df = df.groupby("number_of_promotions")["attrition"].mean().reset_index()
    promo_df["rate"] = (promo_df["attrition"] * 100).round(1)
    promo_df["number_of_promotions"] = promo_df["number_of_promotions"].astype(str)
    fig = px.bar(promo_df, x="number_of_promotions", y="rate", text="rate",
                 color="rate",
                 color_continuous_scale=[[0, GREEN],[0.5, ACCENT],[1, DANGER]],
                 title="Attrition by Number of Promotions",
                 labels={"number_of_promotions": "Number of Promotions", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(range=[0, 60])
    fig.add_hline(y=avg_rate, line_dash="dash", line_color=DANGER,
                  annotation_text=f"Company Average {avg_rate:.1f}%",
                  annotation_position="top right")
    fig.update_layout(**CHART, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    opp_rows = []
    for col, label in [('leadership_opportunities','Leadership Opp.'),
                        ('innovation_opportunities','Innovation Opp.')]:
        t = df.groupby(col)['attrition'].mean().reset_index()
        t['rate'] = (t['attrition'] * 100).round(1)
        t['Opportunity'] = label
        t = t.rename(columns={col: 'Available'})
        opp_rows.append(t)
    opp_df = pd.concat(opp_rows)

    fig = px.bar(opp_df, x="Opportunity", y="rate", color="Available",
                 barmode="group", text="rate",
                 color_discrete_map={"No": DANGER, "Yes": GREEN},
                 title="Attrition by Growth Opportunities",
                 labels={"Opportunity": "", "rate": "Attrition Rate (%)"})
    fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
    fig.update_yaxes(range=[0, 60])
    fig.update_layout(**CHART, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)

st.info("**Insight:** Zero to two promotions all cluster at ~49% attrition — no meaningful difference between them. The real drop comes at 3+ promotions (24%). The first two promotions do not retain — consistent, ongoing advancement does. **Action:** Ensure employees reach their third promotion within a clear, communicated timeframe. Make the path visible from day one.")
st.divider()

# ── Q9 ────────────────────────────────────────────────────
st.subheader("Q9 — The Highest-Risk Profile: Who Is Most Likely to Leave?")

high_risk = df[
    (df['marital_status']    == 'Single') &
    (df['remote_work']       == 'No') &
    (df['overtime']          == 'Yes') &
    (df['work_life_balance'] == 'Poor')
]
hr_count = len(high_risk)
hr_rate  = round(high_risk['attrition'].mean() * 100, 1)

profile_df = pd.DataFrame({
    "Group": ["Company Average", "Highest-Risk Profile"],
    "Rate":  [round(avg_rate, 1), hr_rate],
})

fig = px.bar(profile_df, x="Group", y="Rate", text="Rate",
             color="Group",
             color_discrete_map={"Company Average": ACCENT, "Highest-Risk Profile": DANGER},
             title=f"Highest-Risk Profile vs Company Average  (n = {hr_count:,} employees)",
             labels={"Group": "", "Rate": "Attrition Rate (%)"})
fig.update_traces(texttemplate="%{text}%", textposition="outside", textfont_color="#ffffff")
fig.update_yaxes(range=[0, 100])
fig.add_annotation(x=1, y=55,
    text="Single · On-site · Overtime · Poor WLB",
    font=dict(size=11, color=TEXT), showarrow=False,
    bgcolor=WHITE, bordercolor=DANGER, borderpad=5)
fig.update_layout(**CHART, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

gap = round(hr_rate - avg_rate, 1)
st.info(f"**Insight:** {hr_count:,} employees match this profile — large enough to act on. Their attrition rate of {hr_rate}% is **+{gap} pp above the company average**. All four factors (remote eligibility, overtime, WLB, marital support) are controllable. **Action:** Prioritize this group for immediate intervention. Fixing even two of the four factors would significantly reduce their risk.")
st.divider()

# ── Q10 ───────────────────────────────────────────────────
st.subheader("Q10 — What Moves the Needle? If HR Fixes One Thing, What Should It Be?")

drivers_df = pd.DataFrame({
    "Driver": [
        "Remote Work (No to Yes)",
        "Work-Life Balance (Poor to Excellent)",
        "Promotions (0 to 3+)",
        "Overtime (Yes to No)",
        "Leadership Opportunities (No to Yes)",
    ],
    "Impact": [
        round(df[df['remote_work']=='No']['attrition'].mean()*100 - df[df['remote_work']=='Yes']['attrition'].mean()*100, 1),
        round(df[df['work_life_balance']=='Poor']['attrition'].mean()*100 - df[df['work_life_balance']=='Excellent']['attrition'].mean()*100, 1),
        round(df[df['number_of_promotions']==0]['attrition'].mean()*100 - df[df['number_of_promotions']>=3]['attrition'].mean()*100, 1),
        round(df[df['overtime']=='Yes']['attrition'].mean()*100 - df[df['overtime']=='No']['attrition'].mean()*100, 1),
        round(df[df['leadership_opportunities']=='No']['attrition'].mean()*100 - df[df['leadership_opportunities']=='Yes']['attrition'].mean()*100, 1),
    ]
}).sort_values("Impact", ascending=True)

fig = px.bar(drivers_df, x="Impact", y="Driver", orientation="h", text="Impact",
             color="Impact",
             color_continuous_scale=[[0, ACCENT],[1, DARK]],
             title="Top Attrition Drivers Ranked by Impact (attrition reduction if improved)",
             labels={"Driver": "", "Impact": "Attrition Reduction (percentage points)"})
fig.update_traces(texttemplate="-%{text} pp", textposition="outside", textfont_color="#ffffff")
fig.update_coloraxes(showscale=False)
fig.update_xaxes(range=[0, 35])
fig.update_layout(**CHART, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.info("**Insight — #1 Pick: Remote Work (-28 pp).** It is the single largest controllable lever in the dataset. The company currently offers remote work to only 19% of staff. Expanding access even to 38% would be the fastest, highest-impact action HR can take next quarter. **Rough estimate:** doubling remote eligibility while maintaining current attrition rates for remote workers could retain thousands of employees annually — each worth 6–12x their monthly salary in avoided replacement costs.")