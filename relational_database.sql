/*
 Navicat Premium Data Transfer

 Source Server         : LocalMySQL
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3306
 Source Schema         : relational_databases_new

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date: 17/12/2022 21:11:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for actor
-- ----------------------------
DROP TABLE IF EXISTS `actor`;
CREATE TABLE `actor`  (
  `actor_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `star_movie_num` int NOT NULL,
  `act_movie_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`actor_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for actor_movie
-- ----------------------------
DROP TABLE IF EXISTS `actor_movie`;
CREATE TABLE `actor_movie`  (
  `movie_id` bigint NOT NULL,
  `actor_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_star` tinyint(1) NULL DEFAULT NULL COMMENT '当前演员是否是当前电影的主演',
  PRIMARY KEY (`movie_id`, `actor_name`) USING BTREE,
  INDEX `actor_name`(`actor_name` ASC) USING BTREE,
  INDEX `actor_name_2`(`actor_name` ASC, `is_star` ASC) USING BTREE,
  CONSTRAINT `actor_movie_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `actor_movie_fk1` FOREIGN KEY (`actor_name`) REFERENCES `actor` (`actor_name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `comment_id` bigint NOT NULL,
  `one_star_num` int NULL DEFAULT NULL,
  `two_star_num` int NULL DEFAULT NULL,
  `three_star_num` int NULL DEFAULT NULL,
  `four_star_num` int NULL DEFAULT NULL,
  `five_star_num` int NULL DEFAULT NULL,
  `comment_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`comment_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for director
-- ----------------------------
DROP TABLE IF EXISTS `director`;
CREATE TABLE `director`  (
  `director_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `direct_movie_num` int NOT NULL,
  PRIMARY KEY (`director_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for director_movie
-- ----------------------------
DROP TABLE IF EXISTS `director_movie`;
CREATE TABLE `director_movie`  (
  `movie_id` bigint NOT NULL,
  `director_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`movie_id`, `director_name`) USING BTREE,
  INDEX `director_movie_fk1`(`director_name` ASC) USING BTREE,
  CONSTRAINT `director_movie_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `director_movie_fk1` FOREIGN KEY (`director_name`) REFERENCES `director` (`director_name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for genre
-- ----------------------------
DROP TABLE IF EXISTS `genre`;
CREATE TABLE `genre`  (
  `genre_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `movie_num` int NOT NULL,
  PRIMARY KEY (`genre_title`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for genre_movie
-- ----------------------------
DROP TABLE IF EXISTS `genre_movie`;
CREATE TABLE `genre_movie`  (
  `movie_id` bigint NOT NULL,
  `genre_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`movie_id`, `genre_title`) USING BTREE,
  INDEX `genre_movie_fk1`(`genre_title` ASC) USING BTREE,
  INDEX `movie_id`(`movie_id` ASC) USING BTREE,
  CONSTRAINT `genre_movie_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `genre_movie_fk1` FOREIGN KEY (`genre_title`) REFERENCES `genre` (`genre_title`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie`  (
  `movie_id` bigint NOT NULL,
  `movie_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time_id` bigint NULL DEFAULT NULL,
  `comment_id` bigint NULL DEFAULT NULL,
  `score` float NULL DEFAULT NULL,
  `star_num` int NULL DEFAULT NULL,
  `actor_num` int NULL DEFAULT NULL,
  `director_num` int NULL DEFAULT NULL,
  `comment_num` int NULL DEFAULT NULL,
  `product_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`movie_id`) USING BTREE,
  UNIQUE INDEX `move_id`(`movie_id` ASC) USING BTREE,
  INDEX `movie_fk0`(`time_id` ASC) USING BTREE,
  INDEX `movie_fk1`(`comment_id` ASC) USING BTREE,
  INDEX `score`(`score` ASC) USING BTREE,
  INDEX `movie_title`(`movie_title` ASC) USING BTREE,
  CONSTRAINT `movie_fk0` FOREIGN KEY (`time_id`) REFERENCES `time` (`time_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `movie_fk1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS `product`;
CREATE TABLE `product`  (
  `product_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `movie_id` bigint NULL DEFAULT NULL,
  `source` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`product_id`) USING BTREE,
  INDEX `product_fk0`(`movie_id` ASC) USING BTREE,
  CONSTRAINT `product_fk0` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`movie_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for time
-- ----------------------------
DROP TABLE IF EXISTS `time`;
CREATE TABLE `time`  (
  `time_id` bigint NOT NULL,
  `year` smallint NULL DEFAULT NULL,
  `month` tinyint NULL DEFAULT NULL,
  `season` tinyint NULL DEFAULT NULL,
  `dateday` tinyint NULL DEFAULT NULL,
  `weekday` tinyint NULL DEFAULT NULL,
  PRIMARY KEY (`time_id`) USING BTREE,
  INDEX `year`(`year` ASC) USING BTREE,
  INDEX `season`(`season` ASC) USING BTREE,
  INDEX `month`(`month` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for time_month
-- ----------------------------
DROP TABLE IF EXISTS `time_month`;
CREATE TABLE `time_month`  (
  `year` smallint NOT NULL,
  `month` tinyint NOT NULL,
  `release_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`year`, `month`) USING BTREE,
  INDEX `month`(`month` ASC) USING BTREE,
  INDEX `year`(`year` ASC, `month` ASC) USING BTREE,
  CONSTRAINT `time_month_ibfk_1` FOREIGN KEY (`year`) REFERENCES `time` (`year`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `time_month_ibfk_2` FOREIGN KEY (`month`) REFERENCES `time` (`month`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for time_season
-- ----------------------------
DROP TABLE IF EXISTS `time_season`;
CREATE TABLE `time_season`  (
  `year` smallint NOT NULL,
  `season` tinyint NOT NULL,
  `release_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`season`, `year`) USING BTREE,
  INDEX `year`(`year` ASC) USING BTREE,
  INDEX `year_2`(`year` ASC, `season` ASC) USING BTREE,
  CONSTRAINT `time_season_ibfk_1` FOREIGN KEY (`year`) REFERENCES `time` (`year`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `time_season_ibfk_2` FOREIGN KEY (`season`) REFERENCES `time` (`season`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for time_year
-- ----------------------------
DROP TABLE IF EXISTS `time_year`;
CREATE TABLE `time_year`  (
  `year` smallint NOT NULL,
  `release_num` int NULL DEFAULT NULL,
  PRIMARY KEY (`year`) USING BTREE,
  CONSTRAINT `time_year_ibfk_1` FOREIGN KEY (`year`) REFERENCES `time` (`year`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
