from flask import Flask, stream_with_context, Response
import requests
from qiniu import Auth

app = Flask(__name__)

access_key = "eecEsU-EW1Rg3itOmYKHqUn5toMGf_K-i4Rk1EW-"
secret_key = "YAchzOWeTV4TfyG6jqV3BHfHyc7fREpzJfUmOFD0"
bucket_domain = "s37wu7hc2.hn-bkt.clouddn.com"

# 获取所有的视频私有链接
def get_video_url(video_name):
    base_url = f'http://{bucket_domain}/{video_name}'
    q = Auth(access_key, secret_key)
    private_url = q.private_download_url(base_url, expires=3600)
    return private_url

video_list = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4", "video5.mp4"]
current_video_index = 0

@app.route('/stream_video')
def stream_video():
    global current_video_index
    if current_video_index >= len(video_list):
        current_video_index = 0

    video_url = get_video_url(video_list[current_video_index])

    def generate():
        response = requests.get(video_url, stream=True)
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk
    current_video_index += 1
    return Response(stream_with_context(generate()), content_type='video/mp4')

if __name__ == '__main__':
    app.run(port=5000)
