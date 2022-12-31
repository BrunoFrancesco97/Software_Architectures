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
INSERT INTO `user` VALUES ('dorigo@gmail.com','91cb1f7f26e53e0cdf0dee01af5b2674a4c5cd08857fb907657ce99e81df9e49','V1XULKIU4NC73ZD3NBGKCK7BEUNMFP','Andrea','Dorigo','admin','2022-12-04 18:39:06'),('francym4@gmail.com','5d61da0b40b87c0f4b218248c109c0bf204923118b9b90e951b170a8b8908b49','5AESAPXBKAM735X5S5CRU9F8JE5PG3','Francesco','Bruno','admin','2022-11-30 12:27:42'),('prova@gmail.com','de915337ef8f0a42a1b7175ab0616340bb9f85893396ba42280c568958fed6f2','Z399EOG0DXAH3AKNPHNIK42U7HX6JF','provaN','provaS','user','2022-11-28 10:05:26'),('test','1920f14b515e4a580bdd7e187406684928f2c7950a0b10cc7b29248c30cff842','GRJUUKFRCAKHTH2Y7WV69XL3N726Q8','Francesco','Bruno','user','2022-11-07 19:32:37'),('test@gmail.com','6a05035a9946de88700ce75a662d74e62b0457bc79fa0f203605e492ab5e71f6','ZI7TQTOYRZ3H8GUUYF9FTIP23QCSI4','Andrea','Bruno','user','2022-11-30 12:31:15');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-04 22:26:52