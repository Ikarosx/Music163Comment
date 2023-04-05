# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from sqlalchemy import Column, String, create_engine, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


#
class MAlbumItem(scrapy.Item):
    id = scrapy.Field()
    # 专辑名称
    album_name = scrapy.Field()
    # 发行时间
    publish_time = scrapy.Field()
    # 发行公司
    publish_company = scrapy.Field()

    create_time = scrapy.Field()


# MAlbum mysql Entity
class MAlbumMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_album'

    id = Column(Integer, primary_key=True)

    # 专辑名称
    album_name = Column(String)

    # 发行时间
    publish_time = Column(Date)

    # 发行公司
    publish_company = Column(String)

    create_time = Column(Date)


# 分类
class MCategoryItem(scrapy.Item):
    id = scrapy.Field()
    # 标签名
    label = scrapy.Field()
    target_id = scrapy.Field()
    type = scrapy.Field()



# MCategory mysql Entity
class MCategoryMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_category'

    id = Column(Integer, primary_key=True)

    # 标签名
    label = Column(String)
    target_id = Column(Integer)
    type = Column(Integer)


#
class MCommentItem(scrapy.Item):
    id = scrapy.Field()
    # 0歌曲1mv2歌单
    type = scrapy.Field()
    # 对应ID
    target_id = scrapy.Field()
    # 对应名称
    target_name = scrapy.Field()
    # 评论者id
    person_id = scrapy.Field()
    # 评论者名字
    person_name = scrapy.Field()
    # 评论者头像
    person_url = scrapy.Field()
    # 评论日期
    create_day = scrapy.Field()
    # 点赞数
    liked_count = scrapy.Field()
    # 内容
    content = scrapy.Field()

    create_time = scrapy.Field()


# MComment mysql Entity
class MCommentMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_comment'

    id = Column(Integer, primary_key=True)

    # 0歌曲1mv2歌单
    type = Column(Integer)

    # 对应ID
    target_id = Column(Integer)

    # 对应名称
    target_name = Column(String)

    # 评论者id
    person_id = Column(Integer)

    # 评论者名字
    person_name = Column(String)

    # 评论者头像
    person_url = Column(String)

    # 评论日期
    create_day = Column(Date)

    # 点赞数
    liked_count = Column(Integer)

    # 内容
    content = Column(String)

    create_time = Column(Date)


#
class MLyricItem(scrapy.Item):
    id = scrapy.Field()
    # 歌曲ID
    song_id = scrapy.Field()
    # 歌曲名称
    song_name = scrapy.Field()
    # 歌词
    lrc = scrapy.Field()
    # 歌词版本
    lrc_version = scrapy.Field()
    # 翻译歌词
    tlrc = scrapy.Field()
    # 翻译歌词版本
    tlrc_version = scrapy.Field()
    # 贡献歌词用户ID
    lyric_person_id = scrapy.Field()
    # 贡献歌词用户名称
    lyric_person_name = scrapy.Field()
    # 翻译歌词用户ID
    trans_person_id = scrapy.Field()
    # 翻译歌词用户名称
    trans_person_name = scrapy.Field()

    create_time = scrapy.Field()


# MLyric mysql Entity
class MLyricMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_lyric'

    id = Column(Integer, primary_key=True)

    # 歌曲ID
    song_id = Column(Integer)

    # 歌曲名称
    song_name = Column(String)

    # 歌词
    lrc = Column(String)

    # 歌词版本
    lrc_version = Column(Integer)

    # 翻译歌词
    tlrc = Column(String)

    # 翻译歌词版本
    tlrc_version = Column(Integer)

    # 贡献歌词用户ID
    lyric_person_id = Column(Integer)

    # 贡献歌词用户名称
    lyric_person_name = Column(String)

    # 翻译歌词用户ID
    trans_person_id = Column(Integer)

    # 翻译歌词用户名称
    trans_person_name = Column(String)

    create_time = Column(Date)


