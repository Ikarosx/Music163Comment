# Music163
爬取网抑云音乐热评，包含歌曲评论等

## 目标
递归爬取网易云歌曲~~以及取出1w点赞以上~~评论存到mysql

## 预准备
- 导入sql, music163.sql
- 修改settings.py中的mysql配置, MYSQL_URI
- 修改settings.py中的日志配置, LOG_LEVEL（如果需要写入文件可以开启LOG_FILE）
- 需要有proxy环境，如果没有(那就很快就会出现访问不了的情况)可以注释掉settings.py中DOWNLOADER_MIDDLEWARES的'Music163Spider.middlewares.ProxyMiddleware'
- 如果需要使用代理池，可以参考另一个项目[ProxyPool](https://github.com/jhao104/proxy_pool)

## 使用

```shell
cd Music163Spider
# 启动爬虫
scrapy crawl Music163 
# 启动爬虫并保存爬取状态
scrapy crawl Music163 -s JOBDIR=crawls/Music163
```

