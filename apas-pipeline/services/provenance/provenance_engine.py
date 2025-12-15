import json, hashlib, requests
from confluent_kafka import Consumer, Producer

IPFS_API = "http://ipfs:5001/api/v0"

def ipfs_add_json(obj):
    # Convert python dict → JSON bytes
    data = json.dumps(obj).encode("utf-8")

    # IPFS expects multipart/form-data
    response = requests.post(
        f"{IPFS_API}/add",
        files={"file": ("data.json", data)},
        params={"pin": "true"}
    )
    response.raise_for_status()
    return response.json()["Hash"]

def ipfs_get_json(cid):
    response = requests.post(f"{IPFS_API}/cat", params={"arg": cid})
    response.raise_for_status()
    return json.loads(response.text)

# Kafka consumer
c = Consumer({
    'bootstrap.servers':'kafka1:29092',
    'group.id':'prov-group',
    'auto.offset.reset':'earliest'
})

p = Producer({'bootstrap.servers':'kafka1:29092'})
c.subscribe(['nidd-mapped'])

while True:
    msg = c.poll(1)
    if msg is None:
        continue

    data = json.loads(msg.value().decode('utf-8'))

    # canonical hash
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    sha = hashlib.sha256(encoded).hexdigest()

    # provenance card
    card = {
        "event": data,
        "hash": sha
    }

    cid = ipfs_add_json(card)

    record = {
        "asset_id": data["asset_id"],
        "event_type": "vibration-spike" if data["metric"]["value"] > 85 else "normal",
        "provenance_cid": cid,
        "hash": sha,
        "timestamp": data["timestamp"],
        "event": data
    }

    p.produce("provenance-created", json.dumps(record).encode("utf-8"))
    p.flush()
    print("Provenance Created:", record)
