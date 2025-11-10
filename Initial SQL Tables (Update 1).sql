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

CREATE TABLE Instructor(
    iid INT PRIMARY KEY,
    instructorName TEXT,
    instructorInfo TEXT,
    department TEXT
);

CREATE TABLE Bookings(
    bid INT PRIMARY KEY,
    startTime int,
    endTime int,
    bookingDate int,
    bookingStatus TEXT,
    cid int,
    rid int,
    iid int,
    FOREIGN KEY (cid) REFERENCES Courses(cid),
    FOREIGN KEY (rid) REFERENCES Rooms(rid),
    FOREIGN KEY (iid) REFERENCES Instructor(iid)
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

-- Reject all bookings for room r. 
Update Bookings SET bookingStatus = "Reject" Where rid = 311;

-- Cancel booking b.
DELETE FROM Bookings WHERE bid = 12;

-- Accept booking b.
Update Bookings SET bookingStatus = "Approve" Where bid = 15;





-- 5 Informal Queries

-- For some specific programs, an instructor may want to book classes or events in the same vacinity.
-- Similar to how all our classes for third year Computer Eng Tech are all on the third floor
-- The command is trying to view all the avalible data for rooms within a particular area, in the example it would be all rooms on the third floor

Select * from Rooms WHERE roomLocation Between 300 and 399;

-- This command views all bookings for a specific room. This command could be used by instructors to view all the information about a specific room
-- which would assist when booking for the specified location.

Select * FROM Bookings WHERE rid = 221;

-- This command views all the information about rooms based on the specified tech features. In the example, this could be used by an instructor to
-- plan their room booking based on the technology description they need. This may not work as the text description is very specific to what is stored
-- So if the instructor gets too specific and enters "Macs" for example instead of "Computers" they may not find the correct information.
Select * From Rooms WHERE techFeatures = "Computers";

-- This command is used to reject any bookings after a certain time. This command could be used by the system automatically to reject any bookings that
-- are attempted to be made after operational hours. This command may not work as someone could put in a time outside the boundary but confuse the AM/PM.
-- Therefore the command could fail and book a class based on military time and the user expect a booking at a different time. 
Update Bookings SET bookingStatus = "Reject" WHERE startTime > 2000 AND startTime < 0800;

-- This command would show all the information for bookings made by a specific instructor based on their Instructor ID. This could be used by an Admin to
-- assess the bookings of the specified instructors. This may not work in the event that the admin enters the wrong or invalid instructor ID.
Select * From Bookings where iid = 243;
