CREATE DATABASE  IF NOT EXISTS `alarmostat` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `alarmostat`;
-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: alarmostat
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `component`
--

DROP TABLE IF EXISTS `component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `component` (
  `idcomponent` int(11) NOT NULL AUTO_INCREMENT,
  `componentname` varchar(45) NOT NULL,
  `componenttype` varchar(45) NOT NULL,
  PRIMARY KEY (`idcomponent`),
  UNIQUE KEY `componentname_UNIQUE` (`componentname`),
  UNIQUE KEY `idcomponent_UNIQUE` (`idcomponent`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `component`
--

LOCK TABLES `component` WRITE;
/*!40000 ALTER TABLE `component` DISABLE KEYS */;
INSERT INTO `component` VALUES (1,'ds18b20','thermostat'),(2,'rfidrc522','alarm'),(3,'ada375','alarm'),(4,'hcsr501','alarm'),(5,'web','controls'),(6,'heating','thermostat');
/*!40000 ALTER TABLE `component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `event` (
  `idevent` int(11) NOT NULL AUTO_INCREMENT,
  `eventdatetime` datetime NOT NULL,
  `eventtype` varchar(45) NOT NULL,
  `idcomponent` int(11) NOT NULL,
  `iduser` int(11) NOT NULL,
  PRIMARY KEY (`idevent`),
  UNIQUE KEY `idevent_UNIQUE` (`idevent`),
  KEY `idcomponentevent` (`idcomponent`),
  KEY `iduser` (`iduser`),
  CONSTRAINT `idcomponentevent` FOREIGN KEY (`idcomponent`) REFERENCES `component` (`idcomponent`),
  CONSTRAINT `iduser` FOREIGN KEY (`iduser`) REFERENCES `user` (`iduser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measurement`
--

DROP TABLE IF EXISTS `measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `measurement` (
  `idmeasurement` int(11) NOT NULL AUTO_INCREMENT,
  `measurementdatetime` datetime NOT NULL,
  `measuredvalue` varchar(45) NOT NULL,
  `idcomponent` int(11) NOT NULL,
  PRIMARY KEY (`idmeasurement`),
  UNIQUE KEY `idmeasurement_UNIQUE` (`idmeasurement`),
  KEY `idcomponentmeasurement` (`idcomponent`),
  CONSTRAINT `idcomponentmeasurement` FOREIGN KEY (`idcomponent`) REFERENCES `component` (`idcomponent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measurement`
--

LOCK TABLES `measurement` WRITE;
/*!40000 ALTER TABLE `measurement` DISABLE KEYS */;
/*!40000 ALTER TABLE `measurement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `iduser` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `usertype` varchar(45) NOT NULL,
  `userpassword` varchar(45) NOT NULL,
  `userrfidtag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`iduser`),
  UNIQUE KEY `iduser_UNIQUE` (`iduser`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `userrfidtag_UNIQUE` (`userrfidtag`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'system','administrator','wachtwoord',NULL);
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

-- Dump completed on 2019-06-17  8:58:47
