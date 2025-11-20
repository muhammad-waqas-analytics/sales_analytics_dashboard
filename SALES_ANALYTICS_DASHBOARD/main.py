import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import sys

# Replace the top-level script behavior with a main() and add validations
def main():
    file_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/Data/sales_data.csv"

    # Read CSV with error handling
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print("❌ Failed to read sales CSV:", e)
        sys.exit(1)

    # Ensure required columns exist
    required = ["Quantity", "Unit_Price", "Region", "Product"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print("❌ Missing required columns:", missing)
        sys.exit(1)

    # Basic cleaning: remove exact duplicate rows and only drop rows missing critical fields
    df.drop_duplicates(inplace=True)
    df.dropna(subset=required, inplace=True)

    # Coerce numeric types for calculation (safe)
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Unit_Price"] = pd.to_numeric(df["Unit_Price"], errors="coerce")
    df.dropna(subset=["Quantity", "Unit_Price"], inplace=True)

    # Recalculate Total if missing or if type unsafe
    if 'Total' not in df.columns or not pd.api.types.is_numeric_dtype(df['Total']):
        df['Total'] = df['Quantity'] * df['Unit_Price']

    # Save cleaned file back to CSV
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        print("❌ Failed to write cleaned CSV:", e)

    # Summary stats
    total_sales = df["Total"].sum()
    avg_sales = df["Total"].mean()
    sales_by_region = df.groupby("Region")["Total"].sum()
    sales_by_product = df.groupby("Product")["Total"].sum()

    print("✅ Data cleaned and updated successfully!")
    print("📊 Total Sales:", total_sales)
    print("📈 Average Sale Per Transaction:", avg_sales)

    # Ensure visuals directory exists
    visuals_dir = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/visuals"
    os.makedirs(visuals_dir, exist_ok=True)

    # Visuals (use bbox_inches to avoid cut off)
    region_png = os.path.join(visuals_dir, "sales_by_region.png")
    plt.figure(figsize=(8, 4))
    sns.barplot(x="Region", y="Total", data=df, palette="cool")
    plt.title("Total Sales by Region")
    plt.tight_layout()
    plt.savefig(region_png, bbox_inches="tight")
    plt.close()

    product_png = os.path.join(visuals_dir, "sales_by_product.png")
    plt.figure(figsize=(8, 4))
    sns.barplot(x="Product", y="Total", data=df, palette="magma")
    plt.title("Total Sales by Product")
    plt.tight_layout()
    plt.savefig(product_png, bbox_inches="tight")
    plt.close()

    # PDF generation (paths)
    pdf_path = os.path.join(visuals_dir, "sales_report.pdf")
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

    story.append(Image(region_png, width=400, height=250))
    story.append(Spacer(1, 12))
    story.append(Image(product_png, width=400, height=250))

    try:
        doc.build(story)
        print(f"✅ PDF Report Generated: {pdf_path}")
    except Exception as e:
        print("❌ Failed to generate PDF:", e)

    # Email sending: validate config file first
    config_path = "/workspaces/sales_analytics_dashboard/SALES_ANALYTICS_DASHBOARD/config.json"
    if not os.path.exists(config_path):
        print("❌ Email config.json not found. Skipping email send.")
        return

    import smtplib
    import json
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
    except Exception as e:
        print("❌ Failed to read config.json:", e)
        return

    sender_email = config.get("sender_email")
    app_password = config.get("app_password")
    receiver_email = config.get("receiver_email")
    if not (sender_email and app_password and receiver_email):
        print("❌ Incomplete email config. Skipping email send.")
        return

    subject = "Weekly Sales Report 📊"
    body = "Dear Team,\n\nPlease find the attached latest Sales Report (PDF).\n\nRegards,\nSales Analytics System"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Attach PDF report
    try:
        with open(pdf_path, "rb") as pdf_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_file.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
        message.attach(part)
    except Exception as e:
        print("❌ Failed to attach PDF:", e)
        return

    # Send email via Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(message)
            print("✅ Email sent successfully with attached PDF!")
    except Exception as e:
        print("❌ Error sending email:", e)


if __name__ == "__main__":
    main()

