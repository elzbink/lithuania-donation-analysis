import streamlit as st

st.title("Lithuania Donation Analysis")
st.markdown("""
This interactive app analyses Lithuanian charity donation patterns by municipality, 
based on personal income tax donation declarations from 2021 to 2023.

Data source: [data.gov.lt](https://data.gov.lt)

### Content

**Geographic & Regional Analysis**
- Donation metrics by municipality (total, average, median, standard deviation)
- Top and bottom 10 municipality comparisons across years
- Choropleth map visualisations of donation intensity
- Donation type breakdown and most common recipient organisation by municipality
""")
