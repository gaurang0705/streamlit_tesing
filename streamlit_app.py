import pandas as pd
import plotly.express as px
import streamlit as st

# Sample data
df = pd.read_csv("line_utilization.csv")


# Function to create Plotly figure
def create_plot(line_number):
    filtered_df = df[df["Line"] == line_number]
    fig = px.line(
        filtered_df,
        x="Month_y",
        y="utilization_percentage",
        title=f"Utilization Percentage for {line_number}",
        labels={"Month_y": "Month", "utilization_percentage": "Utilization Percentage"},
    )
    return fig


# Streamlit code
def main():
    st.title("Production Line Utilization Dashboard")

    line_number = st.selectbox("Select Line Number", df["Line"].unique())

    fig = create_plot(line_number)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
