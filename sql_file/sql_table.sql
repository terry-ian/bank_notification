drop database if exists bi_notice;

create database bi_notice;

set global max_allowed_packet = 2*1024*1024*10 ;

SET GLOBAL innodb_buffer_pool_size= 1024*20 ;

use bi_notice;

CREATE TABLE IF NOT EXISTS `bank_webcrawler`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `createtime` TIMESTAMP DEFAULT NOW() ,
   `url` VARCHAR(255) NOT NULL,
   `postdate` VARCHAR(40) NOT NULL,
   `bank` VARCHAR(40) NOT NULL,
   `title` VARCHAR(255) NOT NULL,
   `content` MEDIUMTEXT  NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY unique_url (url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `bank_notification`(
   `id` INT UNSIGNED AUTO_INCREMENT ,
   `createtime` TIMESTAMP DEFAULT NOW() ,
   `updatetime` TIMESTAMP DEFAULT NOW() ON UPDATE NOW(),
   `url` VARCHAR(255) NOT NULL,
   `postdate` VARCHAR(40) NOT NULL,
   `bank` VARCHAR(40) NOT NULL,
   `title` VARCHAR(255) NOT NULL,
   `notes` VARCHAR(255) NOT NULL,
   `status` int(8) NOT NULL,
   PRIMARY KEY (id),
   UNIQUE KEY unique_url (url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

