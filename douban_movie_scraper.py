import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Optional
import json
import os
from urllib.parse import urlparse
from time import sleep


@dataclass
class MovieInfo:
    title: str
    comment: Optional[str]
    poster_url: str
    poster_filename: Optional[str] = None


def get_movie_info(session: requests.Session, user_id: str, start: int = 0) -> list[MovieInfo]:
    """
    Scrape movie information from Douban for a specific page

    Args:
        session: Request session with cookies
        user_id: Douban user ID
        start: Start index for pagination

    Returns:
        list[MovieInfo]: List of movie information
    """
    url = f"https://movie.douban.com/people/{user_id}/collect"
    params = {
        "start": start,
        "sort": "time",
        "rating": "all",
        "filter": "all",
        "mode": "grid",
        "type": "all"
    }

    # 添加随机延迟避免被封
    sleep(1)

    response = session.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = []
    for item in soup.select(".item.comment-item"):
        # Get title
        title_elem = item.select_one(".title em")
        title = title_elem.text.strip() if title_elem else "Unknown Title"

        # Get comment
        comment_elem = item.select_one(".comment")
        comment = comment_elem.text.strip() if comment_elem else None

        # Get poster URL
        poster_elem = item.select_one(".pic img")
        poster_url = poster_elem['src'] if poster_elem else None

        movies.append(MovieInfo(title=title, comment=comment, poster_url=poster_url))

    return movies


def download_image(session: requests.Session, url: str, folder: str) -> Optional[str]:
    """
    Download image from URL to specified folder

    Args:
        session: Request session
        url: Image URL
        folder: Destination folder

    Returns:
        str: Filename of downloaded image, or None if download failed
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)

        # 从URL提取文件名
        filename = os.path.join(folder, os.path.basename(urlparse(url).path))

        # 如果文件已存在，跳过下载
        if os.path.exists(filename):
            return filename

        response = session.get(url)
        response.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(response.content)

        return filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def save_movie_info(movies: list[MovieInfo], output_file: str = "movie_info.json"):
    """
    Save movie information to a JSON file
    """
    movie_data = [
        {
            "title": movie.title,
            "comment": movie.comment,
            "poster_url": movie.poster_url,
            "poster_filename": movie.poster_filename
        }
        for movie in movies
    ]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(movie_data, f, ensure_ascii=False, indent=2)


def main():
    # 配置信息
    cookie = """cookie"""  # 替换为你的cookie
    user_id = "123456789"  # 你的豆瓣用户ID
    image_folder = "movie_posters"  # 图片保存文件夹
    page_size = 15  # 每页电影数量
    max_pages = 10  # 最大爬取页数，可以根据需要调整

    # 初始化session
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })

    # 设置cookies
    cookies_dict = {}
    for item in cookie.split(';'):
        if '=' in item:
            name, value = item.strip().split('=', 1)
            cookies_dict[name] = value
    session.cookies.update(cookies_dict)

    all_movies = []

    try:
        # 分页获取数据
        for page in range(max_pages):
            start = page * page_size
            movies = get_movie_info(session, user_id, start)

            if not movies:  # 如果没有更多数据，退出循环
                break

            print(f"Scraping page {page + 1}, found {len(movies)} movies")

            # 下载每部电影的海报
            for movie in movies:
                if movie.poster_url:
                    filename = download_image(session, movie.poster_url, image_folder)
                    movie.poster_filename = filename
                    if filename:
                        print(f"Downloaded poster for: {movie.title}")

            all_movies.extend(movies)

        # 保存所有电影信息
        save_movie_info(all_movies)
        print(f"\nSuccessfully scraped total {len(all_movies)} movies")
        print(f"Movie information saved to movie_info.json")
        print(f"Movie posters downloaded to {image_folder}/ folder")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
