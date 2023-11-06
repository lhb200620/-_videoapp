from flask import Flask, jsonify, request, stream_with_context, Response
import requests
from flask_cors import CORS
from qiniu import Auth
import pymysql

app = Flask(__name__)
CORS(app)

# Qiniu 配置
access_key = "eecEsU-EW1Rg3itOmYKHqUn5toMGf_K-i4Rk1EW-"
secret_key = "YAchzOWeTV4TfyG6jqV3BHfHyc7fREpzJfUmOFD0"
bucket_domain = "s3jmkz13k.hn-bkt.clouddn.com"

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
            sql = "SELECT video_id FROM videos"
            cursor.execute(sql)
            all_ids = {row['video_id'] for row in cursor.fetchall()}
            return all_ids
    finally:
        connection.close()

def get_video_url_from_id(video_id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT video_name, video_domain FROM videos WHERE video_id = %s LIMIT 1"
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

def get_random_video_url_with_tag(tag):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT video_id FROM videos WHERE tag = %s ORDER BY RAND() LIMIT 1"
            cursor.execute(sql, (tag,))
            result = cursor.fetchone()
            if result:
                return get_video_url_from_id(result['video_id'])
            else:
                return None
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
global_button_id = None
tagUrls = []
current_tag_idx = -1  # 当前播放的带有特定tag的视频的索引

@app.route('/fetch_data')
def fetch_data():
    global global_button_id  # 使用全局关键字引用全局变量
    global tagUrls
    # 从URL参数中提取buttonId
    buttonId = request.args.get('buttonId')
    
    # 保存到全局变量中
    if buttonId:
        tagUrls = []
        global_button_id = buttonId[-1:]
    
    print(f"success get global id: {global_button_id}")
    connection = pymysql.connect(**db_config)
    
    try:
        with connection.cursor() as cursor:
            if global_button_id is None:
                print("Fetching random videos...")
                sql = "SELECT pict_name, video_name, video_domain FROM videos ORDER BY RAND() LIMIT 8"
                cursor.execute(sql)  # 这里不需要参数
            else:
                print(f"Fetching videos with tag: {global_button_id}...")
                sql = "SELECT pict_name, video_name, video_domain FROM videos WHERE tag = %s LIMIT 8"
                cursor.execute(sql, (global_button_id,))  # 这里需要参数
            results = cursor.fetchall()
                
            data = {
                'thumbnails': [],
                'videos': []
            }
            
            for result in results:
                video_name = result['video_name']
                video_domain = result['video_domain']
                pict_name = result['pict_name']
                pict_base_url = f'http://{video_domain}/{pict_name}'
                video_base_url = f'http://{video_domain}/{video_name}'
                q = Auth(access_key, secret_key)
                pict_private_url = q.private_download_url(pict_base_url, expires=3600)
                video_private_url = q.private_download_url(video_base_url, expires=3600)
                data['thumbnails'].append(pict_private_url)
                data['videos'].append(video_private_url)

            return jsonify(data)
    finally:
        connection.close()

@app.route('/next_video')
def next_video():
    global current_tag_idx, tagUrls

    print("receive a request for next video")
    if global_button_id:
        # 有global_button_id时，获取带有特定tag的下一个视频
        if current_tag_idx < len(tagUrls) - 1:
            current_tag_idx += 1
            return stream_video_content(tagUrls[current_tag_idx])
        else:
            new_url = get_random_video_url_with_tag(global_button_id)
            if new_url:
                tagUrls.append(new_url)
                current_tag_idx += 1
                return stream_video_content(new_url)
            else:
                return "", 404
    else:
        print("receive a request")
        prevUrls.append(nextUrls.pop(0))

        ensure_next_urls_filled()
        return stream_video_content(nextUrls[0])

@app.route('/pre_video')
def pre_video():
    global current_tag_idx, tagUrls

    if global_button_id and current_tag_idx > 0:
        # 有global_button_id时，获取带有特定tag的上一个视频
        current_tag_idx -= 1
        return stream_video_content(tagUrls[current_tag_idx])
    elif global_button_id and current_tag_idx == 0:
        # 如果已经是第一个视频，则不再递减
        return stream_video_content(tagUrls[current_tag_idx])
    else:
        if prevUrls:
            nextUrls.insert(0, prevUrls.pop())

            return stream_video_content(nextUrls[0])
        return "", 404

def stream_video_content(url):
    
    def generate():
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

    return Response(stream_with_context(generate()), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=5000)