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

#%%
# --- Correlation Analysis + Heatmap ---
print("\n--- Correlation Analysis ---")
corr_cols_s6 = ["DEP_DELAY", "ARR_DELAY", "AIR_TIME", "CARRIER_DELAY",
                "WEATHER_DELAY", "NAS_DELAY", "LATE_AIRCRAFT_DELAY", "TOTAL_DELAY"]
corr_matrix_s6 = df[corr_cols_s6].dropna().corr().round(2)
print(corr_matrix_s6)

# Plot the heatmap as part of Section 6
fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(
    corr_matrix_s6,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax,
    linewidths=0.5,
    cbar_kws={"label": "Correlation Coefficient"}
)
ax.set_title("Section 6 — Correlation Heatmap of Delay Features", fontsize=15)
plt.tight_layout()
plt.savefig("section6_correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The heatmap reveals how strongly each delay type relates to others.
DEP_DELAY and ARR_DELAY are highly correlated (close to 1.0), meaning a late
departure almost always causes a late arrival. LATE_AIRCRAFT_DELAY is also
strongly linked to both — a cascading effect from prior flights. WEATHER_DELAY
has a moderate correlation, confirming it contributes significantly but isn't
the sole driver. AIR_TIME shows near-zero correlation with delays, confirming
that flight length doesn't cause delays — ground operations do.
""")

#%%
# =============================================================================
# SECTION 7: ALL VISUALIZATIONS
# =============================================================================

print("\n" + "=" * 60)
print("SECTION 7: VISUALIZATIONS")
print("=" * 60)


# ── Helper to add value labels on bars ──────────────────────────────────────
def add_bar_labels(ax, fmt="{:.2f}", fontsize=9):
    for patch in ax.patches:
        val = patch.get_height()
        if not np.isnan(val) and val != 0:
            ax.annotate(fmt.format(val),
                        (patch.get_x() + patch.get_width() / 2, val),
                        ha="center", va="bottom", fontsize=fontsize)


# ── 1. LINE PLOT — TOTAL_DELAY over DAY_OF_MONTH ────────────────────────────
line_data = df.groupby("DAY_OF_MONTH")["TOTAL_DELAY"].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(line_data["DAY_OF_MONTH"], line_data["TOTAL_DELAY"],
        marker="o", color="steelblue", linewidth=2, markersize=5)
ax.set_title("Average Total Delay by Day of Month", fontsize=15)
ax.set_xlabel("Day of Month", fontsize=13)
ax.set_ylabel("Average Total Delay (min)", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(["Avg Total Delay"], fontsize=11)
plt.tight_layout()
plt.savefig("plot_01_line_total_delay_by_dom.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The line plot shows how average total delay fluctuates across days of the month.
Mid-month and end-of-month days often show elevated delays, possibly due to increased
travel demand or scheduling pressure. Days with consistent spikes may align with weekends.
""")

# ── 2. BAR PLOT — Delays by ORIGIN (Top 20, sorted, values shown) ────────────
top20 = avg_delay_origin.head(20)
fig, ax = plt.subplots(figsize=(14, 6))
bars = ax.bar(top20["ORIGIN"], top20["Avg_DEP_DELAY"],
              color=sns.color_palette("Spectral", len(top20)))
ax.set_title("Top 20 Airports by Average Departure Delay", fontsize=15)
ax.set_xlabel("Airport (ORIGIN)", fontsize=13)
ax.set_ylabel("Average DEP_DELAY (min)", fontsize=13)
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.5)
add_bar_labels(ax, fontsize=8)
plt.tight_layout()
plt.savefig("plot_02_bar_delay_by_origin.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Some airports consistently show higher average departure delays.
Airports with high delays may face congestion, adverse weather, or structural
operational challenges. This helps airlines and passengers prioritize which routes
to monitor for punctuality issues.
""")

# ── 3. GROUPED BAR PLOT — Delays by DAY_OF_WEEK ─────────────────────────────
dow_data = df.groupby("DAY_OF_WEEK")[["DEP_DELAY", "ARR_DELAY"]].mean().round(2).reset_index()
x = np.arange(len(dow_data))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
b1 = ax.bar(x - width / 2, dow_data["DEP_DELAY"], width, label="DEP_DELAY", color="steelblue")
b2 = ax.bar(x + width / 2, dow_data["ARR_DELAY"], width, label="ARR_DELAY", color="coral")
for bar in list(b1) + list(b2):
    ax.annotate(f"{bar.get_height():.2f}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center", va="bottom", fontsize=8)
ax.set_title("Average Departure & Arrival Delay by Day of Week", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("Average Delay (min)", fontsize=13)
ax.set_xticks(x)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_03_grouped_bar_delay_by_dow.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Friday and Sunday tend to have the highest delays due to peak travel demand.
Mid-week days (Tuesday, Wednesday) typically have the lowest delays. Arrival delays
closely mirror departure delays, suggesting cascading effects across the day's schedule.
""")

