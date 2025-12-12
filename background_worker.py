import redis
import json
import time

redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

def send_email(email, subject, message):
    print("\n📧 Sending Email...")
    print(f"To: {email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print("✅ Email sent!\n")

def process_message(message):
    data = json.loads(message)

    email = data.get("email")
    subject = data.get("subject", "No Subject")
    message_text = data.get("message", "No Message")

    send_email(email, subject, message_text)

def worker_loop():
    print("📌 Background Worker Started. Waiting for messages...\n")
    while True:
        try:
            queue_name, message = redis_client.blpop("email_queue")
            print("🔔 New message received!")
            process_message(message)
        except Exception as e:
            print(f"❌ Worker error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    worker_loop()
