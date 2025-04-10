import streamlit as st
import pandas as pd
from utils import process_bulk_emails

st.set_page_config(page_title="Bulk Email Sender", layout="centered")
st.title("📧 Bulk Email Sender Tool")

st.sidebar.header("Sender Credentials")
sender_email = st.sidebar.text_input("Sender Email")
password = st.sidebar.text_input("App Password", type="password")

st.subheader("Email Content")
subject = st.text_input("Subject")
body = st.text_area("Body (Personalized with name)")

uploaded_file = st.file_uploader("Upload Excel or CSV file with 'Name' and 'Email' columns", type=["csv", "xlsx"])
pdf_file = st.file_uploader("Optional PDF Attachment", type=["pdf"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    recipients = list(zip(df['Name'], df['Email']))
    st.success(f"{len(recipients)} recipients loaded.")

if st.button("Send Emails"):
    if not all([sender_email, password, subject, body, uploaded_file]):
        st.error("Please fill all required fields.")
    else:
        pdf_bytes = pdf_file.read() if pdf_file else None
        pdf_name = pdf_file.name if pdf_file else None
        st.info("Sending emails...")
        process_bulk_emails(sender_email, password, recipients, subject, body, pdf_bytes, pdf_name)