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
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedor`
--

LOCK TABLES `fornecedor` WRITE;
/*!40000 ALTER TABLE `fornecedor` DISABLE KEYS */;
INSERT INTO `fornecedor` VALUES (1,'Square Enix','11222333000144','1199998888','Shinjuku Eastside Square, Tóquio, Japão'),(2,'Nintendo','22333444000155','1198887777','11-1 Kamitoba Hokodatecho, Quioto, Japão'),(3,'Sony Interactive Entertainment','33444555000166','1197776666','1-7-1 Konan, Minato, Tóquio, Japão'),(4,'Microsoft Gaming','44555666000177','1196665555','One Microsoft Way, Redmond, EUA'),(5,'Electronic Arts','55666777000188','1195554444','209 Redwood Shores Parkway, Califórnia, EUA'),(6,'Ubisoft','66777888000199','1194443333','2 Av. Pasteur, Saint-Mandé, França'),(7,'Activision Blizzard','77888999000100','1193332222','2701 Olympic Blvd, Santa Mônica, EUA'),(8,'Take-Two Interactive','88999000000111','1192221111','110 West 44th Street, Nova York, EUA'),(9,'Bandai Namco','99000111000122','1191110000','5-37-8 Shiba, Minato, Tóquio, Japão'),(10,'Sega','00111222000133','1190009999','Shinagawa Grand Central Tower, Tóquio, Japão'),(11,'Capcom','11222333000244','1189998888','3-1-3 Uchihirano-machi, Chuo-ku, Osaka, Japão'),(12,'Konami','22333444000255','1188887777','1-11-1 Tsurumaki, Tama-shi, Tóquio, Japão'),(13,'Koei Tecmo','33444555000266','1187776666','1-18-12 Minowa-cho, Kohoku-ku, Yokohama, Japão'),(14,'THQ Nordic','44555666000277','1186665555','Hafenstrasse 101, Linz, Áustria'),(15,'505 Games','55666777000288','1185554444','Via Roma 108, Milão, Itália'),(16,'Focus Entertainment','66777888000299','1184443333','41 rue de la Vanne, Montrouge, França'),(17,'NIS America','77888999000200','1183332222','450 Artesia Blvd, Torrance, EUA'),(18,'XSEED Games','88999000000211','1182221111','1000 Bridge Parkway, Redwood City, EUA'),(19,'Marvelous','99000111000222','1181110000','3-39-5 Higashishinagawa, Tóquio, Japão'),(20,'Arc System Works','00111222000233','1180009999','4-5-25 Minamishinagawa, Tóquio, Japão'),(21,'Fangamer','11222333000344','1179998888','1631 E 7th St, Tucson, EUA'),(22,'Limited Run Games','22333444000355','1178887777','1400 East Independence Blvd, Carolina do Norte, EUA'),(23,'Super Rare Games','33444555000366','1177776666','Unit 1, The Old Bakery, Londres, Reino Unido'),(24,'Strictly Limited Games','44555666000377','1176665555','Hedderichstr. 108a, Düsseldorf, Alemanha'),(25,'Special Reserve Games','55666777000388','1175554444','123 Game St, Austin, EUA'),(26,'iam8bit','66777888000399','1174443333','2147 West Sunset Blvd, Los Angeles, EUA'),(27,'Signature Edition Games','77888999000300','1173332222','22 Rue des Peupliers, Paris, França'),(28,'Play-Asia','88999000000311','1172221111','18/F, Tower 2, Kowloon, Hong Kong'),(29,'Video Games Plus','99000111000322','1171110000','5634 Yonge St, Toronto, Canadá'),(30,'The Game Collection','00111222000333','1170009999','Unit 3, The Quadrant, Bristol, Reino Unido'),(31,'CD Projekt RED','11222333000444','1169998888','Jagiellońska 74, Varsóvia, Polônia'),(32,'FromSoftware','22333444000455','1168887777','3-34-1 Shibuya, Tóquio, Japão'),(33,'Larian Studios','33444555000466','1167776666','Cipierstraat 9, Gent, Bélgica'),(34,'Guerrilla Games','44555666000477','1166665555','Oosterdok 2, Amsterdam, Holanda'),(35,'Insomniac Games','55666777000488','1165554444','10900 Wilshire Blvd, Los Angeles, EUA'),(36,'Naughty Dog','66777888000499','1164443333','4444 Lakeside Drive, Los Angeles, EUA'),(37,'PlatinumGames','77888999000400','1163332222','2-2-1 Marunouchi, Chiyoda, Tóquio, Japão'),(38,'Remedy Entertainment','88999000000411','1162221111','Luomanportti 4, Espoo, Finlândia'),(39,'Rockstar Games','99000111000422','1161110000','622 Broadway, Nova York, EUA');
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

-- Dump completed on 2025-05-21 20:44:24
