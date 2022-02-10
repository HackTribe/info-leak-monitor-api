-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 172.18.0.2    Database: info-leak-monitor
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB-1:10.6.5+maria~focal
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;

/*!40101 SET NAMES utf8mb4 */;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;

/*!40103 SET TIME_ZONE='+00:00' */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `alembic_version` (`version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
PRIMARY KEY (`version_num`)) ENGINE=InnoDB DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--
LOCK TABLES `alembic_version` WRITE;

/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;


INSERT INTO `alembic_version`
VALUES ('5b5cad1bb429');

/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `apscheduler_jobs`
--

DROP TABLE IF EXISTS `apscheduler_jobs`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `apscheduler_jobs` (`id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
`next_run_time` double DEFAULT NULL,
`job_state` blob NOT NULL,
PRIMARY KEY (`id`), KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)) ENGINE=InnoDB DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apscheduler_jobs`
--
LOCK TABLES `apscheduler_jobs` WRITE;

/*!40000 ALTER TABLE `apscheduler_jobs` DISABLE KEYS */;

/*!40000 ALTER TABLE `apscheduler_jobs` ENABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `git_access_tokens`
--

DROP TABLE IF EXISTS `git_access_tokens`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `git_access_tokens` (`id` bigint(20) NOT NULL AUTO_INCREMENT,
`create_time` bigint(20) DEFAULT NULL,
`update_time` bigint(20) DEFAULT NULL,
`is_drop` int(11) DEFAULT NULL,
`kind` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
`access_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`next_time` bigint(20) NOT NULL,
PRIMARY KEY (`id`), KEY `ix_git_access_tokens_id` (`id`)) ENGINE=InnoDB DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `git_access_tokens`
--
LOCK TABLES `git_access_tokens` WRITE;

/*!40000 ALTER TABLE `git_access_tokens` DISABLE KEYS */;

/*!40000 ALTER TABLE `git_access_tokens` ENABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `leaks`
--

DROP TABLE IF EXISTS `leaks`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `leaks` (`id` bigint(20) NOT NULL AUTO_INCREMENT,
`create_time` bigint(20) DEFAULT NULL,
`update_time` bigint(20) DEFAULT NULL,
`is_drop` int(11) DEFAULT NULL,
`kind` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
`leakiest` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`sha` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`fragment` text COLLATE utf8mb4_unicode_ci NOT NULL,
`html_url` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
`last_modified` datetime DEFAULT current_timestamp(),
`file_name` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
`repo_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
`repo_url` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
`user_avatar` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
`user_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`user_url` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
`leak_count` int(11) DEFAULT NULL,
`follow` tinyint(1) DEFAULT NULL,
`ignore` tinyint(1) DEFAULT NULL,
`is_white` tinyint(1) DEFAULT NULL,
`is_process` tinyint(1) DEFAULT NULL,
PRIMARY KEY (`id`), KEY `ix_leaks_id` (`id`),
CONSTRAINT `CONSTRAINT_1` CHECK (`follow` in (0,
1)), CONSTRAINT `CONSTRAINT_2` CHECK (`ignore` in (0,
1)), CONSTRAINT `CONSTRAINT_3` CHECK (`is_white` in (0,
1)), CONSTRAINT `CONSTRAINT_4` CHECK (`is_process` in (0,
1))) ENGINE=InnoDB DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaks`
--
LOCK TABLES `leaks` WRITE;

/*!40000 ALTER TABLE `leaks` DISABLE KEYS */;

/*!40000 ALTER TABLE `leaks` ENABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `users` (`id` bigint(20) NOT NULL AUTO_INCREMENT,
`create_time` bigint(20) DEFAULT NULL,
`update_time` bigint(20) DEFAULT NULL,
`is_drop` int(11) DEFAULT NULL,
`username` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
`password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`email` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
PRIMARY KEY (`id`), UNIQUE KEY `username` (`username`),
UNIQUE KEY `email` (`email`),
KEY `ix_users_id` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--
LOCK TABLES `users` WRITE;

/*!40000 ALTER TABLE `users` DISABLE KEYS */;


INSERT INTO `users`
VALUES (1,1644486540,1644486540,0,'admin','$2b$12$puz7h4SxUFHDkFHHF2/LT.xyKHMAfXL0VFoLwVOvv8XcHwuvQDBje','admin@hacktribe.org');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;

UNLOCK TABLES;

--
-- Table structure for table `whitelists`
--

DROP TABLE IF EXISTS `whitelists`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;


CREATE TABLE `whitelists` (`id` bigint(20) NOT NULL AUTO_INCREMENT,
`create_time` bigint(20) DEFAULT NULL,
`update_time` bigint(20) DEFAULT NULL,
`is_drop` int(11) DEFAULT NULL,
`kind` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
`sha` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
`url_path` varchar(512) COLLATE utf8mb4_unicode_ci NOT NULL,
`url_path_last_time` datetime NOT NULL,
PRIMARY KEY (`id`), KEY `ix_whitelists_id` (`id`)) ENGINE=InnoDB DEFAULT
CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `whitelists`
--
LOCK TABLES `whitelists` WRITE;

/*!40000 ALTER TABLE `whitelists` DISABLE KEYS */;

/*!40000 ALTER TABLE `whitelists` ENABLE KEYS */;

UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-10 10:11:12
