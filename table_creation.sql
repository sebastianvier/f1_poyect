CREATE DATABASE formula_1;


USE formula_1;

## 1) First table Drivers
## This table does not have foreign keys

DROP TABLE drivers;
CREATE TABLE drivers (
	DriverId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    BirthDate date,
	Nationality varchar(50),
    Gender varchar(50)
);

SELECT * FROM DRIVERS;
