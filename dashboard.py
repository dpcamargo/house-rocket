import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px
from datetime import datetime
import math


@st.cache(allow_output_mutation=True)
def get_data(path):
    return pd.read_csv(path, usecols=['id', 'date', 'price', 'bedrooms', 'bathrooms', 'sqft_lot', 'sqft_living',
                                      'floors', 'waterfront', 'zipcode', 'lat', 'long', 'yr_built'], parse_dates=['date'])


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)


def set_features(data):
    data['lot_m2'] = data['sqft_lot'] * 0.092903
    data['living_m2'] = data['sqft_living'] * 0.092903
    data = data.drop(['sqft_lot', 'sqft_living'], axis=1)
    data['price_m2'] = data['price'] / data['lot_m2']
    return data


def overview_data(data):
    st.header('Data Overview')
    st.sidebar.title('Data Overview')

    f_attributes = st.sidebar.multiselect('Attributes Filter', data.columns)
    f_zipcodes = st.sidebar.multiselect(
        'Zipcode Filter', data['zipcode'].sort_values().unique())

    # SELECTS DATASET BASED ON FILTER SELECTION
    # attributes + zipcodes = select rows and columns
    # attributes = select columns
    # zipcodes = select lines
    # 0 + 0 = original dataset
    if f_attributes != [] and f_zipcodes != []:
        df = data.loc[data['zipcode'].isin(f_zipcodes), f_attributes]
    elif f_attributes != [] and f_zipcodes == []:
        df = data.loc[:, f_attributes]
    elif f_attributes == [] and f_zipcodes != []:
        df = data.loc[data['zipcode'].isin(f_zipcodes), :]
    else:
        df = data.copy()

    # Zipcode Analysis
    if f_zipcodes == []:  # ZIPCODES FILTER EMPTY. SHOW METRIC FOR FULL DATASET
        df1 = data[['id', 'zipcode']
                   ].groupby('zipcode').count().reset_index()
        df2 = data[['price', 'lot_m2', 'price_m2', 'zipcode']
                   ].groupby('zipcode').mean().reset_index()
    else:
        df1 = data[data['zipcode'].isin(f_zipcodes)].groupby('zipcode')[
            'id'].count().reset_index()
        df2 = data[data['zipcode'].isin(f_zipcodes)].groupby(
            'zipcode')['price', 'lot_m2', 'price_m2'].mean().reset_index()

    df1 = pd.merge(df1, df2, on='zipcode', how='outer')

    # Descriptive statistics
    if f_attributes == ['date']:  # DO NOT describe() IF ONLY date IS FILTERED
        df2 = pd.DataFrame(
            columns=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    else:
        num_attributes = df.select_dtypes(include=['int64', 'float64'])
        df2 = num_attributes.describe().transpose()

    st.dataframe(df, height=400)
    c1, c2 = st.columns((1, 2))
    c1.header('Zipcode Analysis')
    c1.dataframe(df1, height=394)
    c2.header('Filtered Analysis')
    c2.dataframe(df2, height=400)

    return None


def portfolio_density(data, geofile):
    st.sidebar.title('Region Overview')

    f_map_sampling = st.sidebar.slider(
        'Number of Samples', 100, len(data), 100, 1)
    st.sidebar.write('*Sampling used to decrease processing time')

    df = data.sample(f_map_sampling)

    # Region House Density
    st.title('Region Overview')
    c1, c2 = st.columns((1, 1))

    c1.header('Real Estate Density')

    house_density = folium.Map(
        location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to(house_density)
    for name, row in df.iterrows():
        popup = folium.Popup(
            html=f"Sold for <strong>R$ {int(row['price'])//1000}k</strong> on {row['date'].strftime('%m/%Y')}.</br><strong>Size:</strong> {'{:.0f}'.format(row['lot_m2'])}m²</br><strong>Bedrooms:</strong> {row['bedrooms']}</br><strong>Bathrooms:</strong> {row['bathrooms']}", max_width=110)
        folium.Marker([row['lat'], row['long']],
                      popup=popup).add_to(marker_cluster)

    with c1:
        folium_static(house_density)

    # Region Price Density
    c2.header('Price Density')

    df1 = df[['price', 'zipcode']].groupby(
        'zipcode').mean().reset_index().copy()
    df1.columns = ['ZIP', 'PRICE']
    geofile = geofile[geofile['ZIP'].isin(
        df1['ZIP'].tolist())]  # Clears ZIPs not in df4

    price_density = folium.Map(
        location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)
    price_density.choropleth(data=df1, columns=['ZIP', 'PRICE'], geo_data=geofile, key_on='feature.properties.ZIP',
                             fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='Avg Price')

    with c2:
        folium_static(price_density)

    return None


def real_estate_distribution(data):
    yr_built_min = int(data['yr_built'].min())
    yr_built_max = int(data['yr_built'].max())
    date_min = datetime.date(data['date'].min())
    date_max = datetime.date(data['date'].max())
    st.sidebar.title('Real Estate Attributes')
    f_year_built = st.sidebar.slider(
        'Construction Year Interval', yr_built_min, yr_built_max, (yr_built_min, yr_built_max))
    f_date = st.sidebar.slider('Sale Date Interval', date_min,
                               date_max, (date_min, date_max))

    st.title('Real Estate Attributes')

    # Average price per year built
    df = data.loc[(data['yr_built'] >= f_year_built[0])
                  & (data['yr_built'] <= f_year_built[1])]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()
    fig1 = px.line(df, x='yr_built', y='price')

    # Average price per day
    df = data.loc[(data['date'] >= pd.to_datetime(f_date[0])) &
                  (data['date'] <= pd.to_datetime(f_date[1]))]
    df = df[['price', 'date']].groupby('date').mean().reset_index()
    fig2 = px.line(df, x='date', y='price')

    c3, c4 = st.columns((1, 1))
    with c3:
        st.header('Average Price Per Year Built')
        st.plotly_chart(fig1, use_container_width=True)
    with c4:
        st.header('Average Price Per Day')
        st.plotly_chart(fig2, use_container_width=True)

    return None


def attributes_distribution(data):
    st.title('Price Distribution')
    st.sidebar.title('Price distribution')
    price_min = math.floor(data['price'].min())
    price_max = math.ceil(data['price'].max())

    f_price_interval = st.sidebar.slider(
        'Price Interval', price_min, price_max, (price_min, price_max), 10000)

    df = data.loc[(data['price'] >=
                   f_price_interval[0]) & (data['price'] <=
                                           f_price_interval[1])]
    fig3 = px.histogram(df, x='price', nbins=50)
    st.plotly_chart(fig3, use_container_width=True)

    st.sidebar.title('Histogram Filters')
    f_bedrooms = st.sidebar.selectbox(
        'Max bedrooms', data['bedrooms'].sort_values(ascending=False).unique(), index=0)
    f_bathrooms = st.sidebar.selectbox(
        'Max bathrooms', data['bathrooms'].sort_values(ascending=False).unique(), index=0)
    f_floors = st.sidebar.selectbox(
        'Max floors', data['floors'].sort_values(ascending=False).unique(), index=0)
    f_waterview = st.sidebar.checkbox('Only Houses with Water View')

    # House per bedrooms
    c1, c2, c3 = st.columns((1, 1, 1))

    if f_waterview == 1:
        df = data[data['waterfront'] == 1]
    else:
        df = data.copy()

    with c1:
        c1.header('Bedrooms')
        fig = px.histogram(
            df[df['bedrooms'] <= f_bedrooms], x='bedrooms', nbins=19)
        c1.plotly_chart(fig, use_container_width=True)
    # House per bathrooms
    with c2:
        c2.header('Bathrooms')
        fig = px.histogram(
            df[df['bathrooms'] <= f_bathrooms], x='bathrooms', nbins=8)
        c2.plotly_chart(fig, use_container_width=True)
    # House per floors
    with c3:
        c3.header('Floors')
        fig = px.histogram(df[df['floors'] <= f_floors], x='floors', nbins=8)
        c3.plotly_chart(fig, use_container_width=True)

    return None


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    # EXTRACTION
    path = './datasets/kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data(path)
    geofile = get_geofile(url)

    # TRANSFORMATION
    data = set_features(data)
    overview_data(data)
    portfolio_density(data, geofile)
    real_estate_distribution(data)
    attributes_distribution(data)
