"""
email_service.py
================
Email service for sending OTP codes and confirmations via SMTP (Gmail).

Configuration:
    SMTP_USER: Gmail address
    SMTP_PASSWORD: Gmail app password (https://myaccount.google.com/apppasswords)

Usage:
    from email_service import send_otp_email, send_confirmation_email
    send_otp_email("user@example.com", "123456")
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration from environment variables
SMTP_USER = os.getenv("SMTP_USER", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(recipient: str, subject: str, html_content: str) -> bool:
    """Send email via SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = recipient

        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, recipient, msg.as_string())

        print(f"Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"ERROR sending email to {recipient}: {e}")
        return False


def send_otp_email(recipient: str, code: str, purpose: str = "register") -> bool:
    """Send OTP code via email."""

    if purpose == "register":
        subject = "ShopVN - Verify Your Email (OTP)"
        message = "account registration"
    elif purpose == "verify_card":
        subject = "ShopVN - Verify Payment Card (OTP)"
        message = "payment card verification"
    elif purpose == "confirm_transaction":
        subject = "ShopVN - Confirm Transaction (OTP)"
        message = "transaction confirmation"
    else:
        subject = "ShopVN - Verify Identity (OTP)"
        message = "identity verification"

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>ShopVN Verification</h2>
            <p>Hello,</p>
            <p>You are requesting {message} on ShopVN. Please use the following code:</p>

            <div style="background-color: #f5f5f5; padding: 20px; margin: 20px 0; text-align: center; border-radius: 5px;">
                <p style="font-size: 24px; letter-spacing: 5px; font-weight: bold; color: #007bff;">
                    {code}
                </p>
            </div>

            <p><strong>This code expires in 5 minutes.</strong></p>
            <p>If you did not request this code, please ignore this email.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                ShopVN | E-Commerce Platform<br>
                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </body>
    </html>
    """

    return send_email(recipient, subject, html)


def send_confirmation_email(recipient: str, name: str = "User") -> bool:
    """Send account confirmation email."""
    subject = "ShopVN - Welcome!"
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Welcome to ShopVN!</h2>
            <p>Hello {name},</p>
            <p>Your account has been successfully created and verified.</p>

            <p>You can now:</p>
            <ul>
                <li>Browse our catalog of products</li>
                <li>Add items to your cart and checkout</li>
                <li>Track your orders</li>
                <li>Leave reviews on products</li>
            </ul>

            <p style="margin-top: 20px;">
                <a href="http://localhost:3002" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Start Shopping
                </a>
            </p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                ShopVN | E-Commerce Platform<br>
                If you have any questions, please contact us.
            </p>
        </div>
    </body>
    </html>
    """
    return send_email(recipient, subject, html)


def send_order_confirmation_email(recipient: str, order_id: str, amount: float) -> bool:
    """Send order confirmation email."""
    subject = f"ShopVN - Order Confirmed (#{order_id[:8]})"
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Order Confirmed!</h2>
            <p>Your order has been received.</p>

            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px;">
                <p><strong>Order ID:</strong> {order_id[:8]}</p>
                <p><strong>Amount:</strong> GBP {amount:.2f}</p>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>

            <p>You can track your order in your account dashboard.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="color: #666; font-size: 12px;">
                ShopVN | E-Commerce Platform
            </p>
        </div>
    </body>
    </html>
    """
    return send_email(recipient, subject, html)


if __name__ == "__main__":
    # Test email sending
    print("Testing email service...")
    print(f"SMTP User: {SMTP_USER}")
    print(f"SMTP Host: {SMTP_HOST}:{SMTP_PORT}")
    print("Note: Set SMTP_PASSWORD environment variable for testing")
