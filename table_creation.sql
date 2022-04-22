CREATE DATABASE formula_1;


USE formula_1;


DROP TABLE drivers;

CREATE TABLE drivers (
	DriverId INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    FirstName varchar(50) NOT NULL,
    LastName varchar(50) NOT NULL,
    BirthDate DATE,
	Nationality varchar(50),
    Gender varchar(50)
);

SELECT * FROM DRIVERS;

INSERT INTO drivers (FirstName,LastName,BirthDate, Nationality, Gender) 
VALUES ("a",
		"a",
        STR_TO_DATE('1-01-2012', '%d-%m-%Y'),
        "Hello",
        "GoodBye");
