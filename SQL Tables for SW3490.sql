CREATE TABLE Users(
    userid INT PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email TEXT,
    userPassword TEXT,
    permissions boolean
);

CREATE TABLE Events(
    eid INT PRIMARY KEY,
    eventName TEXT,
    eventDate DATE,
    eventTime TIME,
    eventLocation TEXT,
    eventDescription TEXT,
    eventCapacity INT
);

CREATE TABLE Rooms(
    rid INT PRIMARY KEY,
    roomAvailability BOOLEAN
);
