/*
 Navicat Premium Data Transfer

 Source Server         : 本地_root
 Source Server Type    : MySQL
 Source Server Version : 80032
 Source Host           : localhost:3306
 Source Schema         : music163

 Target Server Type    : MySQL
 Target Server Version : 80032
 File Encoding         : 65001

 Date: 06/04/2023 10:18:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for m_album
-- ----------------------------
DROP TABLE IF EXISTS `m_album`;
CREATE TABLE `m_album`  (
  `id` bigint NOT NULL,
  `album_name` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '专辑名称',
  `publish_time` date NULL DEFAULT NULL COMMENT '发行时间',
  `publish_company` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发行公司',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_category
-- ----------------------------
DROP TABLE IF EXISTS `m_category`;
CREATE TABLE `m_category`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `target_id` bigint NOT NULL COMMENT '目标ID',
  `label` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标签名',
  `type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '0电台1歌单',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 260029 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '分类' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_comment
-- ----------------------------
DROP TABLE IF EXISTS `m_comment`;
CREATE TABLE `m_comment`  (
  `id` bigint NOT NULL,
  `type` tinyint NULL DEFAULT NULL COMMENT '0歌曲1mv2歌单',
  `target_id` bigint NULL DEFAULT NULL COMMENT '对应ID',
  `target_name` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '对应名称',
  `person_id` bigint NOT NULL COMMENT '评论者id',
  `person_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '评论者名字',
  `person_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '评论者头像',
  `create_day` datetime NULL DEFAULT NULL COMMENT '评论日期',
  `liked_count` int NOT NULL DEFAULT 0 COMMENT '点赞数',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '内容',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_djradio
-- ----------------------------
DROP TABLE IF EXISTS `m_djradio`;
CREATE TABLE `m_djradio`  (
  `id` bigint NOT NULL,
  `djradio_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '电台名称',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '电台封面',
  `create_person_id` bigint NULL DEFAULT NULL COMMENT '作者ID',
  `create_person_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '作者名称',
  `sub_count` int NOT NULL DEFAULT 0 COMMENT '订阅',
  `category_label` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '分类名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '描述',
  `program_count` int NOT NULL DEFAULT 0 COMMENT '节目期数',
  `create_day` datetime NULL DEFAULT NULL COMMENT '节目创建日期',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '电台' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_lyric
-- ----------------------------
DROP TABLE IF EXISTS `m_lyric`;
CREATE TABLE `m_lyric`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT,
  `song_id` bigint NOT NULL COMMENT '歌曲ID',
  `song_name` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '歌曲名称',
  `lrc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '歌词',
  `lrc_version` int NULL DEFAULT NULL COMMENT '歌词版本',
  `tlrc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '翻译歌词',
  `tlrc_version` int NULL DEFAULT NULL COMMENT '翻译歌词版本',
  `lyric_person_id` int NULL DEFAULT NULL COMMENT '贡献歌词用户ID',
  `lyric_person_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '贡献歌词用户名称',
  `trans_person_id` int NULL DEFAULT NULL COMMENT '翻译歌词用户ID',
  `trans_person_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '翻译歌词用户名称',
  `create_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 229391 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_mv
-- ----------------------------
DROP TABLE IF EXISTS `m_mv`;
CREATE TABLE `m_mv`  (
  `id` bigint NOT NULL,
  `mv_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'MV名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '简介',
  `duration` int NULL DEFAULT NULL COMMENT '时长',
  `image_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '封面url',
  `video_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '视频url',
  `play_count` int NOT NULL DEFAULT 0 COMMENT '播放次数',
  `publish_date` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `sub_count` int NOT NULL DEFAULT 0 COMMENT '收藏',
  `share_count` int NOT NULL DEFAULT 0 COMMENT '转发',
  `liked_count` int NOT NULL DEFAULT 0 COMMENT '点赞',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'MV' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_person
-- ----------------------------
DROP TABLE IF EXISTS `m_person`;
CREATE TABLE `m_person`  (
  `id` bigint NOT NULL,
  `person_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名字',
  `person_img_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '头像',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '性别',
  `birthday` datetime NULL DEFAULT NULL COMMENT '出生日期',
  `area` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属市区',
  `event_count` int NOT NULL DEFAULT 0 COMMENT '动态数',
  `follow_count` int NOT NULL DEFAULT 0 COMMENT '关注数',
  `fan_count` int NOT NULL DEFAULT 0 COMMENT '粉丝数',
  `user_type` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0普通用户，1歌手',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_playlist
-- ----------------------------
DROP TABLE IF EXISTS `m_playlist`;
CREATE TABLE `m_playlist`  (
  `id` bigint NOT NULL,
  `playlist_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '歌单名',
  `playlist_img_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '专辑图片',
  `create_user_id` bigint NOT NULL COMMENT '创建者ID',
  `create_user_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '创建者名字',
  `publish_time` date NULL DEFAULT NULL COMMENT '创建日期',
  `sub_count` int NOT NULL DEFAULT 0 COMMENT '收藏',
  `share_count` int NOT NULL DEFAULT 0 COMMENT '转发',
  `comment_count` int NOT NULL DEFAULT 0 COMMENT '评论',
  `play_count` int NOT NULL DEFAULT 0 COMMENT '播放次数',
  `description` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '介绍',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '歌单' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_program
-- ----------------------------
DROP TABLE IF EXISTS `m_program`;
CREATE TABLE `m_program`  (
  `id` bigint NOT NULL,
  `djradio_id` bigint NOT NULL COMMENT '电台ID',
  `order` int NOT NULL COMMENT '顺序',
  `program_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '节目名称',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '封面图片',
  `play_count` int NOT NULL DEFAULT 0 COMMENT '播放次数',
  `liked_count` int NOT NULL DEFAULT 0 COMMENT '点赞次数',
  `duration` int NULL DEFAULT NULL COMMENT '播放时长',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '描述',
  `create_day` datetime NOT NULL COMMENT '节目创建日期',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '电台节目' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_song
-- ----------------------------
DROP TABLE IF EXISTS `m_song`;
CREATE TABLE `m_song`  (
  `id` bigint NOT NULL,
  `song_name` varchar(400) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '歌曲名',
  `artist_id` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '歌手id，逗号隔开，冗余',
  `artist_name` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '歌手名，逗号隔开，冗余',
  `duration` int NULL DEFAULT NULL COMMENT '单位秒',
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '歌曲链接',
  `mv_id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '专辑ID',
  `publish_time` date NULL DEFAULT NULL COMMENT '发布日期',
  `album_id` int NULL DEFAULT 0 COMMENT '专辑ID',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `m_mv_id`(`mv_id` ASC) USING BTREE,
  INDEX `m_artist_id`(`artist_id` ASC) USING BTREE,
  INDEX `m_album_id`(`album_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '歌曲' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for m_song_play_list_relation
-- ----------------------------
DROP TABLE IF EXISTS `m_song_play_list_relation`;
CREATE TABLE `m_song_play_list_relation`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `song_id` bigint NOT NULL COMMENT '歌曲ID',
  `play_list_id` bigint NOT NULL COMMENT '歌单ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7218048 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
