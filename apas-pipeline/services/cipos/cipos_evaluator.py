from confluent_kafka import Consumer, Producer
import json

c = Consumer({
    'bootstrap.servers':'kafka1:29092',
    'group.id':'cip-group',
    'auto.offset.reset':'earliest'
})
p = Producer({'bootstrap.servers':'kafka1:29092'})
c.subscribe(['provenance-created'])

while True:
    msg = c.poll(1)
    if msg is None:
        continue

    data = json.loads(msg.value().decode('utf-8'))
    v = data["event"]["metric"]["value"]

    status = "violation" if v > 85 else "compliant"
    out = {
        "asset_id": data["asset_id"],
        "status": status,
        "rule": "VibrationThreshold85",
        "ts": data["timestamp"]
    }

    p.produce("cipos-evaluated", json.dumps(out).encode('utf-8'))
    p.flush()
    print("CIPOS:", out)
