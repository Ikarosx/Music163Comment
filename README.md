# Music163Comment
爬取网抑云音乐热评

## 目标
递归爬取网易云歌曲以及取出1w点赞以上评论存到mongodb

## 使用
```shell
# Music163Spider/Music163Spider目录下
scrapy crawl HotComment 
# 暂时中断
scrapy crawl HotComment -s JOBDIR=crawls/HotComment
```

