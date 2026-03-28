#!/usr/bin/env python3
import json, os, hashlib, requests as req_lib
from flask import Flask, request, jsonify, send_from_directory, send_file, Response

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
STATIC_DIR = '/www/wwwrt/nav.wangfan.net'
FAVICON_CACHE_DIR = os.path.join(STATIC_DIR, 'favicon_cache')
os.makedirs(FAVICON_CACHE_DIR, exist_ok=True)

IMAGE_MAGIC = [
    bytes([0x89, 0x50, 0x4e, 0x47]),  # PNG
    bytes([0x00, 0x00, 0x01, 0x00]),  # ICO
    bytes([0x00, 0x00, 0x02, 0x00]),  # ICO cursor
    b'GIF8',                           # GIF
    bytes([0xff, 0xd8, 0xff]),         # JPEG
    b'RIFF',                           # WebP
]
# Google/DuckDuckGo 占位图大小（无图标时返回的默认图），过滤掉
PLACEHOLDER_SIZES = {726, 1478}

def is_valid_image(content, is_third_party=False):
    if len(content) < 64:
        return False
    if is_third_party and len(content) in PLACEHOLDER_SIZES:
        return False
    for magic in IMAGE_MAGIC:
        if content[:len(magic)] == magic:
            return True
    if content[:4] == b'RIFF' and len(content) > 12 and content[8:12] == b'WEBP':
        return True
    return False

DEFAULT_DATA = {
    "tabs": [{"id": "t1", "name": "主页", "columns": [
        {"id": "c1", "widgets": [{"id": "w1", "type": "bookmarks", "title": "常用", "bookmarks": [
            {"id": "b1", "name": "Google", "url": "https://google.com", "icon": "favicon"},
            {"id": "b2", "name": "GitHub", "url": "https://github.com", "icon": "favicon"}
        ]}]},
        {"id": "c2", "widgets": [{"id": "w2", "type": "markdown", "title": "备忘", "content": "## 备忘\n\n在这里写 **Markdown** 笔记..."}]}
    ]}],
    "searchEngines": [
        {"id": "se1", "name": "Google", "url": "https://www.google.com/search?q={query}", "icon": "https://www.google.com/favicon.ico"},
        {"id": "se2", "name": "搜狗", "url": "https://www.sogou.com/web?query={query}", "icon": "https://www.sogou.com/favicon.ico"}
    ],
    "activeEngine": "se1"
}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return DEFAULT_DATA

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load())

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'invalid json'}), 400
    save_data(data)
    return jsonify({'ok': True})

@app.route('/api/favicon')
def favicon_proxy():
    domain = request.args.get('domain', '').strip()
    if not domain:
        return '', 400
    import re
    if not re.match(r'^[a-zA-Z0-9.\-]+$', domain):
        return '', 400

    safe = hashlib.md5(domain.encode()).hexdigest()
    for ext in ['png', 'ico']:
        cache_path = os.path.join(FAVICON_CACHE_DIR, f'{safe}.{ext}')
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as fp:
                content = fp.read()
            if is_valid_image(content):
                mime = 'image/png' if ext == 'png' else 'image/x-icon'
                return send_file(cache_path, mimetype=mime, max_age=86400*30)
            else:
                os.remove(cache_path)

    headers = {'User-Agent': 'Mozilla/5.0 (compatible; FaviconBot/1.0)'}
    # 候选顺序：Google -> DuckDuckGo -> 直接访问
    candidates = [
        (f'https://www.google.com/s2/favicons?domain={domain}&sz=32', True),
        (f'https://icons.duckduckgo.com/ip3/{domain}.ico', True),
        (f'https://{domain}/favicon.ico', False),
        (f'https://{domain}/favicon.png', False),
        (f'https://www.{domain}/favicon.ico' if not domain.startswith('www.') else None, False),
    ]
    for item in candidates:
        if item[0] is None:
            continue
        furl, is_third_party = item
        try:
            r = req_lib.get(furl, timeout=5, headers=headers, allow_redirects=True)
            if r.status_code != 200:
                continue
            if not is_valid_image(r.content, is_third_party=is_third_party):
                continue
            ct = r.headers.get('content-type', '')
            if not is_third_party:
                if 'image' not in ct and not furl.endswith('.ico') and not furl.endswith('.png'):
                    continue
            ext = 'ico' if ('icon' in ct or furl.endswith('.ico')) else 'png'
            cache_path = os.path.join(FAVICON_CACHE_DIR, f'{safe}.{ext}')
            with open(cache_path, 'wb') as fw:
                fw.write(r.content)
            mime = 'image/x-icon' if ext == 'ico' else 'image/png'
            return Response(r.content, mimetype=mime, headers={'Cache-Control': 'public, max-age=2592000'})
        except Exception:
            continue
    return '', 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(STATIC_DIR, path or 'index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5200, debug=False)
