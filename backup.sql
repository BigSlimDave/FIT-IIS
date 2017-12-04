-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: content
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

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
-- Table structure for table `hra`
--

DROP TABLE IF EXISTS `hra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hra` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nazev_hry` varchar(50) NOT NULL,
  `vydavatel_hry` varchar(50) NOT NULL,
  `rok_vydani_hry` date NOT NULL,
  `zanr_hry` varchar(50) DEFAULT NULL,
  `mod_hry` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hra`
--

LOCK TABLES `hra` WRITE;
/*!40000 ALTER TABLE `hra` DISABLE KEYS */;
INSERT INTO `hra` VALUES (1,'Half-life','Valve','1999-03-01','Akcni',''),(2,'Mafia','IS','2002-05-03','Akcni',''),(3,'Dota 2','Blizzard','2008-02-01','Strategie','5v5'),(4,'League of Legends','RIOT','2010-03-02','Moba','5v5'),(5,'Call of Duty','EA','2002-02-03','Akcni','Team Match'),(6,'Heroes of the Storm','Blizzard','2008-05-06','Strategie','5v5'),(7,'Counter-Strike: Global Offensive','Valve','2010-04-08','Akcni','Team Match'),(8,'StarCraft II','Blizzard','2007-08-25','Strategie',NULL),(9,'HeartStone','Blizzard','2005-08-25','Karetni',NULL),(10,'Smite','Hi-rez','2008-08-29','Moba','5v5'),(11,'World of Tanks','Wargaming','2011-08-30','Akcni',NULL),(12,'FIFA 17','EA','2016-09-30','Sportovni',NULL),(13,'Street Fighter V','Capcom','2016-05-07','Fighting','1v1');
/*!40000 ALTER TABLE `hra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hrac`
--

DROP TABLE IF EXISTS `hrac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hrac` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `prezdivka` varchar(50) NOT NULL,
  `jmeno` varchar(70) NOT NULL,
  `odberatel` tinyint(4) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prezdivka` (`prezdivka`),
  CONSTRAINT `hrac_ibfk_1` FOREIGN KEY (`prezdivka`) REFERENCES `uzivatele` (`prezdivka`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hrac`
--

LOCK TABLES `hrac` WRITE;
/*!40000 ALTER TABLE `hrac` DISABLE KEYS */;
INSERT INTO `hrac` VALUES (1,'borec1','Tonda Kasal',1),(2,'borec2','Lukas Belovsky',0),(3,'borec3','Adam Mynarik',1),(4,'borec4','Jan Kraus',1),(5,'borec5','Milos Zeman',0),(7,'Dree','David Holy',0),(8,'Makku','Marek Barvir',0),(9,'Taurruss','Kuba Dravy',1),(10,'Yogish','Hos Silin',0),(11,'Sabazios','Kuba Rav',0),(12,'Bublinka','Martina Prazdna',0),(13,'Blik','Martina Leva',1),(14,'Lemp','Petr Novy',0),(15,'Hade','Jakub Zeidle',1),(16,'Sprikis','Jakub Langusta',1),(17,'Havoczech','Radek Maly',0),(18,'Whitney','Martin Bur',1),(19,'Epso','Radek Rybaty',1),(20,'Manilla','Jarmila Draha',0);
/*!40000 ALTER TABLE `hrac` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `klan`
--

DROP TABLE IF EXISTS `klan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `klan` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nazev` varchar(50) NOT NULL,
  `hymna` varchar(50) DEFAULT NULL,
  `logo` varchar(50) DEFAULT NULL,
  `vudce` int(10) unsigned NOT NULL,
  `hra` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vudce` (`vudce`),
  CONSTRAINT `klan_ibfk_1` FOREIGN KEY (`vudce`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `klan`
--

LOCK TABLES `klan` WRITE;
/*!40000 ALTER TABLE `klan` DISABLE KEYS */;
INSERT INTO `klan` VALUES (1,'drsnaci','hymna.mp3','emblem.jpeg',1,11),(2,'Centuria','CMMS.mp3','emblem.jpeg',9,7),(5,'prasata','181_-_Nirvana_-_Smells_Like_Teen_Spirit.mp3','emblem.jpeg',3,5);
/*!40000 ALTER TABLE `klan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `klan_clenstvi`
--

DROP TABLE IF EXISTS `klan_clenstvi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `klan_clenstvi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hrac` int(10) unsigned NOT NULL,
  `klan` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `klan` (`klan`),
  KEY `hrac` (`hrac`),
  CONSTRAINT `klan_clenstvi_ibfk_1` FOREIGN KEY (`klan`) REFERENCES `klan` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `klan_clenstvi_ibfk_2` FOREIGN KEY (`hrac`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `klan_clenstvi`
--

LOCK TABLES `klan_clenstvi` WRITE;
/*!40000 ALTER TABLE `klan_clenstvi` DISABLE KEYS */;
INSERT INTO `klan_clenstvi` VALUES (5,8,2),(6,10,2),(7,11,2),(8,12,2),(9,13,2),(10,14,2),(11,15,2),(12,16,2),(13,17,2),(14,18,2),(15,19,2),(16,20,1);
/*!40000 ALTER TABLE `klan_clenstvi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `specializace`
--

DROP TABLE IF EXISTS `specializace`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `specializace` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hrac` int(10) unsigned NOT NULL,
  `hra` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `hrac` (`hrac`),
  KEY `hra` (`hra`),
  CONSTRAINT `specializace_ibfk_1` FOREIGN KEY (`hrac`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `specializace_ibfk_2` FOREIGN KEY (`hra`) REFERENCES `hra` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `specializace`
--

LOCK TABLES `specializace` WRITE;
/*!40000 ALTER TABLE `specializace` DISABLE KEYS */;
INSERT INTO `specializace` VALUES (1,2,1),(2,3,3),(3,4,1),(4,8,10),(5,9,10),(6,10,4),(7,11,6),(8,12,7),(9,13,9),(10,14,9),(11,15,2),(12,16,12),(13,17,13),(14,18,11),(15,19,12),(16,20,8),(17,1,1);
/*!40000 ALTER TABLE `specializace` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzor`
--

DROP TABLE IF EXISTS `sponzor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sponzor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `typ` varchar(50) NOT NULL,
  `nazev` varchar(50) NOT NULL,
  `iban` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzor`
--

LOCK TABLES `sponzor` WRITE;
/*!40000 ALTER TABLE `sponzor` DISABLE KEYS */;
INSERT INTO `sponzor` VALUES (1,'zlaty','ibm','CZ6508000000192000145399'),(2,'stribrny','fit vutbr','CZ6508000000192000145399'),(3,'zlaty','coca loca','CZ6508000000192000145399');
/*!40000 ALTER TABLE `sponzor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sponzoroval`
--

DROP TABLE IF EXISTS `sponzoroval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sponzoroval` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `castka` int(11) NOT NULL,
  `sponzor` int(10) unsigned NOT NULL,
  `turnaj` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sponzor` (`sponzor`),
  KEY `turnaj` (`turnaj`),
  CONSTRAINT `sponzoroval_ibfk_1` FOREIGN KEY (`sponzor`) REFERENCES `sponzor` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `sponzoroval_ibfk_2` FOREIGN KEY (`turnaj`) REFERENCES `turnaj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sponzoroval`
--

LOCK TABLES `sponzoroval` WRITE;
/*!40000 ALTER TABLE `sponzoroval` DISABLE KEYS */;
INSERT INTO `sponzoroval` VALUES (4,25000,1,7),(5,25000,3,7),(6,20000,1,8),(7,5000,2,8),(8,1000,2,9);
/*!40000 ALTER TABLE `sponzoroval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnaj`
--

DROP TABLE IF EXISTS `turnaj`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnaj` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nazev` varchar(50) NOT NULL,
  `odmena` int(11) NOT NULL,
  `kdy` date NOT NULL,
  `kde` varchar(50) NOT NULL,
  `kapacita` int(11) DEFAULT NULL,
  `bezny` int(10) unsigned DEFAULT NULL,
  `wc` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bezny` (`bezny`),
  KEY `wc` (`wc`),
  CONSTRAINT `turnaj_ibfk_1` FOREIGN KEY (`bezny`) REFERENCES `turnaj_bezny` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnaj_ibfk_2` FOREIGN KEY (`wc`) REFERENCES `turnaj_wc` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnaj`
--

LOCK TABLES `turnaj` WRITE;
/*!40000 ALTER TABLE `turnaj` DISABLE KEYS */;
INSERT INTO `turnaj` VALUES (7,'Prague open',50000,'2017-05-05','Praha hl. n.',6000,NULL,3),(8,'Brno open',25000,'2017-09-19','Brno hl. n.',3000,NULL,4),(9,'Olomoucký šmudla',1000,'2017-12-24','Olomouc hl. n.',100,5,NULL);
/*!40000 ALTER TABLE `turnaj` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnaj_bezny`
--

DROP TABLE IF EXISTS `turnaj_bezny`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnaj_bezny` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `vitez` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vitez` (`vitez`),
  CONSTRAINT `turnaj_bezny_ibfk_1` FOREIGN KEY (`vitez`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnaj_bezny`
--

LOCK TABLES `turnaj_bezny` WRITE;
/*!40000 ALTER TABLE `turnaj_bezny` DISABLE KEYS */;
INSERT INTO `turnaj_bezny` VALUES (5,NULL),(1,1),(2,2),(3,3),(4,3);
/*!40000 ALTER TABLE `turnaj_bezny` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `turnaj_wc`
--

DROP TABLE IF EXISTS `turnaj_wc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `turnaj_wc` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `prvni` int(10) unsigned DEFAULT NULL,
  `druhy` int(10) unsigned DEFAULT NULL,
  `treti` int(10) unsigned DEFAULT NULL,
  `ctvrty` int(10) unsigned DEFAULT NULL,
  `paty` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `prvni` (`prvni`),
  KEY `druhy` (`druhy`),
  KEY `treti` (`treti`),
  KEY `ctvrty` (`ctvrty`),
  KEY `paty` (`paty`),
  CONSTRAINT `turnaj_wc_ibfk_1` FOREIGN KEY (`prvni`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnaj_wc_ibfk_2` FOREIGN KEY (`druhy`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnaj_wc_ibfk_3` FOREIGN KEY (`treti`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnaj_wc_ibfk_4` FOREIGN KEY (`ctvrty`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `turnaj_wc_ibfk_5` FOREIGN KEY (`paty`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `turnaj_wc`
--

LOCK TABLES `turnaj_wc` WRITE;
/*!40000 ALTER TABLE `turnaj_wc` DISABLE KEYS */;
INSERT INTO `turnaj_wc` VALUES (1,2,3,1,NULL,NULL),(2,2,1,3,NULL,NULL),(3,NULL,NULL,NULL,NULL,NULL),(4,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `turnaj_wc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tym`
--

DROP TABLE IF EXISTS `tym`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tym` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nazev` varchar(50) NOT NULL,
  `emblem` varchar(50) NOT NULL,
  `popis` varchar(255) DEFAULT NULL,
  `vudce` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vudce` (`vudce`),
  CONSTRAINT `tym_ibfk_1` FOREIGN KEY (`vudce`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tym`
--

LOCK TABLES `tym` WRITE;
/*!40000 ALTER TABLE `tym` DISABLE KEYS */;
INSERT INTO `tym` VALUES (1,'team 1','emblem.jpeg','tym jednicek',4),(2,'team 2','emblem.jpeg','tym dvojek',2),(3,'team 3','emblem.jpeg','tym trojek',3);
/*!40000 ALTER TABLE `tym` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tym_clenstvi`
--

DROP TABLE IF EXISTS `tym_clenstvi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tym_clenstvi` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hrac` int(10) unsigned NOT NULL,
  `tym` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tym` (`tym`),
  KEY `hrac` (`hrac`),
  CONSTRAINT `tym_clenstvi_ibfk_1` FOREIGN KEY (`tym`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tym_clenstvi_ibfk_2` FOREIGN KEY (`hrac`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tym_clenstvi`
--

LOCK TABLES `tym_clenstvi` WRITE;
/*!40000 ALTER TABLE `tym_clenstvi` DISABLE KEYS */;
INSERT INTO `tym_clenstvi` VALUES (3,4,3),(4,5,1),(6,7,1),(7,8,3),(8,9,3),(9,10,3),(10,11,3),(12,13,1),(13,14,3),(14,15,1),(15,16,1),(16,17,2),(17,18,2),(18,19,3),(19,20,3),(21,12,3);
/*!40000 ALTER TABLE `tym_clenstvi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ucastnici_zapasu`
--

DROP TABLE IF EXISTS `ucastnici_zapasu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ucastnici_zapasu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_zapas` int(10) unsigned NOT NULL,
  `id_tym1` int(10) unsigned DEFAULT NULL,
  `id_tym2` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_zapas` (`id_zapas`),
  KEY `id_tym1` (`id_tym1`),
  KEY `id_tym2` (`id_tym2`),
  CONSTRAINT `ucastnici_zapasu_ibfk_1` FOREIGN KEY (`id_zapas`) REFERENCES `zapas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ucastnici_zapasu_ibfk_2` FOREIGN KEY (`id_tym1`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ucastnici_zapasu_ibfk_3` FOREIGN KEY (`id_tym2`) REFERENCES `tym` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ucastnici_zapasu`
--

LOCK TABLES `ucastnici_zapasu` WRITE;
/*!40000 ALTER TABLE `ucastnici_zapasu` DISABLE KEYS */;
INSERT INTO `ucastnici_zapasu` VALUES (11,15,2,3),(12,16,2,1),(13,17,2,NULL),(14,18,3,1),(15,19,2,3),(16,20,1,NULL),(17,21,2,3),(18,22,3,2),(19,23,NULL,NULL);
/*!40000 ALTER TABLE `ucastnici_zapasu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uzivatele`
--

DROP TABLE IF EXISTS `uzivatele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uzivatele` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `prezdivka` varchar(50) NOT NULL,
  `heslo` binary(77) NOT NULL,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prezdivka` (`prezdivka`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uzivatele`
--

LOCK TABLES `uzivatele` WRITE;
/*!40000 ALTER TABLE `uzivatele` DISABLE KEYS */;
INSERT INTO `uzivatele` VALUES (1,'borec1','$5$rounds=535000$LDFS3GerTIL4giqf$6aSwr0aVYesVT88OLlZlbNzuc/IlfrDtkchJsp5w2L5','user'),(2,'borec2','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(3,'borec3','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(4,'borec4','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(5,'borec5','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(6,'admin','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','admin'),(7,'Dree','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(8,'Makku','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(9,'Taurruss','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(10,'Yogish','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(11,'Sabazios','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(12,'Bublinka','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(13,'Blik','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(14,'Lemp','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(15,'Hade','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(16,'Sprikis','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(17,'Havoczech','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(18,'Whitney','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(19,'Epso','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user'),(20,'Manilla','$5$rounds=535000$luAVQo8aU4Rof7K7$a4dRavFVKAPSPc0ID8JPSBkElgrIJtuLO4kDCsXgxJ7','user');
/*!40000 ALTER TABLE `uzivatele` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vybaveni`
--

DROP TABLE IF EXISTS `vybaveni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vybaveni` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `typ` varchar(50) NOT NULL,
  `vyrobce` varchar(50) NOT NULL,
  `model` varchar(50) NOT NULL,
  `popis` varchar(255) DEFAULT NULL,
  `vlastnik` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vlastnik` (`vlastnik`),
  CONSTRAINT `vybaveni_ibfk_1` FOREIGN KEY (`vlastnik`) REFERENCES `hrac` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vybaveni`
--

LOCK TABLES `vybaveni` WRITE;
/*!40000 ALTER TABLE `vybaveni` DISABLE KEYS */;
INSERT INTO `vybaveni` VALUES (1,'Klavesnice','Asus','Model1',NULL,1),(2,'Mys','Asus','Mysak','Cerna',1),(3,'Graficka karta','Amd','270r',NULL,4),(4,'Procesor','Intel','i7','Kaby Lake',5),(5,'Klavesnice','ASUS','XL1','White',2),(7,'Myš','Asus','Klikač','dobře kliká',3);
/*!40000 ALTER TABLE `vybaveni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zamereni`
--

DROP TABLE IF EXISTS `zamereni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zamereni` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `klan` int(10) unsigned NOT NULL,
  `hra` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `klan` (`klan`),
  KEY `hra` (`hra`),
  CONSTRAINT `zamereni_ibfk_1` FOREIGN KEY (`klan`) REFERENCES `klan` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `zamereni_ibfk_2` FOREIGN KEY (`hra`) REFERENCES `hra` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zamereni`
--

LOCK TABLES `zamereni` WRITE;
/*!40000 ALTER TABLE `zamereni` DISABLE KEYS */;
INSERT INTO `zamereni` VALUES (1,1,1);
/*!40000 ALTER TABLE `zamereni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zapas`
--

DROP TABLE IF EXISTS `zapas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zapas` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kdy` date NOT NULL,
  `skore` varchar(32) DEFAULT NULL,
  `typ` varchar(50) NOT NULL,
  `hra` int(10) unsigned NOT NULL,
  `turnaj` int(10) unsigned DEFAULT NULL,
  `cas` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `hra` (`hra`),
  KEY `turnaj` (`turnaj`),
  CONSTRAINT `zapas_ibfk_1` FOREIGN KEY (`hra`) REFERENCES `hra` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `zapas_ibfk_2` FOREIGN KEY (`turnaj`) REFERENCES `turnaj` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zapas`
--

LOCK TABLES `zapas` WRITE;
/*!40000 ALTER TABLE `zapas` DISABLE KEYS */;
INSERT INTO `zapas` VALUES (15,'2017-05-05','5:2','DeathMatch',3,7,'12:00:00'),(16,'2017-05-05','2:1','DeathMatch',3,7,'13:00:00'),(17,'2017-05-05','','DeathMatch',3,7,'14:00:00'),(18,'2017-09-19','4:8','FlagHunt',5,8,'18:00:00'),(19,'2017-09-19',NULL,'FlagHunt',5,8,'19:00:00'),(20,'2017-09-19','','FlagHunt',5,8,'20:00:00'),(21,'2017-12-24','1:0','KillSatan',9,9,'10:00:00'),(22,'2017-12-10','','KillAll',4,NULL,'19:00:00'),(23,'2017-12-13','','DeathMatch',5,NULL,'10:00:00');
/*!40000 ALTER TABLE `zapas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-12-04 21:28:43
