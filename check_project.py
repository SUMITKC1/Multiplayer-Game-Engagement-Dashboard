import os
from typing import List, Dict

REQUIRED_FILES = [
    "data/engagement_data.csv",
    "notebooks/engagement_analysis.ipynb",
    "dashboards/powerbi_dashboard.pbix",
    "dashboards/tableau_dashboard.twb",
    "dashboards/screenshots",
    "src/engagement_analysis.py",
    "README.md",
    "requirements.txt",
    ".gitignore",
]

REQUIRED_COLUMNS = [
    "PlayerID","Age","Gender","Location","GameGenre",
    "PlayTimeHours","InGamePurchases","GameDifficulty",
    "SessionsPerWeek","AvgSessionDurationMinutes",
    "PlayerLevel","AchievementsUnlocked","EngagementLevel"
]

README_SECTIONS = [
    "Overview", "Dataset", "KPIs", "Dashboards", "Tech Stack", "Example Insight", "Quickstart"
]


def check_files(paths: List[str]) -> Dict[str, bool]:
    return {p: os.path.exists(p) for p in paths}


def check_dataset_columns(csv_path: str, required_cols: List[str]) -> Dict[str, List[str]]:
    import pandas as pd
    if not os.path.exists(csv_path):
        return {"missing": required_cols, "present": []}
    try:
        df_head = pd.read_csv(csv_path, nrows=5)
        cols = [c.strip() for c in df_head.columns]
        present = [c for c in required_cols if c in cols]
        missing = [c for c in required_cols if c not in cols]
        return {"present": present, "missing": missing}
    except Exception:
        return {"present": [], "missing": required_cols}


def check_readme_sections(path: str, required_sections: List[str]) -> Dict[str, bool]:
    if not os.path.exists(path):
        return {s: False for s in required_sections}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return {s: (s.lower() in content.lower()) for s in required_sections}


def main() -> int:
    print("Running project health checks...\n")

    file_results = check_files(REQUIRED_FILES)
    missing_files = [p for p, ok in file_results.items() if not ok]

    dataset_results = check_dataset_columns("data/engagement_data.csv", REQUIRED_COLUMNS)

    readme_results = check_readme_sections("README.md", README_SECTIONS)
    missing_readme = [s for s, ok in readme_results.items() if not ok]

    issues = False

    if missing_files:
        issues = True
        print("Missing files/directories:")
        for p in missing_files:
            print(f" - {p}")
        print()

    if dataset_results.get("missing"):
        if len(dataset_results["missing"]) > 0:
            issues = True
            print("Dataset is missing required columns:")
            print(", ".join(dataset_results["missing"]))
            print()

    if missing_readme:
        issues = True
        print("README is missing sections:")
        print(", ".join(missing_readme))
        print()

    if not issues:
        print("Project is GitHub-ready! You can confidently publish.")
        return 0
    else:
        print("Warnings found. Please address the items above.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())