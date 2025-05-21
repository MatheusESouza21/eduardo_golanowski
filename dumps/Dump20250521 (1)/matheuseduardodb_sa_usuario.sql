-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: matheuseduardodb_sa
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) DEFAULT NULL,
  `senha` varchar(30) DEFAULT NULL,
  `tipo` enum('administrador','comum') NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'admin','admin123','administrador'),(2,'john_gamer','jo123456','administrador'),(3,'mary_plays','mary@2023','administrador'),(4,'peter_stream','pet3rTw1tch','administrador'),(5,'game_master','gm2023!','administrador'),(6,'alex_kidd','alex1989','administrador'),(7,'lara_croft','tombraider','administrador'),(8,'sonic_speed','bluehedgehog','administrador'),(9,'mario_jump','itsame','administrador'),(10,'zelda_fan','triforce3','administrador'),(11,'kratos_rage','boy2022','administrador'),(12,'dante_devil','sparda666','administrador'),(13,'cloud_strife','buster99','administrador'),(14,'samus_aran','metroid85','administrador'),(15,'link_hero','hyrule123','administrador'),(16,'solid_snake','metalgear','administrador'),(17,'pacman_chomp','wakawaka','administrador'),(18,'ryu_street','hadouken','administrador'),(19,'chun_li','spinningbird','administrador'),(20,'sub_zero','fatality','administrador'),(21,'scorpion','getoverhere','administrador'),(22,'raiden_shock','lightning','administrador'),(23,'geralt_rivia','witcher3','administrador'),(24,'ciri_sword','zireael','administrador'),(25,'yennefer','magic123','administrador'),(26,'triss_merigold','redhair','administrador'),(27,'dovahkiin','fusrodah','administrador'),(28,'commander_shepard','n7normandy','administrador'),(29,'gordon_freeman','blackmesa','administrador'),(30,'booker_dewitt','columbia1912','administrador'),(31,'elizabeth','tears1999','administrador'),(32,'joel_miller','ellie2023','administrador'),(33,'ellie_williams','joel123','administrador'),(34,'arthur_morgan','rdr21899','administrador'),(35,'john_marston','reddead1911','administrador'),(36,'niko_bellic','libertycity','administrador'),(37,'trevor_philips','psycho123','administrador'),(38,'michael_townley','northyankton','administrador'),(39,'franklin_clinton','grovestreet','administrador'),(40,'lara_soft','password123','administrador'),(42,'alan_wake','brightfalls','administrador'),(43,'jill_valentine','stars1998','administrador'),(44,'leon_kennedy','residentevil','administrador'),(45,'chris_redfield','boulderpunch','administrador'),(46,'ada_wong','spy4hire','administrador'),(47,'claire_redfield','motocycle','administrador'),(48,'nemesis','stars1999','comum'),(49,'albert_wesker','umbrella','administrador'),(50,'heisenberg','village123','administrador'),(51,'Matt','2103','comum');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-21 20:44:24
