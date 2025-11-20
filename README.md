<img width="1536" height="1024" alt="sales_dashboard banner" src="https://github.com/user-attachments/assets/d0edbcab-ed82-4411-8866-728bde4f6810" />
# 📊 Smart Sales Analytics Dashboard Automation  
**Author:** Muhammad Waqas — Data Analyst (Python Projects)  

---

## 🧠 Project Overview
This project is a **Smart Sales Analytics Dashboard Automation System** built entirely in Python.  
It automates the complete sales-data workflow — from raw data to final report delivery.

The system automatically:
- Reads sales data from a CSV file  
- Cleans and validates the data (removes duplicates and handles missing values)  
- Calculates total and average sales  
- Generates professional visual charts for **Sales by Region** and **Sales by Product**  
- Exports all insights into a well-formatted **PDF report**  
- Sends the report automatically via **email**

This project demonstrates a full **end-to-end data automation pipeline**, showcasing real-world Data Analyst skills — including data cleaning, visualization, reporting, and automation.

---

## ⚙️ Key Features
✅ Cleans and validates raw sales data automatically  
✅ Removes duplicates & handles missing values  
✅ Recalculates totals using Quantity × Unit Price  
✅ Creates bar charts for **Sales by Region** and **Sales by Product**  
✅ Exports a professional **PDF report**  
✅ Sends the report via email automatically  
✅ Includes detailed error handling for missing files or invalid data  

---
<img width="1784" height="1181" alt="sales_visuals_overview" src="https://github.com/user-attachments/assets/b259355b-72aa-497a-b3fb-cc0eccfc7f06" />

---
## 🧰 Tools & Libraries Used
- **Python 3.11**  
- **Pandas** → Data Cleaning & Analysis  
- **Matplotlib / Seaborn** → Visualization  
- **ReportLab** → PDF Report Generation  
- **smtplib (Gmail SMTP)** → Email Automation  

---

## ⚙️ How to Run

1. **Clone this repository**
   ```bash
   git clone https://github.com/muhammad-waqas-analytics/sales_analytics_dashboard.git
   cd sales_analytics_dashboard


Install dependencies

pip install pandas matplotlib seaborn reportlab


Add your config.json

{
  "sender_email": "youremail@gmail.com",
  "app_password": "your_app_password",
  "receiver_email": "receiver@gmail.com"
}


Run the main script

python main.py

📊 Output Preview

The script automatically generates:

📈 Visual graphs for region-wise and product-wise sales

🧾 PDF report summarizing the data

✉️ Sends the report via email automatically

👨‍💻 Author

Muhammad Waqas
Data Analyst | Python Automation | Dashboard Development
📧 trendytreasures017@gmail.com

🔗 LinkedIn Profile : https://www.linkedin.com/in/mr-waqas/

⭐ If you find this project useful, please give it a star on GitHub!

---
## 🧰 Virtual Environment (recommended)

Create and use a local virtual environment so dependencies don't conflict with your system Python.

Linux / macOS

```bash
# from project root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell)

```powershell
# from project root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Notes:
- The `.venv/` directory is ignored by the repository (`.gitignore`) — do not commit it.
- To update `requirements.txt` from your venv:

```bash
.venv/bin/python -m pip freeze > requirements.txt
git add requirements.txt && git commit -m "Update requirements.txt"
```

---
## ⚠️ (Optional) Purge `.venv` from Git history

If `.venv` was accidentally committed and you need to remove it from the repository history (this rewrites history and will require all collaborators to re-clone), two common tools are:

1) git-filter-repo (recommended)

```bash
# install (once)
python -m pip install git-filter-repo

# from repository root — WARNING: rewrites history
git clone --mirror <repo-url> repo-mirror.git
cd repo-mirror.git
git-filter-repo --invert-paths --paths .venv
git push --force
```

2) BFG Repo-Cleaner

```bash
# download BFG or install via package manager
# from repository root (create a mirror clone first)
git clone --mirror <repo-url> repo-mirror.git
java -jar bfg.jar --delete-folders .venv repo-mirror.git
cd repo-mirror.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

If you want me to run the history-purge commands for you, I can do that — but please confirm you understand this will rewrite the repository history and everyone with clones will need to re-clone or follow recovery steps.
