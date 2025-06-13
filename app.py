import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.title("📊 Mutual Fund Holding Trends Dashboard")

# Session state to hold uploaded files as {filename: file_bytes}
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

st.sidebar.header("Upload Excel Files")
uploaded = st.sidebar.file_uploader(
    "Upload Excel file(s)", 
    type=["xlsx", "xls"], 
    accept_multiple_files=True
)

# Add new uploaded files to session_state
for file in uploaded:
    if file.name not in st.session_state.uploaded_files:
        st.session_state.uploaded_files[file.name] = file.getvalue()

# If no files uploaded yet
if not st.session_state.uploaded_files:
    st.warning("Please upload one or more Excel files to proceed.")
    st.stop()

# Select which uploaded file to analyze
selected_file = st.sidebar.selectbox(
    "Select File to Analyze",
    options=list(st.session_state.uploaded_files.keys())
)

@st.cache_data
def load_data_from_bytes(file_bytes):
    try:
        xls = pd.ExcelFile(BytesIO(file_bytes))
        all_data = []
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            df.dropna(how='all', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)
            df['Month'] = sheet
            all_data.append(df)
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined[combined['Sr. No.'].notna()]  # Filter valid rows
        combined['% to Net Assets'] = pd.to_numeric(combined['% to Net Assets'], errors='coerce')
        combined['Quantity'] = pd.to_numeric(combined['Quantity'], errors='coerce')
        combined['Market value (Rs. In lakhs)'] = pd.to_numeric(combined['Market value (Rs. In lakhs)'], errors='coerce')
        return combined
    except Exception as e:
        st.error(f"Failed to load or parse Excel file: {e}")
        return pd.DataFrame()

data = load_data_from_bytes(st.session_state.uploaded_files[selected_file])

if data.empty:
    st.warning("No valid data found in the selected file.")
    st.stop()

# Sort months properly (assuming format 'Jan 2024', etc)
def month_sort_key(m):
    try:
        return pd.to_datetime(m, format="%b %Y")
    except:
        return pd.Timestamp.min

months_sorted = sorted(data['Month'].unique(), key=month_sort_key)
data['Month'] = pd.Categorical(data['Month'], categories=months_sorted, ordered=True)

# Sidebar filters
st.sidebar.header("Filters")
selected_months = st.sidebar.multiselect("Select Months", months_sorted, default=months_sorted)

stocks = sorted(data['Name of Instrument'].dropna().unique())

select_all_stocks = st.sidebar.checkbox("Select All Stocks")

if select_all_stocks:
    selected_stocks = stocks
else:
    avg_assets = data.groupby('Name of Instrument')['% to Net Assets'].mean().sort_values(ascending=False)
    default_stocks = avg_assets.head(5).index.tolist() if not avg_assets.empty else []
    selected_stocks = st.sidebar.multiselect("Select Stocks to Analyze", stocks, default=default_stocks)

# Filtered data
filtered = data[data['Month'].isin(selected_months)]

# Plot each metric separately
metrics = ["% to Net Assets", "Quantity", "Market value (Rs. In lakhs)"]
chart_type = st.sidebar.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Area Chart"])

for metric in metrics:
    st.subheader(f"📈 {metric} Over Time for Selected Stocks")
    pivot = filtered.pivot_table(index='Month', columns='Name of Instrument', values=metric, aggfunc='sum')

    if selected_stocks:
        pivot_selected = pivot[selected_stocks]
        pivot_melted = pivot_selected.reset_index().melt(id_vars='Month', var_name='Stock', value_name=metric)
        pivot_melted['Month'] = pd.Categorical(pivot_melted['Month'], categories=months_sorted, ordered=True)
        pivot_melted = pivot_melted.sort_values("Month")

        if chart_type == "Line Chart":
            fig = px.line(
                pivot_melted,
                x="Month",
                y=metric,
                color="Stock",
                markers=True,
                title=f"{metric} Over Time"
            )
        elif chart_type == "Bar Chart":
            fig = px.bar(
                pivot_melted,
                x='Month',
                y=metric,
                color='Stock',
                barmode='group',
                title=f"{metric} Over Time - Bar Chart"
            )
        elif chart_type == "Area Chart":
            fig = px.area(
                pivot_melted,
                x="Month",
                y=metric,
                color="Stock",
                title=f"{metric} Over Time - Area Chart"
            )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title=metric,
            legend_title="Stock",
            template="plotly_white",
            hovermode="x unified",
            height=600,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one stock to view its trend.")

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered)
