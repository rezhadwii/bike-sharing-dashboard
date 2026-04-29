import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style="whitegrid")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

data_path = Path(__file__).parent / "main_data.csv"
hour_bike = pd.read_csv(data_path)
hour_bike["dteday"] = pd.to_datetime(hour_bike["dteday"])

st.sidebar.header("Filter Data")

min_date = hour_bike["dteday"].min()
max_date = hour_bike["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = hour_bike[
    (hour_bike["dteday"] >= pd.to_datetime(start_date)) &
    (hour_bike["dteday"] <= pd.to_datetime(end_date))
]

st.title("Dashboard Penyewaan Sepeda")
st.write(
    "Dashboard ini menampilkan pola penyewaan sepeda berdasarkan bulan, musim, cuaca, jam, dan level demand."
)

total_rentals = main_df["cnt"].sum()
avg_rentals = round(main_df["cnt"].mean(), 2)
total_registered = main_df["registered"].sum()
total_casual = main_df["casual"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")

with col2:
    st.metric("Rata-rata Penyewaan", value=avg_rentals)

with col3:
    st.metric("Pengguna Registered", value=f"{total_registered:,}")

with col4:
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

st.subheader("Total Penyewaan Sepeda per Bulan")

monthly_rentals = main_df.resample(rule="ME", on="dteday").agg({
    "cnt": "sum"
}).reset_index()

monthly_rentals["month_year"] = monthly_rentals["dteday"].dt.strftime("%b %Y")

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_rentals,
    x="month_year",
    y="cnt",
    marker="o",
    ax=ax
)

ax.set_title("Total Penyewaan Sepeda per Bulan Tahun 2011-2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.subheader("Rata-rata Penyewaan berdasarkan Musim dan Kondisi Cuaca")

season_rentals = main_df.groupby("season", as_index=False).agg({
    "cnt": "mean"
})

weather_rentals = main_df.groupby("weathersit", as_index=False).agg({
    "cnt": "mean"
})

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

sns.barplot(
    data=season_rentals.sort_values(by="cnt", ascending=False),
    x="season",
    y="cnt",
    ax=ax[0]
)
ax[0].set_title("Rata-rata Penyewaan berdasarkan Musim")
ax[0].set_xlabel("Musim")
ax[0].set_ylabel("Rata-rata Penyewaan")

sns.barplot(
    data=weather_rentals.sort_values(by="cnt", ascending=False),
    x="weathersit",
    y="cnt",
    ax=ax[1]
)
ax[1].set_title("Rata-rata Penyewaan berdasarkan Kondisi Cuaca")
ax[1].set_xlabel("Kondisi Cuaca")
ax[1].set_ylabel("Rata-rata Penyewaan")
ax[1].tick_params(axis="x", rotation=20)

plt.tight_layout()
st.pyplot(fig)

st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Jam")

hourly_rentals = main_df.groupby("hr", as_index=False).agg({
    "cnt": "mean"
})

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_rentals,
    x="hr",
    y="cnt",
    marker="o",
    ax=ax
)

ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(0, 24))
st.pyplot(fig)

st.subheader("Level Demand Penyewaan Sepeda berdasarkan Jam")

hourly_demand = main_df.groupby("hr", as_index=False).agg({
    "cnt": "mean"
})

def demand_level(avg_rentals):
    if avg_rentals < 150:
        return "Low Demand"
    elif avg_rentals < 300:
        return "Medium Demand"
    else:
        return "High Demand"

hourly_demand["demand_level"] = hourly_demand["cnt"].apply(demand_level)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=hourly_demand,
    x="hr",
    y="cnt",
    hue="demand_level",
    ax=ax
)

ax.set_title("Level Demand Penyewaan Sepeda berdasarkan Jam")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(0, 24))
ax.legend(title="Level Demand")
st.pyplot(fig)

st.subheader("Ringkasan Insight")

st.write(
    """
    - Penyewaan sepeda pada tahun 2012 cenderung lebih tinggi dibandingkan tahun 2011.
    - Rata-rata penyewaan tertinggi terjadi pada musim Fall dan saat cuaca Clear.
    - Penyewaan sepeda ramai pada pagi hari sekitar jam 08.00 dan sore hari sekitar jam 17.00.
    - Jam dengan kategori High Demand dapat menjadi prioritas untuk menjaga ketersediaan sepeda.
    """
)

st.caption("Bike Sharing Dashboard")

