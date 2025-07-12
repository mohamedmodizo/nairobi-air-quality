"""
Nairobi PM2.5 Air Quality Trend Analysis (2024–2025)

This script pulls one year of air pollution data (PM2.5) for Nairobi from OpenAQ,
cleans and resamples the data, and then plots the monthly average to visualize
pollution trends over time.

Author: mohamedmodizo
Date: July 2025
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create directory for plots if not exists
os.makedirs("plots", exist_ok=True)

# Fetch PM2.5 data from OpenAQ API
print("Fetching air quality data for Nairobi...")

url = "https://api.openaq.org/v2/measurements"
params = {
    "city": "Nairobi",
    "parameter": "pm25",
    "date_from": "2024-07-01",
    "date_to": "2025-07-01",
    "limit": 1000,
    "sort": "desc",
    "order_by": "datetime"
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Failed to fetch data.")
    exit()

data = response.json()
records = pd.json_normalize(data['results'])

# Process the data
print("Processing data...")
records['datetime'] = pd.to_datetime(records['date.utc'])
records.set_index('datetime', inplace=True)

# Resample to monthly average PM2.5 levels
monthly_avg = records['value'].resample('M').mean()

# Plot the results
print("Creating the plot...")
plt.figure(figsize=(10, 6))
monthly_avg.plot(marker='o', linestyle='-', color='darkgreen')
plt.title('Monthly Average PM2.5 Levels in Nairobi (2024–2025)')
plt.xlabel('Month')
plt.ylabel('PM2.5 (µg/m³)')
plt.grid(True)
plt.tight_layout()
plt.savefig('plots/monthly_pm25_nairobi.png')
plt.show()

print("Done! Chart saved in 'plots/monthly_pm25_nairobi.png'")
