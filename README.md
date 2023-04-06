# Music163
爬取网抑云音乐热评，包含歌曲评论等

## 目标
递归爬取网易云歌曲~~以及取出1w点赞以上~~评论存到mysql

## 预准备
- 导入sql, music163.sql
- 修改settings.py中的mysql配置

## 使用
```shell
cd Music163Spider
# 启动爬虫
scrapy crawl Music163 
# 启动爬虫并保存爬取状态
scrapy crawl Music163 -s JOBDIR=crawls/Music163
```