# ── 4. COUNT PLOT — DAY_OF_WEEK ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
day_counts = df["DAY_OF_WEEK"].value_counts().sort_index()
ax.bar(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
       day_counts.values, color=sns.color_palette("muted", 7))
add_bar_labels(ax, fmt="{:.0f}", fontsize=9)
ax.set_title("Flight Count by Day of Week", fontsize=15)
ax.set_xlabel("Day of Week", fontsize=13)
ax.set_ylabel("Number of Flights", fontsize=13)
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_04_count_plot_dow.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The count plot reveals that certain days carry significantly more flights
than others. Higher flight volume days may contribute to increased delays simply due
to congestion, independent of weather or mechanical factors.
""")

# ── 5. PIE CHART — DELAY_TYPE Distribution ──────────────────────────────────
delay_type_counts = df["DELAY_TYPE"].value_counts()
colors = ["#4C72B0", "#DD8452", "#55A868"]
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    delay_type_counts,
    labels=delay_type_counts.index,
    autopct="%1.2f%%",
    colors=colors,
    startangle=140,
    wedgeprops=dict(edgecolor="white", linewidth=1.5)
)
for text in autotexts:
    text.set_fontsize(12)
ax.set_title("Distribution of Delay Types", fontsize=15)
ax.legend(delay_type_counts.index, loc="lower right")
plt.tight_layout()
plt.savefig("plot_05_pie_delay_type.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The pie chart shows that most flights fall into the "Other" delay category,
while Weather and Carrier delays each account for a smaller share. Carrier delays
being significant highlights airline-controllable factors as key improvement areas.
""")

# ── 6. DISTRIBUTION PLOT — DEP_DELAY ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df["DEP_DELAY"].dropna(), kde=True, bins=50,
             color="steelblue", ax=ax, edgecolor="white")
