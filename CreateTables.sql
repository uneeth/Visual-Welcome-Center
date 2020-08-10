CREATE DATABASE Visual_Welcome_Center;
USE Visual_Welcome_Center;

-- the user table stores all the user details
CREATE TABLE `user`
(
`email` varchar(50) NOT NULL,
`full_name` varchar(255) DEFAULT NULL,
`enrolled_on` datetime DEFAULT NULL,
`designation` varchar(500) DEFAULT NULL,
`department` varchar(100) DEFAULT NULL,
`phone` varchar(10) DEFAULT NULL,
`website` varchar(100) DEFAULT NULL,
PRIMARY KEY (`email`)
);
-- the timesheet table saves user entries 
CREATE TABLE `timesheet`
(
`email` varchar(50) NOT NULL,
`date` varchar(10) NOT NULL,
`clock_in` varchar(5) NOT NULL,
FOREIGN KEY (`email`) REFERENCES `User`(`email`) on delete cascade
);
-- image table saves the path to the latest image of each user
CREATE TABLE `image`
(
`email` varchar(50) NOT NULL,
`image_path` varchar(1000) NOT NULL,
FOREIGN KEY (`email`) REFERENCES `User`(`email`) ON DELETE CASCADE
)
