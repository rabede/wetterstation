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

