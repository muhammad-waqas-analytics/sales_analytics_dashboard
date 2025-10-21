# ====================================================
# STEP 3 - Smart Auto Update and Clean Sales Dashboard
# ====================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# ✅ 1. Read latest sales data
file_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/Data/sales_data.csv"
df = pd.read_csv(file_path)

# ✅ 2. Basic cleaning (remove duplicates & nulls)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

# ✅ 3. Recalculate total column if missing
if 'Total' not in df.columns:
    df['Total'] = df['Quantity'] * df['Unit_Price']

# ✅ 4. Save cleaned file back to CSV
df.to_csv(file_path, index=False)

# ✅ 5. Summary stats
total_sales = df["Total"].sum()
avg_sales = df["Total"].mean()
sales_by_region = df.groupby("Region")["Total"].sum()
sales_by_product = df.groupby("Product")["Total"].sum()

print("✅ Data cleaned and updated successfully!")
print("📊 Total Sales:", total_sales)
print("📈 Average Sale Per Transaction:", avg_sales)

# ========================================
# ✅ VISUALS SECTION
# ========================================

plt.figure(figsize=(8, 4))
sns.barplot(x="Region", y="Total", data=df, hue="Region", palette="cool", legend=False)
plt.title("Total Sales by Region")
plt.savefig("/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_by_region.png")
plt.close()

plt.figure(figsize=(8, 4))
sns.barplot(x="Product", y="Total", data=df, hue="Product", palette="magma", legend=False)
plt.title("Total Sales by Product")
plt.savefig("/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_by_product.png")
plt.close()

# ========================================
# ✅ PDF REPORT GENERATION
# ========================================

pdf_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Sales Analytics Report", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph(f"Total Sales: {total_sales}", styles["Normal"]))
story.append(Paragraph(f"Average Sale per Transaction: {avg_sales:.2f}", styles["Normal"]))
story.append(Spacer(1, 12))

story.append(Paragraph("Sales by Region:", styles["Heading2"]))
story.append(Paragraph(sales_by_region.to_string(), styles["Code"]))
story.append(Spacer(1, 12))

story.append(Paragraph("Sales by Product:", styles["Heading2"]))
story.append(Paragraph(sales_by_product.to_string(), styles["Code"]))
story.append(Spacer(1, 12))

story.append(Image("/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_by_region.png", width=400, height=250))
story.append(Spacer(1, 12))
story.append(Image("/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_by_product.png", width=400, height=250))

doc.build(story)

print(f"✅ PDF Report Generated: {pdf_path}")

# ====================================================
# STEP 4 - Email Automation (Send PDF Report)
# ====================================================

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# ✅ Read email credentials from config.json
config_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/config.json"
with open(config_path, 'r') as file:
    config = json.load(file)

sender_email = config["sender_email"]
app_password = config["app_password"]
receiver_email = config["receiver_email"]

# ✅ Email setup
subject = "Weekly Sales Report 📊"
body = "Dear Team,\n\nPlease find the attached latest Sales Report (PDF).\n\nRegards,\nSales Analytics System"

# ✅ Create email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# ✅ Attach PDF report
pdf_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals/sales_report.pdf"
with open(pdf_path, "rb") as pdf_file:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_file.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
message.attach(part)

# ✅ Send email via Gmail SMTP
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(message)
        print("✅ Email sent successfully with attached PDF!")
except Exception as e:
    print("❌ Error sending email:", e)

