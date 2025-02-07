import sqlite3
import pandas as pd
import scipy.stats as stats
import itertools

# Database connection
conn = sqlite3.connect("Marketing.db")
query = "SELECT Creative_Type, CTR, CPC, CVR, ROAS FROM ads"  # Replace with your actual table name
df = pd.read_sql(query, conn)
conn.close()

# Drop missing values
df = df.dropna()

# Define your five creative groups
creative_groups = ["Carousel", "Search", "Video", "Image", "Display"]

# Ensure all creative groups exist in the dataset
available_groups = df["Creative_Type"].unique()
missing_groups = [g for g in creative_groups if g not in available_groups]

if missing_groups:
    print(f"⚠️ Warning: The following creative groups are missing from the dataset: {missing_groups}")

# Perform ANOVA for each metric (CTR, CPC, CVR, ROAS)
metrics = ["CTR", "CPC", "CVR", "ROAS"]

for metric in metrics:
    values = [df[df["Creative_Type"] == group][metric] for group in creative_groups]
    anova_result = stats.f_oneway(*values)
    
    print(f"\nANOVA Test for {metric} Across Creative Groups:")
    print(f"F-Statistic: {anova_result.statistic:.4f}, p-value: {anova_result.pvalue:.4f}")

    if anova_result.pvalue < 0.05:
        print(f"✅ Significant difference in {metric} across creative groups.\n")
    else:
        print(f"❌ No significant difference in {metric} across creative groups.\n")

# Pairwise t-tests for each creative group combination and metric
for metric in metrics:
    print(f"\nPairwise T-Tests for {metric}:")
    for g1, g2 in itertools.combinations(creative_groups, 2):
        group_1 = df[df["Creative_Type"] == g1][metric]
        group_2 = df[df["Creative_Type"] == g2][metric]
        
        if not group_1.empty and not group_2.empty:
            t_test_result = stats.ttest_ind(group_1, group_2, equal_var=False)
            print(f"{g1} vs {g2} - T-Statistic: {t_test_result.statistic:.4f}, p-value: {t_test_result.pvalue:.4f}")
            if t_test_result.pvalue < 0.05:
                print(f"✅ Significant difference in {metric} between {g1} and {g2}.\n")
            else:
                print(f"❌ No significant difference in {metric} between {g1} and {g2}.\n")
