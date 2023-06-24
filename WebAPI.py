import json

from flask import Flask, jsonify, request
from datetime import datetime
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.upload import Upload
from presentation_processor import PresentationProcessor

app = Flask(__name__)

db_file = "db/explainer.db"
engine = create_engine(f"sqlite:///{db_file}")
User.metadata.create_all(engine)
Upload.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

UPLOADS_FOLDER = "uploads"
OUTPUTS_FOLDER = "outputs"

presentation_processor = PresentationProcessor()

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    uid = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    original_filename = file.filename
    filename = f'{timestamp}_{original_filename}'

    file.save(os.path.join(UPLOADS_FOLDER, filename))

    if 'email' in request.form:
        email = request.form['email']
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email)
            session.add(user)
            session.commit()
    else:
        user = None

    upload = Upload(uid=uid, filename=original_filename, status='uploaded', user=user)
    session.add(upload)
    session.commit()

    return jsonify({'uid': uid}), 200

@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    upload = session.query(Upload).filter_by(uid=uid).first()
    if not upload:
        return jsonify({'error': 'Upload not found'}), 404

    data = {
        'status': upload.status,
        'filename': upload.filename,
        'upload_time': upload.upload_time,
        'finish_time': upload.finish_time,
        'user_id': upload.user_id
    }

    return jsonify(data), 200

@app.route('/history', methods=['GET'])
def history():
    uploads = session.query(Upload).all()
    data = []
    for upload in uploads:
        data.append({
            'uid': upload.uid,
            'filename': upload.filename,
            'status': upload.status,
            'upload_time': upload.upload_time,
            'finish_time': upload.finish_time,
            'user_id': upload.user_id
        })

    return jsonify(data), 200

@app.route('/process_presentation/<uid>', methods=['GET'])
async def process_presentation(uid):
    upload = session.query(Upload).filter_by(uid=uid).first()
    if not upload:
        return jsonify({'error': 'Upload not found'}), 404

    if upload.status == 'processed':
        return jsonify({'error': 'Presentation already processed'}), 400

    upload.status = 'processing'
    session.commit()

    presentation_path = os.path.join(UPLOADS_FOLDER, upload.filename)

    try:
        explanations = await presentation_processor.process_presentation(presentation_path)

        filename_without_extension = os.path.splitext(os.path.basename(upload.filename))[0]
        output_file_path = os.path.join(OUTPUTS_FOLDER, f"{filename_without_extension}.json")

        with open(output_file_path, 'w') as f:
            json.dump(explanations, f, indent=4)

        upload.status = 'processed'
        upload.finish_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session.commit()

        return jsonify({'message': 'Presentation processed successfully'}), 200
    except Exception as e:
        upload.status = 'failed'
        session.commit()
        return jsonify({'error': 'Failed to process presentation', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run()
