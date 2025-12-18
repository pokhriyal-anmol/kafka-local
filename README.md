

## 1. Go to the directory containing the file

```bash
cd path/to/your/project
```

Verify the file exists:

```bash
ls
```

You should see:

```text
docker-compose.full-demo.yml
```

---

## 2. Start the full demo stack

Use **Docker Compose v2 syntax** (recommended):

```bash
docker compose -f docker-compose.full-demo.yml up -d
```

What this does:

* `-f` → explicitly tells Docker which compose file to use
* `up` → creates + starts containers
* `-d` → detached mode (runs in background)

---

## 3. Verify everything is running

```bash
docker compose -f docker-compose.full-demo.yml ps
```

You should see all services in **Running** state.

---

## 4. View logs (important for Kafka)

If something doesn’t start:

```bash
docker compose -f docker-compose.full-demo.yml logs -f
```

To check a specific service:

```bash
docker compose -f docker-compose.full-demo.yml logs kafka
```

(or whatever the service name is)

---

## 5. Access common demo components (if included)

Typical URLs in your full demo:

* Kafka UI

  ```
  http://localhost:8080
  ```
* Any API / demo service

  ```
  http://localhost:<port>
  ```

(Exact ports depend on your YAML, but this is usually correct for your setup.)

---

## 6. Stop the demo cleanly

When you’re done:

```bash
docker compose -f docker-compose.full-demo.yml down
```

To also remove volumes (⚠ deletes Kafka data):

```bash
docker compose -f docker-compose.full-demo.yml down -v
```

---

## Common mistakes (check this if it fails)

### 1. Using old syntax

❌ Don’t use:

```bash
docker-compose up
```

✅ Use:

```bash
docker compose up
```

---

### 2. Port already in use

If Kafka UI or Kafka won’t start:

```bash
lsof -i :8080
```

Kill the process or change the port in the YAML.

---

### 3. Apple Silicon warning

If images fail on M1/M2:

Add this to affected services:

```yaml
platform: linux/amd64
```

---

* Add **healthchecks** so Kafka waits for Zookeeper
* Add a **producer container** that auto-publishes demo events every second
