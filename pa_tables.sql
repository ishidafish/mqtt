use pabox;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `item`;
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
  `attr06` varchar(200) DEFAULT NULL,
  `attr07` varchar(200) DEFAULT NULL,
  `attr08` varchar(200) DEFAULT NULL,
  `attr09` varchar(200) DEFAULT NULL,
  `attr10` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `item_iot_id` (`iot_id`),
  KEY `item_imei` (`imei`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

BEGIN;
INSERT INTO `item` VALUES (1, '測試的', 'testiotid', 'testimei', '只是測試', 'OK', NULL, NULL, '2019-07-26 12:49:39', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
COMMIT;

DROP TABLE IF EXISTS `code_detail`;
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


BEGIN;
INSERT INTO `code_detail` VALUES ('REPLY', '02', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '05', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '13', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '14', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '15', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '0A', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '0D', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('REPLY', '0E', 'F0', '接收到 0xF0指令,回复', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '02', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '05', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '0A', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '0D', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '0E', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '13', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '14', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
INSERT INTO `code_detail` VALUES ('PUBLISH', '15', 'DIRTY', '当ITEM资料有变动', NULL, NULL, NULL, NULL, NULL);
COMMIT;


DROP TABLE IF EXISTS `trandata`;
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

BEGIN;
INSERT INTO `trandata` VALUES (3, 'test123', '02', 'TSYN', 0, '时间同步', '[2019, 7, 24, 8, 45, 32]', '7', NULL, NULL, NULL, NULL, '2019-07-24 00:45:32');
INSERT INTO `trandata` VALUES (4, 'test123', '02', 'TSYN', 0, '时间同步', '[2019, 7, 24, 8, 48, 40]', '7', NULL, NULL, NULL, NULL, '2019-07-24 00:48:40');
INSERT INTO `trandata` VALUES (5, '', '01', 'PING', 1, '连接握手(sec)', '[80]', '2', NULL, NULL, NULL, NULL, '2019-08-01 12:33:09');
INSERT INTO `trandata` VALUES (6, '', '01', 'PING', 1, '连接握手(sec)', '[80]', '2', NULL, NULL, NULL, NULL, '2019-08-01 12:42:53');
INSERT INTO `trandata` VALUES (7, '861929041497593', '01', 'PING', 1, '连接握手(sec)', '[80]', '2', NULL, NULL, NULL, NULL, '2019-08-01 12:49:02');
INSERT INTO `trandata` VALUES (8, '861929041497593', '01', 'PING', 1, '[R]:连接握手(sec)', '[80]', '2', NULL, NULL, NULL, NULL, '2019-08-01 12:49:02');
COMMIT;




