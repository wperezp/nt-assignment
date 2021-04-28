create table analytics.dwh_fincidents (
    incident_number CHAR(10) PRIMARY KEY,
    incident_date TIMESTAMP,
    call_number CHAR(10),
    alarm_time TIMESTAMP,
    arrival_time TIMESTAMP,
    close_time TIMESTAMP,
    suppression_units INT,
    suppression_personnel INT,
    ems_units INT,
    ems_personnel INT,
    other_units INT,
    other_personnel INT,
    first_unit_on_scene VARCHAR(100),
    fire_fatalities INT,
    fire_injuries INT,
    civilian_fatalities INT,
    civilian_injuries INT,
    number_alarms INT,
    mutual_aid VARCHAR(50),
    action_taken_primary VARCHAR(100),
    action_taken_secondary VARCHAR(100),
    action_taken_other VARCHAR(100)
);