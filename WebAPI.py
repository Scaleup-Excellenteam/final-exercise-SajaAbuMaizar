from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import os
import glob

app = Flask(__name__)

UPLOADS_FOLDER = 'uploads'
OUTPUTS_FOLDER = 'outputs'


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Generate UID and timestamp
    uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Create a new filename
    original_filename = file.filename
    filename = f'{original_filename}_{timestamp}_{uid}'

    # Save the file
    file.save(os.path.join(UPLOADS_FOLDER, filename))

    return jsonify({'uid': uid}), 200


@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    # Check if the file exists
    files = glob.glob(f'{UPLOADS_FOLDER}/*_{uid}')
    if not files:
        return jsonify({'status': 'not found'}), 404

    # Get the latest file with the given UID
    latest_file = max(files, key=os.path.getctime)
    filename = os.path.basename(latest_file)
    timestamp = filename.split('_')[1]

    # Extract only the filename without the timestamp and UID
    file_parts = filename.split('_')
    if len(file_parts) > 2:
        extracted_filename = '_'.join(file_parts[:-2])
    else:
        extracted_filename = file_parts[0]

    # Remove the file extension
    extracted_filename1 = os.path.splitext(extracted_filename)[0]
    # Check if the output file exists
    output_file = f'{extracted_filename1}.json'
    if os.path.exists(os.path.join(OUTPUTS_FOLDER, output_file)):
        # Read the explanation from the output file
        with open(os.path.join(OUTPUTS_FOLDER, output_file), 'r') as f:
            explanation = f.read()
        return jsonify({
            'status': 'done',
            'filename': extracted_filename,
            'timestamp': timestamp,
            'explanation': explanation
        }), 200
    else:
        return jsonify({
            'status': 'pending',
            'filename': extracted_filename,
            'timestamp': timestamp,
            'explanation': None
        }), 200


if __name__ == '__main__':
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)
    app.run()
