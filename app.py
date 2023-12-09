"""sms 2 way"""

import os
from flask import Flask, request, jsonify
from infobip_channels.sms.channel import SMSChannel
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

# Access the variables using os.getenv
BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')    # obtained from
                                  # https://portal.infobip.com/dev/api-keys


@app.route('/sms/receive', methods=['POST'])
def receive_sms():
    """get realtime sms from web hook"""

    data = request.json

    # Process your data here
    print("Received data:", data)

    # You can perform various operations based on the data received
    # For example, parsing the message, sending a response, etc.

    return jsonify({'status': 'success', 'message': 'Data received'})

@app.route('/sms/send', methods=['POST'])
def send_sms():
    """send sms api 
       accept request body:
       {"message": "<message to send via sms>", "recipient": "<receive-number>"}
    """
    data = request.json
    message_to_send:str = data.get('message')
    recipient = data.get('recipient')

    if not message_to_send:
        return jsonify({'status': 'error', 'message': 'No message provided'}), 400

    # Here you would integrate with your SMS service to send the message
    print("Sending SMS:", message_to_send)

    channel = SMSChannel.from_auth_params(
        {
            "base_url": BASE_URL,
            "api_key": API_KEY,
        }
    )

     # Send a message with the desired fields.
    sms_response = channel.send_sms_message(
        {
            "messages": [
                {
                    "destinations": [{"to": recipient}],
                    "text": message_to_send,
                }
            ]
        }
    )

    # Get delivery reports for the message. It may take a few seconds show the just-sent message.
    query_parameters = {"limit": 10}
    delivery_reports = channel.get_outbound_sms_delivery_reports(query_parameters)

    # See the delivery reports.
    print(delivery_reports)

    # Simulate a successful send
    return jsonify({'status': 'success', 'message': 'SMS sent successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
