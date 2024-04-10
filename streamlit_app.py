import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import math

st.title("Data App Assignment")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")

option = st.selectbox(
    'Category',
    df["Category"].unique())

st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")

options = st.multiselect(
    'Pick a subcategory',
    df[df['Category'] == option]['Sub_Category'].unique()
    )

st.write(option)
st.dataframe(df[df['Category'] == option])


st.write("### (3) show a line chart of sales for the selected items in (2)")

st.write(type(options))
st.dataframe(df[df['Sub_Category'].isin(options)])

df2 = df[df['Sub_Category'].isin(options)]

st.dataframe(df2.filter(items=['Sales']))

#filtered_sales_by_month = st.dataframe(df[df['Sub_Category'].isin(options)]).filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
#st.line_chart(filtered_sales_by_month, y="Sales")


#I tried to follow the same logic as the line graph example that was provided
#sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()



st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
