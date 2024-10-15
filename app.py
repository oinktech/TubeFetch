from flask import Flask, render_template, request, redirect, flash, url_for
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
    videos = []
    page = request.args.get('page', 1, type=int)
    per_page = 5  # 每頁顯示的影片數量

    if form.validate_on_submit():
        keyword = form.keyword.data
        flash(f'搜尋 "{keyword}" 的結果', 'success')
        search = Search(keyword)
        videos = search.results
        total_videos = len(videos)
        total_pages = ceil(total_videos / per_page)
        start = (page - 1) * per_page
        end = start + per_page
        videos = videos[start:end]
        return render_template('index.html', form=form, videos=videos, page=page, total_pages=total_pages)

    return render_template('index.html', form=form, videos=videos, page=page, total_pages=0)

@app.route('/watch/<video_id>')
def watch(video_id):
    return render_template('watch.html', video_id=video_id)

@app.route('/download/<video_id>', methods=['POST'])
def download(video_id):
    video = videos[int(video_id)]  # 根据 video_id 获取视频对象
    stream = video.streams.get_highest_resolution()
    stream.download()
    flash('影片下載成功！', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10000)
