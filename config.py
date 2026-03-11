# 爬虫配置

# 目标网站 URL（默认: Unsplash 壁纸页面）
TARGET_URL = "https://unsplash.com/t/wallpapers"

# 图片保存目录
DOWNLOAD_DIR = "downloads"

# 每页下载数量限制（0 = 不限制）
MAX_IMAGES = 20

# 请求间隔（秒），避免过于频繁
REQUEST_DELAY = 1

# 请求超时时间（秒）
TIMEOUT = 30

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}
