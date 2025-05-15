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
-- Table structure for table `fornecedor`
--

DROP TABLE IF EXISTS `fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedor` (
  `id_fornecedor` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) DEFAULT NULL,
  `cnpj` char(14) DEFAULT NULL,
  `telefone` varchar(12) DEFAULT NULL,
  `endereco` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_fornecedor`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedor`
--

LOCK TABLES `fornecedor` WRITE;
/*!40000 ALTER TABLE `fornecedor` DISABLE KEYS */;
INSERT INTO `fornecedor` VALUES (1,'Valve Corporation','12345678000199','5541999999','Bellevue, Washington, EUA'),(2,'Riot Games','98765432000111','5541888888','Los Angeles, California, EUA'),(3,'Blizzard Entertainment','11111111000122','5541777777','Irvine, California, EUA'),(4,'Electronic Arts','22222222000133','5541666666','Redwood City, California, EUA'),(5,'Ubisoft','33333333000144','5541555555','Montreuil, França'),(6,'CD Projekt Red','44444444000155','485555555','Varsóvia, Polônia'),(7,'Rockstar Games','55555555000166','5541444444','Nova York, EUA'),(8,'Epic Games','66666666000177','5541333333','Cary, Carolina do Norte, EUA'),(9,'Square Enix','77777777000188','8133333333','Tóquio, Japão'),(10,'Capcom','88888888000199','8144444444','Osaka, Japão'),(11,'Bandai Namco','99999999000100','8155555555','Tóquio, Japão'),(12,'Sega','10101010000111','8166666666','Tóquio, Japão'),(13,'Nintendo','12121212000122','8177777777','Quioto, Japão'),(14,'Bethesda Softworks','13131313000133','5541222222','Rockville, Maryland, EUA'),(15,'Activision','14141414000144','5541111111','Santa Monica, California, EUA'),(16,'Naughty Dog','15151515000155','5541000000','Santa Monica, California, EUA'),(17,'Insomniac Games','16161616000166','5541999988','Burbank, California, EUA'),(18,'Santa Monica Studio','17171717000177','5541888877','Los Angeles, California, EUA'),(19,'Guerrilla Games','18181818000188','312345678','Amsterdã, Holanda'),(20,'FromSoftware','19191919000199','8134567890','Tóquio, Japão'),(21,'BioWare','20202020000100','5541777766','Edmonton, Canadá'),(22,'2K Games','21212121000111','5541666655','Novato, California, EUA'),(23,'Paradox Interactive','22222222000122','4688888888','Estocolmo, Suécia'),(24,'Kojima Productions','23232323000133','8133333444','Tóquio, Japão'),(25,'Remedy Entertainment','24242424000144','358123456','Espoo, Finlândia'),(26,'Techland','25252525000155','482222222','Wrocław, Polônia'),(27,'Bluehole Studio','26262626000166','822345678','Seul, Coreia do Sul'),(28,'Mojang Studios','27272727000177','468123456','Estocolmo, Suécia'),(29,'Hello Games','28282828000188','4412345678','Guildford, Reino Unido'),(30,'Gearbox Software','29292929000199','5541555544','Frisco, Texas, EUA'),(31,'Crytek','30303030000100','496123456','Frankfurt, Alemanha'),(32,'4A Games','31313131000111','380123456','Kyiv, Ucrânia'),(33,'Firaxis Games','32323232000122','5541444433','Sparks, Maryland, EUA'),(34,'Larian Studios','33333333000133','322345678','Dublin, Irlanda'),(35,'Behaviour Interactive','34343434000144','514123456','Montreal, Canadá'),(36,'NetherRealm Studios','35353535000155','5541333322','Chicago, Illinois, EUA'),(37,'Treyarch','36363636000166','5541222211','Santa Monica, California, EUA'),(38,'Infinity Ward','37373737000177','5541111100','Woodland Hills, California, EUA'),(39,'Respawn Entertainment','38383838000188','5541999977','Sherman Oaks, California, EUA'),(40,'DICE','39393939000199','468765432','Estocolmo, Suécia'),(41,'Playground Games','40404040000100','441234567','Leamington Spa, Reino Unido'),(42,'Turn 10 Studios','41414141000111','5541888866','Redmond, Washington, EUA'),(43,'The Coalition','42424242000122','5541777755','Vancouver, Canadá'),(44,'343 Industries','43434343000133','5541666644','Redmond, Washington, EUA'),(45,'Bungie','44444444000144','5541555533','Bellevue, Washington, EUA'),(46,'Media Molecule','45454545000155','441234568','Guildford, Reino Unido'),(47,'Sucker Punch Productions','46464646000166','5541444422','Bellevue, Washington, EUA'),(48,'Quantic Dream','47474747000177','331234567','Paris, França'),(49,'PlatinumGames','48484848000188','813456789','Osaka, Japão'),(50,'Grinding Gear Games','49494949000199','644123456','Auckland, Nova Zelândia'),(51,'Klei Entertainment','50505050000100','5541333311','Vancouver, Canadá');
/*!40000 ALTER TABLE `fornecedor` ENABLE KEYS */;
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
