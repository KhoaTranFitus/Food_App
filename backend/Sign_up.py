from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
import smtplib
from email.mime.text import MIMEText
import random

app = Flask(__name__)

cred = credentials.Certificate("food-app-d0127-firebase-adminsdk-fbsvc-fb06070e09.json")
firebase_admin.initialize_app(cred)

# --- gửi mail ---
def send_verification_email(to_email, code):
    sender = "luminkhoi@gmail.com"
    app_password = "ztimyvmgtrdfrcan"  # thay bằng app password thật
    msg = MIMEText(f"Your verification code: {code}")
    msg['Subject'] = 'Verify Food App Register'
    msg['From'] = sender
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(msg)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        user = auth.create_user(email=email, password=password)
        code = random.randint(100000, 999999)
        send_verification_email(email, code)
        return jsonify({"message": "User created successfully. Check your email for verification code."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)