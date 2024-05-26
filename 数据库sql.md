-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: stu_instru_management
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'username',
  `password` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'password',
  `phone` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'phone',
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'email',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` VALUES (1,'admin1','a6366adf2eef448dd906a30ea24135a7','13458769578','123@abc.com'),(9,'方任','0185cdb38869b36851067425ae7ccb81','19978066054','123@outlook.com'),(15,'admin3','59a5623f2076ab7f5dffd9c366ddcc3f','19978066054','123@outlook.com'),(16,'admin65','fcb7d7716d6d94098065b618d4a4c691','19978066054','123@outlook.com');

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lecture_id` int DEFAULT NULL COMMENT 'lecture_id',
  `title` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'title',
  `deadline` timestamp NULL DEFAULT NULL COMMENT 'deadline',
  `description` text COMMENT 'description',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'is_delete',
  PRIMARY KEY (`id`),
  KEY `lecture_id` (`lecture_id`),
  CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`lecture_id`) REFERENCES `lecture` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

INSERT INTO `assignment` VALUES (1,1,'期中作业','2024-06-17 07:29:10','尽快完成',0),(2,1,'期末作业','2024-07-17 11:23:41','可以延后',0),(3,1,'平时测试1','2024-04-25 00:36:39','编写课上布置的软件需求文档作业',1),(5,1,'平时测验5','2024-04-27 20:01:56','占期末成绩的5%',1),(6,8,'期末作业2','2024-05-27 00:26:38','编写课上布置的作业',1);

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'course_name',
  `description` varchar(256) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'description',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

INSERT INTO `course` VALUES (1,'高等数学A(1)','大类课'),(2,'离散数学','大类课'),(3,'编程能力提升','有趣，学习技术'),(6,'线性代数','线性代数高级课'),(7,'线性代数','线性代数高级课3');

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollment` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `level` int NOT NULL DEFAULT '0' COMMENT '"评分等级"',
  `academic_year` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'academic_year',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'status',
  `lecture_id` int NOT NULL COMMENT 'lecture_id',
  `student_id` int NOT NULL COMMENT '学生id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` VALUES (2,0,'秋季学期',1,2,1),(3,0,'秋季学期',1,1,2),(4,0,'秋季学期',1,8,1);

--
-- Table structure for table `feedback_detail`
--

DROP TABLE IF EXISTS `feedback_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `criteria` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '尺度',
  `comment` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT '教师评论',
  `score_sum` int NOT NULL DEFAULT '0' COMMENT '该项总分',
  `score_get` int DEFAULT '0' COMMENT '获得的分数',
  `submission_feedback_id` int NOT NULL COMMENT '关联的反馈表的id',
  PRIMARY KEY (`id`),
  KEY `feedback_detail_submission_feedback_id_fk` (`submission_feedback_id`),
  CONSTRAINT `feedback_detail_submission_feedback_id_fk` FOREIGN KEY (`submission_feedback_id`) REFERENCES `submission_feedback` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback_detail`
--

INSERT INTO `feedback_detail` VALUES (1,'Functionality','The software exceeds the specified requirements and performs itsintended functions exceptionally well.\n',10,8,2),(2,'Usability','The user interface is highly intuitive, user-friendly, and provides anexceptional user experience.',5,4,2),(3,'Performance','The software demonstrates outstanding efficiency andresponsiveness across all tasks and loads.',5,4,2),(4,'Adherence to project requirements','The software aligns perfectly with the project\'s defined scope,objectives, and constraints.',5,4,2),(5,'Sprint documentation quality','The documentation is thorough, meticulously organized, and exhibitsexcellent clarity and consistency.',10,8,2),(6,'Question response','The response meets or exceeds the word count requirement and iswell-structured, coherent, and engaging to read.',5,5,2);

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'username',
  `password` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'password',
  `phone` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'phone',
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'email',
  `department` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT 'department',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` VALUES (1,'小美','d04e6570081e7353a953f9316140cb34',NULL,NULL,'法学'),(2,'小红','e018e21da4568ddbb018f70cb9ebafbc',NULL,NULL,'计算机'),(4,'ins1','cd93b1ffd0917368554205852c7818bf','19978066054','123@outlook.com','信息学院');

--
-- Table structure for table `lecture`
--

DROP TABLE IF EXISTS `lecture`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecture` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` datetime DEFAULT NULL COMMENT 'time',
  `instructor_id` int NOT NULL COMMENT 'instructor_id ',
  `course_id` int NOT NULL COMMENT 'course_id',
  `is_delete` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'is_delete',
  `lecture_name` varchar(32) DEFAULT NULL,
  `course_name` varchar(32) NOT NULL,
  `status` int NOT NULL DEFAULT '0' COMMENT '教课评判状态',
  `academic_year` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecture`
