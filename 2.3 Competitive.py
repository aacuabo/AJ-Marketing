import sqlite3
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect("Marketing.db")

# Query to fetch data
query = "SELECT Is_Competitive_Event, CTR, CPC, CVR, ROAS FROM ads"  # Ensure your column names match
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Drop missing values
df = df.dropna()

# Define the two groups: Competitive Event vs. Non-Competitive Event
event_groups = ["TRUE", "FALSE"]

# Ensure both categories exist in the dataset
available_groups = df["Is_Competitive_Event"].unique()
missing_groups = [g for g in event_groups if g not in available_groups]

if missing_groups:
    print(f"⚠️ Warning: The following groups are missing from the dataset: {missing_groups}")

# T-Test for CTR
ctr_yes = df[df["Is_Competitive_Event"] == "TRUE"]["CTR"]
ctr_no = df[df["Is_Competitive_Event"] == "FALSE"]["CTR"]

t_test_ctr = stats.ttest_ind(ctr_yes, ctr_no, equal_var=False)

print("\nT-Test for CTR (Competitive Event vs. No Event):")
print(f"T-Statistic: {t_test_ctr.statistic:.4f}, p-value: {t_test_ctr.pvalue:.4f}")

if t_test_ctr.pvalue < 0.05:
    print("✅ Significant difference in CTR between Competitive Events and Non-Events.\n")
else:
    print("❌ No significant difference in CTR.\n")

# T-Test for CPC
cpc_yes = df[df["Is_Competitive_Event"] == "TRUE"]["CPC"]
cpc_no = df[df["Is_Competitive_Event"] == "FALSE"]["CPC"]

t_test_cpc = stats.ttest_ind(cpc_yes, cpc_no, equal_var=False)

print("T-Test for CPC (Competitive Event vs. No Event):")
print(f"T-Statistic: {t_test_cpc.statistic:.4f}, p-value: {t_test_cpc.pvalue:.4f}")

if t_test_cpc.pvalue < 0.05:
    print("✅ Significant difference in CPC between Competitive Events and Non-Events.\n")
else:
    print("❌ No significant difference in CPC.\n")

# T-Test for CVR
cvr_yes = df[df["Is_Competitive_Event"] == "TRUE"]["CVR"]
cvr_no = df[df["Is_Competitive_Event"] == "FALSE"]["CVR"]

t_test_cvr = stats.ttest_ind(cvr_yes, cvr_no, equal_var=False)

print("T-Test for CVR (Competitive Event vs. No Event):")
print(f"T-Statistic: {t_test_cvr.statistic:.4f}, p-value: {t_test_cvr.pvalue:.4f}")

if t_test_cvr.pvalue < 0.05:
    print("✅ Significant difference in CVR between Competitive Events and Non-Events.\n")
else:
    print("❌ No significant difference in CVR.\n")

# T-Test for ROAS
roas_yes = df[df["Is_Competitive_Event"] == "TRUE"]["ROAS"]
roas_no = df[df["Is_Competitive_Event"] == "FALSE"]["ROAS"]

t_test_roas = stats.ttest_ind(roas_yes, roas_no, equal_var=False)

print("T-Test for ROAS (Competitive Event vs. No Event):")
print(f"T-Statistic: {t_test_roas.statistic:.4f}, p-value: {t_test_roas.pvalue:.4f}")

if t_test_roas.pvalue < 0.05:
    print("✅ Significant difference in ROAS between Competitive Events and Non-Events.\n")
else:
    print("❌ No significant difference in ROAS.\n")
