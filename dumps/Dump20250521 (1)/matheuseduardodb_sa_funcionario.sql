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
-- Table structure for table `funcionario`
--

DROP TABLE IF EXISTS `funcionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionario` (
  `id_funcionario` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(40) DEFAULT NULL,
  `cargo` varchar(30) DEFAULT NULL,
  `cpf` varchar(14) DEFAULT NULL,
  `salario` double DEFAULT NULL,
  PRIMARY KEY (`id_funcionario`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionario`
--

LOCK TABLES `funcionario` WRITE;
/*!40000 ALTER TABLE `funcionario` DISABLE KEYS */;
INSERT INTO `funcionario` VALUES (1,'Matheus Eduardo','CEO','12345678901',25000),(2,'Carlos Silva','Diretor de Tecnologia','23456789012',18000),(3,'Ana Oliveira','Diretora Comercial','34567890123',18000),(5,'Juliana Costa','Gerente de Comunidade','56789012345',14000),(6,'Ricardo Pereira','Desenvolvedor Sênior','67890123456',12000),(7,'Fernanda Lima','Designer Chefe','78901234567',11000),(8,'Lucas Rodrigues','Analista de Sistemas','89012345678',10000),(9,'Patricia Alves','Gerente de Suporte','90123456789',10000),(10,'Marcos Souza','Especialista em Jogos','01234567890',9500),(11,'Camila Rocha','Marketing Digital','98765432109',9000),(12,'Gustavo Henrique','Desenvolvedor Backend','87654321098',9500),(13,'Isabela Martins','UX Designer','76543210987',8500),(14,'Rodrigo Ferreira','Analista de Dados','65432109876',8500),(15,'Amanda Dias','Gerente de Relações','54321098765',9000),(16,'Bruno Carvalho','Especialista em Anti-Cheat','43210987654',8000),(17,'Tatiane Nunes','Produtora de Conteúdo','32109876543',7500),(18,'Diego Ramos','Administrador de Redes','21098765432',8000),(19,'Vanessa Cruz','Recursos Humanos','10987654321',7500),(20,'Roberto Andrade','Financeiro','09876543210',7000),(21,'Sandra Vieira','Atendimento ao Cliente','98765432100',6500),(22,'Felipe Cardoso','Desenvolvedor Mobile','87654321009',8500),(23,'Larissa Moreira','Community Manager','76543210098',7000),(24,'Eduardo Barbosa','Especialista em Cloud','65432100987',9500),(25,'Mariana Lopes','Trader de Itens','54321009876',6000),(26,'Alexandre Cunha','Suporte Técnico','43210098765',5500),(27,'Cristina Batista','Assistente Administrativo','32100987654',5000),(28,'Rafael Menezes','Analista de Segurança','21009876543',8500),(29,'Daniela Freitas','Copywriter','10098765432',6000),(30,'Thiago Gonçalves','QA Tester','00987654321',5500),(31,'Viviane Castro','Social Media','98765432111',5000),(32,'Leonardo Duarte','DevOps','87654321109',10000),(33,'Gabriela Monteiro','UI Designer','76543211098',7500),(34,'Hugo Correia','Especialista em VR','65432110987',9000),(35,'Renata Marques','Gerente de Parcerias','54321109876',11000),(36,'André Brito','Desenvolvedor Frontend','43211098765',8500),(37,'Simone Xavier','Contadora','32110987654',6500),(38,'Paulo Junior','Assistente de TI','21109876543',4500),(39,'Elaine Medeiros','Coordenadora de Eventos','11098765432',6000),(40,'Marcelo Santana','Especialista em Economia','00987654322',7500),(41,'Lucia Helena','Jurídico','98765432211',8000),(42,'Oscar Fernandes','SysAdmin','87654322110',7500),(43,'Yasmin Teixeira','Estagiária de Design','76543221109',2000),(44,'Victor Hugo','Estagiário de Dev','65432211098',2000),(45,'Natalia Ribeiro','Assistente Comercial','54322110987',3500),(46,'Igor Martins','Analista de Qualidade','43221109876',6000),(47,'Adriana Leal','Coordenadora de Suporte','32211098765',7000),(48,'Caio Vinicius','Especialista em APIs','22110987654',8500),(49,'Priscila Santos','Tradutora','11109876543',5000),(50,'Gilberto Ramos','Técnico de Hardware','00098765432',4500),(51,'João da Silva','Desenvolvedor Sênior','52998224725',12000);
/*!40000 ALTER TABLE `funcionario` ENABLE KEYS */;
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
