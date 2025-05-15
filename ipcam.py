from flask import Flask, Response
import cv2
import tkinter as tk
from tkinter import messagebox
import threading
import socket
import os

# ----------------------------
# Flask App Setup
# ----------------------------
flask_app = Flask(__name__)
camera = cv2.VideoCapture(0)
server_running = False

def generate_frames():
    while server_running:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@flask_app.route('/')
def index():
    return "<h2>IP Camera Stream</h2><p>Visit <a href='/video_feed'>/video_feed</a> to see the live feed.</p>"

@flask_app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_server():
    try:
        print(">>> Flask server starting...")
        flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"!!! Flask server failed: {e}")

# ----------------------------
# Utility Functions
# ----------------------------
def get_real_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to fetch IP"

def write_info_files():
    ip = get_real_ip()
    shared_dir = "/srv/Recive"
    os.makedirs(shared_dir, exist_ok=True)

    # BAT file for Windows
    bat_path = os.path.join(shared_dir, "OpenCameraFeed.bat")
    with open(bat_path, "w") as f:
        f.write(f"@echo off\nstart http://{ip}:5000/video_feed\n")

    # Text info file
    txt_path = os.path.join(shared_dir, "server_ip.txt")
    with open(txt_path, "w") as f:
        f.write(f"Stream Server IP: http://{ip}:5000\n")

# ----------------------------
# Tkinter GUI
# ----------------------------
class ServerControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi IP Camera")
        self.root.geometry("300x250")

        self.server_thread = None
        self.video_thread = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="IP Camera Control", font=("Arial", 16)).pack(pady=10)

        self.ip_label = tk.Label(self.root, text=f"IP: {get_real_ip()}:5000", font=("Arial", 12))
        self.ip_label.pack(pady=10)

        tk.Button(self.root, text="Start Server", command=self.start_server,
                  bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="Stop Server", command=self.stop_server,
                  bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

    def start_server(self):
        global server_running
        if not server_running:
            server_running = True
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()

            write_info_files()

            self.video_thread = threading.Thread(target=self.show_video, daemon=True)
            self.video_thread.start()

            messagebox.showinfo("Server Started", f"Server is running at http://{get_real_ip()}:5000")

    def stop_server(self):
        global server_running
        if server_running:
            server_running = False
            camera.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Server Stopped", "The server has been stopped.")
            self.root.quit()

    def show_video(self):
        while server_running:
            success, frame = camera.read()
            if not success:
                break
            cv2.imshow("Live Camera Feed (press 'q' to hide)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

# ----------------------------
# Main Execution
# ----------------------------
if __name__ == '__main__':
    root = tk.Tk()
    gui = ServerControlApp(root)
    root.mainloop()
