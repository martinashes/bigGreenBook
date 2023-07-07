import requests
from bs4 import BeautifulSoup
import os


def get_article_content(url, i):
    folder_name = "0" + str(i)
    file_name = "1.txt"
    os.makedirs(folder_name, exist_ok=True)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # 发送HTTP请求并获取页面内容
    response = requests.get(url, headers=headers)
    html_content = response.content

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(html_content, 'html.parser')
    title = get_title(soup)
    content = get_content(soup)
    get_picture(soup, folder_name)

    # 创建文件夹


    # 构建文件路径
    file_path = os.path.join(folder_name, file_name)

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(title + "\n\n" + content)


def get_content(soup):
    # 遍历所有匹配的节点
    text = ""
    for p in soup.find_all('p', itemprop='description'):
        # 提取文本内容
        node_text = p.get_text().strip()

        # 如果节点有文本内容，则保存到text变量中
        if node_text:
            text += node_text + "\n"

    # 输出保存的文本内容
    return(text)


def get_picture(soup, folder_name):
    for p in soup.find_all('p', itemprop='description'):
        # 查找节点下的所有<img>标签
        images = p.find_all('img')
        for img in images:
            src = img['src']
            response = requests.get(src)
            filename = os.path.basename(src)
            filepath = os.path.join(folder_name, filename)
            with open(filepath, 'wb') as file:
                file.write(response.content)


def get_title(soup):
    title = soup.find('title')
    title = title.get_text().strip()
    return title


def get_article_list(url, pages):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    links = []

    for j in range(1, pages):
        url = format_url(j, url)
        # 发送HTTP请求并获取页面内容
        response = requests.get(url, headers=headers)
        html_content = response.content

        # 使用BeautifulSoup解析页面内容
        soup = BeautifulSoup(html_content, 'html.parser')

        # 默认一页显示20篇
        for i in range(1, 21):
            selector = format_selector(i)
            # 根据选择器提取指定内容
            selected_elements = soup.select(selector)

            # 提取带有href属性的<a>标签的链接
            for element in selected_elements:
                links.append(element['href'])

    return links


# 拼接selector
def format_selector(i):
    i = i
    first_part = "#feed-main-list > li:nth-child("
    second_part = ") > div > div.z-feed-img.block-img-wide > a:nth-child(2)"
    combined_selector = first_part + str(i) + second_part
    return combined_selector


# 循环拼接url
def format_url(i, url):
    url = url + str(i)
    return url


def main():
    url = "https://post.smzdm.com/tab/ribai/p"
    links = get_article_list(url, 3)

    for i in range(len(links)):
        get_article_content(links[i], i)


main()
