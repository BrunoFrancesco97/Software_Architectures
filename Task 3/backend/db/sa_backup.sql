-- MariaDB dump 10.18  Distrib 10.4.17-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sa
-- ------------------------------------------------------
-- Server version	10.4.17-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `assignments`
--

DROP TABLE IF EXISTS `assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  `creation` timestamp NOT NULL DEFAULT current_timestamp(),
  `course` varchar(40) NOT NULL,
  `deadline` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `course` (`course`),
  CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`course`) REFERENCES `courses` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments`
--

LOCK TABLES `assignments` WRITE;
/*!40000 ALTER TABLE `assignments` DISABLE KEYS */;
INSERT INTO `assignments` VALUES (6,'task_1','2022-11-28 10:53:11','Software_Architectures','2023-04-12 14:45:00'),(7,'task_2','2022-11-28 10:54:08','Software_Architectures','2023-04-12 14:45:00'),(14,'test_3','2022-12-01 14:40:17','Software_Architectures','2022-07-14 10:30:00');
/*!40000 ALTER TABLE `assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel_subscriptions`
--

DROP TABLE IF EXISTS `channel_subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channel_subscriptions` (
  `channel` int(11) NOT NULL,
  `user` varchar(40) NOT NULL,
  `subscription` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`channel`,`user`),
  KEY `user` (`user`),
  CONSTRAINT `channel_subscriptions_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `channels` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `channel_subscriptions_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel_subscriptions`
--

LOCK TABLES `channel_subscriptions` WRITE;
/*!40000 ALTER TABLE `channel_subscriptions` DISABLE KEYS */;
INSERT INTO `channel_subscriptions` VALUES (13,'test','2022-11-24 21:52:18'),(16,'francym4@gmail.com','2022-11-30 12:40:37'),(16,'prova@gmail.com','2022-11-28 10:55:40'),(16,'test@gmail.com','2022-11-30 12:44:38');
/*!40000 ALTER TABLE `channel_subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channels`
--

DROP TABLE IF EXISTS `channels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `channels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channels`
--

LOCK TABLES `channels` WRITE;
/*!40000 ALTER TABLE `channels` DISABLE KEYS */;
INSERT INTO `channels` VALUES (13,'test1'),(16,'cafoscari');
/*!40000 ALTER TABLE `channels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_subscriptions`
--

DROP TABLE IF EXISTS `course_subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_subscriptions` (
  `course` varchar(40) NOT NULL,
  `user` varchar(40) NOT NULL,
  `subscription` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`course`,`user`),
  KEY `user` (`user`),
  CONSTRAINT `course_subscriptions_ibfk_1` FOREIGN KEY (`course`) REFERENCES `courses` (`name`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `course_subscriptions_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_subscriptions`
--

LOCK TABLES `course_subscriptions` WRITE;
/*!40000 ALTER TABLE `course_subscriptions` DISABLE KEYS */;
INSERT INTO `course_subscriptions` VALUES ('Software Developmente Methodologies','test','2022-11-24 22:46:30'),('Software_Architectures','francym4@gmail.com','2022-11-30 12:42:11'),('Software_Architectures','prova@gmail.com','2022-11-28 10:57:10'),('Software_Architectures','test@gmail.com','2022-11-30 12:44:54');
/*!40000 ALTER TABLE `course_subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `name` varchar(40) NOT NULL,
  `channel` int(11) NOT NULL,
  PRIMARY KEY (`name`),
  KEY `channel` (`channel`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`channel`) REFERENCES `channels` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('Software Architectures',13),('Software Developmente Methodologies',13),('Software_Architectures',16);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exercises`
--

DROP TABLE IF EXISTS `exercises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exercises` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quest` varchar(255) NOT NULL,
  `correct` varchar(255) DEFAULT NULL,
  `wrong1` varchar(255) DEFAULT NULL,
  `wrong2` varchar(255) DEFAULT NULL,
  `wrong3` varchar(255) DEFAULT NULL,
  `assignment` int(11) NOT NULL,
  `type` enum('multiple','open','develop','quiz') NOT NULL DEFAULT 'develop',
  PRIMARY KEY (`id`),
  KEY `assignment` (`assignment`),
  CONSTRAINT `exercises_ibfk_2` FOREIGN KEY (`assignment`) REFERENCES `assignments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exercises`
--

LOCK TABLES `exercises` WRITE;
/*!40000 ALTER TABLE `exercises` DISABLE KEYS */;
INSERT INTO `exercises` VALUES (7,'Sviluppa un programma che mi ritorni hello world','hello world',NULL,NULL,NULL,6,'develop'),(13,'Scrivi una funzione che dato in input un numero mi stampa 1 se è pari, 0 se è dispari',NULL,NULL,NULL,NULL,14,'develop');
/*!40000 ALTER TABLE `exercises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
  `name` varchar(255) NOT NULL,
  `course` varchar(40) NOT NULL,
  PRIMARY KEY (`name`,`course`),
  KEY `course` (`course`),
  CONSTRAINT `files_ibfk_1` FOREIGN KEY (`course`) REFERENCES `courses` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES ('List_4_1.pdf','Software_Architectures'),('List_8_1.pdf','Software_Architectures');
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `results` (
  `assignment` int(11) NOT NULL,
  `user` varchar(40) NOT NULL,
  `subscription` timestamp NOT NULL DEFAULT current_timestamp(),
  `result` int(11) DEFAULT NULL CHECK (`result` >= 0 and `result` <= 100),
  `comment` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `assignment` (`assignment`),
  KEY `user` (`user`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`assignment`) REFERENCES `assignments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES (14,'francym4@gmail.com','2022-12-01 15:46:49',100,NULL,43);
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `solution` (
  `exercise` int(11) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `user` varchar(40) NOT NULL,
  `correct` tinyint(1) DEFAULT 0,
  `hash` varchar(255) NOT NULL,
  `review` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`exercise`,`user`),
  KEY `user` (`user`),
  CONSTRAINT `solution_ibfk_1` FOREIGN KEY (`exercise`) REFERENCES `exercises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `solution_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (7,'print(\"ciao\")','prova@gmail.com',0,'120fde05c487848e306da1d5f258c1f5c2a915868c42b8dcedbec9e75a385d1c',1),(13,'\r\nimport sys \r\n\r\ndef parity():\r\n    if len(sys.argv) == 2:\r\n        if int(sys.argv[1]) % 2 == 0:\r\n            print(\"1\")\r\n        else:\r\n            print(\"0\")\r\n\r\nif __name__ == \'__main__\':\r\n    parity()','francym4@gmail.com',1,'704569818c4e4e804a46842594aa5a44e5419edfd440270ea6876ff1ecfaf915',1);
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supports`
--

DROP TABLE IF EXISTS `supports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supports` (
  `sender` varchar(40) NOT NULL,
  `receiver` varchar(40) NOT NULL,
  `object` varchar(40) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `sender` (`sender`),
  KEY `receiver` (`receiver`),
  CONSTRAINT `supports_ibfk_1` FOREIGN KEY (`sender`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `supports_ibfk_2` FOREIGN KEY (`receiver`) REFERENCES `user` (`email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supports`
--

LOCK TABLES `supports` WRITE;
/*!40000 ALTER TABLE `supports` DISABLE KEYS */;
/*!40000 ALTER TABLE `supports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `comment` varchar(60) DEFAULT NULL,
  `exercise` int(11) DEFAULT NULL,
  `given_value` varchar(255) NOT NULL,
  `expected` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exercise` (`exercise`),
  CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`exercise`) REFERENCES `exercises` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (1,'test_1','Test if number',7,'10',''),(2,'Check 10',NULL,13,'10','1'),(3,'Check 11',NULL,13,'11','0');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `email` varchar(40) NOT NULL,
  `password` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `surname` varchar(40) DEFAULT NULL,
  `role` enum('user','staff','admin') NOT NULL DEFAULT 'user',
  `creation` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('francym4@gmail.com','5d61da0b40b87c0f4b218248c109c0bf204923118b9b90e951b170a8b8908b49','5AESAPXBKAM735X5S5CRU9F8JE5PG3','Francesco','Bruno','admin','2022-11-30 12:27:42'),('prova@gmail.com','de915337ef8f0a42a1b7175ab0616340bb9f85893396ba42280c568958fed6f2','Z399EOG0DXAH3AKNPHNIK42U7HX6JF','provaN','provaS','user','2022-11-28 10:05:26'),('test','1920f14b515e4a580bdd7e187406684928f2c7950a0b10cc7b29248c30cff842','GRJUUKFRCAKHTH2Y7WV69XL3N726Q8','Francesco','Bruno','user','2022-11-07 19:32:37'),('test@gmail.com','6a05035a9946de88700ce75a662d74e62b0457bc79fa0f203605e492ab5e71f6','ZI7TQTOYRZ3H8GUUYF9FTIP23QCSI4','Andrea','Bruno','user','2022-11-30 12:31:15');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-02  9:41:48
