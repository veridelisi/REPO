import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE = "https://data.financialresearch.gov/v1"
START_DATE = "2025-09-01"
END_DATE   = "2025-09-30"

SERIES = {
    "U.S. Treasury":      "REPO-TRI_TV_T-P",
    "Agency & GSE":       "REPO-TRI_TV_AG-P",
    "Corporate Debt":     "REPO-TRI_TV_CORD-P",
    "Other Collateral":   "REPO-TRI_TV_O-P",
    "Total":              "REPO-TRI_TV_TOT-P",
}

params = {
    "mnemonics": ",".join(SERIES.values()),
    "start_date": START_DATE,
    "end_date": END_DATE,
}

raw = requests.get(f"{BASE}/series/multifull", params=params, timeout=60).json()

frames = []
for label, mnem in SERIES.items():
    ts = raw[mnem]["timeseries"]
    sub = list(ts.keys())[0]
    df_tmp = pd.DataFrame(ts[sub], columns=["date", "value"])
    df_tmp["date"] = pd.to_datetime(df_tmp["date"])
    df_tmp["series"] = label
    frames.append(df_tmp)

df = pd.concat(frames, ignore_index=True).sort_values("date")
df["value_trn"] = df["value"] / 1e12

sns.set_theme(style="whitegrid", context="talk", font_scale=0.9)

plt.figure(figsize=(14,6))
sns.lineplot(
    data=df[df["series"] != "Total"],
    x="date",
    y="value_trn",
    hue="series",
    linewidth=2
)

plt.title(
    "Tri-Party Repo Transaction Volume (Preliminary)\n"
    "Collateral Breakdown — September 2025",
    pad=12
)
plt.ylabel("Transaction Volume (Trillion USD)")
plt.xlabel("")
plt.legend(title="Collateral Type", frameon=False)
plt.tight_layout()
plt.show()

pivot = (
    df
    .groupby("series")["value"]
    .mean()
)

total_val = pivot["Total"]

shares = (
    pivot.drop("Total")
    .div(total_val)
    .mul(100)
    .reset_index()
)

shares.columns = ["Collateral", "Share (%)"]

print("\n2025 Eylül — Collateral Payları (%)")
print(shares.round(2))

plt.figure(figsize=(8,5))
sns.barplot(
    data=shares,
    x="Collateral",
    y="Share (%)"
)

plt.title("Tri-Party Repo Collateral Composition — September 2025 (Preliminary)")
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()
