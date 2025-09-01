import os
import requests
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv(override=True)

# Step 1: Generate email with Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are an assistant that drafts professional emails."},
        {"role": "user", "content": "Write an email to confirm a project meeting on Friday."}
    ]
}
resp = requests.post(groq_url, headers=headers, json=data)
email_text = "Fallback message"

if "choices" in resp.json():
    email_text = resp.json()["choices"][0]["message"]["content"]
    print("\nGenerated Email:\n", email_text)
else:
    print("\n⚠️ Error from Groq:", resp.json())

# Step 2: Send with SMTP instead of Resend
smtp_host = "smtp.gmail.com"       # Use your SMTP server
smtp_port = 587
smtp_username = os.getenv("SMTP_USERNAME")  # Your email address
smtp_password = os.getenv("SMTP_PASSWORD")    # Use an App Password or real password

msg = MIMEText(email_text)
msg["Subject"] = "Meeting Confirmation"
msg["From"] = "your-email-address-as-sender"
msg["To"] = "your-email-address-as-receiver"

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(msg["From"], [msg["To"]], msg.as_string())
