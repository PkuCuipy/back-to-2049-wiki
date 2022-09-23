# 2022-09-23
# 先运行这个, 涉及爬虫过程, 需要调整 22 行的 Cookie
# 然后运行第二个文件 (process.py), 涉及生成 markdown
import requests
from tqdm import trange
import time
import pickle

# 回到 2049 的 UID 和视频总页数
UP_UID = 58617276
N_PAGES = 70

# 建立一个带 header 的 session, 否则会被视为爬虫 (这里是我通过浏览器进行访问时的 header)
ss = requests.session()
ss.headers = {
    "Host": "api.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "",   # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
}

verbose_collect = []
for page_no in trange(1, N_PAGES + 1):
    url = f"https://api.bilibili.com/x/space/arc/search?mid={UP_UID}&ps=30&tid=0&pn={page_no}&keyword=&order=pubdate&jsonp=jsonp"
    while True:
        try:
            json_dict = ss.get(url).json()
            infos = json_dict["data"]["list"]["vlist"]
            for info in infos:
                timestamp = info["created"]                                     # 0. 发布日期
                date_str = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                title = info["title"]                                           # 1. 视频标题
                bvid = info["bvid"]                                             # 2. 视频 BV 号
                time_len = info["length"]                                       # 3. 视频时长
                whole_url = f"[{bvid}](https://www.bilibili.com/video/{bvid})"  # 4. 视频链接
                verbose_collect.append([
                    date_str,
                    title,
                    bvid,
                    time_len,
                    whole_url,
                ])
            break
        except Exception as e:
            print(str(e) + "retry...")
            time.sleep(3)


save_filename = "./" + time.strftime("%Y-%m-%d(%H.%M.%S)", time.localtime(time.time())) + ".md"

f = open(save_filename, "w")
verbose_collect.sort(key=lambda x: x[0])
for info in verbose_collect:
    print("", info[0], info[1], info[4], info[3], "", "", sep=" | ", file=f)
f.close()

pickle.dump(verbose_collect, open("./verbose_collect.data", "wb"))
