import requests
from bs4 import BeautifulSoup
import os

# 代码已经完成了 但是由于好像妹子网站长做了写设置导致无法访问原图
# 具体原因之后的课程应该会有讲


class mzitu(object):
    def request(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
        content = requests.get(url, headers=headers)
        return content

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join(
            "/home/hiro/Documents/mzitu", path))
        if not isExists:
            print(path, u'is making')
            os.makedirs(os.path.join("/home/hiro/Documents/mzitu", path))
            os.chdir(os.path.join("/home/hiro/Documents/mzitu", path))
            return True
        else:
            print(path, u'had been make')
            return False

    def save(self, img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)
        print(img.content)
        with open(img_url[-9:-4] + '.jpg', 'wb') as file:
            file.write(img.content)

    def all_url(self, url):
        html = self.request(url)
        all_a = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            href = a['href']
            print(u'start saving...', title)
            path = str(title).replace('?', title)
            self.mkdir(path)
            self.html(href)

    def html(self, url):
        html = self.request(url)
        max_span = BeautifulSoup(html.text, 'lxml').find(
            'div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = url + '/' + str(page)
            self.img(page_url)

    def img(self, url):
        img_html = self.request(url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find(
            'div', class_='main-image').find('img')['src']
        self.save(img_url)


if __name__ == '__main__':
    mzitu = mzitu()
    mzitu.save("http://i.meizitu.net/2017/07/05c09.jpg")
