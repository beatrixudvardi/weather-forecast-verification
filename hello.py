import requests
import pandas as pd
import matplotlib.pyplot as plt
"""
url= "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 47.4979,
    "longitude": 19.0402,
    "hourly": "temperature_2m",
}

response = requests.get(url, params=params)
#print(response.json())

data= response.json()
# Till the print, we can shortage the structure: df = pd.DataFrame(data["hourly"])
times = data['hourly']['time']
temperature = data['hourly']['temperature_2m']
#print(max(temperature))

df= pd.DataFrame({"time":times, "temperature": temperature})
#print(df.head())

df['time'] = pd.to_datetime(df['time'])
df['date'] = df['time'].dt.date
#print(df.head())
daily_max = df.groupby('date')['temperature'].max()
print(daily_max)

plt.plot(daily_max.index, daily_max.values, marker='o', linestyle='-', color='b'    )
#plt.show()
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Daily Maximum Temperature")
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m/%d')) 
plt.xticks(rotation=90)
plt.savefig("daily_temperature.png")
plt.show()
"""

lat, lon = 47.4979, 19.0402
start_date = "2026-08-10"
end_date = "2026-08-25"
# 1. Fetch Actual/Reanalysis Ground Baseline 
archive_url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
archive_data = requests.get(archive_url).json()['hourly']
# 2. Fetch the Forecast issued for those identical dates
forecast_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
forecast_data = requests.get(forecast_url).json()['hourly']
# 3. Align and Calculate Error
df= pd.DataFrame({
    "time": archive_data['time'],
    "actual_temperature": archive_data['temperature_2m'],
    "forecast_temperature": forecast_data['temperature_2m']
})
df['time'] = pd.to_datetime(df['time'])
df['date'] = df['time'].dt.date
#Mean absolute error (MAE) and root mean square error (RMSE)
df['absolute_error'] = abs(df['forecast_temperature'] - df['actual_temperature'])
df['squared_error'] = (df['forecast_temperature'] - df['actual_temperature']) ** 2
#df['difference']= df['forecast_temperature'] - df['actual_temperature']
#print(df.head())
daily_absolute_mean= df.groupby('date')['absolute_error'].mean()
# Save to inspect locally
df.to_csv("temperature_comparison.csv", index=False)

print(daily_absolute_mean.head())
plt.plot(daily_absolute_mean.index, daily_absolute_mean.values, marker='o', linestyle='-', color='r')
plt.xlabel("Time")
plt.ylabel("Absolute error (°C)")
plt.title("Temperature Uncertaity Analysis")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
plt.savefig("temperature_uncertainty.png")

