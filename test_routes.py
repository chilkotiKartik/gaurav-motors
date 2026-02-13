"""Quick test to check all major routes for 500 errors"""
import requests

BASE = "http://127.0.0.1:5000"
routes = [
    '/', '/services', '/book-car-service', '/contact',
    '/spare-parts', '/login', '/faq', '/about',
    '/register', '/accessories',
]

print("Testing routes...")
for r in routes:
    try:
        resp = requests.get(BASE + r, allow_redirects=False, timeout=5)
        status = resp.status_code
        ok = "OK" if status < 500 else "FAIL"
        print(f"  {ok}  {status}  {r}")
    except Exception as e:
        print(f"  ERR  ---  {r}  ({e})")

print("\nDone!")
