import RPi.GPIO as GPIO
import requests
import smtplib
import time
from email.mime.text import MIMEText

channel_id = "2161248"  # Replace with your ThingSpeak channel ID
read_api_key = "JFFXYEV41B1MMQPO"  # Replace with your ThingSpeak read API key
threshold = 100  # Replace with your desired moisture level threshold
light_pin = 17  # Replace with the GPIO pin connected to the light

mailgun_smtp_hostname = "smtp.mailgun.org"
mailgun_smtp_port = 587
mailgun_smtp_username = "postmaster@sandbox529d90819aa1491b997c8ab9ad6635d6.mailgun.org"
mailgun_smtp_password = "a6db42fd94fd01b5df2a0058c7d80b59-07ec2ba2-0db4edc9"
email_sender = "postmaster@sandbox529d90819aa1491b997c8ab9ad6635d6.mailgun.org"
email_recipient = "maiblefive201@gmail.com"  # Replace with the recipient's email address

GPIO.setmode(GPIO.BCM)
GPIO.setup(light_pin, GPIO.OUT)


def read_moisture_level():
    try:
        url = f"https://api.thingspeak.com/channels/{channel_id}/fields/1/last.json?api_key={read_api_key}"
        response = requests.get(url)
        data = response.json()
        if "field1" in data:
            return int(data["field1"])
    except Exception as e:
        print("Error:", e)
    return None

def send_email(subject, message):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = email_sender
        msg['To'] = email_recipient

        with smtplib.SMTP(mailgun_smtp_hostname, mailgun_smtp_port) as server:
            server.starttls()
            server.login(mailgun_smtp_username, mailgun_smtp_password)
            server.sendmail(email_sender, email_recipient, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

while True:
    moisture_level = read_moisture_level()
    if moisture_level is not None:
        print("Moisture level:", moisture_level)
        if moisture_level < threshold:
            GPIO.output(light_pin, GPIO.HIGH)  # Turn on the light
            time.sleep(2)  # Keep the light on for 2 seconds
            GPIO.output(light_pin, GPIO.LOW)  # Turn off the light
            subject = "Moisture Level Alert"
            message = "Moisture level is below the threshold!"
            send_email(subject, message)
    else:
        print("Failed to read moisture level.")

    time.sleep(5)  # Wait for 5 seconds before reading again
