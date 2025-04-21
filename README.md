# 🧾 Web Proxy Server – Full Technical Documentation

## 📘 Project Title:
**Python-Based Web Proxy Server with Caching, Filtering, Throttling, and Persistence**

## 🧩 Purpose

This project is a custom-built HTTP/HTTPS proxy server using Python and Flask. It handles:
- Forwarding web requests
- Caching pages for performance
- Blocking/filtering specific sites
- Throttling bandwidth for testing slow networks


## 🛠️ Used Technologies & Libraries

| Library        | Purpose                                                                 |
|----------------|-------------------------------------------------------------------------|
| `Flask`        | Web framework to expose the proxy server via HTTP routes                |
| `requests`     | To fetch external web content (since Flask doesn’t handle that natively)|
| `time`         | Used for cache expiration and throttling delays                         |


## 📂 File Structure

```
proxy-server/
│
├── proxy_server.py     # Main server implementation
└── README.md           # This documentation
```

## 🚀 How to Run

### 1. Install dependencies:
```bash
pip install flask requests
```

### 2. Run the server:
```bash
python proxy_server.py
```

### 3. Use it like this:
```
http://127.0.0.1:5050/proxy?url=https://example.com
```

## 🧠 Key Features & Concepts

### 1. ✅ Request Forwarding

Handles client requests, forwards them to the destination website, and returns the result.

```python
target_url = request.args.get('url')
response = requests.get(target_url)
return Response(response.content, content_type=response.headers.get('Content-Type'))
```

### 2. 🔁 In-Memory Caching

Stores website responses to serve repeated requests faster.

```python
cache = {}
CACHE_EXPIRY = 40  # seconds
```

```python
if time.time() - timestamp < CACHE_EXPIRY:
    return Response(content, content_type="text/html")
```


### 3. 🚫 Content Filtering

Blocks unwanted websites based on keywords.

```python
BLOCKED_KEYWORDS = ["facebook", "porn", "badsite"]

for keyword in BLOCKED_KEYWORDS:
    if keyword in target_url.lower():
        return "Access to this site is blocked by proxy.", 403
```

### 4. 🐢 Bandwidth Throttling

Slows down the response to simulate low-speed internet.

```python
BANDWIDTH_LIMIT = 50 * 1024  # 50KB/sec

def generate_throttled_response(content: bytes):
    for i in range(0, len(content), BANDWIDTH_LIMIT):
        yield content[i:i + BANDWIDTH_LIMIT]
        time.sleep(1)
```

Used like:
```python
return Response(generate_throttled_response(content), content_type=...)
```

### 5. 🔁 Generator Explanation

Generators (with `yield`) let us stream data chunk-by-chunk instead of all at once, useful for throttling.

## 🔐 Future Ideas

- Support POST requests
- Authenticated proxy
- Redis-based caching
- Admin dashboard
- Logging & analytics

## 👨‍💻 Credits

- Developer: Moataz salah ezzat!

