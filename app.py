from flask import Flask, render_template, request, send_file
import sys
sys.path.insert(1, '/utils')
from utils import mash  

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/submit', methods=['GET','POST'])
def compute():
    if request.method == "POST":
        artist = request.form.get("artist")
        duration = int(request.form.get("duration"))
        videos = int(request.form.get("videos"))
        output_file = request.form.get("filename")
        mash_up = mash.Mashup(artist, videos)
        links = mash_up.scrape_links()
        print(links)
        audios = mash_up.download(links)
        print("done with audios")
        mash_up.mash(audios, duration, output_file)
        
    return send_file(output_file)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
