import pandas as pd
import streamlit as st
import plotly.express as px

#set header and webpage page_title
st.set_page_config(page_title = "Avocado stats", layout = 'wide')
st.header("Avocado Interactive Sales Visualization with Streamlit")


# read in the file
df = pd.read_csv("avocado-updated-2020.csv")

# -- PANDAS ANALYSIS
df.drop_duplicates(inplace = True) # drop duplicates

st.write("""
    #### Total Bags of Avocados Sold Through 2015-2020 ####
    """
)
# to calculate the total number of bags sold each year
#2015
yr_15 = round(df[df['year'] == 2015]['total_bags'].sum())

#2016
yr_16 = round(df[df['year'] == 2016]['total_bags'].sum())

#2017
yr_17 = round(df[df['year'] == 2017]['total_bags'].sum())

#2018
yr_18 = round(df[df['year'] == 2018]['total_bags'].sum())

#2019
yr_19 = round(df[df['year'] == 2019]['total_bags'].sum())

#2020
yr_20 = round(df[df['year'] == 2020]['total_bags'].sum())


# calculate percentage increase between 2015 and 2020
per_increase = round((int(yr_20 - yr_15)/ yr_15) * 100, 1)
percent_increase = f"{per_increase}%"

# STYLING FOR THE METRIC

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


# ADD THIS TO A STREAMLIT METRIC
col1, col2, col3, col4 = st.columns(4)

col1.metric(label = "2015 Sales",
            value = (yr_15),
)

col2.metric(label = "2016 Sales",
            value = (yr_16),
            delta = round(float((yr_16 - yr_15)/yr_15) *100, 1)
)


col3.metric(label = "2017 Sales",
            value = (yr_17),
            delta = round(float((yr_17 - yr_16)/yr_16) *100)
)

col4.metric(label = "2018 Sales",
            value = (yr_18),
            delta = round(float((yr_18 - yr_17)/yr_17) *100,1)
)

st.markdown("<hr/>", unsafe_allow_html = True)

col5, col6, col7 = st.columns(3)

col5.metric(label = "2019 Sales",
            value = (yr_19),
            delta = round(float((yr_19 - yr_18)/yr_18) *100, 1)
)

col6.metric(label = "2020 Sales",
            value = (yr_20),
            delta = round(float((yr_20 - yr_19)/yr_19) *100)
)

col7.metric(label = "% increase between 2015-2020",
            value = (percent_increase)

)



