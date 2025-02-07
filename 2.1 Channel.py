import sqlite3
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import itertools
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests

# Connect to SQLite database
conn = sqlite3.connect("Marketing.db")

# Load data
query = "SELECT Platform, CTR, CPC, CVR, ROAS FROM ads"  # Make sure "Channel" exists in your dataset
df = pd.read_sql(query, conn)

# Close database connection
conn.close()

# Drop missing values
df = df.dropna()

# Define your channels
channels = ["FB", "Google", "TT"]

# Ensure all channels exist in the dataset
available_channels = df["Platform"].unique()
missing_channels = [c for c in channels if c not in available_channels]

if missing_channels:
    print(f"⚠️ Warning: The following channels are missing from the dataset: {missing_channels}")

# ANOVA for CTR across all channels
ctr_values = [df[df["Platform"] == channel]["CTR"] for channel in channels]
anova_ctr = stats.f_oneway(*ctr_values)

print("\nANOVA Test for CTR Across Channels:")
print(f"F-Statistic: {anova_ctr.statistic:.4f}, p-value: {anova_ctr.pvalue:.4f}")

# ANOVA for CPC across all channels
cpc_values = [df[df["Platform"] == channel]["CPC"] for channel in channels]
anova_cpc = stats.f_oneway(*cpc_values)

print("\nANOVA Test for CPC Across Channels:")
print(f"F-Statistic: {anova_cpc.statistic:.4f}, p-value: {anova_cpc.pvalue:.4f}")

# ANOVA for CVR across all channels
cvr_values = [df[df["Platform"] == channel]["CVR"] for channel in channels]
anova_cvr = stats.f_oneway(*cvr_values)

print("\nANOVA Test for CVR Across Channels:")
print(f"F-Statistic: {anova_cvr.statistic:.4f}, p-value: {anova_cvr.pvalue:.4f}")

# ANOVA for ROAS across all channels
roas_values = [df[df["Platform"] == channel]["ROAS"] for channel in channels]
anova_roas = stats.f_oneway(*roas_values)

print("\nANOVA Test for ROAS Across Channels:")
print(f"F-Statistic: {anova_roas.statistic:.4f}, p-value: {anova_roas.pvalue:.4f}")
if anova_roas.pvalue < 0.05:
            print(f"✅ Significant difference in ROAS Across Channels.\n")
else:
            print(f"❌ No significant difference in ROAS Across Channels.\n")

# Pairwise T-tests with Bonferroni correction
metrics = ["CTR", "CPC", "CVR", "ROAS"]
for metric in metrics:
    print(f"\nPairwise T-Tests for {metric}:")
    p_values = []
    pairs = list(itertools.combinations(channels, 2))

    for ch1, ch2 in pairs:
        group_1 = df[df["Platform"] == ch1][metric]
        group_2 = df[df["Platform"] == ch2][metric]

        if not group_1.empty and not group_2.empty:
            t_test = stats.ttest_ind(group_1, group_2, equal_var=False)
            p_values.append(t_test.pvalue)
    
    # Bonferroni correction
    adjusted_p_values = multipletests(p_values, method="bonferroni")[1]

    for i, (ch1, ch2) in enumerate(pairs):
        print(f"{ch1} vs {ch2} - Adjusted p-value: {adjusted_p_values[i]:.4f}")
        if adjusted_p_values[i] < 0.05:
            print(f"✅ Significant difference in {metric} between {ch1} and {ch2}.\n")
        else:
            print(f"❌ No significant difference in {metric} between {ch1} and {ch2}.\n")

# Visualization: Boxplots for CTR, CPC, CVR, ROAS across channels
for metric in metrics:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="Platform", y=metric, data=df)
    plt.title(f"{metric} Distribution Across Channels")
    plt.show()
