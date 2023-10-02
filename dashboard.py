import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
sns.set_style('dark')

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

final_df=pd.read_csv('./Dataset/E-Commerce_Dataset/final_dataset.csv')

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
    total_revenue=format_currency(daily_order_df.revenue.sum(),'$')
    st.metric('Total Revenue = ',total_revenue)

fig, ax=plt.subplots(figsize=(16,8))
ax.plot(
    daily_order_df['order_date'],
    daily_order_df['order_count'],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y',labelsize=20)
ax.tick_params(axis='x',labelsize=15)

st.pyplot(fig)

st.subheader('Highest and Lowest Sales')
fig, ax =plt.subplots(nrows=1,ncols=2,figsize=(20,5))
colors = sns.color_palette("viridis", len(sum_order_items_df.head(5)))

sns.barplot(x='order_id',y='product_category_name',data=sum_order_items_df.head(5),ax=ax[0], palette=colors)
ax[0].set_title('Top 5 Product Category Highest Sales',fontsize=14)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x='order_id',y='product_category_name',data=sum_order_items_df.sort_values(by='order_id', ascending=True).head(5),ax=ax[1], palette=colors)
ax[1].set_title('Bottom 5 Product Category Lowest Sales',fontsize=14)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='y', labelsize=12)
plt.subplots_adjust(wspace=0.3)  
st.pyplot(fig)

st.subheader('Highest and Lowest Review Score')
fig, ax =plt.subplots(nrows=1,ncols=2,figsize=(20,5))
colors = sns.color_palette("viridis", len(mean_review_score_df.head(5)))

sns.barplot(x='review_score',y='product_category_name',data=mean_review_score_df.head(5),ax=ax[0], palette=colors)
ax[0].set_title('Top 5 Product Category by Review Score',fontsize=14)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x='review_score',y='product_category_name',data=mean_review_score_df.sort_values(by='review_score', ascending=True).head(5),ax=ax[1], palette=colors)
ax[1].set_title('Bottom 5 Product Category by Review Score',fontsize=14)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].tick_params(axis='y', labelsize=12)
plt.subplots_adjust(wspace=0.7)
st.pyplot(fig)

st.subheader('Distribution of Payment Methods')
colors = sns.color_palette("Set3", 4)
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(
    x=sum_payment_type_df['order_id'],
    autopct='%.0f%%',
    pctdistance=0.85,
    colors=colors,
    explode=(0.1, 0, 0, 0),
    shadow=True,
    startangle=90
)
ax.legend(sum_payment_type_df['payment_type'], loc='upper right', bbox_to_anchor=(1.2, 1))
st.pyplot(fig)
