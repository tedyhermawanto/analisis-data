import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

day_df = pd.read_csv('./Data/day.csv')
hour_df = pd.read_csv('./Data/hour.csv')

# Preprocessing
day_df.dropna(inplace=True)
hour_df.dropna(inplace=True)
day_df['date'] = pd.to_datetime(day_df['dteday'])
hour_df['date'] = pd.to_datetime(hour_df['dteday'])

day_df['year'] = day_df['date'].dt.year
day_df['month'] = day_df['date'].dt.month

# Sidebar for start and end date selection
st.sidebar.title("Date Range Selection")
min_date = day_df['date'].min()
max_date = day_df['date'].max()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

filtered_day_df = day_df[(day_df['date'] >= pd.to_datetime(start_date)) & (day_df['date'] <= pd.to_datetime(end_date))]

# Dashboard Title
st.title(f"Bike Sharing Dashboard ({start_date} - {end_date})")

# Correlation matrix
numerical_columns = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
correlation_matrix = filtered_day_df[numerical_columns].corr()
st.subheader('Correlation Matrix')
st.write(correlation_matrix)

st.subheader('Trend of Bike Rentals Over Time')
fig, ax = plt.subplots()
sns.lineplot(x='date', y='cnt', data=filtered_day_df, ax=ax)
ax.set_title(f'Daily Bike Rentals')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization 1: Temperature vs Bike Rentals
st.subheader('Temperature vs Bike Rentals')
fig, ax = plt.subplots()
sns.scatterplot(x='temp', y='cnt', data=filtered_day_df, ax=ax)
ax.set_title('Temperature vs Bike Rentals')
ax.set_xlabel('Temperature (Normalized)')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Visualization 2: Humidity vs Bike Rentals
st.subheader('Humidity vs Bike Rentals')
fig, ax = plt.subplots()
sns.scatterplot(x='hum', y='cnt', data=filtered_day_df, ax=ax)
ax.set_title('Humidity vs Bike Rentals')
ax.set_xlabel('Humidity (Normalized)')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Visualization 3: Windspeed vs Bike Rentals
st.subheader('Windspeed vs Bike Rentals')
fig, ax = plt.subplots()
sns.scatterplot(x='windspeed', y='cnt', data=filtered_day_df, ax=ax)
ax.set_title('Windspeed vs Bike Rentals')
ax.set_xlabel('Windspeed (Normalized)')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Boxplot: Effect of weather conditions on bike rentals
st.subheader('Effect of Weather Conditions on Bike Rentals')
fig, ax = plt.subplots()
palette = {'1': 'steelblue', '2': 'skyblue', '3': 'lightblue'}
sns.boxplot(x='weathersit', y='cnt', data=filtered_day_df, ax=ax, palette=palette)
ax.set_title('Bike Rentals under Different Weather Conditions')
ax.set_xlabel('Weather Condition')
ax.legend(labels=['Clear', 'Cloudy', 'Rain/Snow'], title='Weather Condition')
ax.set_ylabel('Bike Rentals')
st.pyplot(fig)

# Visualization: Average Bike Rentals on Weekdays vs Holidays
st.subheader('Average Bike Rentals on Weekdays vs Holidays')
fig, ax = plt.subplots()
workingday_mean = filtered_day_df.groupby('workingday')['cnt'].mean()
ax.bar(workingday_mean.index, workingday_mean.values)
ax.set_xlabel('0 = Hari Libur, 1 = Hari Kerja')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)

# Visualization: Average Bike Rentals by Season
st.subheader('Average Bike Rentals by Season')
fig, ax = plt.subplots()
season_mean = filtered_day_df.groupby('season')['cnt'].mean()
ax.bar(season_mean.index, season_mean.values)
ax.set_xlabel('Musim (1 = Winter, 2 = Spring, 3 = Summer, 4 = Fall)')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
st.pyplot(fig)
