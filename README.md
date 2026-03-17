📊 Media Content Analytics Dashboard
![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?logo=plotly)
![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit%20Cloud-FF4B4B)
An interactive, fully filterable BI dashboard built to demonstrate real-world Business Intelligence Analyst skills — the kind of work done at companies like Hearst Magazines, Share Local Media, and other data-driven media organizations.
---
🖥️ Live Demo
> **[Launch Dashboard →]([https://share.streamlit.io/jarvissimms12/media-content-analytics-dashboard](https://media-content-analytics--dashboard-ykhuyt9siqectqqde5ezch.streamlit.app/))**  
> *Deployed on Streamlit Cloud — no installation required*
---
📸 Dashboard Preview
![Dashboard Screenshot](assets/dashboard_preview.png)
---
🎯 What This Dashboard Demonstrates
Skill	Implementation
KPI Tracking	5 live metrics with period-over-period delta comparisons
Trend Analysis	Weekly views vs revenue dual-axis line chart
Audience Segmentation	Traffic source breakdown, regional performance
Engagement Analysis	Scatter plot of time-on-page vs engagement rate
Revenue Intelligence	Category × Source revenue heatmap
Interactive Filtering	Sidebar filters for category, source, and date range
Data Storytelling	Clean layout with section headers, annotations, top-10 table
---
📐 Dashboard Sections
1. KPI Summary Row
Total Views, Unique Visitors, Avg Engagement Rate, Avg Time on Page, Total Revenue
Each metric shows period-over-period delta
2. Performance Trends
Weekly Views vs Revenue — dual-axis line chart with area fill
Views by Category — horizontal bar chart colored by engagement rate
3. Audience & Source Deep Dive
Traffic Source Breakdown — donut chart
Day-of-Week Performance — bar chart showing optimal publish timing
Time on Page vs Engagement — scatter plot with category color and size by views
4. Revenue Intelligence
Revenue Heatmap — category × traffic source matrix showing top-performing combinations
Top 10 Articles — sortable table with views, engagement, and revenue
---
🛠️ Tech Stack
Python 3.8+ — core language
Streamlit — interactive web app framework
Plotly — interactive charts (line, bar, pie, scatter, heatmap)
pandas — data manipulation and aggregation
numpy — statistical data generation
---
🚀 Run Locally
```bash
# 1. Clone the repo
git clone https://github.com/jarvissimms12/media-content-analytics-dashboard.git
cd media-content-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`
---
📁 Project Structure
```
media-content-analytics-dashboard/
├── app.py                  # Main Streamlit dashboard
├── requirements.txt        # Python dependencies
├── assets/
│   └── dashboard_preview.png
└── README.md
```
---
🔗 Related Projects
NYC Housing Data Analysis — API ingestion, data cleaning, and reporting pipeline
Credit Card Fraud Detection — ML classification with SMOTE and Random Forest
Agricultural Crop Classifier — Deep learning with ResNet50, 81.9% accuracy
---
👤 Author
Jarvis Simms | MS Data Science, NYIT 2025 | Brooklyn, NY  
GitHub • LinkedIn
