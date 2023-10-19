import pandas as pd
import seaborn as sns
import plotly.express as px
import streamlit as st
from babel.numbers import format_currency
sns.set_style('dark')
st.set_page_config(layout="wide")

def create_daily_order_df(df):
    daily_order_df=df.resample(rule='D',on='order_date').agg({
    'order_id':'nunique',
    'price':'sum',
})
    daily_order_df=daily_order_df.reset_index()
    daily_order_df.rename(columns={'order_id':'order_count', 'price':'revenue'},inplace=True)
    return daily_order_df

def create_sum_order_items_df(df):
    sum_order_items_df=df.groupby(by='product_category_name').order_id.nunique().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_mean_review_score_df(df):
    mean_review_score_df=df.groupby(by='product_category_name').review_score.mean().sort_values(ascending=False).reset_index()
    return mean_review_score_df

def create_sum_payment_type_df(df):
    sum_payment_type_df=df.groupby(by='payment_type').order_id.nunique().sort_values(ascending=False).reset_index()
    return sum_payment_type_df

final_df=pd.read_csv('./dashboard/final_dataset.csv')

final_df.sort_values(by='order_date',inplace=True)
final_df.reset_index(inplace=True)

for column in ['order_date']:
    final_df[column] = pd.to_datetime(final_df[column]) 

min_date=final_df['order_date'].min()
max_date=final_df['order_date'].max()

st.markdown("<h1 style='text-align: center;'>🚀 Dashboard Data E-Commerce 🚀</h1>", unsafe_allow_html=True)
start_date,end_date=st.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date,max_date]
)

main_df=final_df[(final_df['order_date']>=str(start_date))&(final_df['order_date']<=str(end_date))]

daily_order_df=create_daily_order_df(main_df)
sum_order_items_df=create_sum_order_items_df(main_df)
mean_review_score_df=create_mean_review_score_df(main_df)
sum_payment_type_df=create_sum_payment_type_df(main_df)

st.subheader('Daily Order')

col1,col2=st.columns(2)

with col1:
    total_orders=daily_order_df.order_count.sum()
    st.metric('Total Order = ',total_orders)
with col2:
    total_revenue=format_currency(daily_order_df.revenue.sum(),'$',locale='en_US')
    st.metric('Total Revenue = ',total_revenue)

col1,col2=st.columns(2)
with col1:
    fig = px.line(daily_order_df, x='order_date', y='order_count', markers=True, line_shape='linear')
    fig.update_traces(marker=dict(size=5, color='#90CAF9', symbol='circle'), line=dict(width=2))

    fig.update_xaxes(tickfont=dict(size=15))
    fig.update_yaxes(tickfont=dict(size=20))

    fig.update_layout(
        title='Grafik Order Harian',
        xaxis_title='Tanggal Pesanan',
        yaxis_title='Jumlah Pesanan',
        autosize=True,
    )
    st.plotly_chart(fig)
with col2:
    fig = px.pie(
        sum_payment_type_df,
        values='order_id',
        names='payment_type',
        title='Payment Types Distribution'
    )

    st.plotly_chart(fig)


st.subheader('Highest and Lowest Sales')
col1, col2 = st.columns(2)

with col1:
    fig_top = px.bar(sum_order_items_df.head(5), x='order_id', y='product_category_name', color='product_category_name', title='Top 5 Product Category Highest Sales')
    st.plotly_chart(fig_top)

with col2:
    fig_bottom = px.bar(sum_order_items_df.sort_values(by='order_id', ascending=True).head(5), x='order_id', y='product_category_name', color='product_category_name', title='Bottom 5 Product Category Lowest Sales')
    st.plotly_chart(fig_bottom)

st.subheader('Highest and Lowest Review Score')
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(
        mean_review_score_df.head(5),
        x='review_score',
        y='product_category_name',
        color='product_category_name',
        title='Top 5 Product Category by Review Score'
    )
    st.plotly_chart(fig)
with col2:
    fig_bottom = px.bar(
        mean_review_score_df.sort_values(by='review_score', ascending=True).head(5),
        x='review_score',
        y='product_category_name',
        color='product_category_name',
        title='Bottom 5 Product Category by Review Score'
    )
    st.plotly_chart(fig_bottom)

