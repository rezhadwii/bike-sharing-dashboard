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

st.title("Bike Sharing Dashboard")

st.write(
    """
    Dashboard ini menyajikan hasil analisis penyewaan sepeda berdasarkan tren bulanan,
    musim, kondisi cuaca, jam, dan tipe hari. Analisis ini bertujuan untuk membantu
    memahami pola permintaan pengguna serta menentukan waktu prioritas penyediaan sepeda.
    """
)

st.divider()

st.subheader("Ringkasan Data")

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

st.divider()


st.subheader("Pertanyaan 1")
st.markdown(
    "**Bagaimana perbandingan tren total penyewaan sepeda setiap bulan antara tahun 2011 dan 2012, serta pada bulan apa terjadi penyewaan tertinggi dan terendah?**"
)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

monthly_yearly_rentals = main_df.groupby(["yr", "mnth"], as_index=False).agg({
    "cnt": "sum"
})

monthly_yearly_rentals["mnth"] = pd.Categorical(
    monthly_yearly_rentals["mnth"],
    categories=month_order,
    ordered=True
)

monthly_yearly_rentals = monthly_yearly_rentals.sort_values(["yr", "mnth"])

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(
    data=monthly_yearly_rentals,
    x="mnth",
    y="cnt",
    hue="yr",
    marker="o",
    palette=["tab:blue", "tab:orange"],
    ax=ax
)

ax.set_title("Perbandingan Total Penyewaan Sepeda per Bulan antara Tahun 2011 dan 2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.tick_params(axis="x", rotation=45)
ax.legend(title="Tahun")
st.pyplot(fig)

st.info(
    "Total penyewaan sepeda pada tahun 2012 lebih tinggi dibandingkan tahun 2011 di setiap bulan. "
    "Puncak penyewaan terjadi pada September 2012, sedangkan penyewaan terendah terjadi pada Januari 2011."
)

st.divider()


st.subheader("Pertanyaan 2")
st.markdown(
    "**Bagaimana perbedaan rata-rata penyewaan sepeda pada berbagai musim dan kondisi cuaca antara tahun 2011 dan 2012?**"
)

season_order = ["Spring", "Summer", "Fall", "Winter"]
weather_order = ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]

season_year_rentals = main_df.groupby(["yr", "season"], as_index=False).agg({
    "cnt": "mean"
})

weather_year_rentals = main_df.groupby(["yr", "weathersit"], as_index=False).agg({
    "cnt": "mean"
})

season_year_rentals["season"] = pd.Categorical(
    season_year_rentals["season"],
    categories=season_order,
    ordered=True
)

weather_year_rentals["weathersit"] = pd.Categorical(
    weather_year_rentals["weathersit"],
    categories=weather_order,
    ordered=True
)

season_year_rentals = season_year_rentals.sort_values(["season", "yr"])
weather_year_rentals = weather_year_rentals.sort_values(["weathersit", "yr"])

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

sns.barplot(
    data=season_year_rentals,
    x="season",
    y="cnt",
    hue="yr",
    palette=["tab:blue", "tab:orange"],
    ax=ax[0]
)

ax[0].set_title("Rata-rata Penyewaan berdasarkan Musim")
ax[0].set_xlabel("Musim")
ax[0].set_ylabel("Rata-rata Penyewaan")
ax[0].legend(title="Tahun")

sns.barplot(
    data=weather_year_rentals,
    x="weathersit",
    y="cnt",
    hue="yr",
    palette=["tab:blue", "tab:orange"],
    ax=ax[1]
)

ax[1].set_title("Rata-rata Penyewaan berdasarkan Kondisi Cuaca")
ax[1].set_xlabel("Kondisi Cuaca")
ax[1].set_ylabel("Rata-rata Penyewaan")
ax[1].legend(title="Tahun")

plt.tight_layout()
st.pyplot(fig)

st.info(
    "Rata-rata penyewaan sepeda pada tahun 2012 cenderung lebih tinggi dibandingkan tahun 2011. "
    "Penyewaan tertinggi terjadi pada musim Fall dan saat cuaca Clear, sedangkan terendah terjadi pada musim Spring dan saat Heavy Rain/Snow."
)

st.divider()


st.subheader("Pertanyaan 3")
st.markdown(
    "**Bagaimana perbedaan pola rata-rata penyewaan sepeda per jam antara Working Day dan Non-Working Day selama tahun 2011–2012?**"
)

hourly_workingday = main_df.groupby(["hr", "workingday"], as_index=False).agg({
    "cnt": "mean"
})

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=hourly_workingday,
    x="hr",
    y="cnt",
    hue="workingday",
    marker="o",
    ax=ax
)

ax.set_title("Rata-rata Penyewaan Sepeda per Jam berdasarkan Tipe Hari")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(0, 24))
ax.legend(title="Tipe Hari")
st.pyplot(fig)

st.info(
    "Pada Working Day, penyewaan meningkat pada jam 08.00 serta 17.00–18.00. "
    "Pada Non-Working Day, penyewaan lebih banyak terjadi pada siang hingga sore hari."
)

st.divider()


st.subheader("Analisis Lanjutan: Pengelompokan Level Demand")

st.write(
    """
    Pada bagian ini, rata-rata penyewaan sepeda dikelompokkan menjadi Low Demand,
    Medium Demand, dan High Demand berdasarkan jam dan tipe hari.
    """
)

demand_by_hour_day = main_df.groupby(["workingday", "hr"], as_index=False).agg({
    "cnt": "mean"
})

def demand_level(avg_rentals):
    if avg_rentals < 150:
        return "Low Demand"
    elif avg_rentals < 300:
        return "Medium Demand"
    else:
        return "High Demand"

demand_by_hour_day["demand_level"] = demand_by_hour_day["cnt"].apply(demand_level)

g = sns.catplot(
    data=demand_by_hour_day,
    x="hr",
    y="cnt",
    hue="demand_level",
    col="workingday",
    kind="bar",
    height=5,
    aspect=1.3,
    palette=["tab:blue", "tab:orange", "tab:green"]
)

g.set_axis_labels("Jam", "Rata-rata Penyewaan")
g.set_titles("{col_name}")
g.fig.suptitle("Pengelompokan Level Demand Penyewaan Sepeda berdasarkan Jam dan Tipe Hari", y=1.05)

st.pyplot(g.fig)

st.success(
    "Hasil pengelompokan demand dapat membantu menentukan waktu prioritas penyediaan sepeda "
    "dan waktu yang lebih tepat untuk pengecekan atau penataan ulang unit sepeda."
)

st.divider()


st.subheader("Kesimpulan Utama")

st.markdown(
    """
    - Total penyewaan sepeda pada tahun 2012 lebih tinggi dibandingkan tahun 2011 di setiap bulan.
    - Rata-rata penyewaan sepeda pada tahun 2012 cenderung lebih tinggi dibandingkan tahun 2011 pada berbagai musim dan kondisi cuaca.
    - Musim Fall dan cuaca Clear memiliki rata-rata penyewaan yang tinggi.
    - Pada Working Day, penyewaan meningkat pada pagi dan sore hari.
    - Pada Non-Working Day, penyewaan lebih banyak terjadi pada siang hingga sore hari.
    - Periode Low Demand dapat dimanfaatkan untuk pengecekan kondisi sepeda dan penataan ulang unit sepeda.
    """
)

st.caption("Bike Sharing Dashboard | Proyek Analisis Data")