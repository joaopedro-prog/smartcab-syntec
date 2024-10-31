import traceback
from flask import Flask, render_template, Response, jsonify
import db_connect
from flask_cors import CORS
import camera_detection
import logic_control

# ============================= Server requests =============================
app = Flask(__name__)
CORS(app)  # Permite solicitações de todas as origens

@app.route('/')
def index():
    return render_template('gui/index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera_detection.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/gate_state')
def gate_state():
    response = jsonify({'locked_gate': logic_control.locked_gate})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/user_info')
def user_info():
    response = jsonify(logic_control.user)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/tools_info')
def tools_info():
    tools_info = db_connect.db.query(f'SELECT tools.name AS ferramenta, users.name AS pessoa FROM tools JOIN users ON tools.location_id = users.id WHERE tools.active = 1;')
    response = jsonify(tools_info)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
