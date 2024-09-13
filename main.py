from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import mss
from PIL import Image
import io
import pyautogui
import base64

app = Flask(__name__)
socketio = SocketIO(app)

# Capture the primary screen only
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
        
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=70)
        buffer.seek(0)
        return buffer.getvalue()

    return None

# Handle remote control actions with accurate scaling for touch control
def control_mouse_and_keyboard(x, y, action, screen_width, screen_height, sensitivity=1.0):
    desktop_width, desktop_height = pyautogui.size()
    
    # Adjust the touch sensitivity
    x = x * sensitivity
    y = y * sensitivity

    # Scale the phone's touch coordinates to match desktop resolution
    scaled_x = int(x * desktop_width / screen_width)
    scaled_y = int(y * desktop_height / screen_height)
    
    # Constrain the values to stay within screen bounds
    scaled_x = min(max(scaled_x, 0), desktop_width - 1)
    scaled_y = min(max(scaled_y, 0), desktop_height - 1)
    
    if action == 'move':
        pyautogui.moveTo(scaled_x, scaled_y)
    elif action == 'click':
        pyautogui.click(scaled_x, scaled_y)
    elif action == 'scroll':
        pyautogui.scroll(10)


@socketio.on('capture')
def handle_capture():
    img_data = capture_screen()
    if img_data:
        encoded_img = base64.b64encode(img_data).decode('utf-8')
        emit('screen_data', encoded_img)
    else:
        emit('screen_data', None)

@socketio.on('remote_control')
def handle_remote_control(data):
    x = data['x']
    y = data['y']
    action = data['action']
    screen_width = data['screen_width']
    screen_height = data['screen_height']
    
    control_mouse_and_keyboard(x, y, action, screen_width, screen_height)
@app.route('/')
def index():
    return render_template_string('''
        <html>
            <head>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: #e0f7fa;
                        color: #37474f;
                        overflow: hidden;
                    }
                    h1 {
                        text-align: center;
                        padding: 20px 0;
                        color: #00796b;
                        font-size: 2.5em;
                    }
                    .container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        flex-direction: column;
                        width: 100%;
                        height: 100vh;
                        padding: 0;
                        background-color: #ffffff;
                        overflow: hidden;
                    }
                    .left {
                        width: 100%;
                        height: 100%;
                        position: relative;
                    }
                    .left img {
                        width: 100%;
                        height: 100%;
                        object-fit: contain;
                        border-radius: 0;
                    }
                    #virtual-cursor {
                        position: absolute;
                        width: 20px;
                        height: 20px;
                        background: red;
                        border-radius: 50%;
                        pointer-events: none;
                    }
                </style>
            </head>
            <body>
                <h1>Live Desktop Connection</h1>
                <div class="container">
                    <div class="left">
                        <img id="screen" src="" alt="Shared Screen">
                        <div id="virtual-cursor"></div>
                    </div>
                    <label for="sensitivity">Touch Sensitivity:</label>
                    <input type="range" id="sensitivity" name="sensitivity" min="0.1" max="2.0" step="0.1" value="1.0">
                </div>
                <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
                <script>
                    const socket = io();
                    let sensitivity = 1.0;

                    document.getElementById('sensitivity').addEventListener('input', function(event) {
                        sensitivity = parseFloat(event.target.value);
                    });

                    function startCapture() {
                        setInterval(() => {
                            socket.emit('capture');
                        }, 1000); // Capture every second
                    }

                    socket.on('screen_data', function(imgData) {
                        if (imgData) {
                            const imgElement = document.getElementById('screen');
                            imgElement.src = 'data:image/jpeg;base64,' + imgData;
                        }
                    });

                    document.addEventListener('mousemove', function(event) {
                        const screen = document.getElementById('screen');
                        const screenRect = screen.getBoundingClientRect();
                        const screenWidth = screenRect.width;
                        const screenHeight = screenRect.height;
                        
                        const x = event.clientX - screenRect.left;
                        const y = event.clientY - screenRect.top;

                        // Update virtual cursor position
                        const cursor = document.getElementById('virtual-cursor');
                        cursor.style.left = x + 'px';
                        cursor.style.top = y + 'px';
                        
                        socket.emit('remote_control', { x: x, y: y, action: 'move', screen_width: screenWidth, screen_height: screenHeight, sensitivity: sensitivity });
                    });

                    document.addEventListener('click', function(event) {
                        const screen = document.getElementById('screen');
                        const screenRect = screen.getBoundingClientRect();
                        const screenWidth = screenRect.width;
                        const screenHeight = screenRect.height;

                        const x = event.clientX - screenRect.left;
                        const y = event.clientY - screenRect.top;
                        
                        socket.emit('remote_control', { x: x, y: y, action: 'click', screen_width: screenWidth, screen_height: screenHeight, sensitivity: sensitivity });
                    });

                    // Start capturing when the page loads
                    startCapture();
                </script>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
