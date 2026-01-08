import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors

# Load data
df = pd.read_csv("rv-dashboard.csv")
df = df[['WEEKENDING','RPHO_REGION','COV_POSITIVES']]

# Clean
df['COV_POSITIVES'] = pd.to_numeric(df['COV_POSITIVES'], errors='coerce').fillna(0)
df['WEEKENDING'] = pd.to_datetime(df['WEEKENDING'], format='%m/%d/%Y')

# Extract year
df['year'] = df['WEEKENDING'].dt.year

# Aggregate
yearly_region = (
    df.groupby(['year','RPHO_REGION'])['COV_POSITIVES']
      .sum()
      .reset_index()
)

# Plot
plt.figure(figsize=(12,6))
ax = sns.barplot(
    data=yearly_region,
    x='year',
    y='COV_POSITIVES',
    hue='RPHO_REGION'
)

plt.title("Year-wise COVID Cases vs RPHO Regions")
plt.xlabel("Year")
plt.ylabel("Total Cases")


# Hover
cursor = mplcursors.cursor(ax.containers, hover=True)

@cursor.connect("add")
def on_add(sel):
    sel.annotation.set_text(
        f"Cases: {int(sel.target[1])}"
    )

plt.show()
