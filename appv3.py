from flask import Flask, stream_with_context, Response
import requests
from flask_cors import CORS
from qiniu import Auth
import pymysql

app = Flask(__name__)
CORS(app)

# Qiniu 配置
access_key = "eecEsU-EW1Rg3itOmYKHqUn5toMGf_K-i4Rk1EW-"
secret_key = "YAchzOWeTV4TfyG6jqV3BHfHyc7fREpzJfUmOFD0"
bucket_domain = "s37wu7hc2.hn-bkt.clouddn.com"

# MySQL 配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'db': 'QiniuVideo',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_video_url():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT video_name, video_domain FROM video_hub ORDER BY RAND() LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            video_name = result['video_name']
            video_domain = result['video_domain']
            base_url = f'http://{video_domain}/{video_name}'
            q = Auth(access_key, secret_key)
            private_url = q.private_download_url(base_url, expires=3600)
            return private_url
    finally:
        connection.close()

def ensure_next_urls_filled():
    while len(nextUrls) < 10:
        nextUrls.append(get_video_url())

nextUrls = [get_video_url() for _ in range(10)]
prevUrls = []

@app.route('/next_video')
def next_video():
    current_url = nextUrls.pop(0)  # 获取并移除下一个视频链接
    prevUrls.append(current_url)  # 将当前视频链接添加到prevUrls
    ensure_next_urls_filled()
    return stream_video_content(current_url)

@app.route('/pre_video')
def pre_video():
    if prevUrls:
        current_url = prevUrls.pop()  # 获取并移除上一个视频链接
        nextUrls.insert(0, current_url)  # 将当前视频链接添加到nextUrls的开头
        return stream_video_content(current_url)
    return "", 404

# @app.route('/stream_video')
def stream_video_content(url):
    
    def generate():
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

    return Response(stream_with_context(generate()), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=5000)