# MV
class MMvItem(scrapy.Item):
    id = scrapy.Field()
    # MV名称
    mv_name = scrapy.Field()
    # 简介
    description = scrapy.Field()
    # 播放次数
    play_count = scrapy.Field()
    # 发布时间
    publish_date = scrapy.Field()
    # 收藏
    sub_count = scrapy.Field()
    # 播放时长
    duration = scrapy.Field()
    # 转发
    share_count = scrapy.Field()
    # 点赞
    liked_count = scrapy.Field()
    # video
    video_url = scrapy.Field()
    # image
    image_url = scrapy.Field()

    create_time = scrapy.Field()


# MMv mysql Entity
class MMvMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_mv'

    id = Column(Integer, primary_key=True)

    # MV名称
    mv_name = Column(String)

    # 简介
    description = Column(String)

    # 播放时长
    duration = Column(Integer)

    # 视频
    video_url = Column(String)

    # 封面
    image_url = Column(String)

    # 播放次数
    play_count = Column(Integer)

    # 发布时间
    publish_date = Column(Date)

    # 收藏
    sub_count = Column(Integer)

    # 转发
    share_count = Column(Integer)

    # 点赞
    liked_count = Column(Integer)

    create_time = Column(Date)


# 用户
class MPersonItem(scrapy.Item):
    id = scrapy.Field()
    # 名字
    person_name = scrapy.Field()
    # 头像
    person_img_url = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 动态
    event_count = scrapy.Field()
    # 关注
    follow_count = scrapy.Field()
    # 年龄
    birthday = scrapy.Field()
    # 所属市区
    area = scrapy.Field()
    # 粉丝
    fan_count = scrapy.Field()
    # 0未认证，1认证
    verify = scrapy.Field()
    # 0普通用户，1歌手
    user_type = scrapy.Field()

    create_time = scrapy.Field()


# MPerson mysql Entity
class MPersonMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_person'

    id = Column(Integer, primary_key=True)

    # 名字
    person_name = Column(String)

    # 性别
    gender = Column(Integer)

    # 头像
    person_img_url = Column(String)

    # 年龄
    birthday = Column(String)

    # 所属市区
    area = Column(String)

    # 动态
    event_count = Column(Integer)
    # 关注
    follow_count = Column(Integer)

    # 粉丝
    fan_count = Column(Integer)

    # 0普通用户，1歌手
    user_type = Column(Integer)

    create_time = Column(Date)


# 歌单
class MPlaylistItem(scrapy.Item):
    id = scrapy.Field()
    # 歌单名
    playlist_name = scrapy.Field()
    # 专辑图片
    playlist_img_url = scrapy.Field()
    # 创建者ID
    create_user_id = scrapy.Field()
    # 创建者名字
    create_user_name = scrapy.Field()
    # 创建日期
    publish_time = scrapy.Field()
    # 收藏
    sub_count = scrapy.Field()
    # 转发
    share_count = scrapy.Field()
    # 评论
    comment_count = scrapy.Field()
    # 播放次数
    play_count = scrapy.Field()
    # 介绍
    description = scrapy.Field()

    create_time = scrapy.Field()


# MPlaylist mysql Entity
class MPlaylistMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_playlist'

    id = Column(Integer, primary_key=True)

    # 歌单名
    playlist_name = Column(String)

    # 专辑图片
    playlist_img_url = Column(String)

    # 创建者ID
    create_user_id = Column(Integer)

    # 创建者名字
    create_user_name = Column(String)

    # 创建日期
    publish_time = Column(Date)

    # 收藏
    sub_count = Column(Integer)

    # 转发
    share_count = Column(Integer)

    # 评论
    comment_count = Column(Integer)

    # 播放次数
    play_count = Column(Integer)

    # 介绍
    description = Column(String)

    create_time = Column(Date)


