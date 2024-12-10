from flask_cors import CORS
from flask_sockets import Sockets, SocketMiddleware
from flask import Flask, request, Response, jsonify
from hand_detection import detect_hand_gestures

app = Flask(__name__)
sockets = Sockets(app)
CORS(app)

@app.route('/GestureDetector', methods=['POST', 'GET'])
def predictvideodata():
  # detect_hand_gestures()
  return {"data": 'data'}
  
if __name__ == '__main__':
  app.run(debug=True)
