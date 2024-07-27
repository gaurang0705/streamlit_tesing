import pandas as pd
import plotly.express as px
import streamlit as st

# Load data for line utilization
utilization_df = pd.read_csv("line_utilization.csv")

# Load data for demand fulfillment
demand_df = pd.read_csv("demand_fulfilment.csv")


# Function to create utilization plot
def create_utilization_plot(line_number):
    filtered_df = utilization_df[utilization_df["Line"] == line_number]
    fig = px.line(
        filtered_df,
        x="Month_y",
        y="utilization_percentage",
        title=f"Utilization Percentage for {line_number}",
        labels={"Month_y": "Month", "utilization_percentage": "Utilization Percentage"},
        markers=True,
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Utilization Percentage",
        template="plotly_white",
        title_font=dict(size=20, family="Arial, sans-serif"),
        title_x=0.5,
    )
    return fig


# Function to calculate overall utilization
def calculate_overall_utilization():
    utilization_summary = []
    for line in utilization_df['Line'].unique():
        line_df = utilization_df[utilization_df['Line'] == line]
        total_production = line_df['Quantity'].sum()
        total_capacity = (line_df['total_working_days'] * line_df['daily_capacity']).sum()
        overall_utilization = (total_production / total_capacity) * 100
        utilization_summary.append({
            'Line': line,
            'Total Production': total_production,
            'Total Capacity': total_capacity,
            'Overall Utilization Percentage': overall_utilization
        })
    return pd.DataFrame(utilization_summary)


# Function to create demand fulfillment plot
def create_demand_plot(selected_products):
    filtered_df = demand_df[demand_df["Product"].isin(selected_products)]
    fig = px.bar(
        filtered_df,
        x="Month",
        y=["Optimized Plan quantity", "Sale Demand"],
        barmode="group",
        title="Monthly Demand Fulfillment",
        labels={"value": "Quantity", "variable": "Legend"},
        height=400,
    )
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, family="Arial, sans-serif"),
        title_x=0.5,
    )
    return fig


# Function to calculate overall demand fulfillment
def calculate_overall_demand_fulfillment():
    demand_summary = []
    for product in demand_df['Product'].unique():
        product_df = demand_df[demand_df['Product'] == product]
        total_optimized_plan = product_df['Optimized Plan quantity'].sum()
        total_demand = product_df['Sale Demand'].sum()
        overall_fulfillment = (total_optimized_plan / total_demand) * 100
        demand_summary.append({
            'Product': product,
            'Total Optimized Plan': total_optimized_plan,
            'Total Demand': total_demand,
            'Fulfillment Percentage': overall_fulfillment
        })
    return pd.DataFrame(demand_summary)


# Streamlit code
def main():
    st.set_page_config(page_title="Production Line Dashboard", layout="wide")

    st.title("Production Line Dashboard")
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
        line_number = st.sidebar.selectbox(
            "Select Line Number", utilization_df["Line"].unique()
        )
        view_type = st.sidebar.radio('Select View', ['Monthly Utilization', 'Overall Utilization'])
        
        if view_type == 'Monthly Utilization':
            with st.spinner("Updating Dashboard..."):
                fig = create_utilization_plot(line_number)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("## Data Table")
            st.dataframe(utilization_df[utilization_df["Line"] == line_number])

        elif view_type == 'Overall Utilization':
            utilization_summary_df = calculate_overall_utilization()
            st.markdown("## Overall Utilization")
            st.dataframe(utilization_summary_df)
        
    elif analysis_type == "Demand Fulfillment":
        products = st.sidebar.multiselect(
            "Select Product(s)",
            demand_df["Product"].unique(),
            default=demand_df["Product"].unique(),
        )
        view_type = st.sidebar.radio('Select View', ['Monthly Fulfillment', 'Overall Fulfillment'])
        
        if view_type == 'Monthly Fulfillment':
            with st.spinner("Updating Dashboard..."):
                fig = create_demand_plot(products)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("## Data Table")
            st.dataframe(demand_df[demand_df["Product"].isin(products)])
        
        elif view_type == 'Overall Fulfillment':
            demand_summary_df = calculate_overall_demand_fulfillment()
            st.markdown("## Overall Demand Fulfillment")
            st.dataframe(demand_summary_df)


if __name__ == "__main__":
    main()
