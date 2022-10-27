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



# CREATING SIDEBAR WIDGET FILTERS
geo_widget = df['geography'].unique().tolist()
type_widget = list(df['type'].unique())
year_widget = list(df['year'].unique())

# ADD THE FILTERS
with st.sidebar:
    st.write("""#### Interact with the dashboard by filtering options from this sidebar. ####""")
    type = st.multiselect(label = 'Choose an avocado type', options = type_widget, default= type_widget)
    years = st.multiselect('Choose a year between 2015 - 2020', options = year_widget, default = year_widget)
    regions = st.multiselect(label = 'Choose a region', options = geo_widget, default = ['Albany', 'California', 'Boise'])
    st.write("""
    Avocado Prices or Sales Dataset Information
Avocado dataset originally compiled from the Hass Avocado Board (or HAB, for short) data and published on Kaggle by Justin Kiggins in 2018. The dataset features historical data on avocado prices and sales volume in multiple cities, states, and regions of the USA. I used an updated version that includes data up to 2020.

This new data was downloaded from the HAB's website which allows downloading the data for years 2017 -- 2020 (as of August 2020).

Huge thanks to Justin Kiggins for the original dataset and to Hass Avocado Board for making the data publicly available!

    """)

# Slim down the filters
filtered_value = (df['year'].isin(years))  &(df['type'].isin(type)) #& (df['geography'].isin(regions))
new_df = (df['year'].isin(years))  &(df['type'].isin(type)) & (df['geography'].isin(regions))

#   GROUBPY ANALYSIS FOR PLOTTING
df_avg = round(df[filtered_value].groupby(by=['year']).mean()[['average_price']],2)
df_avg = df_avg.reset_index()

df_sum_of_bags= df[new_df].groupby(by = ['year']).sum()[['small_bags', 'large_bags', 'xlarge_bags']]
df_sum_of_bags = df_sum_of_bags.reset_index()

dia1, dia2 = st.columns(2)
with dia1:
    st.write("""
    ##### Average price sold per year #####
    """)
    fig = px.bar(df_avg, x = 'year', y = 'average_price', template = 'ggplot2')
    st.plotly_chart(fig)

with dia2:
    st.write("""
    ##### Scatterplot of average price vs total_bags solds #####
    """)
    fig2 = px.scatter(df, x = 'average_price', y = 'total_bags',
                      size = 'total_volume', color= 'type', hover_name = 'type',
                      log_x = True, size_max = 45,
                      animation_frame = 'year',animation_group = 'geography')

    st.plotly_chart(fig2)
    fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 3

dia3, dia4 = st.columns(2)
with dia3:
    # to get the sum of the columns of 4046, 4225, 4770
    new_df = df.iloc[:, 3:6].sum()
    df_piechart = px.pie(df_avg,
                title = 'Pie chart to compare the total sales of the PLUs',
                values = new_df,
                names = ['4046', '4225', '4770'])
    st.plotly_chart(df_piechart)


with dia4:
    fig4 = px.bar(df_sum_of_bags, x = 'year', y= ['small_bags', 'large_bags', 'xlarge_bags'],
                opacity = 0.9, orientation = 'v', barmode = 'group',
                title = 'Yearly total of different sizes of bags sold between 2015-2020', template = 'seaborn')
    st.plotly_chart(fig4)
