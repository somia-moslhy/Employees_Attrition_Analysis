# Employee Attrition Analytics Dashboard

An end-to-end data analytics project on a synthetic HR dataset of 44,686 employees.
Built for the **Kayfa AI & Data Analytics Internship Program — Month 1, Week 1.**

---

## What This Project Does

Analyzes employee attrition data to answer one business question:

> **What 3 decisions should HR make today to stop attrition?**

---

## Key Findings

| # | Decision | Evidence |
|---|----------|----------|
| 01 | Mandate hybrid for Senior employees | Remote + Senior = **95% attrition** |
| 02 | Create career tracks above Senior | 3+ promotions = **94% attrition** |
| 03 | Invest in Entry-level early | Entry level = only **37% attrition** |

---

## Project Structure

```
├── app.py               # Streamlit dashboard
├── combined.csv         # Dataset (train + test combined)
├── requirements.txt     # Dependencies
├── EDA_notebook.ipynb   # Google Colab notebook
└── .streamlit/
    └── config.toml      # Light mode config
```

---

## Tools Used

- **Python** — Pandas, Plotly Express
- **Streamlit** — Interactive dashboard
- **Google Colab** — EDA notebook

---

## Dataset

- **Source:** [Kaggle — Synthetic Employee Attrition Dataset](https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset)
- **Size:** 74,498 rows (train + test combined to 44,686 after processing)
- **Nature:** Synthetic — patterns are realistic but generated

---

## Live Dashboard

[View on Streamlit Community Cloud]([https://your-app-link.streamlit.app](https://employeesattritionanalysis-8oyehtzk3vac2gs5qm3pzg.streamlit.app/))

---

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
