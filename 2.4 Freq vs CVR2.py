##PEARSON'S CORRELATION COEFFICIENT (FREQUENCY VS. CONVERSION RATE)

import sqlite3
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Connect to SQLite database
conn = sqlite3.connect("Marketing.db")

# Fetch data (assuming the table has 'Frequency' and 'CVR' columns)
query = "SELECT Frequency, CVR FROM ads"
df = pd.read_sql(query, conn)

# Close connection
conn.close()

# Drop missing values
df = df.dropna()

# Calculate Pearson correlation
correlation, p_value = stats.pearsonr(df["Frequency"], df["CVR"])

print(f"📊 Pearson Correlation between Frequency and CVR: {correlation:.4f}, p-value: {p_value:.4f}")

if p_value < 0.05:
    print("✅ Significant relationship detected.\n")
else:
    print("❌ No significant relationship found.\n")

# Scatterplot
plt.figure(figsize=(8, 5))
sns.regplot(x=df["Frequency"], y=df["CVR"], scatter_kws={"alpha": 0.5})
plt.title("Frequency vs Conversion Rate (CVR)")
plt.xlabel("Ad Frequency")
plt.ylabel("Conversion Rate (CVR)")
plt.show()
