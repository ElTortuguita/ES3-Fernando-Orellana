
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_usuario'),(22,'Can change user',6,'change_usuario'),(23,'Can delete user',6,'delete_usuario'),(24,'Can view user',6,'view_usuario'),(25,'Can add categoria',7,'add_categoria'),(26,'Can change categoria',7,'change_categoria'),(27,'Can delete categoria',7,'delete_categoria'),(28,'Can view categoria',7,'view_categoria'),(29,'Can add experiencia',8,'add_experiencia'),(30,'Can change experiencia',8,'change_experiencia'),(31,'Can delete experiencia',8,'delete_experiencia'),(32,'Can view experiencia',8,'view_experiencia'),(33,'Can add reserva',9,'add_reserva'),(34,'Can change reserva',9,'change_reserva'),(35,'Can delete reserva',9,'delete_reserva'),(36,'Can view reserva',9,'view_reserva');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `cuentas_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas_usuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `rol` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `cuentas_usuario` WRITE;
/*!40000 ALTER TABLE `cuentas_usuario` DISABLE KEYS */;
INSERT INTO `cuentas_usuario` VALUES (1,'pbkdf2_sha256$1000000$UUwpHApcrNJ1yj3gb06Kxm$H3i002Ws8kkRpBqhmXo9Ur98g188IdAXAjhzSRRmxRE=','2026-11-15 01:10:22.007081',1,'fernando','Fernando','Orellana','',1,1,'2026-11-15 00:47:24.098262','admin'),(2,'pbkdf2_sha256$1000000$Uo6Y45MW7WuLsBG1WyKhzP$jY3Lc3IlGKD0DtCaD/LaTNB/J6Ntu6WpI7nWd1Vd318=','2026-11-15 01:10:22.490683',0,'gabriela','Gabriela','San Martín','',0,1,'2026-11-15 00:47:24.584884','guia'),(3,'pbkdf2_sha256$1000000$1d4qnaUSBnZFrRpNVI6pMQ$a2cFLN+JQFYaXOlBV0Nr3gvFA5dhzJx8xj+jSu1YrOY=','2026-11-15 01:10:22.971550',0,'joseismael','José Ismael','','',0,1,'2026-11-15 00:47:25.064503','guia'),(4,'pbkdf2_sha256$1000000$LH9DngzChPvTUrQAW3fJkX$vNq938Fo2DLHay1EP4Zinb2Cjulm3DHdyeHDfUoNr3I=','2026-11-15 01:10:23.468929',0,'mordelina','Mordelina','Orellana','',0,1,'2026-11-15 00:47:25.564113','turista'),(5,'pbkdf2_sha256$1000000$o1lXKyClgLmIBJts9hDGkG$wJgi6fLkeYJ6OlrrMj6gKFDsTK8xST2pR71Bh/f6wVo=','2026-11-15 01:10:23.956962',0,'javier','Javier','Orellana','',0,1,'2026-11-15 00:47:26.061826','turista');
/*!40000 ALTER TABLE `cuentas_usuario` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `cuentas_usuario_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas_usuario_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cuentas_usuario_groups_usuario_id_group_id_f5ef6c73_uniq` (`usuario_id`,`group_id`),
  KEY `cuentas_usuario_groups_group_id_e6725cc8_fk_auth_group_id` (`group_id`),
  CONSTRAINT `cuentas_usuario_groups_group_id_e6725cc8_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `cuentas_usuario_groups_usuario_id_251ff583_fk_cuentas_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `cuentas_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `cuentas_usuario_groups` WRITE;
/*!40000 ALTER TABLE `cuentas_usuario_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuentas_usuario_groups` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `cuentas_usuario_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas_usuario_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `usuario_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cuentas_usuario_user_per_usuario_id_permission_id_26c0acea_uniq` (`usuario_id`,`permission_id`),
  KEY `cuentas_usuario_user_permission_id_1753ad79_fk_auth_perm` (`permission_id`),
  CONSTRAINT `cuentas_usuario_user_permission_id_1753ad79_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `cuentas_usuario_user_usuario_id_5a9718f1_fk_cuentas_u` FOREIGN KEY (`usuario_id`) REFERENCES `cuentas_usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `cuentas_usuario_user_permissions` WRITE;
/*!40000 ALTER TABLE `cuentas_usuario_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `cuentas_usuario_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_cuentas_usuario_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_cuentas_usuario_id` FOREIGN KEY (`user_id`) REFERENCES `cuentas_usuario` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(6,'cuentas','usuario'),(7,'experiencias','categoria'),(8,'experiencias','experiencia'),(9,'experiencias','reserva'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-11-15 00:47:22.037720'),(2,'contenttypes','0002_remove_content_type_name','2026-11-15 00:47:22.127744'),(3,'auth','0001_initial','2026-11-15 00:47:22.429536'),(4,'auth','0002_alter_permission_name_max_length','2026-11-15 00:47:22.486262'),(5,'auth','0003_alter_user_email_max_length','2026-11-15 00:47:22.492335'),(6,'auth','0004_alter_user_username_opts','2026-11-15 00:47:22.498397'),(7,'auth','0005_alter_user_last_login_null','2026-11-15 00:47:22.505682'),(8,'auth','0006_require_contenttypes_0002','2026-11-15 00:47:22.509414'),(9,'auth','0007_alter_validators_add_error_messages','2026-11-15 00:47:22.515957'),(10,'auth','0008_alter_user_username_max_length','2026-11-15 00:47:22.522996'),(11,'auth','0009_alter_user_last_name_max_length','2026-11-15 00:47:22.530242'),(12,'auth','0010_alter_group_name_max_length','2026-11-15 00:47:22.547361'),(13,'auth','0011_update_proxy_permissions','2026-11-15 00:47:22.555064'),(14,'auth','0012_alter_user_first_name_max_length','2026-11-15 00:47:22.561940'),(15,'cuentas','0001_initial','2026-11-15 00:47:22.868460'),(16,'admin','0001_initial','2026-11-15 00:47:23.005286'),(17,'admin','0002_logentry_remove_auto_add','2026-11-15 00:47:23.014207'),(18,'admin','0003_logentry_add_action_flag_choices','2026-11-15 00:47:23.021641'),(19,'experiencias','0001_initial','2026-11-15 00:47:23.321416'),(20,'sessions','0001_initial','2026-11-15 00:47:23.369426');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('s5ev7obm494eubymdqykqb6g67gwz73j','.eJxVjLsKwzAMAP9FczGWZRw7Y_d-Q5Alu05bEshjKv33EsjQrnfHvWHgfWvDvpZlGBV6cHD5ZZnlWaZD6IOn-2xknrZlzOZIzGlXc5u1vK5n-zdovDbogZxSRvQRrVZL0Zcu5YjiXOqsZ_VIuVDoJIlIRUrZaWVCX0LgkAJ8vsXFN2k:1xSOWP:85l7hrSVcGKGTipXH1E2kedJKV9YhD1suD2iqApN9S8','2026-11-29 00:55:05.274099'),('zooyyrndyddp3ekpzwxlyhfn0k7ukker','.eJxVjDkOwjAQAP-yNbJ8ZH2kpOcN0dpe4wCypRwV4u8oUgpoZ0bzhon2rU77yss0ZxgB4fLLIqUnt0PkB7V7F6m3bZmjOBJx2lXceubX9Wz_BpXWCiN4CqhZZY2stfKFitE2DchoUMrAAUNBN6TBSFOUtKRtpODIBZ_QxgifL8YKNx8:1xSOlD:gOWQs1VIfuBt-lsE_ht6oWmGG4HSMPuFwkqKzirjg5M','2026-11-29 01:10:23.962835');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `experiencias_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `experiencias_categoria` WRITE;
/*!40000 ALTER TABLE `experiencias_categoria` DISABLE KEYS */;
INSERT INTO `experiencias_categoria` VALUES (1,'Trekking','Caminatas guiadas por senderos naturales.',1),(2,'Canopy','Recorridos en altura con equipo de seguridad.',1),(3,'Kayak','Navegación guiada en aguas tranquilas.',1),(4,'Arriendo de equipos','Equipamiento para actividades al aire libre.',1);
/*!40000 ALTER TABLE `experiencias_categoria` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `experiencias_experiencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_experiencia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` decimal(10,0) NOT NULL,
  `cupo_maximo` int unsigned NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `categoria_id` bigint NOT NULL,
  `creador_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `experiencias_experie_categoria_id_b03f452f_fk_experienc` (`categoria_id`),
  KEY `experiencias_experie_creador_id_70b19025_fk_cuentas_u` (`creador_id`),
  CONSTRAINT `experiencias_experie_categoria_id_b03f452f_fk_experienc` FOREIGN KEY (`categoria_id`) REFERENCES `experiencias_categoria` (`id`),
  CONSTRAINT `experiencias_experie_creador_id_70b19025_fk_cuentas_u` FOREIGN KEY (`creador_id`) REFERENCES `cuentas_usuario` (`id`),
  CONSTRAINT `experiencias_experiencia_chk_1` CHECK ((`cupo_maximo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `experiencias_experiencia` WRITE;
/*!40000 ALTER TABLE `experiencias_experiencia` DISABLE KEYS */;
INSERT INTO `experiencias_experiencia` VALUES (1,'Sendero de Gabriela','Caminata guiada por Gabriela San Martín entre senderos y miradores del ecoparque.',12000,10,'2026-11-22 14:00:00.000000',1,1,2),(2,'Canopy del bosque azul','Circuito de canopy a cargo de Gabriela, con orientación y equipo de seguridad.',18000,10,'2026-11-23 14:00:00.000000',1,2,2),(3,'Kayak con Fernando','Una salida de kayak pensada para compartir un paseo con Fernando Orellana.',15000,10,'2026-11-24 14:00:00.000000',1,3,2),(4,'Equipo para paseo familiar','Arriendo de equipo para que Fernando, Gabriela y la familia recorran los senderos.',8000,10,'2026-11-25 14:00:00.000000',1,4,2),(5,'Ruta de José Ismael','Recorrido guiado por José Ismael para disfrutar el bosque y llegar al mirador.',12000,10,'2026-11-26 14:00:00.000000',1,1,3),(6,'Canopy de los Orellana','Una experiencia de canopy para una jornada de aventura de la familia Orellana.',18000,10,'2026-11-27 14:00:00.000000',1,2,3),(7,'Kayak al atardecer','Salida de kayak guiada por José Ismael para disfrutar del paisaje al atardecer.',15000,10,'2026-11-28 14:00:00.000000',1,3,3),(8,'Campamento Mordelina','Arriendo de equipo de campamento con un nombre dedicado a Mordelina Orellana.',8000,10,'2026-11-29 14:00:00.000000',1,4,3);
/*!40000 ALTER TABLE `experiencias_experiencia` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `experiencias_reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_reserva` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_inscripcion` datetime(6) NOT NULL,
  `estado_pago` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `experiencia_id` bigint NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `experiencias_reserva_usuario_id_experiencia_id_ded11f3e_uniq` (`usuario_id`,`experiencia_id`),
  KEY `experiencias_reserva_experiencia_id_ca702f09_fk_experienc` (`experiencia_id`),
  CONSTRAINT `experiencias_reserva_experiencia_id_ca702f09_fk_experienc` FOREIGN KEY (`experiencia_id`) REFERENCES `experiencias_experiencia` (`id`),
  CONSTRAINT `experiencias_reserva_usuario_id_8724df18_fk_cuentas_usuario_id` FOREIGN KEY (`usuario_id`) REFERENCES `cuentas_usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `experiencias_reserva` WRITE;
/*!40000 ALTER TABLE `experiencias_reserva` DISABLE KEYS */;
INSERT INTO `experiencias_reserva` VALUES (1,'2026-11-15 00:47:26.599551','confirmado',1,4),(2,'2026-11-15 00:47:26.604899','pendiente',2,4),(3,'2026-11-15 00:47:26.610545','pendiente',3,4),(4,'2026-11-15 00:47:26.615273','confirmado',4,5),(5,'2026-11-15 00:47:26.619955','pendiente',5,5),(6,'2026-11-15 00:47:26.624804','pendiente',6,5),(7,'2026-11-15 00:49:21.840299','pendiente',7,4);
/*!40000 ALTER TABLE `experiencias_reserva` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

