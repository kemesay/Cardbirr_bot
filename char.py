import socketio

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Define a connection event handler
@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected")

# Define a custom event handler for checkout
@sio.event
def checkout(sid, data):
    print(f"Checkout event received from client {sid}")
    user_id = data.get('user_id')
    checkout_url = data.get('checkout_url')

    # Implement your actions with the checkout_url
    print(f"User {user_id} is checking out with URL: {checkout_url}")

# Define a disconnect event handler
@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected")

# Run the Socket.IO server
if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)
