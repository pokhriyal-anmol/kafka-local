from confluent_kafka import Consumer, Producer
import json

c = Consumer({
    'bootstrap.servers':'kafka1:29092',
    'group.id':'nidd-group',
    'auto.offset.reset':'earliest'
})

p = Producer({'bootstrap.servers':'kafka1:29092'})
c.subscribe(['raw-events'])

while True:
    msg = c.poll(1)
    if msg is None:
        continue
    data = json.loads(msg.value().decode('utf-8'))

    mapped = {
        "asset_type": "pump",
        "asset_id": data["pump_id"],
        "metric": {
            "name": "vibration",
            "value": data["vibration"],
            "unit": "mm/s"
        },
        "timestamp": data["ts"],
        "nidd_version": "1.0",
        "raw": data
    }

    p.produce("nidd-mapped", json.dumps(mapped).encode("utf-8"))
    p.flush()
    print("Mapped:", mapped)
