import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE = "https://data.financialresearch.gov/v1"

START_DATE = "2025-09-01"
END_DATE   = "2025-09-30"

SERIES = {
    "Total":            "REPO-TRI_TV_TOT-P",
    "Overnight/Open":   "REPO-TRI_TV_OO-P",
    "Term 2–7 Days":    "REPO-TRI_TV_B27-P",
    "Term 8–30 Days":   "REPO-TRI_TV_B830-P",
    "Term >30 Days":    "REPO-TRI_TV_G30-P",
}

params = {
    "mnemonics": ",".join(SERIES.values()),
    "start_date": START_DATE,
    "end_date": END_DATE,
}

resp = requests.get(f"{BASE}/series/multifull", params=params, timeout=60)
resp.raise_for_status()
raw = resp.json()

frames = []

for label, mnem in SERIES.items():
    ts = raw[mnem]["timeseries"]
    sub = list(ts.keys())[0]   # genelde "aggregation"
    tmp = pd.DataFrame(ts[sub], columns=["date", "value"])
    tmp["date"] = pd.to_datetime(tmp["date"])
    tmp["series"] = label
    frames.append(tmp)

df = pd.concat(frames, ignore_index=True).sort_values("date")

print("Kullanılan tarih aralığı:",
      df["date"].min().date(), "→", df["date"].max().date())

sns.set_theme(style="whitegrid")
plt.figure(figsize=(14,6))

sns.lineplot(
    data=df[df["series"] != "Total"],  # total'i özellikle dışarıda tutuyoruz
    x="date",
    y="value",
    hue="series",
    linewidth=2
)

plt.title("Tri-Party Repo Transaction Volume (Preliminary) — Components (Sep 2025)")
plt.xlabel("Date")
plt.ylabel("Transaction Volume")
plt.legend(title="Component")
plt.tight_layout()
plt.show()


# -----------------------
# 2025 Eylül payları
# -----------------------
pivot = df.pivot_table(
    index="series",
    values="value",
    aggfunc="mean"
)

total_val = pivot.loc["Total", "value"]

shares = (
    pivot
    .drop(index="Total")
    .assign(share=lambda x: x["value"] / total_val * 100)
    .reset_index()
)

print("\n2025 Eylül — Ortalama Paylar (%)")
print(shares[["series", "share"]].round(2))

plt.figure(figsize=(8,5))
sns.barplot(
    data=shares,
    x="series",
    y="share"
)

plt.title("Tri-Party Repo Composition — September 2025 (Preliminary)")
plt.ylabel("Share of Total (%)")
plt.xlabel("")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
