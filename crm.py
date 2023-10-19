from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = '3umZ9-UQCRgKu2-sEBe3gS55RrF8bqbcBlwvLuSlQ_8'
CLIENT_SECRET = '36lSZxcIngXKXOM3Dn0dxH2hqPbk8zKKDa42gEp0eVg'
REDIRECT_URI = 'http://134.195.159.15:3000/callback/whop'

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    webhook_data = request.json

    if webhook_data.get('action') == "membership.went_valid":
        extract_relevant_data(webhook_data['data'])

    return jsonify({"message": "Received"}), 200

def extract_relevant_data(data):
    plan_id = data['plan']['id']
    product_id = data['plan']['product']['id']
    product_created_at = data['plan']['product']['created_at']
    product_name = data['plan']['product']['name']
    custom_fields_responses = data['custom_fields_responses']
    discord = data.get('discord')
    email = data['email']

    print(f"Plan ID: {plan_id}")
    print(f"Product ID: {product_id}")
    print(f"Product Created At: {product_created_at}")
    print(f"Product Name: {product_name}")
    print(f"Custom Fields Responses: {custom_fields_responses}")
    print(f"Discord: {discord}")
    print(f"Email: {email}")

@app.route('/callback/whop')
def whop_callback():
    code = request.args.get('code')

    token_data = get_auth_token(code)
    access_token = token_data.get('access_token')

    access_data = check_access('YOUR_ACCESS_PASS_ID', access_token)
    has_access = access_data.get('has_access')

    if has_access:
        pass
    else:
        pass

    return jsonify(access_data)

def get_auth_token(code):
    response = requests.post('https://api.whop.com/api/v2/oauth/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
    })

    return response.json()

def check_access(access_pass_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.whop.com/api/v2/me/has_access/{access_pass_id}', headers=headers)

    return response.json()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=3000)



