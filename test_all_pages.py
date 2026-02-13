"""Quick test of all pages"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from app import app, db

app.config['TESTING'] = True

with app.test_client() as c:
    # Test public pages
    pages = ['/', '/login', '/register', '/faq', '/spare-parts', '/services', '/contact', '/about', '/book-car-service']
    for p in pages:
        try:
            r = c.get(p)
            status = 'OK' if r.status_code == 200 else f'GOT {r.status_code}'
            print(f"  GET {p}: {status}")
        except Exception as e:
            print(f"  GET {p}: ERROR - {e}")

    # Login as admin
    r = c.post('/login', data={'username': 'admin', 'password': 'Admin@123456'}, follow_redirects=False)
    print(f"\n  POST /login: {r.status_code} -> {r.headers.get('Location','')}")
    
    # Follow to admin dashboard
    r = c.post('/login', data={'username': 'admin', 'password': 'Admin@123456'}, follow_redirects=True)
    print(f"  Admin dashboard: {r.status_code}")
    if r.status_code != 200:
        data = r.data.decode()
        if 'TemplateNotFound' in data:
            import re
            m = re.search(r'TemplateNotFound: (.+?)[\n<]', data)
            if m: print(f"    Missing template: {m.group(1)}")
        elif 'BuildError' in data:
            import re
            m = re.search(r'BuildError[^<]+', data)
            if m: print(f"    {m.group(0)[:200]}")
        else:
            print(f"    Response: {data[:300]}")

    # Test admin sub-pages
    admin_pages = ['/admin', '/admin/customers', '/admin/service-bookings', '/admin/analytics', '/admin/parts', '/admin/add_customer', '/admin/add_technician']
    for p in admin_pages:
        try:
            r = c.get(p)
            status = 'OK' if r.status_code == 200 else f'GOT {r.status_code}'
            print(f"  GET {p}: {status}")
            if r.status_code == 500:
                data = r.data.decode()
                if 'TemplateNotFound' in data:
                    import re
                    m = re.search(r'TemplateNotFound: (.+?)[\n<]', data)
                    if m: print(f"    Missing: {m.group(1)}")
                elif 'BuildError' in data:
                    import re
                    m = re.search(r"BuildError[^<]+", data)
                    if m: print(f"    {m.group(0)[:200]}")
        except Exception as e:
            print(f"  GET {p}: ERROR - {e}")

print("\nDone!")
