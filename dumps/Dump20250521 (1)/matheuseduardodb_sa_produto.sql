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
  `nome` varchar(100) DEFAULT NULL,
  `descricao` varchar(100) DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  `preco` decimal(10,2) DEFAULT NULL,
  `id_fornecedor` int DEFAULT NULL,
  PRIMARY KEY (`id_produto`),
  KEY `fk_id_fornecedor` (`id_fornecedor`),
  CONSTRAINT `fk_id_fornecedor` FOREIGN KEY (`id_fornecedor`) REFERENCES `fornecedor` (`id_fornecedor`)
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (181,'Final Fantasy XVI','RPG de ação da renomada série',120,349.90,1),(182,'Forspoken','Ação em mundo aberto com magia',85,299.90,1),(183,'Octopath Traveler II','RPG em estilo HD-2D',75,249.90,1),(184,'The Legend of Zelda: Tears of the Kingdom','Sequência de Breath of the Wild',200,349.90,2),(185,'Metroid Prime Remastered','Remasterização do clássico de GameCube',110,199.90,2),(186,'Splatoon 3','Tiro em terceira pessoa multijogador',150,279.90,2),(187,'Marvel\'s Spider-Man 2','Aventura do Homem-Aranha',180,399.90,3),(188,'Gran Turismo 7','Simulador de corridas realista',130,349.90,3),(189,'Demon\'s Souls Remake','Remake do clássico RPG de ação',95,299.90,3),(190,'Starfield','RPG espacial em mundo aberto',160,349.90,4),(191,'Forza Motorsport (2023)','Simulador de corridas',115,349.90,4),(192,'Age of Empires IV','Estratégia em tempo real',90,199.90,4),(193,'Dead Space Remake','Remake do clássico de terror',105,299.90,5),(194,'Star Wars Jedi: Survivor','Ação e aventura no universo Star Wars',140,349.90,5),(195,'Need for Speed Unbound','Jogo de corrida arcade',95,249.90,5),(196,'Assassin\'s Creed Mirage','Ação stealth no mundo árabe',150,299.90,6),(197,'Skull and Bones','Aventura naval pirata',80,349.90,6),(198,'Prince of Persia: The Lost Crown','Ação e plataforma',110,249.90,6),(199,'Call of Duty: Modern Warfare III','FPS militar moderno',220,399.90,7),(200,'Diablo IV Collector\'s Edition','RPG de ação sombrio',125,599.90,7),(201,'Crash Team Rumble','Jogo de arena multijogador',75,199.90,7),(202,'Grand Theft Auto VI','Mundo aberto criminal (pré-venda)',300,449.90,8),(203,'NBA 2K24','Simulador de basquete',140,349.90,8),(204,'BioShock Collection','Trilogia remasterizada',90,199.90,8),(205,'Armored Core VI: Fires of Rubicon','Mecha ação',110,349.90,9),(206,'Tekken 8 Collector\'s Edition','Jogo de luta 3D',95,499.90,9),(207,'One Piece Odyssey','RPG baseado no anime',85,299.90,9),(208,'Like a Dragon: Infinite Wealth','RPG de ação',120,349.90,10),(209,'Sonic Superstars','Plataforma 2D clássico',100,249.90,10),(210,'Total War: Pharaoh','Estratégia em tempo real',75,299.90,10),(211,'Resident Evil 4 Remake','Terror em terceira pessoa',180,349.90,11),(212,'Street Fighter 6 Deluxe','Jogo de luta',130,399.90,11),(213,'Dragon\'s Dogma 2','RPG de ação em mundo aberto',140,349.90,11),(214,'Metal Gear Solid: Master Collection','Compilação de clássicos',95,299.90,12),(215,'Silent Hill 2 Remake','Remake do clássico de terror',110,349.90,12),(216,'eFootball 2024','Simulador de futebol free-to-play',200,0.00,12),(217,'Wo Long: Fallen Dynasty','RPG de ação desafiador',105,299.90,13),(218,'Dead or Alive Xtreme Venus Vacation','Jogo de simulação',65,199.90,13),(219,'Atelier Ryza 3','RPG alquímico',80,279.90,13),(220,'Alone in the Dark','Remake do clássico de terror',90,299.90,14),(221,'SpongeBob SquarePants: The Cosmic Shake','Aventura plataforma',70,199.90,14),(222,'Destroy All Humans! 2 - Reprobed','Ação e comédia',60,249.90,14),(223,'Cyberpunk 2077: Phantom Liberty','Expansão do RPG futurista',150,199.90,31),(224,'The Witcher 3: Complete Edition','RPG de mundo aberto',180,149.90,31),(225,'Project Orion (pré-venda)','Próximo jogo Cyberpunk',200,299.90,31),(226,'Elden Ring: Shadow of the Erdtree','Expansão do aclamado RPG',170,199.90,32),(227,'Sekiro: Shadows Die Twice','Ação desafiadora',95,199.90,32),(228,'Armored Core VI: Fires of Rubicon','Mecha ação',110,349.90,32),(229,'Red Dead Redemption 2: Ultimate Edition','Faroeste em mundo aberto',130,349.90,39),(230,'Max Payne 3','Ação em terceira pessoa',85,149.90,39),(231,'Bully: Anniversary Edition','Ação e aventura escolar',75,129.90,39),(232,'Jogo da cobrinha','Coma maçã',90,500.00,39);
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

-- Dump completed on 2025-05-21 20:44:24
