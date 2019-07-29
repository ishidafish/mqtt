CREATE USER 'iot'@localhost IDENTIFIED BY 'iot';
GRANT ALL ON *.* to iot@localhost;
CREATE DATABASE `pabox`;
USE `pabox`;
CREATE TABLE `code_detail` (
  `code_type` varchar(32) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `code_name` varchar(45) DEFAULT NULL,
  `desc` varchar(45) DEFAULT NULL,
  `attr01` varchar(45) DEFAULT NULL,
  `attr02` varchar(45) DEFAULT NULL,
  `attr03` varchar(45) DEFAULT NULL,
  `attr04` varchar(45) DEFAULT NULL,
  `attr05` varchar(45) DEFAULT NULL,
  UNIQUE KEY `code_UNIQUE` (`code_type`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `iot_id` varchar(45) DEFAULT NULL,
  `imei` varchar(45) DEFAULT NULL,
  `desc` varchar(45) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `last_off_time` datetime DEFAULT NULL,
  `on_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `attr01` varchar(45) DEFAULT NULL,
  `attr02` varchar(45) DEFAULT NULL,
  `attr03` varchar(45) DEFAULT NULL,
  `attr04` varchar(45) DEFAULT NULL,
  `attr05` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_iot_id` (`iot_id`),
  KEY `item_imei` (`imei`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `trandata` (
  `line_id` int(11) NOT NULL AUTO_INCREMENT,
  `imei` varchar(32) DEFAULT NULL,
  `code` varchar(45) DEFAULT NULL,
  `code_name` varchar(45) DEFAULT NULL,
  `seq` int(11) DEFAULT NULL,
  `desc` varchar(45) DEFAULT NULL,
  `data` varchar(200) DEFAULT NULL,
  `attr01` varchar(45) DEFAULT NULL,
  `attr02` varchar(45) DEFAULT NULL,
  `attr03` varchar(45) DEFAULT NULL,
  `attr04` varchar(45) DEFAULT NULL,
  `attr05` varchar(45) DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`line_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
