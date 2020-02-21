drop database if exists DBbank_crawler;

create database DBbank_crawler;

use DBbank_crawler;

CREATE TABLE IF NOT EXISTS `bank_webcrawler`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `createtime` TIMESTAMP DEFAULT NOW() ,
   `url` VARCHAR(256) NOT NULL,
   `postdate` VARCHAR(40) NOT NULL,
   `bank` VARCHAR(40) NOT NULL,
   `title` VARCHAR(256) NOT NULL,
   `content` MEDIUMTEXT  NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY unique_url (url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bank_notification`(
   `id` INT UNSIGNED AUTO_INCREMENT ,
   `createtime` TIMESTAMP DEFAULT NOW() ,
   `updatetime` TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
   `url` VARCHAR(256) NOT NULL,
   `postdate` VARCHAR(40) NOT NULL,
   `bank` VARCHAR(40) NOT NULL,
   `title` VARCHAR(256) NOT NULL,
   `notes` VARCHAR(256) NOT NULL,
   `status` int(8) NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY unique_url (url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;




