import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard - coffee sales",
    page_icon="🙂",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

df = pd.ExcelFile("https://github.com/Anomali99/Visualisasi-Data/raw/main/Raw-Data-coffee-sales2.xlsx")
orders = pd.read_excel(df, 'orders')
customers = pd.read_excel(df, 'customers')
products = pd.read_excel(df, 'products')

st.title("Dashboard coffee sales")

with st.sidebar:
    st.header("Nur Fatiq (09040622071)")

    country = list(customers['Country'].unique())[::-1]
    selected_country = st.multiselect('Select country', (country + ["All"]), default=["All"])
    if "All" not in selected_country:
        customers = customers[customers['Country'].isin(selected_country)]
        orders = orders[orders['Customer ID'].isin(customers['Customer ID'])]
        products = products[products['Product ID'].isin(orders['Product ID'])]

    city = list(customers['City'].unique())[::-1]
    selected_city = st.multiselect('Select city', city + ["All"], default=["All"])
    if "All" not in selected_city:
        customers = customers[customers['City'].isin(selected_city)]
        orders = orders[orders['Customer ID'].isin(customers['Customer ID'])]
        products = products[products['Product ID'].isin(orders['Product ID'])]

    address = list(customers['Address Line 1'].unique())[::-1]
    selected_address = st.multiselect('Select address', address + ["All"], default=["All"])
    if "All" not in selected_address:
        customers = customers[customers['Address Line 1'].isin(selected_address)]
        orders = orders[orders['Customer ID'].isin(customers['Customer ID'])]
        products = products[products['Product ID'].isin(orders['Product ID'])]

    dates = list(pd.to_datetime(orders['Order Date']).dt.year.unique())[::-1]
    selected_dates = st.multiselect('Select year', dates + ["All"], default=["All"])
    if "All" not in selected_dates:
        orders = orders[pd.to_datetime(orders['Order Date']).dt.year.isin(selected_dates)]
        products = products[products['Product ID'].isin(orders['Product ID'])]

    dates = list(pd.to_datetime(orders['Order Date']).dt.month.unique())[::-1]
    dates.sort()
    selected_dates = st.multiselect('Select month', dates + ["All"], default=["All"])
    if "All" not in selected_dates:
        orders = orders[pd.to_datetime(orders['Order Date']).dt.month.isin(selected_dates)]
        products = products[products['Product ID'].isin(orders['Product ID'])]


col = st.columns((6, 2), gap='medium')

with col[0]:

    st.markdown("***")
    st.write("""#### Jumlah produk terjual di setiap negara """)
    order_counts = orders.groupby('Country').size().reset_index(name='Count')
    st.bar_chart(order_counts, x = 'Country', y = 'Count', use_container_width=True)

    st.markdown("***")
    st.write("""#### Persebaran produk terjual """)
    len_count = max(order_counts['Count'])
    choropleth = px.choropleth(order_counts, 
                                locations=order_counts['Country'], 
                                locationmode='country names', 
                                color='Count',
                                range_color=(0, len_count/2,len_count),
                                labels={'Count':'Order Count'}
                            )
    choropleth.update_layout(template='plotly_dark')
    st.plotly_chart(choropleth, use_container_width=True)

    st.markdown("***")
    st.write("""#### Jumlah produk dibeli """)
    cs_type = orders.groupby('Product ID').size().reset_index(name='Count')
    cs_product = pd.merge(cs_type, products, on='Product ID')
    chart = (
        alt.Chart(cs_product)
        .mark_bar()
        .encode(
            x=alt.X("Count", type="quantitative", title="Count"),
            y=alt.Y("Coffee Type", type="nominal", title="Coffee Type",sort='-x'),
            color=alt.Color("Roast Type", type="nominal", title="Roast Type"),
            order=alt.Order("Coffee Type", sort="descending"),
        )
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("***")
    st.write("""#### Jumlah order setiap tahun """)
    new_order = orders[:]
    new_order['Order Date 2'] = list(pd.to_datetime(new_order['Order Date']).dt.year)
    df2 = new_order.groupby(['Order Date 2','Coffee Type']).size().reset_index(name='Count')
    fig = go.Figure(
        data=[go.Bar(
            name=coffee_type, 
            x=df2[df2['Coffee Type'] == coffee_type]['Order Date 2'], 
            y=df2[df2['Coffee Type'] == coffee_type]['Count']
            ) for coffee_type in df2['Coffee Type'].unique()]
        )
    fig.update_layout(barmode='group', xaxis_title='Tahun', yaxis_title='Jumlah Pesanan')
    st.plotly_chart(fig)

    st.markdown("***")
    st.write("""#### Jumlah order setiap negara """)
    newOrder = orders.groupby(['Country','Coffee Type']).size().reset_index(name='Count')
    fig = px.treemap(newOrder, path=['Country', 'Coffee Type'], values='Count')
    st.plotly_chart(fig)

with col[1]:
    st.write("""#### 10 teratas pelanggan """)
    cs_order = orders.groupby('Customer ID').size().reset_index(name='Count')
    cs_name_order = pd.merge(cs_order, customers, on='Customer ID')
    cs_name_order_sorted = cs_name_order.sort_values('Count', ascending=False)

    chart = (
        alt.Chart(cs_name_order_sorted[:10])
        .mark_bar()
        .encode(
            x=alt.X("Count", type="quantitative", title="Count"),
            y=alt.Y("Customer Name", type="nominal", title="Customer Name", sort='-x'),
            order=alt.Order("Count", sort="descending"),
        )
    )
    st.altair_chart(chart, use_container_width=True)
    st.write(f"""###### dari {len(cs_name_order_sorted)} pelanggan""")

    st.markdown("***")
    st.write("""#### Jumlah pelanggan dengan Loyalty Card """)
    loyalty_counts = customers.groupby('Loyalty Card').size().reset_index(name='Count')
    fig = px.pie(loyalty_counts, values=loyalty_counts['Count'], names=loyalty_counts['Loyalty Card'])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("***")
    st.write("""#### Jumlah profit di setiap negara """)
    price_counts = orders.groupby('Country')['Unit Price'].sum().reset_index()
    fig = px.pie(price_counts, values=price_counts['Unit Price'], names=price_counts['Country'], hole=.4)
    st.plotly_chart(fig, use_container_width=True)
        