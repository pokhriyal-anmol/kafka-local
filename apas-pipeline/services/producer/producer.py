import time, random, json
from confluent_kafka import Producer

p = Producer({'bootstrap.servers': 'kafka1:29092'})

def generate(base, variance):
    return round(base + random.uniform(-variance, variance), 2)

while True:
    payload = {
        "pump_id": "P-19",
        "vibration": generate(70, 20),
        "temperature": generate(80, 5),
        "pressure": generate(4.2, 0.3),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    p.produce("raw-events", json.dumps(payload).encode("utf-8"))
    p.flush()
    print("Sent:", payload)
    time.sleep(1)
