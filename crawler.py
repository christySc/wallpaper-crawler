"""壁纸爬虫核心模块 - 基于 Wallhaven API"""

import os
import time
from urllib.parse import urlparse

import requests

import config


def search_wallpapers(query: str = "", page: int = 1) -> list[dict]:
    """通过 Wallhaven API 搜索壁纸，返回壁纸信息列表"""
    url = f"{config.API_BASE}/search"
    params = dict(config.SEARCH_PARAMS)
    params["page"] = page
    if query:
        params["q"] = query
    if config.API_KEY:
        params["apikey"] = config.API_KEY

    try:
        resp = requests.get(url, params=params, headers=config.HEADERS, timeout=config.TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        wallpapers = data.get("data", [])
        meta = data.get("meta", {})
        total = meta.get("total", 0)
        print(f"📊 搜索结果: 共 {total} 张，当前第 {page} 页，本页 {len(wallpapers)} 张")
        return wallpapers
    except requests.RequestException as e:
        print(f"[错误] API 请求失败: {e}")
        return []


def download_wallpaper(wallpaper: dict, save_dir: str) -> bool:
    """下载单张壁纸"""
    image_url = wallpaper.get("path", "")
    wp_id = wallpaper.get("id", "unknown")
    resolution = wallpaper.get("resolution", "unknown")

    if not image_url:
        print(f"[错误] 壁纸 {wp_id} 没有下载链接")
        return False

    try:
        resp = requests.get(image_url, headers=config.HEADERS, timeout=config.TIMEOUT, stream=True)
        resp.raise_for_status()

        # 从 URL 提取文件名
        filename = os.path.basename(urlparse(image_url).path)
        if not filename:
            filename = f"wallhaven-{wp_id}.jpg"

        filepath = os.path.join(save_dir, filename)

        if os.path.exists(filepath):
            print(f"[跳过] 已存在: {filename}")
            return False

        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = os.path.getsize(filepath)
        size_mb = file_size / (1024 * 1024)
        print(f"[下载] {filename} | {resolution} | {size_mb:.1f}MB")
        return True
    except requests.RequestException as e:
        print(f"[错误] 下载失败 {wp_id}: {e}")
        return False


def run(query: str = "", max_images: int = None):
    """运行爬虫"""
    max_images = max_images if max_images is not None else config.MAX_IMAGES

    print(f"🔍 搜索关键词: {query or '(热门壁纸)'}")
    print(f"📁 保存目录: {config.DOWNLOAD_DIR}")
    print(f"🖼️  目标数量: {max_images}")
    print()

    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)

    # 搜索壁纸
    wallpapers = search_wallpapers(query=query, page=1)
    if not wallpapers:
        print("未找到壁纸")
        return

    wallpapers = wallpapers[:max_images]

    # 下载
    success = 0
    for i, wp in enumerate(wallpapers, 1):
        print(f"[{i}/{len(wallpapers)}] ", end="")
        if download_wallpaper(wp, config.DOWNLOAD_DIR):
            success += 1
        time.sleep(config.REQUEST_DELAY)

    print(f"\n✅ 完成！成功下载 {success} 张壁纸到 {config.DOWNLOAD_DIR}/")
