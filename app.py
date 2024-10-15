from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 請更換為安全的密鑰

# 設定日誌記錄
logging.basicConfig(level=logging.INFO)

class SearchForm(FlaskForm):
    keyword = StringField('請輸入 YouTube 關鍵字:', validators=[DataRequired()])
    submit = SubmitField('搜索')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    video_url = None
    if form.validate_on_submit():
        keyword = form.keyword.data
        video_url = search_youtube(keyword)
        if not video_url:
            flash('未找到視頻，請嘗試其他關鍵字。', 'danger')
            return redirect(url_for('index'))
    return render_template('index.html', form=form, video_url=video_url)

def search_youtube(keyword):
    # 使用關鍵字生成搜索 URL，這裡可以自訂更複雜的搜索邏輯
    search_url = f"https://www.youtube.com/results?search_query={keyword}"
    return search_url

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download()
        flash('視頻已成功下載！', 'success')
    except Exception as e:
        flash(f'下載失敗: {str(e)}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=10000)
