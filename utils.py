import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from concurrent.futures import ThreadPoolExecutor
import streamlit as st

def send_email(sender_email, password, recipient_email, subject, body, name=None, pdf_bytes=None, pdf_name=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if name:
            body = f"Dear {name},\n\n" + body

        msg.attach(MIMEText(body, 'plain'))

        if pdf_bytes and pdf_name:
            part = MIMEApplication(pdf_bytes, _subtype="pdf")
            part.add_header('Content-Disposition', 'attachment', filename=pdf_name)
            msg.attach(part)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return f"✅ Mail sent to {recipient_email}"
    except Exception as e:
        return f"❌ Failed for {recipient_email}: {e}"

def process_bulk_emails(sender_email, password, recipients, subject, body, pdf_bytes=None, pdf_name=None):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for name, email in recipients:
            futures.append(executor.submit(send_email, sender_email, password, email, subject, body, name, pdf_bytes, pdf_name))

        for future in futures:
            result = future.result()
            st.write(result)
            results.append(result)
    return results