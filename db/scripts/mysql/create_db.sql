USE DbMysql04;

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
	play_list_name VARCHAR(255), 
	date_created DATETIME NOT_NULL, 
	PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE artists (
	id INT AUTO_INCREMENT, 
    artist_name VARCHAR(255) NOT NULL UNIQUE,
    play_count BIGINT NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE tracks (
	id INT AUTO_INCREMENT, 
	artist_id INT NOT NULL, 
	track_name VARCHAR(255) NOT NULL,
    album VARCHAR(255),
    play_count BIGINT NOT NULL,
	img VARCHAR(255),
	lyrics TEXT, 
	description TEXT,
	PRIMARY KEY (id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE youtubes (
	id INT AUTO_INCREMENT, 
	track_id INT NOT NULL, 
	video_id VARCHAR(255) NOT NULL,
	duration INT, 
	date_published DATETIME NOT NULL,  
	PRIMARY KEY (id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

CREATE TABLE tags (
	id INT AUTO_INCREMENT, 	
	tag_name VARCHAR(255) NOT NULL UNIQUE, 
	PRIMARY KEY (id),
    INDEX(tag_name)
);

CREATE TABLE events (
	id INT AUTO_INCREMENT, 
	artist_id INT NOT NULL, 
	country VARCHAR(255),
	city VARCHAR(255),
	venue VARCHAR(255),
	date DATETIME NOT NULL,
	url VARCHAR(255) NOT NULL,
	title VARCHAR(511),
	img VARCHAR(255),
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

CREATE TABLE tracks_to_play_lists (
	play_list_id INT NOT NULL,
	track_id INT NOT NULL,
	track_position INT NOT NULL,
	PRIMARY KEY (play_list_id, track_id),
    FOREIGN KEY (play_list_id) REFERENCES play_lists(id),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

CREATE TABLE tracks_isam (
	id INT,
	track_name VARCHAR(255) NOT NULL,
	lyrics TEXT,
	description TEXT,
	PRIMARY KEY (id),
    FULLTEXT INDEX (lyrics, description, track_name)
) ENGINE = MyISAM;

CREATE VIEW artists_tracks_youtubes AS
SELECT artists.id as artist_id, artists.artist_name, artists.play_count as artist_play_count, tracks.id as track_id, tracks.track_name, tracks.img, 
	tracks.play_count as track_play_count, youtubes.video_id, youtubes.date_published,
youtubes.duration
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists ON tracks.artist_id = artists.id;

CREATE VIEW artists_newest_track AS
SELECT DISTINCT x.id as artist_id, x.artist_name, x.play_count as artist_play_count, tracks.id as track_id,
    tracks.track_name, tracks.img, tracks.play_count as track_play_count, youtubes.video_id, youtubes.date_published
FROM youtubes
INNER JOIN tracks ON youtubes.track_id = tracks.id
INNER JOIN artists AS x ON tracks.artist_id = x.id
AND youtubes.date_published = (
	SELECT MAX(date_published) 
    FROM youtubes
	INNER JOIN tracks ON tracks.id = youtubes.track_id
    WHERE x.id = tracks.artist_id
);