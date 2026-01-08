import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("rv-dashboard.csv")
 
# Converting datetime (MM/DD/YYYY)
df['WEEKENDING'] = pd.to_datetime(df['WEEKENDING'], format='%m/%d/%Y')

# Create month-year column
df['month_year'] = df['WEEKENDING'].dt.strftime('%b %Y')  # e.g., 'Aug 2023'

# Aggregate COVID positives by month
monthly_covid = df.groupby('month_year')['COV_POSITIVES'].sum().reset_index()

# Sort months chronologically
monthly_covid['month_dt'] = pd.to_datetime(monthly_covid['month_year'], format='%b %Y')
monthly_covid = monthly_covid.sort_values('month_dt')

# Calculate month-over-month growth rate
monthly_covid['prev_month'] = monthly_covid['COV_POSITIVES'].shift(1)
monthly_covid['growth_rate'] = (
    (monthly_covid['COV_POSITIVES'] - monthly_covid['prev_month']) / monthly_covid['prev_month']
)
monthly_covid['growth_rate'] = monthly_covid['growth_rate'].replace([float('inf'), -float('inf')], 0)
monthly_covid['growth_rate'] = monthly_covid['growth_rate'].fillna(0)

# Plot 1: Monthly COVID Cases
plt.figure(figsize=(12,5))
plt.plot(
    monthly_covid['month_year'],
    monthly_covid['COV_POSITIVES'],
    marker='o',
    linewidth=2,
    color='skyblue',
    label='Monthly COVID Cases'
)

# Add numbers on points
for i, val in enumerate(monthly_covid['COV_POSITIVES']):
    plt.text(i, val + 0.5, str(val), ha='center', va='bottom', color='blue')

plt.title('Monthly COVID Cases')
plt.xlabel('Month')
plt.ylabel('Total Cases')
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# Plot 2: Monthly Growth Rate

plt.figure(figsize=(12,5))
plt.plot(
    monthly_covid['month_year'],
    monthly_covid['growth_rate'],
    marker='s',
    linewidth=2,
    color='orange',
    label='Monthly Growth Rate'
)

# Add numbers on points
for i, val in enumerate(monthly_covid['growth_rate']):
    plt.text(i, val + 0.01, f"{val:.2f}", ha='center', va='bottom', color='orange')

plt.title('Monthly COVID Growth Rate')
plt.xlabel('Month')
plt.ylabel('Growth Rate')
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
