import os
import time
import subprocess

'''
利用youtube-dl命令，自动批量下载youtube视频到指定目录
'''


# list.txt路径
PATH = os.path.dirname(os.path.abspath(__file__)) + '/list.txt'

# 查询视频信息语句 + socks5代理
COMMAND_PREFIX_CHECK = 'youtube-dl --proxy socks5://127.0.0.1:1080 -F '

# 下载1080p视频语句 + scoks代理
COMMAND_PREFIX_DOWNLOAD= 'youtube-dl --proxy socks5://127.0.0.1:1080 -f 137+140 '

# 指定目录
TODIR = "-o \"~/Movies/%(title)s.%(ext)s\" "


# 传入url，加载相应的1080p视频
def download_by_url(url):
    p = subprocess.Popen(COMMAND_PREFIX_DOWNLOAD + TODIR + url, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    start = time.time()
    print("********\tStart download: " + url + "\t" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start)))
    while True:
        line = bytes.decode(p.stdout.readline())
        if not line == '':
            print(line)
        else:
            break
    p.wait()
    end = time.time()
    print("********\tEnd\t"+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end)), end = " ")
    print("taking："+str(int(end-start))+" seconds")
    mark_downloaded_url(url)

def get_url_from_list():
    print("\n********\tGet url")
    f = open(PATH, 'r+')
    for line in f.readlines():
        if not line == '\n':
            if line[0] == 'h':
                return line.strip('\n')
    return ''

# 标记已经下载过的url（url前面加上*）
def mark_downloaded_url(url):
    output = []
    f = open(PATH, 'r+')
    i = 0
    for line in f.readlines():
        line = line.strip('\n')
        url = url.strip('\n')
        if line == url:
            line = "*" + line
        output.append(line+"\n")
        i = i + 1
    f.close()
    f = open(PATH, 'w+')
    f.writelines(output)
    f.close()

if __name__ == '__main__':
    # 检查list.txt文件是否存在
    if not os.path.exists(PATH):
        print ("can't find "+PATH)
        exit(0)
    while True:
        # 若想暂停下载，在同级目录下建一个stop.txt
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/stop.txt'):
            exit(0)
        url = get_url_from_list()
        print("\t\t\tRead:" + url)
        if url == '':
            print("FINISH DOWNLOAD")
            exit(0)
        download_by_url(url)