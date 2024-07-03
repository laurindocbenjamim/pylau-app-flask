from flask import Flask
import hvac

app = Flask(__name__)

# Initialize Vault client
client = hvac.Client(url='http://localhost:8200')
client.token = 'your_vault_token'

# Generate and store secret key
def generate_secret_key():
    secret_key = client.sys.generate_random_bytes(32)
    client.secrets.kv.v2.create_or_update_secret(
        path='myapp/secret_key',
        secret=dict(secret_key=secret_key)
    )

# Retrieve secret key
def get_secret_key():
    response = client.secrets.kv.v2.read_secret_version(path='myapp/secret_key')
    secret_key = response['data']['data']['secret_key']
    return secret_key

@app.route('/')
def index():
    secret_key = get_secret_key()
    return f'Secret Key: {secret_key}'

if __name__ == '__main__':
    app.run()