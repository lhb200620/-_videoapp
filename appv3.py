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

def load_all_video_ids():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT video_id FROM video_hub"
            cursor.execute(sql)
            all_ids = {row['video_id'] for row in cursor.fetchall()}
            return all_ids
    finally:
        connection.close()

def get_video_url_from_id(video_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT video_name, video_domain FROM video_hub WHERE video_id = %s LIMIT 1"
            cursor.execute(sql, (video_id,))
            result = cursor.fetchone()
            video_name = result['video_name']
            video_domain = result['video_domain']
            base_url = f'http://{video_domain}/{video_name}'
            q = Auth(access_key, secret_key)
            private_url = q.private_download_url(base_url, expires=3600)
            return private_url
    finally:
        connection.close()

all_video_ids = load_all_video_ids()


def get_random_video_url():
    video_id = all_video_ids.pop()  # 从集合中随机获取一个ID并删除它
    return get_video_url_from_id(video_id)

def ensure_next_urls_filled():
    while len(nextUrls) < 10:
        nextUrls.append(get_random_video_url())

nextUrls = [get_random_video_url() for _ in range(10)]
prevUrls = []

@app.route('/next_video')
def next_video():
    print("receive a request")
    prevUrls.append(nextUrls.pop(0))

    ensure_next_urls_filled()
    return stream_video_content(nextUrls[0])

@app.route('/pre_video')
def pre_video():
    if prevUrls:
        nextUrls.insert(0, prevUrls.pop())

        return stream_video_content(nextUrls[0])
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