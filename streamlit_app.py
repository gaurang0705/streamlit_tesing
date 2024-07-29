import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Load data based on the selected file
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to create utilization plot
def create_utilization_plot(line_number, utilization_df):
    filtered_df = utilization_df[utilization_df["Line"] == line_number]
    fig = px.bar(
        filtered_df,
        x="Month_y",
        y="utilization_percentage",
        title=f"Utilization Percentage for {line_number}",
        labels={"Month_y": "Month", "utilization_percentage": "Utilization Percentage"},
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Utilization Percentage",
        yaxis=dict(range=[0, 100]),
        template="plotly_white",
        title_font=dict(size=20, family="Arial, sans-serif"),
        title_x=0.25,
    )
    return fig

# Function to calculate overall utilization
def calculate_overall_utilization(utilization_df):
    utilization_summary = []
    for line in utilization_df['Line'].unique():
        line_df = utilization_df[utilization_df['Line'] == line]
        total_production = line_df['Quantity'].sum()
        total_capacity = round((line_df['total_working_days'] * line_df['daily_capacity']).sum(), 0)
        overall_utilization = round((total_production / total_capacity) * 100, 0)
        utilization_summary.append({
            'Line': line,
            'Total Production': total_production,
            'Total Capacity': total_capacity,
            'Overall Utilization Percentage': overall_utilization
        })
    return pd.DataFrame(utilization_summary)

# Function to create demand fulfillment plot
def create_demand_plot(selected_products, demand_df):
    prod_name = ', '.join(selected_products)
    
    filtered_df = demand_df[demand_df["Product"].isin(selected_products)]
    fig = px.bar(
        filtered_df,
        x="Month",
        y=["Optimized Plan quantity", "Sale Demand"],
        barmode="group",
        title=f"Monthly Demand Fulfillment for {prod_name}",
        labels={"value": "Quantity", "variable": "Legend"},
        height=400,
    )
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, family="Arial, sans-serif"),
        title_x=0.25,
    )
    return fig

# Function to calculate overall demand fulfillment
def calculate_overall_demand_fulfillment(demand_df):
    demand_summary = []
    for product in demand_df['Product'].unique():
        product_df = demand_df[demand_df['Product'] == product]
        total_optimized_plan = product_df['Optimized Plan quantity'].sum()
        total_demand = product_df['Sale Demand'].sum()
        overall_fulfillment = round((total_optimized_plan / total_demand) * 100, 0)
        demand_summary.append({
            'Product': product,
            'Total Optimized Plan': total_optimized_plan,
            'Total Demand': total_demand,
            'Fulfillment Percentage': overall_fulfillment
        })
    return pd.DataFrame(demand_summary)

# Streamlit code
def main():
    st.set_page_config(page_title="Production Schedule Dashboard", layout="wide")

    st.title("Production Schedule Dashboard")
    st.markdown("## Overview")
    st.markdown(
        """
        This dashboard provides insights into the production lines and demand fulfillment.
        Select an analysis type and configure the options to view the respective analysis.
        """
    )

    st.sidebar.title("Configuration")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type", ["Line Utilization", "Demand Fulfillment"]
    )

    if analysis_type == "Line Utilization":
        utilization_files = sorted(os.listdir('line_utilization'), reverse=True)
        selected_utilization_file = st.sidebar.selectbox(
            "Select Utilization File", utilization_files
        )
        utilization_df = load_data(f'line_utilization/{selected_utilization_file}')
        
        line_number = st.sidebar.selectbox(
            "Select Line Number", utilization_df["Line"].unique()
        )
        view_type = st.sidebar.radio('Select View', ['Monthly Utilization', 'Overall Utilization'])
        
        if view_type == 'Monthly Utilization':
            with st.spinner("Updating Dashboard..."):
                fig = create_utilization_plot(line_number, utilization_df)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("## Data Table")
            st.dataframe(utilization_df[utilization_df["Line"] == line_number])

        elif view_type == 'Overall Utilization':
            utilization_summary_df = calculate_overall_utilization(utilization_df)
            st.markdown("## Overall Utilization")
            st.dataframe(utilization_summary_df)
        
    elif analysis_type == "Demand Fulfillment":
        demand_files = sorted(os.listdir('demand'), reverse=True)
        selected_demand_file = st.sidebar.selectbox(
            "Select Demand File", demand_files
        )
        demand_df = load_data(f'demand/{selected_demand_file}')
        
        products = st.sidebar.multiselect(
            "Select Product(s)",
            demand_df["Product"].unique(),
            default=demand_df["Product"].unique(),
        )
        view_type = st.sidebar.radio('Select View', ['Monthly Fulfillment', 'Overall Fulfillment'])
        
        if view_type == 'Monthly Fulfillment':
            with st.spinner("Updating Dashboard..."):
                fig = create_demand_plot(products, demand_df)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("## Data Table")
            st.dataframe(demand_df[demand_df["Product"].isin(products)])
        
        elif view_type == 'Overall Fulfillment':
            demand_summary_df = calculate_overall_demand_fulfillment(demand_df)
            st.markdown("## Overall Demand Fulfillment")
            st.dataframe(demand_summary_df)


if __name__ == "__main__":
    main()
