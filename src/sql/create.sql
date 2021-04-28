create table analytics.dwh_fincidents (
    "Incident Number" CHAR(10) PRIMARY KEY,
    "Incident Date" TIMESTAMP,
    "Call Number" CHAR(10),
    "Alarm DtTm" TIMESTAMP,
    "Arrival DtTm" TIMESTAMP,
    "Close DtTm" TIMESTAMP,
    "Suppression Units" INT,
    "Suppression Personnel" INT,
    "EMS Units" INT,
    "EMS Personnel" INT,
    "Other Units" INT,
    "Other Personnel" INT,
    "First Unit On Scene" VARCHAR(100),
    "Fire Fatalities" INT,
    "Fire Injuries" INT,
    "Civilian Fatalities" INT,
    "Civilian Injuries" INT,
    "Number of Alarms" INT,
    "Mutual Aid" VARCHAR(50),
    "Action Taken Primary" VARCHAR(100),
    "Action Taken Secondary" VARCHAR(100),
    "Action Taken Other" VARCHAR(100)
);

create table analytics.dwh_dgeography (
    "Incident Number" CHAR(10) PRIMARY KEY,
    "Address" VARCHAR(200),
    "City" VARCHAR(100),
    "zipcode" CHAR(20),
    "Battalion" VARCHAR(20),
    "Station Area" VARCHAR(20),
    "Box" VARCHAR(20),
    "Supervisor District" VARCHAR(50),
    "neighborhood_district" VARCHAR(50),
    "point" POINT
)


create table staging.dwh_fincidents (
    "Incident Number" VARCHAR(100) PRIMARY KEY,
    "Incident Date" VARCHAR(100),
    "Call Number" VARCHAR(100),
    "Alarm DtTm" VARCHAR(100),
    "Arrival DtTm" VARCHAR(100),
    "Close DtTm" VARCHAR(100),
    "Suppression Units" VARCHAR(100),
    "Suppression Personnel" VARCHAR(100),
    "EMS Units" VARCHAR(100),
    "EMS Personnel" VARCHAR(100),
    "Other Units" VARCHAR(100),
    "Other Personnel" VARCHAR(100),
    "First Unit On Scene" VARCHAR(100),
    "Fire Fatalities" VARCHAR(100),
    "Fire Injuries" VARCHAR(100),
    "Civilian Fatalities" VARCHAR(100),
    "Civilian Injuries" VARCHAR(100),
    "Number of Alarms" VARCHAR(100),
    "Mutual Aid" VARCHAR(100),
    "Action Taken Primary" VARCHAR(100),
    "Action Taken Secondary" VARCHAR(100),
    "Action Taken Other" VARCHAR(100)
);
