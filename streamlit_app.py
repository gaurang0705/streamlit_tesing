import pandas as pd
import plotly.express as px
import streamlit as st

# Sample data for line utilization


utilization_df = pd.read_csv("line_utilization.csv")

# Sample data for demand fulfillment
d
demand_df = pd.read_csv("demand_filfilment.csv")


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


# Function to create demand fulfillment plot
def create_demand_plot():
    fig = px.bar(
        demand_df,
        x="Product",
        y=["Optimized Plan quantity", "Sale Demand"],
        barmode="group",
        title="Demand Fulfillment",
        labels={"value": "Quantity", "variable": "Legend"},
        height=400,
    )
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, family="Arial, sans-serif"),
        title_x=0.5,
    )
    return fig


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
        with st.spinner("Updating Dashboard..."):
            fig = create_utilization_plot(line_number)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Data Table")
        st.dataframe(utilization_df[utilization_df["Line"] == line_number])

    elif analysis_type == "Demand Fulfillment":
        with st.spinner("Updating Dashboard..."):
            fig = create_demand_plot()
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Data Table")
        st.dataframe(demand_df)


if __name__ == "__main__":
    main()
