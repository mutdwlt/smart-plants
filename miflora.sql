-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: miflora
-- ------------------------------------------------------
-- Server version	5.5.54-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `plants_info`
--

DROP TABLE IF EXISTS `plants_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plants_info` (
  `mac_address` varchar(20) DEFAULT NULL,
  `plants_name` varchar(100) DEFAULT NULL,
  `sun_bottom` int(11) DEFAULT NULL,
  `sun_top` int(11) DEFAULT NULL,
  `moi_bottom` int(11) DEFAULT NULL,
  `moi_top` int(11) DEFAULT NULL,
  `tem_bottom` float DEFAULT NULL,
  `tem_top` float DEFAULT NULL,
  `fer_bottom` int(11) DEFAULT NULL,
  `fer_top` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL DEFAULT '0',
  `baterry` int(11) DEFAULT NULL,
  `firmware` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plants_info`
--

LOCK TABLES `plants_info` WRITE;
/*!40000 ALTER TABLE `plants_info` DISABLE KEYS */;
INSERT INTO `plants_info` VALUES ('C4:7C:8D:60:93:25','cây cẩm nhung',1200,3300,15,20,20,35,350,2000,1,100,'2.6.');
/*!40000 ALTER TABLE `plants_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_data`
--

DROP TABLE IF EXISTS `sensor_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sunlight` int(11) DEFAULT NULL,
  `moisture` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `fertility` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=211 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_data`
--

LOCK TABLES `sensor_data` WRITE;
/*!40000 ALTER TABLE `sensor_data` DISABLE KEYS */;
INSERT INTO `sensor_data` VALUES (2,0,0,0,0,'2017-05-24 23:57:39'),(3,0,0,0,0,'2017-05-25 04:56:48'),(4,0,0,0,0,'2017-05-25 05:58:24'),(5,0,0,0,0,'2017-05-25 07:51:20'),(6,0,0,0,0,'2017-05-25 08:52:56'),(7,0,0,0,0,'2017-05-25 09:50:59'),(8,0,0,0,0,'2017-05-25 11:50:06'),(9,0,0,0,0,'2017-05-25 12:50:32'),(10,0,0,0,0,'2017-05-25 12:52:18'),(11,0,0,0,0,'2017-05-25 12:54:04'),(12,0,0,0,0,'2017-05-25 12:55:50'),(13,0,0,0,0,'2017-05-25 12:57:36'),(14,0,0,0,0,'2017-05-25 12:59:22'),(15,0,0,0,0,'2017-05-26 03:53:37'),(16,0,0,0,0,'2017-05-26 03:55:25'),(17,21,1,29,0,'2017-05-26 03:57:13'),(18,13,1,28,0,'2017-05-26 03:58:46'),(19,0,1,28,0,'2017-05-26 04:58:28'),(20,1051,1,32,0,'2017-05-26 16:52:58'),(21,10,1,32,0,'2017-05-28 21:58:25'),(22,0,1,32,0,'2017-05-28 23:57:35'),(23,6,1,32.6,0,'2017-05-29 22:50:01'),(24,13,1,32.4,0,'2017-05-29 23:55:01'),(25,0,1,32.1,0,'2017-05-30 00:45:01'),(26,0,1,31.6667,0,'2017-05-30 01:30:01'),(27,3,1,31,0,'2017-05-30 02:45:01'),(28,9,1,31,0,'2017-05-30 03:30:01'),(29,3,1,31,0,'2017-05-30 04:45:02'),(30,10,1,31,0,'2017-05-30 05:45:02'),(31,14,1,31,0,'2017-05-30 06:30:01'),(32,26,1,31,0,'2017-05-30 07:45:02'),(33,24,1,31.5,0,'2017-05-30 08:30:01'),(34,20,1,32,0,'2017-05-30 09:45:01'),(35,14,1,32,0,'2017-05-30 10:45:01'),(36,400,1,32.3333,0,'2017-05-30 13:45:01'),(37,226,1,32.25,0,'2017-05-30 14:45:01'),(38,1175,1,33,0,'2017-05-30 15:45:01'),(39,2447,1,34,0,'2017-05-30 16:45:01'),(40,441,19,32.5,649,'2017-05-30 17:15:01'),(41,24,19,31.5,634,'2017-05-30 18:30:01'),(42,0,21,30.5,849,'2017-05-30 19:45:02'),(43,0,21,29.8,1058,'2017-05-30 20:50:01'),(44,2,18,29,1189,'2017-05-30 21:50:01'),(45,5,17,29,1266,'2017-05-30 22:50:01'),(46,4,17,28.8,1343,'2017-05-30 23:50:02'),(47,47,17,28,1401,'2017-05-31 00:50:01'),(48,0,17,28,1449,'2017-05-31 01:50:01'),(49,5,17,27.2,1490,'2017-05-31 02:50:01'),(50,0,17,27,1520,'2017-05-31 03:50:02'),(51,0,17,27,1539,'2017-05-31 04:40:01'),(52,79,17,27,1555,'2017-05-31 05:50:01'),(53,749,17,27.5,1529,'2017-05-31 06:50:01'),(54,2148,17,29.2,1494,'2017-05-31 07:50:01'),(55,2342,17,30.4,1473,'2017-05-31 08:50:01'),(56,2051,17,31,1473,'2017-05-31 09:30:01'),(57,2010,18,32,1448,'2017-05-31 10:20:01'),(58,366,15,32.5,375,'2017-05-31 11:50:02'),(59,352,24,31.5,354,'2017-05-31 12:50:01'),(60,282,23,32.8,361,'2017-05-31 13:54:17'),(61,2060,23,33.4,367,'2017-05-31 14:50:01'),(62,2053,23,31.3,385,'2017-05-31 15:50:01'),(63,1583,23,31,393,'2017-05-31 16:50:02'),(64,50,23,30,407,'2017-05-31 17:50:01'),(65,11,23,30,412,'2017-05-31 18:50:01'),(66,0,23,30.8,409,'2017-05-31 19:50:01'),(67,0,23,31,412,'2017-05-31 20:50:01'),(68,3,24,31,414,'2017-05-31 21:50:01'),(69,7,24,31,416,'2017-05-31 22:40:02'),(70,0,24,31,422,'2017-05-31 23:50:01'),(71,0,24,31,423,'2017-06-01 00:40:01'),(72,4,24,31.3,424,'2017-06-01 01:50:01'),(73,0,24,31,426,'2017-06-01 02:50:01'),(74,0,24,31.8,427,'2017-06-01 03:50:01'),(75,0,24,32,427,'2017-06-01 04:50:01'),(76,43,24,32,426,'2017-06-01 05:50:01'),(77,1403,24,32.5,420,'2017-06-01 06:50:01'),(78,1862,24,33,416,'2017-06-01 07:50:01'),(79,1903,24,33,413,'2017-06-01 08:40:01'),(80,1939,24,33,415,'2017-06-01 09:40:01'),(81,1946,24,34,410,'2017-06-01 10:50:01'),(82,2102,24,34.8,401,'2017-06-01 11:40:02'),(83,2111,24,35,403,'2017-06-01 12:50:01'),(84,1921,24,31.8,431,'2017-06-01 13:50:01'),(85,2016,25,30.8,451,'2017-06-01 14:50:02'),(86,1981,26,30,502,'2017-06-01 15:50:01'),(87,214,28,30,554,'2017-06-01 16:50:01'),(88,1340,27,29.8,554,'2017-06-01 17:50:02'),(89,333,27,29.5,527,'2017-06-01 18:50:01'),(90,0,26,30.6,504,'2017-06-01 19:50:01'),(91,7,26,31.2,491,'2017-06-01 20:50:01'),(92,3,26,32,487,'2017-06-01 21:50:01'),(93,3,26,32,486,'2017-06-01 22:50:01'),(94,14,27,32,484,'2017-06-01 23:50:01'),(95,14,27,32,482,'2017-06-02 00:40:01'),(96,14,27,32,483,'2017-06-02 01:50:02'),(97,4,27,32,484,'2017-06-02 02:50:01'),(98,11,27,32,481,'2017-06-02 03:50:01'),(99,11,27,32,480,'2017-06-02 04:50:01'),(100,5,26,32,479,'2017-06-02 05:50:01'),(101,1400,27,33,469,'2017-06-02 06:50:02'),(102,1893,27,34,463,'2017-06-02 07:50:01'),(103,1943,27,34,462,'2017-06-02 08:50:01'),(104,1943,27,34.8,454,'2017-06-02 09:50:01'),(105,1939,26,34.3,458,'2017-06-02 10:40:01'),(106,1935,26,31.3,476,'2017-06-02 11:50:01'),(107,1937,26,30.2,474,'2017-06-02 12:50:01'),(108,1975,26,30.2,462,'2017-06-02 13:50:01'),(109,2018,26,30,459,'2017-06-02 14:40:01'),(110,2125,26,31,454,'2017-06-02 15:30:01'),(111,2123,29,29.8,553,'2017-06-02 16:50:01'),(112,2023,34,29,753,'2017-06-02 17:30:01'),(113,467,57,30,776,'2017-06-07 11:50:02'),(114,387,57,30.5,824,'2017-06-07 12:50:02'),(115,779,57,30,850,'2017-06-07 13:50:01'),(116,664,57,30,862,'2017-06-07 14:50:01'),(117,345,57,30,860,'2017-06-07 15:50:02'),(118,189,57,30,864,'2017-06-07 16:40:01'),(119,16,1,31.6,0,'2017-06-07 21:50:01'),(120,2,1,31.8,0,'2017-06-07 22:50:01'),(121,0,1,32,0,'2017-06-07 23:50:01'),(122,0,1,32,0,'2017-06-08 00:50:01'),(123,0,1,32,0,'2017-06-08 01:50:01'),(124,0,1,32,0,'2017-06-08 02:50:01'),(125,0,1,32,0,'2017-06-08 03:50:01'),(126,0,1,31.6,0,'2017-06-08 04:50:01'),(127,1,1,31.3,0,'2017-06-08 05:50:01'),(128,0,1,34.6,0,'2017-06-08 06:40:01'),(129,4,1,35,0,'2017-06-08 07:50:01'),(130,0,1,35,0,'2017-06-08 08:50:01'),(131,0,1,36,0,'2017-06-08 09:50:02'),(132,33,1,36.8,0,'2017-06-08 10:50:02'),(133,13,1,37,0,'2017-06-08 11:10:02'),(134,317,33,32.5,486,'2017-06-08 13:50:01'),(135,452,34,32.6,551,'2017-06-08 14:50:02'),(136,267,41,33,747,'2017-06-08 15:30:01'),(137,10,1,31,0,'2017-06-08 21:50:01'),(138,0,1,30.2,0,'2017-06-08 22:50:01'),(139,0,1,30,0,'2017-06-08 23:50:02'),(140,0,1,30,0,'2017-06-09 00:50:01'),(141,0,1,30,0,'2017-06-09 01:50:01'),(142,0,1,30,0,'2017-06-09 02:40:02'),(143,2,1,30,0,'2017-06-09 03:50:01'),(144,2,1,30,0,'2017-06-09 04:50:02'),(145,7,1,29,0,'2017-06-09 05:50:01'),(146,8,1,29,0,'2017-06-09 06:40:01'),(147,0,1,29,0,'2017-06-09 07:50:01'),(148,0,1,29,0,'2017-06-09 08:50:01'),(149,0,1,29,0,'2017-06-09 09:10:02'),(150,785,55,31.6,741,'2017-06-09 11:50:02'),(151,690,55,32,750,'2017-06-09 12:50:02'),(152,669,55,32.8,747,'2017-06-09 13:50:01'),(153,484,54,30.7,783,'2017-06-09 14:20:02'),(154,306,26,28.7,270,'2017-06-09 16:50:01'),(155,272,35,28.7,371,'2017-06-09 17:50:01'),(156,648,21,30.5,335,'2017-06-10 09:50:01'),(157,544,21,30.6,340,'2017-06-10 10:50:01'),(158,744,21,31.4,337,'2017-06-10 11:50:01'),(159,842,21,32,335,'2017-06-10 12:40:02'),(160,298,21,32.6,335,'2017-06-10 13:40:01'),(161,124,21,29,351,'2017-06-10 14:40:01'),(162,170,21,30,346,'2017-06-10 15:50:01'),(163,57,12,30,223,'2017-06-10 16:50:01'),(164,36,10,30,176,'2017-06-10 17:50:01'),(165,7,22,29.8,354,'2017-06-10 18:40:01'),(166,0,27,29,425,'2017-06-10 19:50:01'),(167,7,27,29,428,'2017-06-10 20:50:01'),(168,7,27,29,435,'2017-06-10 21:50:01'),(169,2,26,29,440,'2017-06-10 22:50:02'),(170,26,26,28.5,443,'2017-06-10 23:50:01'),(171,0,26,28,444,'2017-06-11 00:50:01'),(172,0,26,28,445,'2017-06-11 01:50:01'),(173,0,26,28,443,'2017-06-11 02:50:01'),(174,0,26,28,443,'2017-06-11 03:40:01'),(175,0,26,28,442,'2017-06-11 04:50:01'),(176,34,26,28,443,'2017-06-11 05:40:01'),(177,252,26,28.5,439,'2017-06-11 06:50:01'),(178,559,26,29.4,433,'2017-06-11 07:50:01'),(179,878,26,30.8,428,'2017-06-11 08:40:01'),(180,1025,26,32,422,'2017-06-11 09:50:02'),(181,752,26,32,422,'2017-06-11 10:40:02'),(182,719,25,33,414,'2017-06-11 11:50:01'),(183,523,25,32.4,414,'2017-06-11 12:50:01'),(184,253,25,31,420,'2017-06-11 13:40:02'),(185,187,18,29.6,424,'2017-06-11 14:50:01'),(186,216,16,30,415,'2017-06-11 15:50:01'),(187,302,23,30.5,391,'2017-06-11 16:50:01'),(188,335,25,31,388,'2017-06-11 17:30:01'),(189,69,25,31,391,'2017-06-11 18:50:01'),(190,24,25,30.3,397,'2017-06-11 19:50:01'),(191,0,25,30,399,'2017-06-11 20:50:01'),(192,0,25,29.8,398,'2017-06-11 21:50:01'),(193,0,25,29,398,'2017-06-11 22:50:01'),(194,3,25,29,403,'2017-06-11 23:40:02'),(195,0,25,29,403,'2017-06-12 00:50:01'),(196,0,25,28.7,406,'2017-06-12 01:50:02'),(197,2,25,28,406,'2017-06-12 02:50:01'),(198,0,25,29,407,'2017-06-12 03:50:01'),(199,0,25,29,414,'2017-06-12 04:50:01'),(200,27,25,29,414,'2017-06-12 05:50:02'),(201,132,25,29,403,'2017-06-12 06:50:01'),(202,939,19,32,280,'2017-06-12 08:30:02'),(203,1508,51,33.2,672,'2017-06-12 09:50:01'),(204,1491,52,34,680,'2017-06-12 10:50:01'),(205,1500,52,34,674,'2017-06-12 11:50:01'),(206,1457,51,32,691,'2017-06-12 12:50:01'),(207,1382,50,31,691,'2017-06-12 13:50:02'),(208,1466,50,30.5,684,'2017-06-12 14:50:01'),(209,1685,39,30,661,'2017-06-12 15:50:01'),(210,2226,35,28.5,649,'2017-06-12 16:50:01');
/*!40000 ALTER TABLE `sensor_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_data_hour`
--

DROP TABLE IF EXISTS `sensor_data_hour`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_data_hour` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sunlight` int(11) DEFAULT NULL,
  `moisture` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `fertility` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `light` tinyint(1) DEFAULT NULL,
  `water` tinyint(1) DEFAULT NULL,
  `fan` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_data_hour`
--

LOCK TABLES `sensor_data_hour` WRITE;
/*!40000 ALTER TABLE `sensor_data_hour` DISABLE KEYS */;
INSERT INTO `sensor_data_hour` VALUES (1,2167,35,29,642,'2017-06-12 17:00:01',1,0,0,0),(2,2167,35,29,642,'2017-06-12 17:00:01',0,0,0,0);
/*!40000 ALTER TABLE `sensor_data_hour` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_data_test`
--

DROP TABLE IF EXISTS `sensor_data_test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_data_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sunlight` int(11) DEFAULT NULL,
  `moisture` int(11) DEFAULT NULL,
  `temperature` float DEFAULT NULL,
  `fertility` int(11) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_data_test`
--

LOCK TABLES `sensor_data_test` WRITE;
/*!40000 ALTER TABLE `sensor_data_test` DISABLE KEYS */;
INSERT INTO `sensor_data_test` VALUES (1,21,1,29,0,'2017-05-26 03:57:13'),(2,13,1,28,0,'2017-05-26 03:58:46'),(3,0,1,28,0,'2017-05-26 04:00:18'),(4,0,1,29,0,'2017-05-26 04:01:52'),(5,0,1,28,0,'2017-05-26 04:03:26'),(6,0,1,28,0,'2017-05-26 04:38:18'),(7,0,1,28,0,'2017-05-26 04:48:24'),(8,0,1,28,0,'2017-05-26 04:58:28'),(9,0,1,28,0,'2017-05-26 05:08:31'),(10,0,1,28,0,'2017-05-26 05:18:33'),(11,14,1,29,0,'2017-05-26 09:19:55'),(12,1049,1,32,0,'2017-05-26 16:02:45'),(13,987,1,32,0,'2017-05-26 16:12:50'),(14,1143,1,32,0,'2017-05-26 16:22:51'),(15,1096,1,32,0,'2017-05-26 16:32:53'),(16,1033,1,32,0,'2017-05-26 16:42:56'),(17,1002,1,32,0,'2017-05-26 16:52:58'),(18,908,1,32,0,'2017-05-26 17:03:01'),(19,876,1,32,0,'2017-05-26 17:13:04'),(20,718,1,32,0,'2017-05-26 17:23:08'),(21,624,1,32,0,'2017-05-26 17:33:10'),(22,514,1,32,0,'2017-05-26 17:43:12'),(23,14,1,32,0,'2017-05-28 21:18:17'),(24,14,1,32,0,'2017-05-28 21:28:19'),(25,0,1,32,0,'2017-05-28 21:38:21'),(26,14,1,32,0,'2017-05-28 21:48:23'),(27,8,1,32,0,'2017-05-28 21:58:25'),(28,0,1,33,0,'2017-05-28 22:08:29'),(29,0,1,32,0,'2017-05-28 22:18:32'),(30,0,1,33,0,'2017-05-28 22:28:34'),(31,0,1,32,0,'2017-05-28 23:07:21'),(32,0,1,32,0,'2017-05-28 23:57:35'),(33,0,1,32,0,'2017-05-29 00:07:37'),(34,13,1,32,0,'2017-05-29 10:18:52'),(35,13,1,32,0,'2017-05-29 10:19:54'),(36,32,1,32,0,'2017-05-29 10:20:56'),(38,13,1,331,0,'2017-05-29 11:35:01'),(39,13,1,331,0,'2017-05-29 11:35:07'),(40,0,1,337,0,'2017-05-29 19:24:51'),(41,14,1,337,0,'2017-05-29 19:25:27');
/*!40000 ALTER TABLE `sensor_data_test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) DEFAULT NULL,
  `user_username` varchar(30) DEFAULT NULL,
  `user_password` varchar(30) DEFAULT NULL,
  `role` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','root','raspberry',1),(2,'Thinh dz','thinh','123456',0);
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

-- Dump completed on 2017-06-13 11:55:56
