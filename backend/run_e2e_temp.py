import requests
import time

base = 'http://localhost:8000'
email = f'e2e.test+{int(time.time())}@example.com'
password = 'shortpass'

print('Registering:', email)
reg = {'name': 'E2E Test', 'email': email, 'password': password}
try:
    r = requests.post(f'{base}/api/auth/register', json=reg, timeout=10)
    print('Register status:', r.status_code)
    print(r.text)
except Exception as e:
    print('Register error:', repr(e))

try:
    r2 = requests.post(f'{base}/api/auth/login', data={'username': email, 'password': password}, timeout=10)
    print('Login status:', r2.status_code)
    print(r2.text)
    if r2.status_code == 200:
        token = r2.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        r3 = requests.get(f'{base}/api/auth/me', headers=headers, timeout=10)
        print('/api/auth/me status:', r3.status_code)
        print(r3.text)
    else:
        print('Login failed; not calling /me')
except Exception as e:
    print('Login error:', repr(e))
