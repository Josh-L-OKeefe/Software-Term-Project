CREATE TABLE Rooms(
    rid INT PRIMARY KEY,
    capacity INT,
    roomLocation INT,
    techFeatures TEXT,
    availableStatus boolean
);

CREATE TABLE Courses(
    cid INT PRIMARY KEY,
    courseName TEXT,
    creditHours int,
    requirements TEXT
);

CREATE TABLE Bookings(
    bid INT PRIMARY KEY,
    startTime int,
    endTime int,
    bookingDate int,
    cid int,
    FOREIGN KEY (cid) REFERENCES Courses(cid),
    FOREIGN KEY (rid) REFERENCES Rooms(rid)
);

CREATE TABLE Instructor(
    iid INT PRIMARY KEY,
    instructorName TEXT,
    instructorInfo TEXT,
    department TEXT
);

CREATE TABLE Administrator(
    aid INT PRIMARY KEY,
    adminName TEXT,
    adminInfo TEXT
);