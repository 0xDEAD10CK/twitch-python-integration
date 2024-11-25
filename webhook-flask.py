from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to handle EventSub notifications
@app.route('/eventsub/', methods=['POST'])
def eventsub():
    # Get the event data from Twitch
    event_data = request.json
    print("Received EventSub data:", event_data)
    
    # You can process the event data here (e.g., for subscription or follow events)
    
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('server.cert', 'server.key'))  # Using SSL for HTTPS (temporary)


#, ssl_context=('server.cert', 'server.key')