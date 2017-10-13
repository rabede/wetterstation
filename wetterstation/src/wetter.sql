--<ScriptOptions statementTerminator=";"/>

CREATE TABLE `database`.`wetter` (
	`temperatur` FLOAT,
	`humidity` SMALLINT,
	`windspeed` FLOAT,
	`downfall` FLOAT,
	`rain` BIT,
	`timestamp` TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP' NOT NULL,
	PRIMARY KEY (`timestamp`)
) ENGINE=InnoDB;

create table lastcheckedsensor (sensor_id varchar(6));
insert into lastcheckedsensor (sensor_id) values ('6269');



