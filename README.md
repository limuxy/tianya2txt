tianya2txt 
==========

天涯帖子脱水脚本,保存成txt, 方便阅读

##版本
v0.1.1

##用途
保存脱水后的天涯帖子到txt文件

##用法
依赖python2

依赖BeautifulSoup4，所以需要先`pip install beautifulsoup4`

clone或直接下载后：`chmod +x tianya2txt.py`

运行： `./tianya2txt.py`

输入天涯帖子地址，比如http://bbs.tianya.cn/post-16-1008143-1.shtml

##说明
如果输入的地址不是第一页，则会从该页开始获取。

txt文件最后会显示获取到的最新楼层，方便以后更新

默认设置了4个线程

##更新记录
###2014-08-06
第一个版本
###2014-08-07
添加了.gitignore文件，调整了txt排版