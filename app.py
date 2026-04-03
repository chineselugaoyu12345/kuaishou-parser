import os
from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)


@app.route('/parse', methods=['GET'])
def parse():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'missing url'}), 400

    # 你的解析逻辑（示例：从页面提取视频地址）
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        # 这里写你的解析正则
        match = re.search(r'"videoUrl":"([^"]+)"', resp.text)
        if match:
            video_url = match.group(1).replace('\\u002F', '/')
            return jsonify({'type': 'video', 'url': video_url})
        return jsonify({'error': 'no media found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    # 关键：端口从环境变量读取，监听 0.0.0.0
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)