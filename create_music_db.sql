CREATE TABLE Genre (
	id serial PRIMARY KEY, 
	name varchar(100) NOT null
);

CREATE TABLE Artist (
	id serial PRIMARY KEY, 
	name varchar(100) NOT null
);

CREATE TABLE Album (
	id serial PRIMARY KEY, 
	title varchar(100) NOT NULL,
	release_year int NOT null
);

CREATE TABLE Track (
	id serial PRIMARY KEY, 
	title varchar(100) NOT NULL,
	duration time NOT NULL,
	album_id int REFERENCES album(id)
);

CREATE TABLE Compilation (
	id serial PRIMARY KEY,
	title varchar(100) NOT NULL,
	release_year int NOT NULL
);

CREATE TABLE artist_genre(
	artist_id int REFERENCES Artist(id),
	genre_id int REFERENCES Genre(id),
	PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE album_artist (
	album_id int REFERENCES Album(id),
	artist_id int REFERENCES Artist(id),
	PRIMARY KEY (album_id, artist_id)
);

CREATE TABLE compilation_track (
	compilation_id int REFERENCES Compilation(id),
	track_id int REFERENCES Track(id),
	PRIMARY KEY (compilation_id, track_id)
);