import requests
import pandas as pd

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