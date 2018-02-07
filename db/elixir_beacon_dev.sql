-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: elixir_beacon_dev
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `adam_table`
--

DROP TABLE IF EXISTS `adam_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adam_table` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `attribute` varchar(50) NOT NULL,
  `description` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `attribute` (`attribute`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adam_table`
--

LOCK TABLES `adam_table` WRITE;
/*!40000 ALTER TABLE `adam_table` DISABLE KEYS */;
INSERT INTO `adam_table` VALUES (1,'anyCountry','within any country/location'),(2,'allowedCountries','within specified countries/locations'),(3,'excludedCountries','within any country/location other than those specified'),(4,'anyOrganisation','by all organisations'),(5,'anyNonProfitOrganisation','by any non-profit organisations'),(6,'allowedNonProfitOrganisations','by specified non-profit organisations'),(7,'excludedNonProfitOrganisations','by any non-profit organisations other than those specified'),(8,'anyProfitOrganisation','by any profit organisations'),(9,'allowedProfitOrganisations','by specified profit organisations'),(10,'excludedProfitOrganisations','by any profit organisation other than those specified'),(11,'anyPerson','by any category of person'),(12,'anyAcademicProfessional','by any category of academic professional'),(13,'allowedAcademicProfessionals','by specified categories of academic professional'),(14,'excludedAcademicProfessionals','by any category of academic professional other than those specified'),(15,'anyClinicalProfessional','by any category of clinical professional'),(16,'allowedClinicalProfessionals','by specified categories of clinical professional'),(17,'excludedClinicalProfessionals','by any category of clinical professional other than those specified'),(18,'anyProfitmakingProfessional','by any category of profit-making professional'),(19,'allowedProfitmakingProfessionals','by specified categories of profit-making professional'),(20,'excludedProfitmakingProfessionals','by any category of profit-making professional other than those specified'),(21,'anyNonProfessional','by any category of non-professional'),(22,'allowedNonProfessionals','by specified categories of non-professional'),(23,'excludedNonProfessionals','by any category of non-professional other than those specified'),(24,'anyDomain','for any domain'),(25,'anyResearch','for any research purpose'),(26,'anyFundamentalBiologyResearch','for research w.r.t. fundamental biology'),(27,'anyMethodsDevelopmentResearch','for research w.r.t. methods development'),(28,'anyPopulationResearch','for research w.r.t. populations'),(29,'anyAncestryResearch','for research w.r.t. ancestry'),(30,'anyGeneticResearch','for research w.r.t. genetics'),(31,'anyDrugDevelopmentResearch','for research w.r.t. drug development'),(32,'anyDiseaseResearch','for research w.r.t. any disease'),(33,'allowedDiseasesResearch','for research w.r.t. any disease other than those specified'),(34,'excludedDiseasesResearch','for research w.r.t. specified diseases'),(35,'allowedAgeCategoriesResearch','for research w.r.t. specified age categories'),(36,'allowedGenderCategoriesResearch','for research w.r.t. specified gender categories'),(37,'allowedOtherResearch','for other specified categories of research'),(38,'anyClinicalCare','for any clinical care purpose'),(39,'anyDiseasesClinicalCare','for clinical care w.r.t.  any disease'),(40,'allowedDiseasesClinicalCare','for clinical care w.r.t.  any disease other than those specified'),(41,'excludedDiseasesClinicalCare','for clinical care w.r.t. specified diseases'),(42,'allowedOtherClinicalCare','for other specified categories of clinical care'),(43,'anyProfitPurpose','for any profit purpose'),(44,'allowedProfitPurposes','for specified profit purposes'),(45,'excludedProfitPurposes','for any profit purpose other than those specified'),(46,'anyNonProfitPurpose','for any non-profit purpose'),(47,'allowedNonProfitPurposes','for specified non-profit purposes'),(48,'excludedNonProfitPurposes','for any non-profit purpose other than those specified'),(49,'metaConditions','Meta-Conditions:'),(50,'noOtherConditions','There are no other restrictions/limitations in force which are not herein specified'),(51,'whichOtherConditions','Other permissions/limitations may apply as specified'),(52,'sensitivePopulations','No special evaluation required for access requests involving sensitive/restricted populations'),(53,'uniformConsent','Identical consent permissions have been provided by all subjects'),(54,'termsOfAgreement','Terms of agreement:'),(55,'noAuthorizationObligations','There are no requirements for any formal approval, contract or review conditions to be satisfied'),(56,'whichAuthorizationObligations','Formal approval, contract or review conditions are to be met, as specified'),(57,'noPublicationObligations','There are no requirements regarding publication or disclosure of derived results'),(58,'whichPublicationObligations','Publication or disclosure of derived results is subject to restrictions, as specified'),(59,'noTimelineObligations','There are no timeline restrictions'),(60,'whichTimelineObligations','The period of access has time limitations, as specified'),(61,'noSecurityObligations','There are no requirements regarding data security measures'),(62,'whichSecurityObligations','User must have adequate data security measures, as specified'),(63,'noExpungingObligations','There are no requirements regarding withdrawal, destruction or return of any subject data'),(64,'whichExpungingObligations','Some subject data must be withdrawn, destroyed or returned, as specified'),(65,'noLinkingObligations','There are no restrictions regarding the linking of accessed records to other datasets'),(66,'whichLinkingObligations','Accessed records may only be linked to other datasets, as specified'),(67,'noRecontactProvisions','There is no possibility of recontacting data subjects'),(68,'allowedRecontactProvisions','Subject recontact may occur in certain circumstances, as specified'),(69,'compulsoryRecontactProvisions','Subject recontact must occur in certain circumstances, as specified'),(70,'noIPClaimObligations','There are no restrictions regarding intellectual property claims based on use of the accessed resource'),(71,'whichIPClaimObligations','Options for intellectual property claims based on use of the accessed resources are limited, as specified'),(72,'noReportingObligations','There are no requirements to report back regarding use of the accessed resources'),(73,'whichReportingObligations','Reporting on use of the accessed resources may be required, as specified'),(74,'noPaymentObligations','No fees will be levied for access of the resources'),(75,'whichPaymentObligations','Fees may be levied for access of the resources, as specified');
/*!40000 ALTER TABLE `adam_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adam_value_table`
--

DROP TABLE IF EXISTS `adam_value_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adam_value_table` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(13) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adam_value_table`
--

LOCK TABLES `adam_value_table` WRITE;
/*!40000 ALTER TABLE `adam_value_table` DISABLE KEYS */;
INSERT INTO `adam_value_table` VALUES (1,'NOT SPECIFIED'),(2,'UNTRUE'),(3,'TRUE');
/*!40000 ALTER TABLE `adam_value_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `beacon_data`
--

DROP TABLE IF EXISTS `beacon_data`;
/*!50001 DROP VIEW IF EXISTS `beacon_data`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `beacon_data` (
 `dataset_id` tinyint NOT NULL,
  `chromosome` tinyint NOT NULL,
  `position` tinyint NOT NULL,
  `alternate` tinyint NOT NULL,
  `reference_genome` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `beacon_data_table`
--

DROP TABLE IF EXISTS `beacon_data_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beacon_data_table` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `dataset_id` varchar(50) NOT NULL,
  `chromosome` varchar(2) NOT NULL,
  `position` int(11) NOT NULL,
  `alternate` varchar(250) DEFAULT NULL,
  `occurrence` int(10) DEFAULT NULL,
  `chr_pos_alt_dset` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `dataset_id` (`dataset_id`,`chromosome`,`position`,`alternate`),
  UNIQUE KEY `track_vars` (`chr_pos_alt_dset`)
) ENGINE=InnoDB AUTO_INCREMENT=540276 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon_data_table`
--

LOCK TABLES `beacon_data_table` WRITE;
/*!40000 ALTER TABLE `beacon_data_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `beacon_data_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `beacon_dataset`
--

DROP TABLE IF EXISTS `beacon_dataset`;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `beacon_dataset` (
 `id` tinyint NOT NULL,
  `description` tinyint NOT NULL,
  `access_type` tinyint NOT NULL,
  `reference_genome` tinyint NOT NULL,
  `size` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `beacon_dataset_adam`
--

DROP TABLE IF EXISTS `beacon_dataset_adam`;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset_adam`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `beacon_dataset_adam` (
 `dataset_id` tinyint NOT NULL,
  `attribute` tinyint NOT NULL,
  `value` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `beacon_dataset_adam_detailed_table`
--

DROP TABLE IF EXISTS `beacon_dataset_adam_detailed_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beacon_dataset_adam_detailed_table` (
  `dataset_id` varchar(50) NOT NULL,
  `adam_id` int(11) NOT NULL,
  `value` varchar(200) NOT NULL,
  PRIMARY KEY (`dataset_id`,`adam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon_dataset_adam_detailed_table`
--

LOCK TABLES `beacon_dataset_adam_detailed_table` WRITE;
/*!40000 ALTER TABLE `beacon_dataset_adam_detailed_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `beacon_dataset_adam_detailed_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beacon_dataset_adam_table`
--

DROP TABLE IF EXISTS `beacon_dataset_adam_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beacon_dataset_adam_table` (
  `dataset_id` varchar(50) NOT NULL,
  `adam_id` int(11) NOT NULL,
  `value_id` int(11) NOT NULL,
  PRIMARY KEY (`dataset_id`,`adam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon_dataset_adam_table`
--

LOCK TABLES `beacon_dataset_adam_table` WRITE;
/*!40000 ALTER TABLE `beacon_dataset_adam_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `beacon_dataset_adam_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `beacon_dataset_consent_code`
--

DROP TABLE IF EXISTS `beacon_dataset_consent_code`;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset_consent_code`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `beacon_dataset_consent_code` (
 `dataset_id` tinyint NOT NULL,
  `code` tinyint NOT NULL,
  `description` tinyint NOT NULL,
  `detail` tinyint NOT NULL,
  `category` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `beacon_dataset_consent_code_table`
--

DROP TABLE IF EXISTS `beacon_dataset_consent_code_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beacon_dataset_consent_code_table` (
  `dataset_id` varchar(50) NOT NULL,
  `consent_code_id` int(11) NOT NULL,
  `detail` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`dataset_id`,`consent_code_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon_dataset_consent_code_table`
--

LOCK TABLES `beacon_dataset_consent_code_table` WRITE;
/*!40000 ALTER TABLE `beacon_dataset_consent_code_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `beacon_dataset_consent_code_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beacon_dataset_table`
--

DROP TABLE IF EXISTS `beacon_dataset_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beacon_dataset_table` (
  `id` varchar(50) NOT NULL,
  `description` varchar(800) DEFAULT NULL,
  `access_type` varchar(10) DEFAULT NULL,
  `reference_genome` varchar(50) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beacon_dataset_table`
--

LOCK TABLES `beacon_dataset_table` WRITE;
/*!40000 ALTER TABLE `beacon_dataset_table` DISABLE KEYS */;
/*!40000 ALTER TABLE `beacon_dataset_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consent_code_category_table`
--

DROP TABLE IF EXISTS `consent_code_category_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consent_code_category_table` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consent_code_category_table`
--

LOCK TABLES `consent_code_category_table` WRITE;
/*!40000 ALTER TABLE `consent_code_category_table` DISABLE KEYS */;
INSERT INTO `consent_code_category_table` VALUES (1,'PRIMARY'),(2,'SECONDARY'),(3,'REQUIREMENT');
/*!40000 ALTER TABLE `consent_code_category_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consent_code_table`
--

DROP TABLE IF EXISTS `consent_code_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `consent_code_table` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `abbr` varchar(4) NOT NULL,
  `description` varchar(400) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consent_code_table`
--

LOCK TABLES `consent_code_table` WRITE;
/*!40000 ALTER TABLE `consent_code_table` DISABLE KEYS */;
INSERT INTO `consent_code_table` VALUES (1,'No restrictions','NRES','No restrictions on data use.',1),(2,'General research use and clinical care','GRU','For health/medical/biomedical purposes, including the study of population origins or ancestry.',1),(3,'Health/medical/biomedical research and clinical care','HMB','Use of the data is limited to health/medical/biomedical purposes; does not include the study of population origins or ancestry.',1),(4,'Disease-specific research and clinical care','DS','Use of the data must be related to [disease].',1),(5,'Population origins/ancestry research','POA','Use of the data is limited to the study of population origins or ancestry.',1),(6,'Oher research-specific restrictions','RS','Use of the data is limited to studies of [research type] (e.g., pediatric research).',2),(7,'Research use only','RUO','Use of data is limited to research purposes (e.g., does not include its use in clinical care).',2),(8,'No “general methods” research','NMDS','Use of the data includes methods development research (e.g., development of software or algorithms) ONLY within the bounds of other data use limitations.',2),(9,'Genetic studies only','GSO','Use of the data is limited to genetic studies only (i.e., no “phenotype-only” research).',2),(10,'Not-for-profit use only','NPU','Use of the data is limited to not-for-profit organizations.',3),(11,'Publication required','PUB','Requestor agrees to make results of studies using the data available to the larger scientific community.',3),(12,'Collaboration required','COL','Requestor must agree to collaboration with the primary study investigator(s).',3),(13,'Ethics approval required','IRB','Requestor must provide documentation of local IRB/REC approval.',3),(14,'Geographical restrictions','GS','Use of the data is limited to within [geographic region].',3),(15,'Publication moratorium/embargo','MOR','Requestor agrees not to publish results of studies until [date].',3),(16,'Time limits on use','TS','Use of data is approved for [x months].',3),(17,'User-specific restrictions','US','Use of data is limited to use by approved users.',3),(18,'Project-specific restrictions','PS','Use of data is limited to use within an approved project.',3),(19,'Institution-specific restrictions','IS','Use of data is limited to use within an approved institution.',3);
/*!40000 ALTER TABLE `consent_code_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `beacon_data`
--

/*!50001 DROP TABLE IF EXISTS `beacon_data`*/;
/*!50001 DROP VIEW IF EXISTS `beacon_data`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `beacon_data` AS select `bd`.`dataset_id` AS `dataset_id`,`bd`.`chromosome` AS `chromosome`,`bd`.`position` AS `position`,`bd`.`alternate` AS `alternate`,`ebdat`.`reference_genome` AS `reference_genome` from (`beacon_data_table` `bd` join `beacon_dataset` `ebdat` on((`bd`.`dataset_id` = `ebdat`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `beacon_dataset`
--

/*!50001 DROP TABLE IF EXISTS `beacon_dataset`*/;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `beacon_dataset` AS select `bdat`.`id` AS `id`,`bdat`.`description` AS `description`,`bdat`.`access_type` AS `access_type`,`bdat`.`reference_genome` AS `reference_genome`,`bdat`.`size` AS `size` from `beacon_dataset_table` `bdat` where ((`bdat`.`access_type` in ('PUBLIC','REGISTERED','CONTROLLED')) and (`bdat`.`size` > 0) and (`bdat`.`reference_genome` <> '')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `beacon_dataset_adam`
--

/*!50001 DROP TABLE IF EXISTS `beacon_dataset_adam`*/;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset_adam`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `beacon_dataset_adam` AS select `subq`.`dataset_id` AS `dataset_id`,`a`.`attribute` AS `attribute`,`subq`.`value` AS `value` from (((select `da`.`dataset_id` AS `dataset_id`,`da`.`adam_id` AS `adam_id`,`av`.`value` AS `value` from (`elixir_beacon_dev`.`beacon_dataset_adam_table` `da` join `elixir_beacon_dev`.`adam_value_table` `av` on((`av`.`id` = `da`.`value_id`)))) union select `detailed`.`dataset_id` AS `dataset_id`,`detailed`.`adam_id` AS `adam_id`,`detailed`.`value` AS `value` from `elixir_beacon_dev`.`beacon_dataset_adam_detailed_table` `detailed` order by `dataset_id`,`adam_id`) `subq` join `elixir_beacon_dev`.`adam_table` `a` on((`a`.`id` = `subq`.`adam_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `beacon_dataset_consent_code`
--

/*!50001 DROP TABLE IF EXISTS `beacon_dataset_consent_code`*/;
/*!50001 DROP VIEW IF EXISTS `beacon_dataset_consent_code`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `beacon_dataset_consent_code` AS select `dc`.`dataset_id` AS `dataset_id`,`code`.`abbr` AS `code`,`code`.`description` AS `description`,`dc`.`detail` AS `detail`,`cat`.`name` AS `category` from ((`beacon_dataset_consent_code_table` `dc` join `consent_code_table` `code` on((`code`.`id` = `dc`.`consent_code_id`))) join `consent_code_category_table` `cat` on((`cat`.`id` = `code`.`category_id`))) order by `dc`.`dataset_id`,`cat`.`id`,`code`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-02-07  9:31:18
