"""壁纸爬虫入口"""

import argparse

from crawler import run


def main():
    parser = argparse.ArgumentParser(description="壁纸图片爬虫")
    parser.add_argument("-u", "--url", help="目标网页 URL")
    parser.add_argument("-n", "--num", type=int, help="最大下载数量")
    args = parser.parse_args()

    run(url=args.url, max_images=args.num)


if __name__ == "__main__":
    main()
