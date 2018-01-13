CREATE DATABASE fogi;
USE fogi;

CREATE TABLE users (
	id INT AUTO_INCREMENT, 
	email VARCHAR(255) NOT NULL UNIQUE, 
	google_id VARCHAR(255) NOT NULL, 
	google_img VARCHAR(255), 
	is_admin BOOLEAN DEFAULT FALSE, 
	PRIMARY KEY (id)
);

CREATE TABLE play_lists (
	id INT AUTO_INCREMENT, 
	user_id INT NOT NULL, 
	name VARCHAR(255), 
	date_created DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE artists (
	id INT AUTO_INCREMENT, 
    name VARCHAR(255) NOT NULL, 
	description VARCHAR(255), 
	PRIMARY KEY (id)
);

CREATE TABLE tracks (
	id INT AUTO_INCREMENT, 
	artist_id INT NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	img VARCHAR(255), 
	lyrics TEXT, 
	description VARCHAR(255), 
	PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);


CREATE TABLE youtubes (
	id INT AUTO_INCREMENT, 
	track_id INT NOT NULL, 
	video_id VARCHAR(255), 
	duration INT, 
	date_published DATETIME,  
	description VARCHAR(255), 
	PRIMARY KEY (id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

CREATE TABLE tags (
	id INT AUTO_INCREMENT, 	
	name VARCHAR(255) NOT NULL UNIQUE, 
	PRIMARY KEY (id),
    INDEX(name)
);


CREATE TABLE events (
	id INT AUTO_INCREMENT, 
	artist_id INT NOT NULL, 
	location VARCHAR(255) NOT NULL, 
	date DATETIME NOT NULL, 
	uri VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE tracks_to_tags (
	track_id INT NOT NULL, 
	tag_id INT NOT NULL, 
	PRIMARY KEY (track_id, tag_id),
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);