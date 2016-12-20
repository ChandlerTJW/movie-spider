import socket
import ssl

# 解析url
def parsed_url(url):
    """
    解析 url 返回 (protocol host port path)
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        # '://' 定位 然后取第一个 / 的位置来切片
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path

# 创建 socket
def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        s = ssl.wrap_socket(socket.socket())
    return s

# 读数据
def response_by_socket(s):
    """
    参数是一个 socket 实例
    返回这个 socket 读取的所有数据
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


# 获取网页的html
def get(url):
    """
    用 GET 请求 url 并返回响应
    """
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)
    body = body = r.split('\r\n\r\n', 1)[1]
    return body

address = 'https://movie.douban.com/top250'


# 解析html，获得我们想要的数据
def parsed_movies(address):
    body = get(address)
    body = body.split('<ol class="grid_view">')[1]
    body = body.split('</ol>')[0]
    movies = body.split('<li>')[1:]
    for movie in movies:
        movie = movie.split('<em class="">')[1]
        index = movie.split('</em>', 1)[0]
        movie = movie.split('<span class="title">', 1)[1]
        name = movie.split('</span>', 1)[0]
        movie = movie.split('<span class="rating_num" property="v:average">', 1)[1]
        score = movie.split('</span>', 1)[0]
        movie = movie.split('<span>', 1)[1]
        number = movie.split('</span>', 1)[0]
        a = movie.find('<span class="inq">')
        if a == -1:
            quotation = '待补充'
        else:
            movie = movie.split('<span class="inq">', 1)[1]
            quotation = movie.split('</span>', 1)[0]
        print('{}, {}, {}, {}, {}'.format(index, name, score, number, quotation))


# 汇总函数功能，解析所有top250网页
def all_movies():
    a = 'https://movie.douban.com/top250'
    movie_list = [
        a,
    ]
    for i in range(1, 10):
        postfix = '?start={}'.format(i * 25)
        url = a + postfix
        movie_list.append(url)
    for address in movie_list:
        parsed_movies(address)

all_movies()











