import streamlit as st
import pandas as pd
from datetime import datetime
import glob
import os
import webbrowser


def load_data():
    try:
        list_of_files = glob.glob('data_positions_full_*.csv')
        if not list_of_files:
            return pd.DataFrame(
                {'title': [], 'company': [], 'location': [], 'url': [], 'application_url': [], 'date_posted': []})
        latest_file = max(list_of_files, key=os.path.getctime)
        df = pd.read_csv(latest_file).astype(str)
        df = df.replace('nan', '')
        df = df.replace('None', '')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(
            {'title': [], 'company': [], 'location': [], 'url': [], 'application_url': [], 'date_posted': []})


def create_dashboard():
    st.set_page_config(page_title="2025 Data Positions", layout="wide")
    st.title('2025 Data Positions Dashboard')

    df = load_data()
    if df.empty:
        st.warning("No data available. Please run the scraper first to collect job listings.")
        return

    st.sidebar.header('Filters')

    try:
        companies = ['All'] + sorted(df['company'].unique().tolist())
        company_filter = st.sidebar.selectbox('Select Company', companies)

        locations = ['All'] + sorted(df['location'].unique().tolist())
        location_filter = st.sidebar.selectbox('Select Location', locations)

        roles = ['All', 'Data Analyst', 'Data Scientist', 'Other']
        role_filter = st.sidebar.selectbox('Select Role Type', roles)

        filtered_df = df.copy()

        if company_filter != 'All':
            filtered_df = filtered_df[filtered_df['company'] == company_filter]
        if location_filter != 'All':
            filtered_df = filtered_df[filtered_df['location'] == location_filter]
        if role_filter != 'All':
            if role_filter == 'Other':
                filtered_df = filtered_df[~filtered_df['title'].str.contains('Analyst|Scientist', case=False, na=False)]
            else:
                filtered_df = filtered_df[filtered_df['title'].str.contains(role_filter, case=False, na=False)]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total Positions', len(filtered_df))
        with col2:
            st.metric('Companies', filtered_df['company'].nunique())
        with col3:
            st.metric('Locations', filtered_df['location'].nunique())

        st.subheader('💼 Available Positions')

        if filtered_df.empty:
            st.info("No positions found matching the selected filters.")
        else:
            for idx, row in filtered_df.iterrows():
                with st.expander(f"🏢 {row['title']} at {row['company']}"):
                    if row['application_url'] and len(row['application_url'].strip()) > 0:
                        st.markdown(f"**Company:** [{row['company']}]({row['application_url']})")
                    else:
                        st.markdown(f"**Company:** {row['company']}")
                    st.markdown(f"**Location:** {row['location']}")
                    st.markdown(f"**Posted:** {row['date_posted']}")

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")


if __name__ == "__main__":
    create_dashboard()