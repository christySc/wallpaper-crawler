"""壁纸爬虫核心模块"""

import os
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

import config


def fetch_page(url: str) -> str | None:
    """获取网页内容"""
    try:
        resp = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"[错误] 获取页面失败: {e}")
        return None


def parse_images(html: str, base_url: str) -> list[str]:
    """从 HTML 中解析图片链接"""
    soup = BeautifulSoup(html, "lxml")
    image_urls = []

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        # 转为绝对 URL
        full_url = urljoin(base_url, src)
        # 过滤小图标等非壁纸图片
        if _is_wallpaper(full_url, img):
            image_urls.append(full_url)

    return image_urls


def _is_wallpaper(url: str, img_tag) -> bool:
    """简单判断是否为壁纸图片（过滤小图标）"""
    # 跳过 SVG、base64
    if url.endswith(".svg") or url.startswith("data:"):
        return False
    # 尝试通过 width/height 属性过滤小图
    width = img_tag.get("width")
    height = img_tag.get("height")
    if width and height:
        try:
            if int(width) < 200 or int(height) < 200:
                return False
        except ValueError:
            pass
    return True


def download_image(url: str, save_dir: str) -> bool:
    """下载单张图片"""
    try:
        resp = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT, stream=True)
        resp.raise_for_status()

        # 从 URL 提取文件名
        filename = os.path.basename(urlparse(url).path)
        if not filename or "." not in filename:
            filename = f"wallpaper_{hash(url) & 0xFFFFFFFF:08x}.jpg"

        filepath = os.path.join(save_dir, filename)

        # 跳过已存在的文件
        if os.path.exists(filepath):
            print(f"[跳过] 已存在: {filename}")
            return False

        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[下载] {filename}")
        return True
    except requests.RequestException as e:
        print(f"[错误] 下载失败 {url}: {e}")
        return False


def run(url: str = None, max_images: int = None):
    """运行爬虫"""
    url = url or config.TARGET_URL
    max_images = max_images if max_images is not None else config.MAX_IMAGES

    print(f"🔍 目标: {url}")
    print(f"📁 保存目录: {config.DOWNLOAD_DIR}")

    # 创建下载目录
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)

    # 获取页面
    html = fetch_page(url)
    if not html:
        return

    # 解析图片链接
    image_urls = parse_images(html, url)
    print(f"🔗 发现 {len(image_urls)} 张图片")

    if max_images > 0:
        image_urls = image_urls[:max_images]

    # 下载图片
    success = 0
    for i, img_url in enumerate(image_urls, 1):
        print(f"[{i}/{len(image_urls)}] ", end="")
        if download_image(img_url, config.DOWNLOAD_DIR):
            success += 1
        time.sleep(config.REQUEST_DELAY)

    print(f"\n✅ 完成！成功下载 {success} 张壁纸到 {config.DOWNLOAD_DIR}/")
