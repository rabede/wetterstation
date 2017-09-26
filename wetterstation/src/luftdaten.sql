--<ScriptOptions statementTerminator=";"/>

CREATE TABLE `database`.`luftdaten` (
	`timestamp` TIMESTAMP DEFAULT 'CURRENT_TIMESTAMP' NOT NULL,
	`sensor_id` VARCHAR(6) NOT NULL,
	`sensor_type` VARCHAR(6),
	`location` VARCHAR(6),
	`lat` FLOAT,
	`lon` FLOAT,
	`p1` FLOAT,
	`p2` FLOAT,
	`pressure` FLOAT,
	`temperature` FLOAT,
	`humidity` FLOAT,
	PRIMARY KEY (`timestamp`,`sensor_id`)
) ENGINE=InnoDB;

