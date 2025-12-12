import redis
import json
import time

redis_client = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

print("📨 Worker started. Listening for jobs...")

while True:
    job = redis_client.brpop("email_queue")
    data = json.loads(job[1])

    print("\n📬 New Email Job Received:")
    print(json.dumps(data, indent=2))

    # Simulate sending email
    time.sleep(1)
    print("✅ Email processed.\n")
