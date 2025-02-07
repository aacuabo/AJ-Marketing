import sqlite3
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import itertools
import matplotlib.pyplot as plt

conn = sqlite3.connect("Marketing.db")

query = "SELECT Region, CTR, CPC, CVR, ROAS FROM ads"  # Replace with your actual table name
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Drop missing values
df = df.dropna()

# Define your four regions
regions = ["West", "South", "Midwest", "Northeast"]

# Ensure all regions exist in the dataset
available_regions = df["Region"].unique()
missing_regions = [r for r in regions if r not in available_regions]

if missing_regions:
    print(f"⚠️ Warning: The following regions are missing from the dataset: {missing_regions}")

# ANOVA for CTR across all four regions
ctr_values = [df[df["Region"] == region]["CTR"] for region in regions]
anova_ctr = stats.f_oneway(*ctr_values)

print("\nANOVA Test for CTR Across Regions:")
print(f"F-Statistic: {anova_ctr.statistic:.4f}, p-value: {anova_ctr.pvalue:.4f}")

if anova_ctr.pvalue < 0.05:
    print("✅ Significant difference in CTR across regions.\n")
else:
    print("❌ No significant difference in CTR across regions.\n")

# ANOVA for CPC across all four regions
cpc_values = [df[df["Region"] == region]["CPC"] for region in regions]
anova_cpc = stats.f_oneway(*cpc_values)

print("ANOVA Test for CPC Across Regions:")
print(f"F-Statistic: {anova_cpc.statistic:.4f}, p-value: {anova_cpc.pvalue:.4f}")

if anova_cpc.pvalue < 0.05:
    print("✅ Significant difference in CPC across regions.\n")
else:
    print("❌ No significant difference in CPC across regions.\n")
    
# ANOVA for CVR across all four regions
cvr_values = [df[df["Region"] == region]["CVR"] for region in regions]
anova_cvr = stats.f_oneway(*cvr_values)

print("ANOVA Test for CVR Across Regions:")
print(f"F-Statistic: {anova_cvr.statistic:.4f}, p-value: {anova_cvr.pvalue:.4f}")

if anova_cvr.pvalue < 0.05:
    print("✅ Significant difference in CVR across regions.\n")
else:
    print("❌ No significant difference in CVR across regions.\n")
    
# ANOVA for ROAS across all four regions
roas_values = [df[df["Region"] == region]["ROAS"] for region in regions]
anova_roas = stats.f_oneway(*roas_values)

print("ANOVA Test for ROAS Across Regions:")
print(f"F-Statistic: {anova_roas.statistic:.4f}, p-value: {anova_roas.pvalue:.4f}")

if anova_roas.pvalue < 0.05:
    print("✅ Significant difference in ROAS across regions.\n")
else:
    print("❌ No significant difference in ROAS across regions.\n")

# Pairwise t-tests for all region combinations
print("\nPairwise T-Tests for CTR:")
for r1, r2 in itertools.combinations(regions, 2):
    ctr_1 = df[df["Region"] == r1]["CTR"]
    ctr_2 = df[df["Region"] == r2]["CTR"]
    
    if not ctr_1.empty and not ctr_2.empty:
        t_test_ctr = stats.ttest_ind(ctr_1, ctr_2, equal_var=False)
        print(f"{r1} vs {r2} - T-Statistic: {t_test_ctr.statistic:.4f}, p-value: {t_test_ctr.pvalue:.4f}")
        if t_test_ctr.pvalue < 0.05:
            print(f"✅ Significant difference in CTR between {r1} and {r2}.\n")
        else:
            print(f"❌ No significant difference in CTR between {r1} and {r2}.\n")

print("\nPairwise T-Tests for CPC:")
for r1, r2 in itertools.combinations(regions, 2):
    cpc_1 = df[df["Region"] == r1]["CPC"]
    cpc_2 = df[df["Region"] == r2]["CPC"]
    
    if not cpc_1.empty and not cpc_2.empty:
        t_test_cpc = stats.ttest_ind(cpc_1, cpc_2, equal_var=False)
        print(f"{r1} vs {r2} - T-Statistic: {t_test_cpc.statistic:.4f}, p-value: {t_test_cpc.pvalue:.4f}")
        if t_test_cpc.pvalue < 0.05:
            print(f"✅ Significant difference in CPC between {r1} and {r2}.\n")
        else:
            print(f"❌ No significant difference in CPC between {r1} and {r2}.\n")

for r1, r2 in itertools.combinations(regions, 2):
    cvr_1 = df[df["Region"] == r1]["CVR"]
    cvr_2 = df[df["Region"] == r2]["CVR"]
    
    if not cvr_1.empty and not cvr_2.empty:
        t_test_cvr = stats.ttest_ind(cvr_1, cvr_2, equal_var=False)
        print(f"{r1} vs {r2} - T-Statistic: {t_test_cvr.statistic:.4f}, p-value: {t_test_cvr.pvalue:.4f}")
        if t_test_cvr.pvalue < 0.05:
            print(f"✅ Significant difference in CVR between {r1} and {r2}.\n")
        else:
            print(f"❌ No significant difference in CVR between {r1} and {r2}.\n")

for r1, r2 in itertools.combinations(regions, 2):
    roas_1 = df[df["Region"] == r1]["ROAS"]
    roas_2 = df[df["Region"] == r2]["ROAS"]
    
    if not roas_1.empty and not roas_2.empty:
        t_test_roas = stats.ttest_ind(roas_1, roas_2, equal_var=False)
        print(f"{r1} vs {r2} - T-Statistic: {t_test_roas.statistic:.4f}, p-value: {t_test_roas.pvalue:.4f}")
        if t_test_roas.pvalue < 0.05:
            print(f"✅ Significant difference in ROAS between {r1} and {r2}.\n")
        else:
            print(f"❌ No significant difference in ROAS between {r1} and {r2}.\n")