--

INSERT INTO `lecture` VALUES (1,'2024-04-17 15:07:45',1,1,0,'高数2班','高等数学A(1)',0,'春季学期'),(2,'2024-04-17 15:07:49',2,2,0,'高数3班','高等数学A(2)',0,'春季学期'),(3,'2024-04-18 13:34:17',2,2,1,'高数4班','高等数学A(2)',1,'春季学期'),(5,'2024-04-18 06:15:22',1,2,1,'离散数学（1）班（一级课程班)','离散数学',1,'春季学期'),(6,'2024-04-18 06:15:22',1,2,1,'离散数学（2）班（一级课程班）','离散数学',1,'春季学期'),(8,'2024-04-18 14:10:59',1,2,1,'离散数学（4）班（一级课程班)','离散数学',1,'春季学期'),(9,'2024-04-21 03:54:42',1,2,0,'离散数学（2）班（二级课程班)','离散数学',1,'春季学期'),(11,'2024-05-20 16:20:57',1,2,0,'离散数学（1）班（二级课程班)','离散数学',0,'春季学期');

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '用户名',
  `password` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '密码',
  `phone` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'phone',
  `email` varchar(64) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'email',
  `major` varchar(16) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'major',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

INSERT INTO `student` VALUES (1,'小刚','1079e43547c7a3f894a721ed8cd1c2a2',NULL,NULL,'法学'),(2,'方任','a0ccd45711ced41fb131a1fc063ef51b','19978066054','123@outlook.com','软件工程'),(4,'方业','a6366adf2eef448dd906a30ea24135a7','19978066054','123@outlook.com','');

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lecture_id` int NOT NULL COMMENT 'lecture_id',
  `student_id` int NOT NULL COMMENT 'student_id',
  `title` varchar(32) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT 'title',
  `submit_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'submit_time',
  `description` text COMMENT 'description',
  `is_delete` tinyint(1) DEFAULT '0' COMMENT 'is_delete',
  PRIMARY KEY (`id`),
  KEY `submission_student_id_fk` (`student_id`),
  KEY `lecture_id` (`lecture_id`),
  CONSTRAINT `submission_ibfk_1` FOREIGN KEY (`lecture_id`) REFERENCES `lecture` (`id`),
  CONSTRAINT `submission_student_id_fk` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

INSERT INTO `submission` VALUES (8,1,1,'期中作业','2024-04-17 04:24:53','very good',0),(9,1,1,'期中作业','2024-04-17 04:25:20','132',0),(10,1,2,'平时测验1','2024-04-20 19:24:09','A+',0),(11,1,2,'期末作业','2024-05-20 03:31:58','666',0),(14,2,2,'期末作业2','2024-05-20 08:53:34','4',0),(15,5,2,'实验3','2024-05-20 08:54:23','good',0),(16,5,1,'实验2','2024-05-20 08:59:09','nice',0),(18,5,1,'实验2','2024-05-20 09:00:03','good',0),(19,5,1,'实验4','2023-05-20 09:04:13','666',0),(20,5,1,'实验1','2024-05-20 12:06:13','',0),(21,1,2,'期末作业','2024-05-20 12:07:06','666',0),(22,5,1,'实验15','2024-05-20 12:11:34','',0),(26,5,1,'实验15','2024-05-20 12:16:07','',0),(27,5,1,'实验15','2024-05-20 12:18:31','',0);

--
-- Table structure for table `submission_feedback`
--

DROP TABLE IF EXISTS `submission_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission_feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `submission_id` int NOT NULL,
  `title_information` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL COMMENT '标题信息',
  `score_total` int NOT NULL DEFAULT '40' COMMENT '总分数',
  `score_get` int DEFAULT NULL COMMENT '获得的总分',
  `provisional_total` double NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `submission_id` (`submission_id`),
  CONSTRAINT `submission_id` FOREIGN KEY (`submission_id`) REFERENCES `submission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission_feedback`
--

INSERT INTO `submission_feedback` VALUES (1,27,'Spring 2024',40,33,0.825),(2,21,'Spring 2024 Final Exam To Student 20211060063',40,33,0.825);
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-26 17:02:41
