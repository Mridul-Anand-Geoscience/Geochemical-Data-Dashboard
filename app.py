import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set up the page layout
st.set_page_config(page_title="Geochemical Dashboard", layout="wide")
st.title("Interactive Geochemical Data Explorer")
st.markdown("Analyze trace element distributions in pyrite samples.")

# 2. Load the data 
# (The @st.cache_data decorator keeps the app fast by not reloading the CSV every time you click something)
@st.cache_data
def load_data():
    return pd.read_csv("pyrite_data.csv")

df = load_data()

# 3. Create a sidebar for user controls
st.sidebar.header("Plot Settings")

# Let the user choose what elements to plot against each other
numeric_columns = df.select_dtypes(['float64', 'int64']).columns.tolist()

x_axis = st.sidebar.selectbox("Select X-Axis Variable", numeric_columns, index=numeric_columns.index('Fe_percent'))
y_axis = st.sidebar.selectbox("Select Y-Axis Variable", numeric_columns, index=numeric_columns.index('Co_ppm'))
color_by = st.sidebar.selectbox("Color By", df.columns.tolist(), index=df.columns.tolist().index('Formation_Type'))

# 4. Create the interactive scatter plot
st.subheader(f"Scatter Plot: {y_axis} vs {x_axis}")

# Plotly makes it interactive automatically
fig = px.scatter(
    df, 
    x=x_axis, 
    y=y_axis, 
    color=color_by,
    hover_data=["Sample_ID", "Depth_meters"], # Shows sample ID when hovering over a dot
    title=f"Correlation between {x_axis} and {y_axis}",
    template="plotly_white"
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# 5. Show the raw data table below the chart
st.divider()
st.subheader("Raw Geochemical Data")
st.dataframe(df, use_container_width=True)