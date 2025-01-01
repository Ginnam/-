# Douban Movie Scraper

## 简介

Douban Movie Scraper 是一个Python脚本，用于从豆瓣网抓取用户的电影收藏信息。它会抓取用户观看过的电影列表，包括电影名称、评论（如果有的话）、以及电影海报图片，并将这些信息保存到本地。

## 特性

- 抓取用户在豆瓣上标记为看过（collect）的电影
- 保存每部电影的标题和评论到JSON文件中
- 下载并保存每部电影的海报图片到指定文件夹
- 支持分页抓取，可以处理大量数据
- 实现了随机延迟以避免被网站封禁

## 使用方法

### 安装依赖

确保你已经安装了Python 3.6或更高版本。然后使用pip安装所需的库：

```bash
pip install requests beautifulsoup4
```

### 设置环境

1. 修改`main()`函数中的`cookie`变量为你自己的豆瓣网站登录后的Cookie。
2. 设置`user_id`为你要抓取的豆瓣用户ID。
3. 可选调整`image_folder`来改变图片保存的文件夹，`page_size`每页电影数量，`max_pages`最大爬取页数。

### 运行脚本

直接运行该Python脚本即可开始抓取：

```bash
python douban_movie_scraper.py
```

## 注意事项

- 豆瓣网站可能会有反爬虫机制，请适当调整`sleep(1)`中的时间间隔以减少对服务器的压力。
- 请遵守豆瓣的服务条款和隐私政策，不要进行非法的数据抓取活动。
- 如果豆瓣改变了页面结构，可能需要更新CSS选择器以匹配新的HTML标签。
- Cookie可能会过期，当发生这种情况时，请更新你的Cookie。

## 文件说明

- `douban_movie_scraper.py`: 主要的Python脚本文件。
- `movie_info.json`: 存储抓取到的电影信息的JSON文件。
- `movie_posters/`: 存放下载的电影海报图片的文件夹，默认名为`movie_posters`。

## 结构说明

代码中定义了几个主要函数：

- `get_movie_info()`: 获取单页的电影信息。
- `download_image()`: 下载电影海报图片。
- `save_movie_info()`: 将电影信息保存为JSON格式。
- `main()`: 脚本的入口点，负责配置参数和调用其他函数。

## 许可证

本项目采用MIT许可证，详情参见LICENSE文件。
