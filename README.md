# 🧭 NavPage — 个人书签导航站

一个轻量、美观、支持自托管的个人导航页，基于 Python Flask + 纯前端构建，无需数据库。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)

---

## ✨ 功能特性

- 📌 **多标签页** — 按场景分组，支持增删改排序
- 🔖 **书签管理** — 可视化编辑，支持拖拽排序
- 🔥 **热力图** — 追踪点击频率，直观显示常用书签
- 🎨 **背景色主题** — 16 种内置配色，实时切换
- 🖼️ **Favicon 自动缓存** — 自动抓取网站图标并本地缓存，含魔数校验防止缓存损坏
- 🏷️ **Tabler 图标支持** — 可使用 [Tabler Icons](https://tabler.io/icons) 作为书签图标
- 📝 **备忘录小组件** — 支持 Markdown 的内嵌便签
- 💾 **本地 JSON 存储** — 数据保存在 `data.json`，备份迁移方便
- 🔒 **编辑模式保护** — 普通模式只读，编辑功能需点击解锁

---

## 📁 项目结构

```
navpage/
├── server.py          # Flask 后端，提供 API 和 favicon 代理
├── index.html         # 前端主页（单文件，内联所有逻辑）
├── data.json          # 书签数据（自动生成，可手动编辑）
├── favicon_cache/     # favicon 缓存目录（自动创建）
├── icon-names.js      # 图标名称辅助文件
├── tabler-names.js    # Tabler 图标名称列表
├── marked.min.js      # Markdown 渲染库
└── 404.html           # 自定义 404 页面
```

---

## 🚀 部署指南

### 方法一：直接运行（开发/测试）

**环境要求：** Python 3.8+

```bash
# 克隆仓库
git clone https://github.com/ppdg123/navpage.git
cd navpage

# 安装依赖
pip install flask requests

# 启动服务
python server.py
```

服务默认监听 `http://127.0.0.1:5200`，打开浏览器访问即可。

---

### 方法二：配合 Nginx 反向代理（生产推荐）

1. **启动后端**

```bash
# 使用 nohup 后台运行
nohup python3 server.py > navpage.log 2>&1 &
```

2. **配置 Nginx**

```nginx
server {
    listen 80;
    server_name nav.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **启用 HTTPS（推荐）**

```bash
# 使用 Certbot 申请免费证书
sudo certbot --nginx -d nav.yourdomain.com
```

---

### 方法三：使用 systemd 托管（开机自启）

创建 `/etc/systemd/system/navpage.service`：

```ini
[Unit]
Description=NavPage Bookmark Navigation
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/navpage
ExecStart=/usr/bin/python3 /path/to/navpage/server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable navpage
sudo systemctl start navpage
```

---

## ⚙️ 配置说明

`data.json` 为数据文件，首次启动若不存在会自动生成示例数据。

结构示例：

```json
{
  "pageBgColor": "#f0f2f5",
  "tabs": [
    {
      "id": "t1",
      "name": "主页",
      "columns": [
        {
          "id": "c1",
          "widgets": [
            {
              "id": "w1",
              "type": "bookmarks",
              "title": "常用工具",
              "bookmarks": [
                {
                  "id": "b1",
                  "name": "GitHub",
                  "url": "https://github.com",
                  "icon": "favicon"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**图标类型：**
- `"icon": "favicon"` — 自动抓取网站 favicon
- `"icon": "tabler:brand-github"` — 使用 Tabler 图标（格式：`tabler:图标名`）

---

## 📡 API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/data` | 获取全部书签数据 |
| POST | `/api/data` | 保存书签数据 |
| GET | `/api/favicon?url=<url>` | 获取/代理网站 favicon |

---

## 🛠️ 技术栈

- **后端**：Python 3 + Flask
- **前端**：原生 HTML/CSS/JavaScript（无框架依赖）
- **图标**：[Tabler Icons](https://tabler.io/icons)（CDN 加载）
- **Markdown**：[marked.js](https://marked.js.org/)

---

## 📄 License

MIT License — 自由使用、修改和分发。

---

## 🙏 致谢

- [Tabler Icons](https://tabler.io/icons) — 精美的开源图标库
- [Flask](https://flask.palletsprojects.com/) — 轻量 Python Web 框架

---

# 🧭 NavPage — Personal Bookmark Navigation

A lightweight, beautiful, self-hosted personal navigation page built with Python Flask + pure frontend. No database required.

---

## ✨ Features

- 📌 **Multiple Tabs** — Group bookmarks by scenario, with add/remove/reorder support
- 🔖 **Bookmark Management** — Visual editor with drag-and-drop sorting
- 🔥 **Heatmap** — Track click frequency to highlight frequently used bookmarks
- 🎨 **Background Themes** — 16 built-in color schemes with real-time switching
- 🖼️ **Auto Favicon Cache** — Automatically fetches and caches site icons locally, with magic-byte validation to prevent corrupt cache
- 🏷️ **Tabler Icons Support** — Use [Tabler Icons](https://tabler.io/icons) as bookmark icons
- 📝 **Memo Widget** — Inline sticky notes with Markdown support
- 💾 **Local JSON Storage** — Data stored in `data.json`, easy to backup and migrate
- 🔒 **Edit Mode Protection** — Read-only by default, editing requires unlocking

---

## 🚀 Deployment

### Option 1: Direct Run (Development/Testing)

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/ppdg123/navpage.git
cd navpage

# Install dependencies
pip install flask requests

# Start the server
python server.py
```

The server listens on `http://127.0.0.1:5200` by default.

---

### Option 2: Nginx Reverse Proxy (Recommended for Production)

1. **Start the backend**

```bash
nohup python3 server.py > navpage.log 2>&1 &
```

2. **Configure Nginx**

```nginx
server {
    listen 80;
    server_name nav.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. **Enable HTTPS (recommended)**

```bash
sudo certbot --nginx -d nav.yourdomain.com
```

---

### Option 3: systemd Service (Auto-start on boot)

Create `/etc/systemd/system/navpage.service`:

```ini
[Unit]
Description=NavPage Bookmark Navigation
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/navpage
ExecStart=/usr/bin/python3 /path/to/navpage/server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable navpage
sudo systemctl start navpage
```

---

## ⚙️ Configuration

`data.json` is the data file. It will be auto-generated with sample data on first run if it doesn't exist.

**Icon types:**
- `"icon": "favicon"` — Auto-fetch the site's favicon
- `"icon": "tabler:brand-github"` — Use a Tabler icon (format: `tabler:<icon-name>`)

---

## 📡 API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/data` | Get all bookmark data |
| POST | `/api/data` | Save bookmark data |
| GET | `/api/favicon?url=<url>` | Fetch/proxy site favicon |

---

## 🛠️ Tech Stack

- **Backend**: Python 3 + Flask
- **Frontend**: Vanilla HTML/CSS/JavaScript (no framework)
- **Icons**: [Tabler Icons](https://tabler.io/icons) (CDN)
- **Markdown**: [marked.js](https://marked.js.org/)

---

## 📄 License

MIT License — Free to use, modify, and distribute.
