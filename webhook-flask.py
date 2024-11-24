from flask import Flask, request
import hashlib
import hmac
import json

app = Flask(__name__)

# Secret you choose when setting up the webhook subscription
secret = 'your_webhook_secret'

# Function to verify signature of the incoming request
def verify_signature(request):
    # Get the headers and payload of the incoming request
    signature = request.headers['Twitch-Eventsub-Message-Signature']
    timestamp = request.headers['Twitch-Eventsub-Message-Timestamp']
    body = request.get_data()

    # Create the signature to verify
    message = f"twitch-eventsub-message-id={request.headers['Twitch-Eventsub-Message-Id']}&twitch-eventsub-message-timestamp={timestamp}&{body.decode()}"
    computed_signature = 'sha256=' + hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(computed_signature, signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Verify the signature before processing the payload
    if not verify_signature(request):
        return 'Unauthorized', 403

    # Parse the incoming JSON payload
    payload = request.json

    # Handle the event (example: follow event)
    if 'event' in payload and payload['event']['type'] == 'follow':
        follower_name = payload['event']['user_name']
        print(f'New follower: {follower_name}')
        # Handle the follow event logic here

    return '', 200  # Respond to acknowledge receipt of the message

if __name__ == '__main__':
    app.run(port=5000)
