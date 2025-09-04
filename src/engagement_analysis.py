import argparse
import sys
from typing import Dict, Tuple

import numpy as np
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Load CSV data into a pandas DataFrame with basic dtype handling.

    Args:
        path: Path to the engagement CSV file.

    Returns:
        DataFrame with the dataset.
    """
    df = pd.read_csv(path)
    # Normalize column names in case of accidental whitespace
    df.columns = [c.strip() for c in df.columns]
    return df


def _safe_divide(numerator: float, denominator: float) -> float:
    return float(numerator) / float(denominator) if float(denominator or 0) != 0 else 0.0


def compute_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """Compute top-level KPIs from the dataset.

    KPIs:
      - average_session_duration_minutes
      - average_sessions_per_week
      - average_purchases_per_user
      - retention_rate_high_engagement (proportion of High in EngagementLevel)

    Args:
        df: Input dataframe

    Returns:
        Dict of KPI name -> value
    """
    df_local = df.copy()

    # Coerce numeric columns safely if present
    numeric_cols = [
        "PlayTimeHours",
        "InGamePurchases",
        "SessionsPerWeek",
        "AvgSessionDurationMinutes",
        "PlayerLevel",
        "AchievementsUnlocked",
    ]
    for col in numeric_cols:
        if col in df_local.columns:
            df_local[col] = pd.to_numeric(df_local[col], errors="coerce")

    # Engagement level normalization
    if "EngagementLevel" in df_local.columns:
        df_local["EngagementLevel"] = df_local["EngagementLevel"].astype(str).str.strip().str.title()

    total_players = df_local.shape[0]

    avg_session_duration = float(df_local["AvgSessionDurationMinutes"].mean()) if "AvgSessionDurationMinutes" in df_local else np.nan
    avg_sessions_per_week = float(df_local["SessionsPerWeek"].mean()) if "SessionsPerWeek" in df_local else np.nan
    avg_purchases_per_user = float(df_local["InGamePurchases"].mean()) if "InGamePurchases" in df_local else np.nan

    retention_rate = np.nan
    if "EngagementLevel" in df_local:
        high_count = (df_local["EngagementLevel"] == "High").sum()
        retention_rate = _safe_divide(high_count, total_players)

    return {
        "total_players": total_players,
        "average_session_duration_minutes": round(avg_session_duration, 2) if not np.isnan(avg_session_duration) else np.nan,
        "average_sessions_per_week": round(avg_sessions_per_week, 2) if not np.isnan(avg_sessions_per_week) else np.nan,
        "average_purchases_per_user": round(avg_purchases_per_user, 2) if not np.isnan(avg_purchases_per_user) else np.nan,
        "retention_rate_high_engagement": round(retention_rate, 4) if not np.isnan(retention_rate) else np.nan,
    }


def segment_analysis(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Compute segmented KPIs by GameGenre, Location, and EngagementLevel.

    Returns a dict of segment name to aggregated DataFrame.
    """
    df_local = df.copy()
    # Ensure numeric
    for col in ["AvgSessionDurationMinutes", "SessionsPerWeek", "InGamePurchases"]:
        if col in df_local.columns:
            df_local[col] = pd.to_numeric(df_local[col], errors="coerce")

    # Normalize categorical fields if present
    for cat_col in ["GameGenre", "Location", "EngagementLevel"]:
        if cat_col in df_local.columns:
            df_local[cat_col] = df_local[cat_col].astype(str).str.strip().str.title()

    aggregations = {
        "AvgSessionDurationMinutes": "mean",
        "SessionsPerWeek": "mean",
        "InGamePurchases": ["mean", "sum"],
        "PlayerID": "count",
    }

    def group_by(col: str) -> pd.DataFrame:
        available_aggs = {k: v for k, v in aggregations.items() if k in df_local.columns}
        if col not in df_local.columns:
            return pd.DataFrame()
        grouped = df_local.groupby(col).agg(available_aggs)
        # Flatten columns
        grouped.columns = [
            "_".join([c for c in map(str, col_tuple) if c != ""]).strip("_") for col_tuple in grouped.columns.values
        ]
        grouped = grouped.rename(columns={"PlayerID_count": "num_players"})
        return grouped.reset_index().sort_values(by=grouped.columns[1] if grouped.shape[1] > 1 else col, ascending=False)

    return {
        "by_genre": group_by("GameGenre"),
        "by_location": group_by("Location"),
        "by_engagement": group_by("EngagementLevel"),
    }


def _format_percentage(x: float) -> str:
    try:
        return f"{100.0 * float(x):.2f}%"
    except Exception:
        return "n/a"


def main(argv: Tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Engagement KPI computation")
    parser.add_argument("--data", "-d", type=str, default="data/engagement_data.csv", help="Path to CSV data")
    args = parser.parse_args(argv)

    try:
        df = load_data(args.data)
    except FileNotFoundError:
        print(f"Data file not found at '{args.data}'. Place the CSV and try again.")
        return 1

    kpis = compute_kpis(df)
    segments = segment_analysis(df)

    print("=== Top-level KPIs ===")
    print(f"Players: {kpis['total_players']}")
    print(f"Avg Session Duration (min): {kpis['average_session_duration_minutes']}")
    print(f"Avg Sessions/Week: {kpis['average_sessions_per_week']}")
    print(f"Avg Purchases/User: {kpis['average_purchases_per_user']}")
    print(f"High Engagement Retention: {_format_percentage(kpis['retention_rate_high_engagement'])}")

    # Print brief segment summaries
    for name, seg_df in segments.items():
        if seg_df.empty:
            continue
        print(f"\n=== Segment: {name} ===")
        # Show top 5 rows
        with pd.option_context('display.max_columns', None):
            print(seg_df.head(5).to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


