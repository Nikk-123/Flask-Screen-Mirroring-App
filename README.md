
---

# Flask Screen Mirroring App

![Live Desktop Connection](https://img.shields.io/badge/Flask-v2.0-blue) ![SocketIO](https://img.shields.io/badge/SocketIO-v4.0-orange)

A Flask-based screen mirroring application that captures your desktop screen and displays it in real-time on a webpage. The app also allows remote control of the desktop using mouse and keyboard input, with enhancements for touch control and virtual cursor visualization.

## 🎉 Features
- **Live Desktop Screen Sharing**: Real-time capture of your desktop screen.
- **Remote Mouse and Keyboard Control**: Control your desktop remotely with mouse movements and clicks.
- **Touch Control Support**: Scaled touch coordinates to match desktop resolution, with adjustable sensitivity.
- **Virtual Mouse Cursor**: Visual representation of touch or mouse movements on the screen.
- **Smooth Performance**: Optimized screen capture with `mss` and `Pillow` for performance.

## 🛠️ Technologies Used
- **Flask**: Backend framework to manage the web server and communication.
- **Flask-SocketIO**: Provides real-time communication between the client and the server.
- **mss**: Efficient screen capture of the desktop.
- **Pillow (PIL)**: Image processing library for converting screenshots to the required format.
- **PyAutoGUI**: Automate mouse and keyboard actions on the desktop.

## 💻 How It Works
1. **Screen Capture**: The application captures the primary monitor and encodes the image as a JPEG.
2. **Real-time Streaming**: The Flask server sends the screen capture as base64-encoded data to the client via SocketIO.
3. **Remote Control**: The client sends touch or mouse data, which is converted to corresponding desktop actions.
4. **Virtual Cursor**: A virtual cursor is displayed on the client to indicate touch or mouse position.
5. **Touch Sensitivity**: Users can adjust the sensitivity of touch controls.

## 🚀 Getting Started

### Prerequisites
- **Python 3.7+**
- **Flask**
- **Flask-SocketIO**
- **mss**
- **Pillow**
- **PyAutoGUI**

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Nikk-123/Flask-Screen-Mirroring-App.git
   cd Flask-Screen-Mirroring-App
   ```

2. Install the necessary dependencies:

   ```bash
   pip install Flask Flask-SocketIO mss Pillow pyautogui
   ```

3. Run the application:

   ```bash
   python main.py
   ```

4. Open your browser and navigate to `http://localhost:5000` to start using the app.

## 📚 Usage

- **Live Screen Sharing**: The app captures your desktop every second and streams it to the connected client.
- **Remote Control**: Move and click on your desktop using the webpage.
- **Virtual Cursor**: View and interact with a virtual cursor that represents touch or mouse movements.
- **Touch Input Scaling**: Works seamlessly across devices with different screen resolutions and includes sensitivity adjustment.

## 📱 Mobile Compatibility

The application supports mobile touch input, scaling it to the desktop screen size for precise control. The touch sensitivity can be adjusted using a slider on the client side.

## 📝 To Do
- [ ] Add support for multi-monitor screen capture.
- [ ] Enhance performance for lower latency.
- [ ] Add keyboard input for more comprehensive remote control.
- [ ] Implement additional touch gestures and calibration options.
- [ ] Improve touch sensitivity to enhance mobile control accuracy.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Nikk-123/Flask-Screen-Mirroring-App/issues) for any bugs or enhancements.

---
