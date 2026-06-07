import streamlit as st

home  = st.Page("home.py",           title="Home",           icon="🏠", default=True)
p1    = st.Page("pages/1_Foundations.py",  title="Foundations",    icon="📊")
p2    = st.Page("pages/2_Segmentation.py", title="Segmentation",   icon="🔍")
p3    = st.Page("pages/3_Decisions.py",    title="Decisions",      icon="🎯")

pg = st.navigation({"Dashboard": [home, p1, p2, p3]})
pg.run()