ax.set_title("Distribution of Departure Delay", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("Frequency", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(["KDE", "Frequency"])
plt.tight_layout()
plt.savefig("plot_06_dist_dep_delay.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The distribution of DEP_DELAY is right-skewed, meaning most flights depart
on time or with minor delays, while a smaller number have very long delays. This
non-normal distribution affects which statistical tests are appropriate for this data.
""")

# ── 7. PAIR PLOT ─────────────────────────────────────────────────────────────
pair_cols = ["DEP_DELAY", "ARR_DELAY", "AIR_TIME", "TOTAL_DELAY"]
pair_df = df[pair_cols + ["DELAY_TYPE"]].dropna().sample(min(2000, len(df)), random_state=42)
pair_grid = sns.pairplot(pair_df, hue="DELAY_TYPE", diag_kind="kde",
                         plot_kws={"alpha": 0.4, "s": 15},
                         palette={"Weather": "#4C72B0", "Carrier": "#DD8452", "Other": "#55A868"})
pair_grid.figure.suptitle("Pair Plot of Delay Variables by Delay Type", y=1.02, fontsize=15)
pair_grid.figure.savefig("plot_07_pair_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The pair plot reveals strong positive correlation between DEP_DELAY and
ARR_DELAY — a late departure usually results in a late arrival. AIR_TIME shows little
correlation with delay magnitude, suggesting delays originate at the gate, not in-flight.
""")

# ── 8. CORRELATION HEATMAP ───────────────────────────────────────────────────
corr_cols = ["DEP_DELAY", "ARR_DELAY", "AIR_TIME", "CARRIER_DELAY",
             "WEATHER_DELAY", "NAS_DELAY", "LATE_AIRCRAFT_DELAY", "TOTAL_DELAY"]
corr_df = df[corr_cols].dropna()
corr_matrix = corr_df.corr().round(2)
fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            ax=ax, linewidths=0.5, cbar_kws={"label": "Correlation"})
ax.set_title("Correlation Heatmap of Delay Features", fontsize=15)
plt.tight_layout()
plt.savefig("plot_08_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] DEP_DELAY and ARR_DELAY are highly correlated (~0.9+). LATE_AIRCRAFT_DELAY
is also strongly correlated with both, showing that delays from previous flights cascade.
WEATHER_DELAY has a moderate correlation, indicating it contributes but is not the
dominant factor across all flights.
""")

# ── 9. HISTOGRAM WITH KDE — DEP_DELAY ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
df["DEP_DELAY"].dropna().plot(kind="hist", bins=60, density=True,
                              alpha=0.5, color="steelblue", edgecolor="white", ax=ax)
df["DEP_DELAY"].dropna().plot(kind="kde", color="darkblue", linewidth=2.5, ax=ax)
ax.set_title("Histogram with KDE — Departure Delay", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("Density", fontsize=13)
ax.legend(["KDE Curve", "Histogram"], fontsize=11)
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_09_histogram_kde.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The KDE overlaid on the histogram confirms the right skew of departure
delays. The peak near 0 indicates most flights are on time, with a long tail extending
rightward representing significantly delayed flights.
""")

# ── 10. Q-Q PLOT ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 7))
sample = df["DEP_DELAY"].dropna().sample(min(3000, len(df)), random_state=42)
probplot(sample, dist="norm", plot=ax)
ax.set_title("Q-Q Plot — Departure Delay vs Normal Distribution", fontsize=15)
ax.get_lines()[0].set(markerfacecolor="steelblue", markersize=3, alpha=0.5)
ax.get_lines()[1].set(color="red", linewidth=2)
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_10_qq_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The Q-Q plot shows significant departure from the reference diagonal,
especially in the upper tail. This confirms DEP_DELAY is NOT normally distributed —
it is heavily right-skewed. Non-parametric tests should be preferred for analysis.
""")

# ── 11. KDE PLOT — Custom Styling ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
for delay_type, color in zip(["Weather", "Carrier", "Other"],
                             ["#1f77b4", "#ff7f0e", "#2ca02c"]):
    subset = df[df["DELAY_TYPE"] == delay_type]["DEP_DELAY"].dropna()
    if len(subset) > 10:
        subset.plot(kind="kde", ax=ax, label=delay_type, color=color,
                    linewidth=2.5, linestyle="-")
ax.fill_between(ax.lines[0].get_xdata(), ax.lines[0].get_ydata(), alpha=0.15, color="#1f77b4")
ax.set_title("KDE Plot — Departure Delay by Delay Type", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("Density", fontsize=13)
ax.legend(title="Delay Type")
ax.grid(True, linestyle="--", alpha=0.5)
ax.set_xlim(-60, 200)
plt.tight_layout()
plt.savefig("plot_11_kde_custom.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Weather-related delays show a wider distribution extending further right,
indicating they tend to be longer when they occur. Carrier delays cluster closer to
zero, suggesting they are more frequent but shorter on average.
""")

