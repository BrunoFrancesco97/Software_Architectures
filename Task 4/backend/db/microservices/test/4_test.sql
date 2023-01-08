
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
  KEY `exercise` (`exercise`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (55,'Checking 10',NULL,34,'10','1'),(56,'Checking 11',NULL,34,'11','0'),(57,'Checking 1',NULL,34,'1','0'),(58,'Checking 0',NULL,34,'0','1');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;