# 歌曲
class MSongItem(scrapy.Item):
    id = scrapy.Field()
    # 歌曲名
    song_name = scrapy.Field()
    # 歌手id，逗号隔开，冗余
    artist_id = scrapy.Field()
    # 歌手名，逗号隔开，冗余
    artist_name = scrapy.Field()
    # 单位秒
    duration = scrapy.Field()
    # 歌曲链接
    url = scrapy.Field()
    # 专辑ID
    mv_id = scrapy.Field()
    # 发布日期
    publish_time = scrapy.Field()
    # 专辑ID
    album_id = scrapy.Field()

    create_time = scrapy.Field()

# 更新歌曲下载链接
class MSongUrlItem(scrapy.Item):
    id = scrapy.Field()

    url = scrapy.Field()


# MSong mysql Entity
class MSongMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_song'

    id = Column(Integer, primary_key=True)

    # 歌曲名
    song_name = Column(String)

    # 歌手id，逗号隔开，冗余
    artist_id = Column(String)

    # 歌手名，逗号隔开，冗余
    artist_name = Column(String)

    # 单位秒
    duration = Column(Integer)

    # 歌曲链接
    url = Column(String)

    # 专辑ID
    mv_id = Column(String)

    # 发布日期
    publish_time = Column(Date)

    # 专辑ID
    album_id = Column(Integer)

    create_time = Column(Date)


# 更新歌曲下载链接
class MSongPlayListItem(scrapy.Item):
    id = scrapy.Field()

    song_id = scrapy.Field()
    play_list_id = scrapy.Field()


# MSong mysql Entity
class MSongPlayListMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_song_play_list_relation'

    id = Column(Integer, primary_key=True)

    song_id = Column(Integer)
    play_list_id = Column(Integer)


class MDjradioItem(scrapy.Item):
    id = scrapy.Field()
    # 电台名称
    djradio_name = scrapy.Field()
    # 电台封面
    cover_url = scrapy.Field()
    # 作者ID
    create_person_id = scrapy.Field()
    # 作者名称
    create_person_name = scrapy.Field()
    # 订阅
    sub_count = scrapy.Field()
    # 分类
    category_label = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 节目期数
    program_count = scrapy.Field()
    # 节目创建日期
    create_day = scrapy.Field()

    create_time = scrapy.Field()


# MDjradio mysql Entity
class MDjradioMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_djradio'

    id = Column(Integer, primary_key=True)

    # 电台名称
    djradio_name = Column(String)

    # 电台封面
    cover_url = Column(String)

    # 作者ID
    create_person_id = Column(Integer)

    # 作者名称
    create_person_name = Column(String)

    # 订阅
    sub_count = Column(Integer)

    # 分类
    category_label = Column(String)

    # 描述
    description = Column(String)

    # 节目期数
    program_count = Column(Integer)

    # 节目创建日期
    create_day = Column(Date)

    create_time = Column(Date)


# 电台节目
class MProgramItem(scrapy.Item):
    id = scrapy.Field()
    # 电台ID
    djradio_id = scrapy.Field()
    # 顺序
    order = scrapy.Field()
    # 节目名称
    program_name = scrapy.Field()
    # 封面图片
    cover_url = scrapy.Field()
    # 播放次数
    play_count = scrapy.Field()
    # 点赞次数
    liked_count = scrapy.Field()
    # 播放时长
    duration = scrapy.Field()
    # 描述
    description = scrapy.Field()
    # 节目创建日期
    create_day = scrapy.Field()

    create_time = scrapy.Field()


# MProgram mysql Entity
class MProgramMysqlEntity(Base):
    # 表名
    __tablename__ = 'm_program'

    id = Column(Integer, primary_key=True)

    # 电台ID
    djradio_id = Column(Integer)

    # 顺序
    order = Column(Integer)

    # 节目名称
    program_name = Column(String)

    # 封面图片
    cover_url = Column(String)

    # 播放次数
    play_count = Column(Integer)

    # 点赞次数
    liked_count = Column(Integer)

    # 播放时长
    duration = Column(Integer)

    # 描述
    description = Column(String)

    # 节目创建日期
    create_day = Column(Date)

    create_time = Column(Date)