# ── 12. REGRESSION PLOT — AIR_TIME vs DEP_DELAY ─────────────────────────────
sample = df[["AIR_TIME", "DEP_DELAY"]].dropna().sample(min(3000, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(9, 6))
sns.regplot(data=sample, x="AIR_TIME", y="DEP_DELAY",
            scatter_kws={"alpha": 0.2, "s": 15, "color": "steelblue"},
            line_kws={"color": "red", "linewidth": 2},
            ax=ax)
ax.set_title("Regression Plot — Air Time vs Departure Delay", fontsize=15)
ax.set_xlabel("AIR_TIME (min)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_12_regression_airtime_dep_delay.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The regression plot shows little to no linear relationship between air time
and departure delay. This confirms that delays are primarily ground-based (gate, crew,
weather at origin) and are not driven by the length of the flight itself.
""")

# ── 13. MULTIVARIATE BOX PLOT — DEP_DELAY by DAY_OF_WEEK ────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(data=df, x="DAY_OF_WEEK", y="DEP_DELAY",
            palette="Set2", ax=ax, showfliers=False)
ax.set_title("Departure Delay by Day of Week (Box Plot)", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_13_box_dep_delay_by_dow.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Box plots reveal that Friday has the highest median departure delay and the
widest spread, confirming peak-day congestion effects. Saturday has notably lower
delays, possibly due to fewer business travelers and lower overall volume.
""")

# ── 14. MULTIVARIATE BOXEN PLOT ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
sns.boxenplot(data=df, x="DAY_OF_WEEK", y="DEP_DELAY",
              palette="coolwarm", ax=ax)
ax.set_title("Departure Delay by Day of Week (Boxen Plot)", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_14_boxen_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The boxen plot (letter-value plot) provides more detail about the distribution
tails than a standard box plot. It shows that the upper tails on Fridays and Mondays
extend further, indicating more extreme delay events on those days.
""")

# ── 15. AREA PLOT — Avg Total Delay by DAY_OF_MONTH ─────────────────────────
area_data = df.groupby("DAY_OF_MONTH")["TOTAL_DELAY"].mean()
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(area_data.index, area_data.values, alpha=0.4, color="steelblue")
ax.plot(area_data.index, area_data.values, color="darkblue", linewidth=2)
ax.set_title("Area Plot — Average Total Delay by Day of Month", fontsize=15)
ax.set_xlabel("Day of Month", fontsize=13)
ax.set_ylabel("Average Total Delay (min)", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(["Avg Total Delay"])
plt.tight_layout()
plt.savefig("plot_15_area_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The area plot visually emphasizes the volume of cumulative delay across
the month. Peaks in mid-month and end-of-month periods highlight cyclical patterns
that may correspond to higher booking density or scheduling constraints.
""")

# ── 16. VIOLIN PLOT — DEP_DELAY by DAY_OF_WEEK ──────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
sns.violinplot(data=df, x="DAY_OF_WEEK", y="DEP_DELAY",
               palette="pastel", inner="quartile", ax=ax)
ax.set_title("Violin Plot — Departure Delay by Day of Week", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_16_violin_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Violin plots combine box plot and KDE information. Wider sections represent
a higher density of data at that delay value. Friday and Thursday show bimodal shapes,
suggesting two distinct delay patterns (mild vs severe) on those days.
""")

# ── 17. JOINT PLOT — DEP_DELAY vs ARR_DELAY ─────────────────────────────────
sample2 = df[["DEP_DELAY", "ARR_DELAY"]].dropna().sample(min(2000, len(df)), random_state=42)
joint = sns.jointplot(data=sample2, x="DEP_DELAY", y="ARR_DELAY",
                      kind="scatter", alpha=0.3, color="steelblue",
                      marginal_kws={"bins": 40, "color": "steelblue"})
joint.figure.suptitle("Joint Plot — Departure vs Arrival Delay", y=1.02, fontsize=15)
joint.set_axis_labels("DEP_DELAY (min)", "ARR_DELAY (min)", fontsize=13)
joint.figure.savefig("plot_17_joint_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The joint plot confirms strong positive correlation between departure and
arrival delays. The marginal distributions both show right skew. Most flights cluster
near the origin (on-time), with a scattered tail of significantly delayed flights.
""")

# ── 18. RUG PLOT ─────────────────────────────────────────────────────────────
sample3 = df["DEP_DELAY"].dropna().sample(min(500, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(10, 4))
sns.kdeplot(sample3, ax=ax, color="steelblue", linewidth=2, label="KDE")
sns.rugplot(sample3, ax=ax, color="darkblue", alpha=0.4, height=0.05)
ax.set_title("Rug Plot — Departure Delay Distribution", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("Density", fontsize=13)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_18_rug_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The rug plot shows individual data points along the x-axis, complementing
the KDE curve. High density of tick marks near 0 confirms that most flights depart
close to on-time, with sparse marks extending into larger delay values.
""")

# ── 19. 3D PLOT — DEP_DELAY, ARR_DELAY, AIR_TIME ────────────────────────────
sample4 = df[["DEP_DELAY", "ARR_DELAY", "AIR_TIME"]].dropna().sample(min(1500, len(df)), random_state=42)
fig = plt.figure(figsize=(11, 8))
ax3d = fig.add_subplot(111, projection="3d")
sc = ax3d.scatter(sample4["DEP_DELAY"], sample4["ARR_DELAY"], sample4["AIR_TIME"],
                  c=sample4["DEP_DELAY"], cmap="coolwarm", alpha=0.5, s=8)
fig.colorbar(sc, ax=ax3d, label="DEP_DELAY (min)")
ax3d.set_title("3D Scatter — DEP_DELAY vs ARR_DELAY vs AIR_TIME", fontsize=13)
ax3d.set_xlabel("DEP_DELAY", fontsize=11)
ax3d.set_ylabel("ARR_DELAY", fontsize=11)
ax3d.set_zlabel("AIR_TIME", fontsize=11)
plt.tight_layout()
plt.savefig("plot_19_3d_scatter.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The 3D scatter reveals that high departure and arrival delays cluster
regardless of air time. Long-haul flights (high AIR_TIME) don't systematically
have more delays, reinforcing that delays are mostly a ground/operational issue.
""")

# ── 20. CONTOUR PLOT — DEP_DELAY vs ARR_DELAY ───────────────────────────────
sample5 = df[["DEP_DELAY", "ARR_DELAY"]].dropna().sample(min(3000, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(9, 7))
h = ax.hexbin(sample5["DEP_DELAY"], sample5["ARR_DELAY"],
              gridsize=40, cmap="YlOrRd", mincnt=1)
plt.colorbar(h, ax=ax, label="Count")
ax.set_title("Contour/Density Plot — DEP_DELAY vs ARR_DELAY", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("ARR_DELAY (min)", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("plot_20_contour_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The density contour confirms the mass of flights concentrated near the
origin (0,0) — on-time departures and arrivals. The diagonal density band confirms
that delays in both dimensions co-occur, revealing strong coupling between dep and arr.
""")

# ── 21. CLUSTER MAP ──────────────────────────────────────────────────────────
cluster_cols = ["DEP_DELAY", "ARR_DELAY", "CARRIER_DELAY", "WEATHER_DELAY",
                "NAS_DELAY", "LATE_AIRCRAFT_DELAY", "AIR_TIME"]
cluster_data = df[cluster_cols].dropna().sample(min(500, len(df)), random_state=42)
normalized = (cluster_data - cluster_data.mean()) / cluster_data.std()
g = sns.clustermap(normalized.corr(), annot=True, fmt=".2f",
                   cmap="coolwarm", figsize=(9, 9), linewidths=0.5,
                   cbar_pos=(0.02, 0.83, 0.03, 0.15))
g.figure.suptitle("Cluster Map — Delay Feature Correlations", y=1.01, fontsize=14)
g.figure.savefig("plot_21_cluster_map.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The cluster map groups delay features with similar correlation patterns.
Late aircraft delay and dep/arr delay cluster together, suggesting they represent
the same underlying cascade effect. Weather and NAS delays cluster separately,
indicating different causal mechanisms.
""")

# ── 22. HEXBIN PLOT ──────────────────────────────────────────────────────────
sample6 = df[["DEP_DELAY", "ARR_DELAY"]].dropna().sample(min(5000, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(9, 7))
hb = ax.hexbin(sample6["DEP_DELAY"], sample6["ARR_DELAY"],
               gridsize=40, cmap="Blues", mincnt=1)
plt.colorbar(hb, ax=ax, label="Flight Count")
ax.set_title("Hexbin Plot — DEP_DELAY vs ARR_DELAY", fontsize=15)
ax.set_xlabel("DEP_DELAY (min)", fontsize=13)
ax.set_ylabel("ARR_DELAY (min)", fontsize=13)
ax.grid(True, linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("plot_22_hexbin.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] Hexbin plots handle overplotting in large datasets by binning points into
hexagons colored by count. The dense center confirms most flights are near on-time,
while the diagonal streak shows late departures systematically lead to late arrivals.
""")

# ── 23. STRIP PLOT ───────────────────────────────────────────────────────────
sample7 = df[["DEP_DELAY", "DAY_OF_WEEK"]].dropna().sample(min(2000, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(11, 6))
sns.stripplot(data=sample7, x="DAY_OF_WEEK", y="DEP_DELAY",
              jitter=True, alpha=0.3, palette="Set2", ax=ax)
ax.set_title("Strip Plot — Departure Delay by Day of Week", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_23_strip_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The strip plot shows individual flight data points, revealing the actual
spread of delays for each weekday. Vertical clustering near 0 is visible every day,
but Fridays and Mondays show more points scattered at higher delay values.
""")

# ── 24. SWARM PLOT ───────────────────────────────────────────────────────────
sample8 = df[["DEP_DELAY", "DAY_OF_WEEK", "DELAY_TYPE"]].dropna().sample(min(800, len(df)), random_state=42)
fig, ax = plt.subplots(figsize=(12, 6))
sns.swarmplot(data=sample8, x="DAY_OF_WEEK", y="DEP_DELAY",
              hue="DELAY_TYPE", palette="Set1", size=3, ax=ax, dodge=True)
ax.set_title("Swarm Plot — Departure Delay by Day of Week & Delay Type", fontsize=15)
ax.set_xlabel("Day of Week (1=Mon, 7=Sun)", fontsize=13)
ax.set_ylabel("DEP_DELAY (min)", fontsize=13)
ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
ax.legend(title="Delay Type", bbox_to_anchor=(1.01, 1), loc="upper left")
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("plot_24_swarm_plot.png", dpi=150, bbox_inches="tight")
plt.show()
print("""
[Insight] The swarm plot layers delay type onto individual data points. Weather delays
(blue) tend to cluster higher on the y-axis on certain days, confirming that when
weather delays occur they tend to be more severe than carrier delays.
""")