import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Load and clean data
df = pd.read_csv(r"C:\Users\user\Desktop\ML\rv-dashboard.csv")
df = df[['WEEKENDING','RPHO_REGION','COV_POSITIVES']]

df['COV_POSITIVES'] = pd.to_numeric(df['COV_POSITIVES'], errors='coerce').fillna(0)
df['WEEKENDING'] = pd.to_datetime(df['WEEKENDING'], format='%m/%d/%Y')

# Aggregate monthly per region
df['month_year'] = df['WEEKENDING'].dt.to_period('M').dt.to_timestamp()
monthly_region = df.groupby(['month_year','RPHO_REGION'])['COV_POSITIVES'].sum().reset_index()

# Select region
region = 'Los Angeles'
data = monthly_region[monthly_region['RPHO_REGION'] == region][['month_year','COV_POSITIVES']]
data = data.set_index('month_year')

# Split 2025 actuals
actual_2025 = data[data.index.year == 2025]

# Fit SARIMA model (monthly data)
# (p,d,q) = (1,1,1), seasonal (P,D,Q,s) = (1,1,1,12) for monthly seasonality
model = SARIMAX(data['COV_POSITIVES'], 
                order=(1,1,1), 
                seasonal_order=(1,1,1,12),
                enforce_stationarity=False,
                enforce_invertibility=False)
results = model.fit(disp=False)

# Forecast next 12 months (2026)
forecast_2026 = results.get_forecast(steps=12)
forecast_index = pd.date_range(start='2026-01-01', periods=12, freq='MS')
forecast_values = forecast_2026.predicted_mean
forecast_df = pd.DataFrame({'month_year': forecast_index, 'Predicted': forecast_values}).set_index('month_year')

#Removing negative values
forecast_values = forecast_values.clip(lower=0)
forecast_df = pd.DataFrame({'month_year': forecast_index, 'Predicted': forecast_values}).set_index('month_year')

# Plot 2025 actual vs 2026 forecast
plt.figure(figsize=(12,6))

# 2025 actuals
plt.plot(actual_2025.index, actual_2025['COV_POSITIVES'], marker='o', color='skyblue', label='2025 Actual Cases')
for i, val in enumerate(actual_2025['COV_POSITIVES']):
    plt.text(actual_2025.index[i], val+0.5, str(int(val)), ha='center', va='bottom', fontsize=9, color='blue')

# 2026 forecast
plt.plot(forecast_df.index, forecast_df['Predicted'], marker='o', color='orange', label='2026 Forecasted Cases')
for i, val in enumerate(forecast_df['Predicted']):
    plt.text(forecast_df.index[i], val+0.5, str(int(val)), ha='center', va='bottom', fontsize=9, color='red')

plt.title(f"COVID Cases: 2025 Actual vs 2026 SARIMA Forecast ({region})")
plt.xlabel("Month")
plt.ylabel("Cases")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
