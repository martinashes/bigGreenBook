import requests
from bs4 import BeautifulSoup


def get_article_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # 发送HTTP请求并获取页面内容
    response = requests.get(url, headers=headers)
    html_content = response.content

    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(html_content, 'html.parser')
    title = get_title(soup)
    content = get_content(soup)


def get_content(soup):
    selector = "#articleId > p"
    text = []
    for p in soup.select(selector):
        print(p)
        # 提取文本内容
    #     text = text.append(p.get_text().strip())
    # print(text)
    return text



def get_title(soup):
    selector = "#articleId > h1"
    selected_elements = soup.select(selector)
    title = selected_elements[0].text.strip()
    return title



def get_article_list():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = "https://post.smzdm.com/tab/ribai/p"  # 替换为你要抓取的网页的URL
    links = []
    pages = 4   # 需要翻页的次数

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
    url = "https://post.smzdm.com/p/ao968vp6/"
    get_article_content(url)


main()