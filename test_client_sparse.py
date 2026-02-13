from app import app

with app.test_client() as client:
    response = client.get('/spare-parts')
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('✓ Test client returned 200!')
        print(f'Content length: {len(response.get_data(as_text=True))} bytes')
    else:
        print(f'Error: {response.status_code}')
        print(response.get_data(as_text=True)[:500])
