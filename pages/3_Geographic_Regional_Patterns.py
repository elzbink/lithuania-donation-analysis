import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
import json
from data_prep import load_data
from matplotlib.colors import to_hex
from matplotlib import cm
import json
import requests
#-----------------------------
# FIRST GRAPH
st.subheader("1. Donation Metrics by Municipality")
df_clean = load_data()

metric_options = {
    'Total Donated': ('total_donated', 'Total Donated (EUR)'),
    'Average Donation': ('average_donation', 'Average Donation (EUR)'),
    'Median Donation': ('median_donation', 'Median Donation (EUR)'),
    'Donation Count': ('donation_count', 'Number of Donations'),
    'Donation Std Dev': ('donation_std', 'Donation Standard Deviation')
}

selected_year = st.selectbox("Select Year", ['Total', '2021', '2022', '2023'], key="map1")
selected_metrics = st.multiselect("Select Metrics", list(metric_options.keys()), default=['Total Donated','Average Donation','Donation Std Dev'])

if selected_year == 'Total':
    df = df_clean.copy()
else:
    df = df_clean[df_clean['metai'] == int(selected_year)]

municipality_stats = df.groupby('gavejo_savivaldybe').agg(
    total_donated=('suma', 'sum'),
    average_donation=('suma', 'mean'),
    median_donation=('suma', 'median'),
    donation_count=('suma', 'count'),
    donation_std=('suma', 'std')
).reset_index()

