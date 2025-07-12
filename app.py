from flask import Flask, render_template, request, send_file
import os
import yt_dlp
from uuid import uuid4

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        filename = f"{uuid4()}.mp3"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filepath,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            return f"❌ Error: {e}"

    return render_template('index.html')
