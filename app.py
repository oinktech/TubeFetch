from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from pytube import Search
from math import ceil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class SearchForm(FlaskForm):
    keyword = StringField('關鍵字', validators=[DataRequired()])
    submit = SubmitField('搜尋')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        keyword = form.keyword.data
        flash(f'搜尋 "{keyword}" 的結果', 'success')
        return redirect(url_for('results', keyword=keyword))

    return render_template('index.html', form=form)

@app.route('/results')
def results():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    search = Search(keyword)
    videos = search.results
    total_videos = len(videos)
    total_pages = ceil(total_videos / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    videos = videos[start:end]

    return render_template('index.html', form=SearchForm(), videos=videos, page=page, total_pages=total_pages)

@app.route('/watch/<path:video_url>')
def watch(video_url):
    video_id = video_url.split('v=')[-1]
    return render_template('watch.html', video_id=video_id)

@app.route('/download/<int:video_index>', methods=['POST'])
def download(video_index):
    keyword = request.args.get('keyword')
    search = Search(keyword)
    video = search.results[video_index]
    stream = video.streams.get_highest_resolution()
    stream.download()
    flash('影片下載成功！', 'success')
    return redirect(url_for('results', keyword=keyword))

if __name__ == '__main__':
    app.run(debug=True,port=10000, host='0.0.0.0')
