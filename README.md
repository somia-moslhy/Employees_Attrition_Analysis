# Week 1 Task: Who Is Leaving and Why?
### Employee Attrition Analytics Dashboard

**Kayfa — AI & Data Analytics Internship Program · Month 1 · Week 1**

---

## Overview

An end-to-end data analytics project on a synthetic HR dataset of 74,498 employees.
The goal was not just to explore the data — but to answer one business question:

> **What decisions should HR make today to reduce attrition?**

---

## Key Findings

| # | Finding | Number |
|---|---------|--------|
| 1 | Remote employees leave at less than half the rate of on-site staff | 24.7% vs 52.8% |
| 2 | The income gap between leavers and stayers | less than $70/month |
| 3 | Attrition peaks at years 3–5 of tenure | 53.1% |
| 4 | Single employees aged 18–25 | 72% attrition |
| 5 | Employees with 3+ promotions | drops to 24% |

## The 3 Decisions

**01 — Expand Remote Work**
Remote work is the largest controllable lever in the data. Expanding eligibility from 19% to 38% of staff is the single highest-impact action HR can take.

**02 — Fix the Promotion Path**
The first two promotions do not retain employees. Consistent advancement to a third promotion is what actually moves the number.

**03 — Retain Single Early-Career Employees**
Single employees aged 18–25 are the most mobile group. Family-focused benefits will not work here — mentorship and fast career tracks will.

---

## Project Structure

```
├── app.py                    # Entry point — st.navigation multipage
├── home.py                   # Homepage with KPIs, decisions, summary charts
├── utils.py                  # Shared data loader and color palette
├── combined.csv              # Dataset (train + test combined)
├── kayfa_logo.png            # Kayfa brand logo
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Dark navy theme
└── pages/
    ├── 1_Foundations.py      # Q1 Q2 Q3 — headline, overtime, remote work
    ├── 2_Segmentation.py     # Q4 Q5 Q6 Q7 — pay, tenure, engagement, life stage
    └── 3_Decisions.py        # Q8 Q9 Q10 — stagnation, risk profile, top driver
```

---

## Dashboard Pages

| Page | Questions Answered |
|------|--------------------|
| Home | KPIs · Top 3 Decisions · Summary Charts |
| Foundations | Q1 Overall attrition · Q2 Overtime · Q3 Remote work |
| Segmentation | Q4 Pay fairness · Q5 Retention timeline · Q6 Engagement · Q7 Life stage |
| Decisions | Q8 Career stagnation · Q9 Highest-risk profile · Q10 What moves the needle |

---

## Tools

- **Python** — Pandas, NumPy, scikit-learn
- **Visualization** — Plotly Express
- **Dashboard** — Streamlit (multipage with `st.navigation`)

---

## Dataset

- **Source:** [Kaggle — Synthetic Employee Attrition Dataset](https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset)
- **Size:** 74,498 rows across train.csv and test.csv
- **Nature:** Synthetic — patterns are realistic but generated

---

## Live Dashboard

[View on Streamlit Community Cloud](https://employeesattritionanalysis-8oyehtzk3vac2gs5qm3pzg.streamlit.app/Decisions)

---

## How to Run Locally

```bash
git clone https://github.com/your-username/your-repo-name
cd your-repo-name
pip install -r requirements.txt
streamlit run app.py
```

---

## Requirements

```
streamlit
pandas
plotly
scikit-learn
numpy
```
