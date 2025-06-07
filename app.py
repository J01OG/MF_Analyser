import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load and preprocess data
@st.cache_data

def load_data(source="local"):
    if source == "google":
        url = st.secrets.get("google_sheet_url", "")
        if not url:
            st.error("Google Sheet URL not configured in Streamlit secrets.")
            return pd.DataFrame()
        xls = pd.ExcelFile(url)
    else:
        xls = pd.ExcelFile("Motilal Oswal Large and Midcap Fund.xlsx")

    sheet_names = xls.sheet_names
    all_data = []
    for sheet in sheet_names:
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

# Sidebar: Choose Data Source
st.sidebar.markdown("### Data Source")
data_source = st.sidebar.radio("Select data source:", ["Local Excel File", "Google Sheet"])
data = load_data("google" if data_source == "Google Sheet" else "local")

# Title
st.title("Mutual Fund Holdings Annual Analytics Dashboard")

# Sidebar filters
months = sorted(data['Month'].unique())
st.sidebar.header("Filters")
selected_months = st.sidebar.multiselect("Select Months", months, default=months)

stocks = sorted(data['Name of Instrument'].dropna().unique())
selected_stocks = st.sidebar.multiselect("Select Stocks to Analyze", stocks)

# Filtered data
filtered = data[data['Month'].isin(selected_months)]

# Pivot entire dataset for % to Net Assets tracking
pivot_full = filtered.pivot_table(index='Month', columns='Name of Instrument', values='% to Net Assets', aggfunc='sum')

st.subheader("📈 Change in Holding Percentages (Graphical)")
if len(selected_months) >= 2:
    month_start, month_end = selected_months[0], selected_months[-1]
    start_holdings = pivot_full.loc[month_start].fillna(0)
    end_holdings = pivot_full.loc[month_end].fillna(0)
    change_df = pd.DataFrame({
        'Stock': start_holdings.index,
        f'{month_start}': start_holdings.values,
        f'{month_end}': end_holdings.values,
        'Change in %': end_holdings.values - start_holdings.values
    })
    change_df = change_df[change_df[f'{month_start}'] != 0]  # Stocks that were present at start
    change_df_sorted = change_df.sort_values('Change in %', ascending=False)

    # Graph comparing Start and End holdings
    st.subheader("Start vs End Month Holding Comparison")
    melted_df = pd.melt(change_df_sorted, id_vars='Stock', value_vars=[f'{month_start}', f'{month_end}'],
                        var_name='Month', value_name='Holding %')
    fig_bar = px.bar(melted_df, x='Stock', y='Holding %', color='Month', barmode='group',
                     title=f"Holdings Comparison: {month_start} vs {month_end}")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Chart for Change in %
    fig_change = px.bar(change_df_sorted, x='Stock', y='Change in %',
                        title="Change in Holding % Over Selected Period")
    st.plotly_chart(fig_change, use_container_width=True)

st.subheader("📊 Full Stock Holding Trend Across Months")
if selected_stocks:
    pivot_selected = pivot_full[selected_stocks]
    fig4 = px.line(pivot_selected, markers=True, title="Monthly Holding % for Selected Stocks")
    st.plotly_chart(fig4, use_container_width=True)

# Show raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered)
