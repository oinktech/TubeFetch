from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from youtube_dl import YoutubeDL, DownloadError

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

class SearchForm(FlaskForm):  # Change here to FlaskForm
    query = StringField('YouTube Search', validators=[DataRequired()])
    submit = SubmitField('Search')

# Initialize search history
search_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm(request.form)
    videos = []

    if request.method == 'POST' and form.validate():
        query = form.query.data
        search_history.append(query)  # Save search query to history
        try:
            with YoutubeDL({'default_search': 'ytsearch', 'max_downloads': 5}) as ydl:
                result = ydl.extract_info(query, download=False)
                videos = result['entries']
        except Exception as e:
            flash(f'An error occurred: {str(e)}')

    return render_template('index.html', form=form, videos=videos, search_history=search_history)

@app.route('/download/<video_id>')
def download(video_id):
    ydl_opts = {
        'format': 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id])
        flash('Download successful!')
    except DownloadError:
        flash('Download failed. Please try again.')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10000)
