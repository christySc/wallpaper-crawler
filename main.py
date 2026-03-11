"""壁纸爬虫入口 - 基于 Wallhaven API"""

import argparse

from crawler import run


def main():
    parser = argparse.ArgumentParser(description="Wallhaven 高清壁纸爬虫")
    parser.add_argument("-q", "--query", default="", help="搜索关键词（如 nature, anime, city）")
    parser.add_argument("-n", "--num", type=int, help="最大下载数量")
    args = parser.parse_args()

    run(query=args.query, max_images=args.num)


if __name__ == "__main__":
    main()
