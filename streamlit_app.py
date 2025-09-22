import streamlit as st

#---- PAGE SETUP--------

about_page = st.Page(
    page = "/home/ayush/Practice_Projects/agents_fe/frontend/cat-agents-frontend/views/about_me.py",
    title = "About Me",
    icon = ":material/account_circle:",
    default=True
)

analysis_page = st.Page(
    page = "/home/ayush/Practice_Projects/agents_fe/frontend/cat-agents-frontend/views/analytics_dashboard.py",
    title = "Analayis dashboard",
    icon = ":material/bar_chart:",
)

chatbot_page = st.Page(
    page = "/home/ayush/Practice_Projects/agents_fe/frontend/cat-agents-frontend/views/chatbot.py",
    title = "chatbot",
    icon = ":material/smart_toy:",
)

#### ------ NAVIAGTION SETUP [WITHOUT SECTIONS}---------
# pg = st.navigation(pages = [about_page,analysis_page,chatbot_page])



#### ------ NAVIAGTION SETUP [SECTIONS}---------
pg = st.navigation(
    {
        "info":[about_page],
        "utilities":[analysis_page,chatbot_page]
    }
)
#---- RUN NAVIGATION----
pg.run()