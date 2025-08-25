import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import streamlit as st


# Project budget plotting
def plot_project_budget(df):
    # Aggregate budget by Project and Activity
    agg_df = df.groupby(["Project", "Activity"], as_index=False)["Amount"].sum()

    st.write("### Budget by Project and Activity")
    st.dataframe(agg_df)

    # Base bar chart
    bars = alt.Chart(agg_df).mark_bar().encode(
        x=alt.X('Activity:N', title='Activity', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Amount:Q', title='Budget'),
        color='Project:N',
        tooltip=['Project', 'Activity', 'Amount']
    )

    # Add labels centered inside the bars
    text = bars.mark_text(
        align='center',
        baseline='middle',
        dy=0,  # centered vertically
        color='white',  # labels visible inside bars
        fontWeight='bold'
    ).encode(
        text='Amount:Q'
    )

    # Combine bars and labels
    chart = (bars + text).properties(width=800, height=400)
    
    st.altair_chart(chart)
