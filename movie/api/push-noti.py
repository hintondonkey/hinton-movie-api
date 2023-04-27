import firebase_admin
from firebase_admin import credentials, messaging

creds = credentials.Certificate('cert.json')
app = firebase_admin.initialize_app(creds)
message = messaging.Message(
    notification= messaging.Notification(title="Hello Flutter", body="Flutter Message from firebase"),
    topic="demo",
)
response = messaging.send(message)
print('Successfully sent message:', response)
