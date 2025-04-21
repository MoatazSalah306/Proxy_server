from flask import Flask, request, Response
import requests # MS- to can make http/s requests
import time # MS- for cache tracking


# ------------------------------- MS- Basic Flask server -------------------------------

app = Flask(__name__)
cache = {}  # MS- Simple in-memory cache


CACHE_EXPIRY = 40  # MS- Cache time in seconds (e.g. 40 seconds)
BANDWIDTH_LIMIT= 100 * 1024 # KB


# ------------------------------- MS- Content Filtering Rules -------------------------------

BLOCKED_DOMAINS = ['google.com', 'youtube.com']
BLOCKED_KEYWORDS = ['tracking', 'spyware']



def generate_throttled_response(content: bytes):
    chunk_size = BANDWIDTH_LIMIT  # 50KB
    for i in range(0, len(content), chunk_size):
        yield content[i:i + chunk_size]
        time.sleep(1)  # MS- Wait 1 second before sending the next chunk


# ------------------------------- MS- Proxy Route -------------------------------

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')

    if not target_url:
        return "Please provide a URL using ?url={https://facebook.com}", 400 # MS- Just An Error Message


    for blocked in BLOCKED_DOMAINS:
        if blocked in target_url:
            return f"❌ Access to {blocked} is blocked by the proxy.", 403

    # MS- Check if the response is already in cache and still valid
    if target_url in cache:
        content, timestamp = cache[target_url]
        if time.time() - timestamp < CACHE_EXPIRY: # MS- minus the now time (seconds from unix timestamp) and cache timestamp , if < ok else not ok
            print("🧠  ------------------------ Serving from cache ------------------------ 🧠")
            return Response(generate_throttled_response(content), content_type="text/html")
        
    try:
        print("🌐 ------------------------ Fetching from web ------------------------ 🌐")
        response = requests.get(target_url)
        content = response.content
        content_type = response.headers.get('Content-Type', 'text/html')

         # MS- Check content filtering before saving or sending
        for keyword in BLOCKED_KEYWORDS:
            if keyword.encode() in content:
                return f"❌ Blocked due to filtered content: '{keyword}'", 403


        cache[target_url] = (content, time.time())  # MS- Store in cache with current time
        return Response(generate_throttled_response(content), content_type=content_type)
    
    except Exception as e:
        return f"Error fetching {target_url}: {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5050, debug=True)




# https://www.postman.com -- contains the word 'tracking' --