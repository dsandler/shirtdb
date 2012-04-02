CREATE TABLE shirts (
    uid integer auto_increment primary key,
	college varchar(20),
	year decimal(4),
	face varchar(16),
	variant varchar(16),
	filename varchar(255),
	author varchar(255),
	description text,
	added datetime
);
CREATE INDEX shirts_college on shirts (college);
CREATE INDEX shirts_year on shirts (year);
CREATE INDEX shirts_college_year on shirts (college, year);
CREATE INDEX shirts_added on shirts (added);

-- CREATE TABLE themes (
-- 	college varchar(20),
-- 	year decimal(4),
-- 	name varchar(255),
-- 	description text
-- );
-- CREATE INDEX themes_college_year on themes (college, year);
