import requests

try:
    r = requests.get('http://127.0.0.1:5000/spare-parts', timeout=5)
    print(f'Status Code: {r.status_code}')
    print(f'\nResponse Body:')
    print(r.text)
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
