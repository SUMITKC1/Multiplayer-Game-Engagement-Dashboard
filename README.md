# Multiplayer Game Engagement Dashboard

A professional analytics project exploring multiplayer gaming engagement using the Kaggle dataset "Predict Online Gaming Behavior".

## Overview
This project analyzes multiplayer gaming sessions and social/monetization behavior to understand engagement patterns across genres and regions.

## Dataset
Columns:
- PlayerID (unique user ID)
- Age
- Gender
- Location
- GameGenre
- PlayTimeHours (total playtime hours)
- InGamePurchases (count of purchases)
- GameDifficulty
- SessionsPerWeek
- AvgSessionDurationMinutes
- PlayerLevel
- AchievementsUnlocked
- EngagementLevel (categorical: Low, Medium, High)

## KPIs
- Avg Session Time: mean of AvgSessionDurationMinutes.
- Sessions/Week: mean of SessionsPerWeek.
- Retention (proxy): share of EngagementLevel == High.
- ARPU: average in-game purchases per player.
- ARPPU: average purchases for paying users or High-engagement users.

## Tech Stack
- Python (pandas, numpy, matplotlib, seaborn)
- Jupyter Notebook
- Power BI, Tableau (dashboard files)

## Repository Structure
`
/ 
 data/
    engagement_data.csv         # Kaggle dataset (place file here)
 notebooks/
    engagement_analysis.ipynb   # EDA + KPIs notebook
 dashboards/
    powerbi_dashboard.pbix      # Power BI file
    tableau_dashboard.twb       # Tableau file (placeholder)
    screenshots/                # exported dashboard screenshots
 src/
    engagement_analysis.py      # Python KPI computations
 README.md
 requirements.txt
 .gitignore
`

## Quickstart
1. Create a virtual environment and install dependencies:
`ash
python -m venv .venv
. .venv/Scripts/Activate.ps1  # PowerShell on Windows
pip install -r requirements.txt
`
2. Place the Kaggle CSV at data/engagement_data.csv.
3. Run the Python script:
`ash
python src/engagement_analysis.py --data data/engagement_data.csv
`
4. Open the notebook:
`ash
jupyter notebook notebooks/engagement_analysis.ipynb
`

## Dashboards
The BI dashboards are organized into four pages with the following visuals and KPIs.

### Overview Page
- KPI cards: Avg Session Duration, Sessions/Week, Retention %, Purchases, ARPU, ARPPU
- Geo map: engagement by Location
- Trend: Sessions per week over time (or by cohort index)

### Engagement Page
- Session duration by GameGenre
- Distribution plots (session duration histograms)
- Engagement level comparisons

### Monetization Page
- Purchases by Engagement Level (boxplots)
- ARPU and ARPPU cards
- Funnel: Login  Session  Purchase  Achievement

### Retention Page
- Cohort heatmap of retention proxy (share of High engagement)
- Genre  Location heatmap

Sample DAX (Power BI):
`
ARPU = DIVIDE(SUM(InGamePurchases), DISTINCTCOUNT(PlayerID))
ARPPU = DIVIDE(SUM(InGamePurchases), CALCULATE(DISTINCTCOUNT(PlayerID), EngagementLevel = "High"))
RetentionRate = DIVIDE(CALCULATE(COUNT(PlayerID), EngagementLevel = "High"), COUNT(PlayerID))
`

## Screenshots
Place exported visuals in dashboards/screenshots/ and link them here:
- ![Overview](dashboards/screenshots/overview.png)
- ![Engagement](dashboards/screenshots/engagement.png)
- ![Monetization](dashboards/screenshots/monetization.png)
- ![Retention](dashboards/screenshots/retention.png)

## Example Insight
"High engagement users had 25% longer sessions and 3x purchases."

## Notes
- Notebook includes dummy data fallback to render plots if the CSV is missing.
- Script prints top-level KPIs and segment summaries by genre, location, and engagement.