#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os, subprocess

'''
http.server 可以完成：
1. 等待用户连接服务器 DONE
2. 解析请求 DONE
3. 计算它所请求
4. 获取数据
5。 格式化数据为 HTML
6. 返回数据 DONE
'''

'''
事件处理
'''
class base_case(object):
    def handle_file(self, handler, full_path):
        '''
        将文件发送往客户端
        '''
        try:
            with open(full_path, 'r') as reader:
                content = reader.read()
                handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)
    def index_path(self, handler):
        '''
        得到 index.html 的路径
        '''
        return os.path.join(handler.full_path, 'index.html')
    def test(self, handler):
        '''
        不同情况必须继承，作为服务器判定当前是哪种请求的依据
        '''
        assert False, 'Not implemented'
    def act(self, handler):
        '''
        如果是当前请求，需要如何做。必须继承
        '''
        assert False, 'Not implemented'

class case_no_file(base_case):
    '''
    没有找到某文件/文件夹/路径
    '''
    def test(self, handler):
        return not os.path.exists(handler.full_path)
    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))

class case_existing_file(base_case):
    '''
    找到某文件，返回它的内容（再加个文件类型判断就好了）
    '''
    def test(self, handler):
        return os.path.isfile(handler.full_path)
    def act(self, handler):
        self.handle_file(handler, full_path)

class case_directory_index_file(base_case):
    '''
    当前请求是一个目录，查找 index.html
    '''
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            os.path.isfile(self.index_path(handler))
    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))

class case_always_fail(base_case):
    '''
    默认处理
    '''
    def test(self, handler):
        return True
    def act(self, handler):
        raise ServerException("Unknow object '{0}'".format(handler.path))

class case_directory_no_index_file(base_case):
    '''
    当前目录没有 index，列出其子目录
    '''
    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
            not os.path.isfile(self.index_path(handler))
    def act(self, handler):
        handler.list_dir(handler.full_path)

class case_cgi_file(base_case):
    '''
    可执行文件
    '''
    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')
    def act(self, handler):
        self.run_cgi(handler, handler.full_path)
    def run_cgi(self, handler, full_path):
        data = subprocess.check_output(["python", full_path])
        handler.send_content(data)


class RequestHandler(BaseHTTPRequestHandler):

    Error_Page = '''
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        '''

    Listing_Page = '''
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>'''

    def list_dir(self, full_path):
        try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e)
                       for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            self.handle_error(msg)

    Cases = [case_no_file(),
             case_cgi_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_directory_no_index_file(),
             case_always_fail()]

    def send_content(self, page, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(bytes(page, "utf-8"))

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                handler = case
                if handler.test(self):
                    handler.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

class ServerException(Exception):
    '''
    Server inner problem
    '''
    pass

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
