import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import pycountry

# Load and preprocess the data
def load_data():
    data = {
        'Row ID': range(1, 75),
        'AUTHOR': ['Nagesh Shukla et al', 'Stephen K. Van Den Eeden et al', ...],  # Your author names
        'Year Published': [2020, 2022, ...],  # Your years
        'Country': ['Australia', 'USA', 'Brazil', 'South Africa', ...],  # Your countries
        'CONTINENT': ['Australia', 'North America', 'South America', 'Africa', ...],
        'Province': ['Nil'] * 74,
        'Health Condition Type': ['CANCERS', 'LIFE STYLE DISEASES', 'INFECTIOUS DISEASES', ...],
        'Health Condition': ['Cancer', 'Cardiovascular disease', 'Dengue', ...],
        'Platform': ['Google Earth'] * 74,
        'Insight': ['Barriers to Healthcare Access', ...]
    }
    
    df = pd.DataFrame(data)
    
    # Clean country names
    country_mapping = {
        'USA': 'United States',
        'UK': 'United Kingdom',
        'Türkiye': 'Turkey',
        'CHINA': 'China',
        'Zanzibar': 'Tanzania',
        'malawi': 'Malawi',
        'Brazi': 'Brazil',
        'EthiopiaMelioidosis': 'Ethiopia',
        'Chinese': 'China'
    }
    
    df['Country'] = df['Country'].replace(country_mapping)
    
    return df

def main():
    st.set_page_config(page_title="Global Disease Distribution", layout="wide")
    st.title("🌍 Global Disease Distribution Dashboard")
    st.markdown("Interactive visualization of disease patterns across countries based on research publications")
    
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Continent filter
    continents = ['All'] + sorted(df['CONTINENT'].dropna().unique().tolist())
    selected_continent = st.sidebar.selectbox("Select Continent", continents)
    
    # Disease type filter
    disease_types = ['All'] + sorted(df['Health Condition Type'].dropna().unique().tolist())
    selected_disease_type = st.sidebar.selectbox("Select Disease Type", disease_types)
    
    # Year range filter
    year_min = int(df['Year Published'].min())
    year_max = int(df['Year Published'].max())
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max)
    )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_continent != 'All':
        filtered_df = filtered_df[filtered_df['CONTINENT'] == selected_continent]
    if selected_disease_type != 'All':
        filtered_df = filtered_df[filtered_df['Health Condition Type'] == selected_disease_type]
    filtered_df = filtered_df[
        (filtered_df['Year Published'] >= selected_years[0]) & 
        (filtered_df['Year Published'] <= selected_years[1])
    ]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Disease Distribution by Country")
        
        # Count diseases by country
        country_disease_count = filtered_df['Country'].value_counts().reset_index()
        country_disease_count.columns = ['Country', 'Count']
        
        # Create choropleth map
        fig = px.choropleth(
            country_disease_count,
            locations="Country",
            locationmode="country names",
            color="Count",
            hover_name="Country",
            color_continuous_scale="Viridis",
            title="Number of Disease Studies by Country"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Countries")
        top_countries = country_disease_count.head(10)
        fig_bar = px.bar(
            top_countries,
            x='Count',
            y='Country',
            orientation='h',
            title="Studies by Country"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.subheader("Disease Type Distribution")
        disease_dist = filtered_df['Health Condition Type'].value_counts()
        fig_pie = px.pie(
            values=disease_dist.values,
            names=disease_dist.index,
            title="Disease Types"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed view
    st.subheader("Detailed Research Data")
    st.dataframe(
        filtered_df[['Country', 'Health Condition Type', 'Health Condition', 'Year Published', 'AUTHOR']],
        height=300
    )
    
    # Statistics
    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("Total Studies", len(filtered_df))
    with col4:
        st.metric("Countries Covered", filtered_df['Country'].nunique())
    with col5:
        st.metric("Disease Types", filtered_df['Health Condition Type'].nunique())

if __name__ == "__main__":
    main()