# 爬虫配置

# Wallhaven API
API_BASE = "https://wallhaven.cc/api/v1"

# 搜索参数
SEARCH_PARAMS = {
    "categories": "111",       # general/anime/people (1=开启, 0=关闭)
    "purity": "100",           # sfw/sketchy/nsfw (需要 API Key 才能开启 nsfw)
    "sorting": "toplist",      # date_added, relevance, random, views, favorites, toplist
    "order": "desc",
    "resolutions": "1920x1080,2560x1440,3840x2160",  # 高清分辨率
    "ratios": "16x9",          # 宽屏比例
}

# API Key（可选，NSFW 内容需要）
API_KEY = ""

# 图片保存目录
DOWNLOAD_DIR = "downloads"

# 每次下载数量
MAX_IMAGES = 5

# 请求间隔（秒），API 限制 45 次/分钟
REQUEST_DELAY = 1.5

# 请求超时时间（秒）
TIMEOUT = 30

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}
