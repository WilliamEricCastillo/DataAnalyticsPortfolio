import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.error import URLError

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

st.markdown("# Sales Dashboard")
st.divider()


@st.cache_data
def get_UN_data(file_path):

    df = pd.read_csv(file_path)

    df['Date'] = pd.to_datetime(df['Date'])

    return df


try:
    df = get_UN_data("/Users/willcastle/Desktop/supermarket_sales.csv")

    df['Total'] = df['Total'].round(0)
    df['gross income'] = df['gross income'].round(2)

    grouped_df = df.groupby(['City', 'Product line'])['Total'].sum().reset_index()
    grouped_df['Total'] = grouped_df['Total'].round(2)

    fig_items_city = px.bar(
        grouped_df,
        x='City',
        y='Total',
        color='Product line',
        title='Popular Items by City',
        labels={'Total': 'Total Sales'},
        barmode='group',
        text='Total',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig_items_city.update_layout(
        xaxis_title='City',
        yaxis_title='Total Sales',
        legend_title='Product Line',
        # title_x=0.5,
        title_font_size=24,
        yaxis_title_font_size=20,
        xaxis_title_font_size=20,
        xaxis_tickfont_size=14,
    )

    st.plotly_chart(fig_items_city, use_container_width=True)
    st.divider()

    st.subheader("Monthly Unit Sales by Product Line ")
    selected_cities = st.multiselect("Choose City", df['City'].unique(), default=df['City'].unique().tolist())

    if not selected_cities:
        st.error("Please select at least one city.")
    else:

        # Filter data for selected cities
        filtered_df = df[df['City'].isin(selected_cities)].copy()
        filtered_df['YearMonth'] = filtered_df['Date'].dt.to_period('M').astype(str)

        # Group by YearMonth and Product line, then sum the Total column
        grouped_df = filtered_df.groupby(['YearMonth', 'Product line'])['Total'].sum().reset_index()
        grouped_df['Total'] = grouped_df['Total'].round(2)

        fig_items_city_monthly = px.bar(
            grouped_df,
            x='YearMonth',
            y='Total',
            color='Product line',
            title='Monthly Unit Sales by Product Line',
            labels={'Total': 'Total Sales'},
            text='Total',
            color_discrete_sequence=px.colors.qualitative.Plotly,
            barmode='stack'
        )
        fig_items_city_monthly.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Unit Sales',
            xaxis_tickformat='%Y-%m',
            legend_title='Product Line',
            # title_x=0.5,
            yaxis_title_font_size=20,
            xaxis_title_font_size=20,
            xaxis_tickfont_size=14

        )
        st.plotly_chart(fig_items_city_monthly, use_container_width=True)
    st.divider()

except URLError as e:
    st.error(f"**This demo requires internet access.** Connection error: {e.reason}")
