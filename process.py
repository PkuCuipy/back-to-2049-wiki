import pickle
from namedlist import namedlist
import re
import time

# [0] 发布日期
# [1] 视频标题
# [2] 视频 BV 号
# [3] 视频时长
# [4] 视频链接
verbose_collect = pickle.load(open("./verbose_collect.data", "rb"))

# 具名化
Info = namedlist("Info", ["date", "title", "duration", "link", "type", "id", "series"])
infos = []
for info in verbose_collect:
    named_info = Info(info[0], info[1], info[3], info[4], "", "", "")
    infos.append(named_info)


for info in infos:

    if info.title.startswith("【回到2049】"):
        info.title = info.title[8:]
        info.type = "长篇"

    if info.title.startswith("【2049日报】"):
        info.title = info.title[8:]
        # info.type = "日报"

    # 提取 "SxxExx" 格式的编号 (if exists)
    if result := re.findall("(S\d+E\d+)", info.title):
        SxxExx = result[0]
        info.title = info.title.replace(SxxExx, "").strip()
        # info.id = SxxExx

    # 提取 "【XXX】" 格式的系列名 (if exists)
    if result := re.findall("(【.*】)", info.title):
        series = result[0]
        info.title = info.title.replace(series, "").strip()
        info.series = series[1:-1]

    # 提取 "XXX：" 格式的系列名 (if exists)
    if result := re.findall("^(.*：)", info.title):
        series = result[0]
        # info.title = info.title.replace(series, "").strip()   # 以冒号标注的系列名会参与标题的构成, 因此不去除
        info.series = series[0:-1]

    # 限制标题长度 <= 18
    info.title = info.title[:18]
    # # 18 的由来:
    # import matplotlib.pyplot as plt
    # lengths = list(map(lambda info: len(info.title), infos))
    # plt.hist(lengths, bins=max(lengths))
    # plt.show()

    # 限制标题长度 <= 10
    info.series = info.series[:10]
    # # 10 的由来:
    # import matplotlib.pyplot as plt
    # lengths = list(map(lambda info: len(info.series), infos))
    # plt.hist(lengths, bins=max(lengths))
    # plt.show()

    # 把链接合并到标题上...
    info.link = f"[{info.title}]" + info.link[14:]


for info in infos:
    print(info)

save_filename = "./" + time.strftime("%Y-%m-%d(%H.%M.%S)", time.localtime(time.time())) + ".md"
with open(save_filename, "w") as f:
    # ["date", "title", "link", "duration", "type", "id", "series"]
    print("""| **日期** | **标题** | **时长** | **系列** | **备注** |\n"""
          """| :-----: | :------- | :-----: | :------: |:-----: |""", file=f)
    for info in infos:
        print(info.date, info.link, info.duration, info.series, info.type, sep=" | ", file=f)