if selected_metrics:
    rows = len(selected_metrics)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                        subplot_titles=[f"{label} ({selected_year})" for label in selected_metrics])

    for i, label in enumerate(selected_metrics, start=1):
        metric_col, y_title = metric_options[label]
        sorted_df = municipality_stats.sort_values(by=metric_col, ascending=False)
        fig.add_trace(go.Bar(
            x=sorted_df['gavejo_savivaldybe'],
            y=sorted_df[metric_col],
            marker=dict(color=sorted_df[metric_col], colorscale='Cividis'),
            showlegend=False
        ), row=i, col=1)
        fig.update_yaxes(title_text=y_title, row=i, col=1)

    fig.update_layout(height=max(600, 300 * rows), showlegend=False)
    for i in range(1, rows + 1):
        fig.update_xaxes(row=i, col=1, tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Select one or more metrics to display.")


with st.expander("Key Insights from 2021–2023"):
    st.markdown("""
**Overall Trends (2021–2023):**
- **Vilnius** consistently leads in both the **total amount donated** and **number of donations** across all years.
- **Neringa** stands out each year with the **highest average and median donation amounts**, despite having one of the **lowest donation counts** — suggesting fewer but wealthier donors.
- **Kaunas** maintains a strong position in donation volume but with more moderate average donation values, indicating broad participation.

**Notable Year-Specific Outliers:**
- Each year there were **unusually high standard deviation** in donation size for diffferent regions, pointing to extreme outliers.
- In **2023**, **Neringa** again led in donation amounts but also had the **highest variability**, highlighting the influence of a few large donations.
""")












#-------------------------------
# SECOND GRAPH
st.subheader("2. Top/Bottom 10 Municipalities")
metric_options10 = {
    'Top 10 by Total Donated': ('total_donated', False, 'Total Donated (EUR)'),
    'Top 10 by Average Donation': ('average_donation', False, 'Average Donation (EUR)'),
    'Top 10 by Number of Donations': ('donation_count', False, 'Number of Donations'),
    'Bottom 10 by Total Donated': ('total_donated', True, 'Total Donated (EUR)'),
    'Bottom 10 by Average Donation': ('average_donation', True, 'Average Donation (EUR)'),
    'Bottom 10 by Number of Donations': ('donation_count', True, 'Number of Donations')
}

selected_year2 = st.selectbox("Select Year", ['Total', '2021', '2022', '2023'], key="map2")
selected_charts = st.multiselect("Select Charts", list(metric_options10.keys()), default=['Top 10 by Average Donation','Bottom 10 by Average Donation'])

if selected_year2 == 'Total':
    df = df_clean.copy()
else:
    df = df_clean[df_clean['metai'] == int(selected_year2)]

municipality_stats = df.groupby('gavejo_savivaldybe').agg(
    total_donated=('suma', 'sum'),
    average_donation=('suma', 'mean'),
    median_donation=('suma', 'median'),
    donation_count=('suma', 'count'),
    donation_std=('suma', 'std')
).reset_index()

if selected_charts:
    rows = len(selected_charts)
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=False, vertical_spacing=0.2,
                        subplot_titles=[f"{label} ({selected_year2})" for label in selected_charts])

    for i, label in enumerate(selected_charts, start=1):
        metric_col, ascending, x_title = metric_options10[label]
        sorted_data = municipality_stats.sort_values(metric_col, ascending=ascending).head(10)
        fig.add_trace(go.Bar(
            x=sorted_data[metric_col],
            y=sorted_data['gavejo_savivaldybe'],
            orientation='h',
            marker=dict(color=sorted_data[metric_col], colorscale='Cividis'),
            showlegend=False
        ), row=i, col=1)
        fig.update_yaxes(autorange="reversed", row=i, col=1)
        fig.update_xaxes(title_text=x_title, row=i, col=1)

    fig.update_layout(height=max(600, 300 * rows), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Select one or more charts to display.")

with st.expander("Municipality-Level Donation Insights (2021–2023)"):
    st.markdown("""
**Consistent Top Performers:**
- **Neringa** leads all years in **average donation amount**, despite ranking in the **bottom 10 by donation count** ,showing its pattern of high value, low frequency donations.
- **Vilnius** dominates in both **total amount donated** and **number of donations** every year, showing strong and broad participation.
- **Klaipėdos m. sav.** and **Kaunas m. sav.** frequently appear in the **top 5** for both donation volume and count.

**Consistent Low Performers:**
- Municipalities like **Šalčininkų r. sav.** and **Kalvarijos sav.** repeatedly appear in the **bottom 10 for average donations**, indicating smaller donation sizes.
- **Visagino sav.** and **Rietavo sav.** are often seen in the **bottom 10 for total amount donated**, suggesting low overall activity.

**Year Specific Notes:**
- In **2021**, **Akmenės r. sav.** unexpectedly topped the average donation chart.
- In **2023**, **Pakruojo r. sav.** showed up in the **bottom 10 for total donations**, possibly indicating a drop in engagement.
""")








#----------------------
# FIRST MAP
st.subheader("3. Choropleth Map of Donations (Log Scale)")
selected_year3 = st.selectbox("Select Year", ['Total', '2021', '2022', '2023'], key="map3")


import json
import streamlit as st

@st.cache_data
def load_geojson():
    with open("lithuania_admin_level_5_simplified.json", "r", encoding="utf-8") as f:
        return json.load(f)

lithuania_geojson = load_geojson()



df = df_clean.copy() if selected_year3 == 'Total' else df_clean[df_clean['metai'] == int(selected_year3)]
map_metric = st.selectbox("Select Metric to Display", ["Total Donated (log)", "Average Donation (log)"], key="map_metric")

stats = df.groupby('gavejo_savivaldybe').agg(
    total_donated=('suma', 'sum'),
    average_donation=('suma', 'mean')
).reset_index()

stats['total_donated_log'] = np.log1p(stats['total_donated'])
stats['average_donation_log'] = np.log1p(stats['average_donation'])

if map_metric == "Total Donated (log)":
    color_col = 'total_donated_log'
    color_title = "Total Donated"
    hover_template = "<b>%{customdata[0]}</b><br>Total Donated: %{customdata[1]:,.0f} EUR<extra></extra>"
    custom_data = ['gavejo_savivaldybe', 'total_donated']
else:
    color_col = 'average_donation_log'
    color_title = "Average Donation"
    hover_template = "<b>%{customdata[0]}</b><br>Average Donation: %{customdata[1]:,.2f} EUR<extra></extra>"
    custom_data = ['gavejo_savivaldybe', 'average_donation']


fig = px.choropleth_mapbox(
    stats,
    geojson=lithuania_geojson,
    locations='gavejo_savivaldybe',
    featureidkey='properties.name',
    color=color_col,
    custom_data=custom_data,
    color_continuous_scale='YlGnBu',
    zoom=5.8,
    center={"lat": 55.1694, "lon": 23.8813},
    opacity=0.7,
    height=650,
    width=2000,
    mapbox_style="carto-positron",
)

fig.update_traces(hovertemplate=hover_template)
fig.update_layout(
    margin={"r":0,"t":40,"l":0,"b":0},
    title_text=f"{color_title} by Municipality ({selected_year3}) — Log Scale",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Total Sum Donation Patterns (2021–2023)"):
    st.markdown("""
**Total Donated Amount:**
- Donation intensity is consistently highest in **Vilnius**, which stands out on the map each year as the top donor municipality.
- Overall, **regional donation patterns are stable**: central and major urban areas donate more, while peripheral regions contribute less.
- In **2023**, several **southern and western municipalities** show slightly deeper colors, indicating a modest rise in total donations.

**Average Donation Amount:**
- **Neringa** consistently leads with the **highest average donation values**, despite being among the least frequent donors.
- The **lowest average donations** tend to cluster in **southern and western regions**, suggesting smaller but more numerous contributions.
- In **2021**, **Akmenės r. sav.** stood out with an **average donation of 85.20 EUR**, one of the highest in the country that year, likely driven by a few large individual contributions.
""")







#-------------------------------
# TABLE
st.subheader("4. Donation Type Share Table by Municipality")
selected_year5 = st.selectbox("Select Year", ['Total', '2021', '2022', '2023'], key="table")
df = df_clean.copy() if selected_year5 == 'Total' else df_clean[df_clean['metai'] == int(selected_year5)]
grouped = df.groupby(['gavejo_savivaldybe', 'gavejo_tipas'])['suma'].sum().reset_index()
pivot = grouped.pivot(index='gavejo_savivaldybe', columns='gavejo_tipas', values='suma').fillna(0)
percent_df = pivot.div(pivot.sum(axis=1), axis=0) * 100
percent_df = percent_df.round(1).reset_index()
st.dataframe(percent_df.head(20))





#------------------------
# SECOND MAP
st.subheader("5. Most Common Organization Type by Municipality")
df_pg = df_clean[
    (df_clean['gavejo_tipas'] == 'Paramos gavėjas') &
    (df_clean['gavejo_imones_rusis'].notna()) &
    (df_clean['gavejo_imones_rusis'].str.lower() != 'kita')
].copy()

selected_year4 = st.selectbox("Select Year", ['Total', '2021', '2022', '2023'], key="map4")
df = df_pg.copy() if selected_year4 == 'Total' else df_pg[df_pg['metai'] == int(selected_year4)]
most_popular = df.groupby(['gavejo_savivaldybe', 'gavejo_imones_rusis']).size().reset_index(name='count')
most_popular = most_popular.sort_values(['gavejo_savivaldybe', 'count'], ascending=[True, False]).drop_duplicates('gavejo_savivaldybe')

color_categories = sorted(df_pg['gavejo_imones_rusis'].unique())
fixed_colors = px.colors.qualitative.Vivid[:len(color_categories)]

color_map = {cat: fixed_colors[i % len(fixed_colors)] for i, cat in enumerate(color_categories)}
category_orders = {"gavejo_imones_rusis": color_categories}


fig = px.choropleth_mapbox(
    most_popular,
    geojson=lithuania_geojson,
    locations='gavejo_savivaldybe',
    featureidkey='properties.name',
    color='gavejo_imones_rusis',
    custom_data=['gavejo_savivaldybe', 'gavejo_imones_rusis', 'count'],
    color_discrete_map=color_map,
    category_orders=category_orders,
    mapbox_style="carto-positron",
    zoom=5.8,
    center={"lat": 55.1694, "lon": 23.8813},
    opacity=0.7,
    height=650,
    width=2000
)

fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><br>Most Common Type: %{customdata[1]}<br>Count: %{customdata[2]}<extra></extra>")
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, title_text=f"Most Common Organization Type by Municipality ({selected_year4})", title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Organization Types by Municipality (2021–2023)"):
    st.markdown("""
**Most Common Recipient Organization Types (2021–2023):**
- **Associations (Asociacija)** are the most common recipient type in the majority of municipalities, with this pattern remaining stable across all years.
- **Public institutions (Viešoji įstaiga)** appear more frequently in western and central Lithuania, suggesting regionally stronger institutional presence or outreach.
- **Charity and support funds (Labdaros ir paramos fondas)** are less common overall but show some regional strength, particularly in southern and southeastern areas.
- In **2021, Druskininkų r.** was uniquely dominated by **religious organizations**, a rare and isolated case not seen in other years.
""")
