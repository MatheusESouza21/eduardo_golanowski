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
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produto` (
  `id_produto` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) DEFAULT NULL,
  `descricao` varchar(30) DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  `id_fornecedor` int DEFAULT NULL,
  PRIMARY KEY (`id_produto`),
  KEY `fk_id_fornecedor` (`id_fornecedor`),
  CONSTRAINT `fk_id_fornecedor` FOREIGN KEY (`id_fornecedor`) REFERENCES `fornecedor` (`id_fornecedor`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'Counter-Strike 2','FPS competitivo',1000,0.00,1),(2,'Dota 2','MOBA gratuito',500,0.00,1),(3,'Half-Life: Alyx','VR FPS',300,199.90,1),(4,'Team Fortress 2','FPS classico',800,0.00,1),(5,'Left 4 Dead 2','Zumbi cooperativo',400,39.90,1),(6,'League of Legends','MOBA popular',2000,0.00,2),(7,'Valorant','FPS tático',1500,0.00,2),(8,'Legends of Runeterra','CCG digital',700,0.00,2),(9,'Halo Infinite','FPS sci-fi',1200,0.00,43),(10,'Destiny 2','FPS MMO',1500,0.00,44),(11,'Dreams','Criação de jogos',300,99.90,45),(12,'Ghost of Tsushima','Ação e aventura',700,249.90,46),(13,'Detroit: Become Human','Narrativa interativa',500,159.90,47),(14,'Nier: Automata','RPG de ação',800,199.90,48),(15,'Path of Exile','RPG de ação',1000,0.00,49),(16,'Don\'t Starve Together','Sobrevivência',400,39.90,50),(17,'Stardew Valley','Simulação rural',900,49.90,NULL),(18,'Minecraft','Sandbox criativo',2500,119.90,28),(19,'No Man\'s Sky','Exploração espacial',600,159.90,29),(20,'Risk of Rain 2','Roguelike',500,79.90,NULL),(21,'Hades','Roguelike',700,99.90,NULL),(22,'Among Us','Jogo social',3000,19.90,NULL),(23,'Phasmophobia','Horror cooperativo',800,49.90,NULL),(24,'Valheim','Sobrevivência viking',1200,59.90,NULL);
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-15 20:45:01
