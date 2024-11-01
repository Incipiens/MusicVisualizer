from flask import Flask, render_template, request
from flask_socketio import SocketIO
from pydub import AudioSegment
import numpy as np
import io

app = Flask(__name__)
socketio = SocketIO(app)

# Route for the main webpage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    audio = AudioSegment.from_file(file)
    samples = np.array(audio.get_array_of_samples())
    # Normalize samples to a standard JSON-friendly format
    samples = samples.astype(float) / np.max(np.abs(samples))  # Normalize to range -1.0 to 1.0
    
    # Emit audio data in chunks for visualization
    for chunk in np.array_split(samples, 100):  # Chunking for smoother visualization
        socketio.emit('audio_chunk', chunk.tolist())  # Send chunk to frontend as a list of floats
    return 'Audio data sent'

if __name__ == "__main__":
    socketio.run(app)