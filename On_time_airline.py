#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from scipy.stats import probplot
from tabulate import tabulate
from mpl_toolkits.mplot3d import Axes3D
import warnings

warnings.filterwarnings("ignore")

# Global style settings for readable, consistent plots
plt.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.titlesize": 17,
})

#%%
# =============================================================================
# SECTION 1: LOAD DATASET
# =============================================================================

print("=" * 60)
print("SECTION 1: LOADING DATASET")
print("=" * 60)

# Load the dataset — update path if needed
df = pd.read_csv("/Users/anushkarajeshsalvi/Desktop/Tech/Visualization_Project_Spring/T_ONTIME_MARKETING_2.csv")

print("Dataset loaded successfully!")
print(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

#%%
print("=" * 60)
print("SECTION 2: DATA UNDERSTANDING")
print("=" * 60)

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- Data Types & Non-Null Counts ---")
df.info()

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Missing Values per Column ---")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
print(missing_df[missing_df["Missing Count"] > 0])

#%%
print("\n" + "=" * 60)
print("SECTION 3: DATA CLEANING")
print("=" * 60)

# Convert FL_DATE to datetime
df["FL_DATE"] = pd.to_datetime(df["FL_DATE"], errors="coerce")
print("FL_DATE converted to datetime.")

# Define numeric delay columns
numeric_cols = [
    "DEP_DELAY", "DEP_DELAY_NEW", "DEP_DEL15",
    "ARR_DELAY", "ARR_DELAY_NEW", "ARR_DEL15",
    "AIR_TIME", "CARRIER_DELAY", "WEATHER_DELAY",
    "NAS_DELAY", "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY"
]

# Ensure numeric types
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill delay cause columns with 0 (no delay recorded = 0 minutes)
delay_cause_cols = ["CARRIER_DELAY", "WEATHER_DELAY", "NAS_DELAY",
                    "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY"]
for col in delay_cause_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Fill core delay columns with median (avoids skewing by extreme outliers)
for col in ["DEP_DELAY", "ARR_DELAY", "AIR_TIME"]:
    if col in df.columns:
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"{col}: missing values filled with median ({median_val:.2f})")

# Drop rows still missing in critical categorical columns
df = df.dropna(subset=["ORIGIN", "DAY_OF_WEEK", "FL_DATE"])
print(f"\nAfter cleaning — Shape: {df.shape[0]} rows × {df.shape[1]} columns")

#%%
print("\n" + "=" * 60)
print("SECTION 4: FEATURE ENGINEERING")
print("=" * 60)

# TOTAL_DELAY = departure delay + arrival delay
df["TOTAL_DELAY"] = df["DEP_DELAY"] + df["ARR_DELAY"]


# DELAY_TYPE: primary cause of delay
def classify_delay(row):
    if row["WEATHER_DELAY"] > 0:
        return "Weather"
    elif row["CARRIER_DELAY"] > 0:
        return "Carrier"
    else:
        return "Other"


df["DELAY_TYPE"] = df.apply(classify_delay, axis=1)

# DELAY_FLAG: 1 if any delay occurred, else 0
df["DELAY_FLAG"] = ((df["DEP_DELAY"] > 0) | (df["ARR_DELAY"] > 0)).astype(int)

print("New columns created:")
print(f"  TOTAL_DELAY  — sample: {df['TOTAL_DELAY'].head(3).tolist()}")
print(f"  DELAY_TYPE   — value counts:\n{df['DELAY_TYPE'].value_counts()}")
print(f"  DELAY_FLAG   — value counts:\n{df['DELAY_FLAG'].value_counts()}")

#%%
print("\n" + "=" * 60)
print("SECTION 5: OUTLIER DETECTION")
print("=" * 60)

# Boxplots BEFORE removal
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax, col, color in zip(axes, ["DEP_DELAY", "ARR_DELAY"], ["steelblue", "coral"]):
    ax.boxplot(df[col].dropna(), patch_artist=True,
               boxprops=dict(facecolor=color, alpha=0.6))
    ax.set_title(f"Boxplot of {col} (Before Outlier Removal)", fontsize=14)
    ax.set_ylabel("Minutes", fontsize=12)
    ax.set_xlabel(col, fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.5)
plt.suptitle("Outlier Detection — Before IQR Removal", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("boxplot_before_outlier_removal.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The boxplots reveal a heavy right-skewed distribution for both DEP_DELAY
and ARR_DELAY. There are many extreme positive outliers (very long delays), which are
real but rare events. These outliers can distort statistical means and regression fits,
so we remove only the most extreme values using IQR × 3 to preserve natural variability.
""")

# IQR method — remove only extreme outliers (3×IQR)
for col in ["DEP_DELAY", "ARR_DELAY"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 3 * IQR
    upper = Q3 + 3 * IQR
    before = len(df)
    df = df[(df[col] >= lower) & (df[col] <= upper)]
    after = len(df)
    print(f"{col}: removed {before - after} extreme outliers | bounds [{lower:.2f}, {upper:.2f}]")

print(f"\nFinal shape after outlier removal: {df.shape}")

#%%
print("\n" + "=" * 60)
print("SECTION 6: STATISTICAL ANALYSIS")
print("=" * 60)

# --- Descriptive Statistics ---
print("\n--- Descriptive Statistics (Delay Columns) ---")
desc_cols = ["DEP_DELAY", "ARR_DELAY", "TOTAL_DELAY", "WEATHER_DELAY", "CARRIER_DELAY"]
print(df[desc_cols].describe().round(2))

# --- Group Analysis: Average delay by ORIGIN ---
avg_delay_origin = (
    df.groupby("ORIGIN")["DEP_DELAY"]
    .mean()
    .sort_values(ascending=False)
    .round(2)
    .reset_index()
    .rename(columns={"DEP_DELAY": "Avg_DEP_DELAY"})
)
print(f"\n--- Top 10 Airports by Average DEP_DELAY ---")
print(avg_delay_origin.head(10).to_string(index=False))

# --- Group Analysis: Average delay by DAY_OF_WEEK ---
avg_delay_dow = (
    df.groupby("DAY_OF_WEEK")["DEP_DELAY"]
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={"DEP_DELAY": "Avg_DEP_DELAY"})
)
print(f"\n--- Average DEP_DELAY by Day of Week ---")
print(avg_delay_dow.to_string(index=False))

# --- Weather Delay Analysis ---
weather_count = (df["WEATHER_DELAY"] > 0).sum()
weather_avg = df[df["WEATHER_DELAY"] > 0]["WEATHER_DELAY"].mean()
print(f"\n--- Weather Delay Analysis ---")
print(f"  Flights with WEATHER_DELAY > 0 : {weather_count}")
print(f"  Average WEATHER_DELAY (when > 0): {weather_avg:.2f} minutes")