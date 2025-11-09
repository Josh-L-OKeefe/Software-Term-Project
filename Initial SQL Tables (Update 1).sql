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


-- View available rooms with capacity over p.
Select * from Rooms WHERE capacity > 20;

-- View available rooms with capacity over p and technology t.
Select * from Rooms WHERE capacity > 20 AND techFeatures = "";



-- 5 Informal Queries

-- For some specific programs, an instructor may want to book classes or events in the same vacinity.
-- Similar to how all our classes for third year Computer Eng Tech are all on the third floor
--The command is trying to view all the avalible data for rooms within a particular area, in the example it would be all rooms on the third floor

Select * from Rooms WHERE roomLocation Between 300 and 399;

