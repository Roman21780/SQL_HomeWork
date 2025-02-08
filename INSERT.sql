INSERT INTO Genre (name) VALUES 
('Rock'),
('Pop'),
('Hip-Hop'),
('Jazz');

INSERT INTO artist (name) VALUES 
('Queen'),
('Michael Jackson'),
('Eminem'),
('Louis Armstrong');

INSERT INTO album (title, release_year) VALUES
('A Night at the Opera', 1975),
('Thriller', 1982),
('The Marshall Mathers LP', 2000),
('What a Wonderful World', 1967);

INSERT INTO track (title, duration, album_id) VALUES
('Bohemian Rhapsody', '00:05:55', 1),
('Love of My Life', '00:03:39', 1),
('Thriller', '00:05:58', 2),
('Beat It', '00:04:18', 2),
('Stan', '00:06:44', 3),
('The Real Slim Shady', '00:04:44', 3),
('What a Wonderful World', '00:02:19', 4),
('Hello Dolly', '00:02:27', 4),
('my own', '00:02:28', 1),
('own my', '00:03:27', 3),
('my', '00:04:27', 4),
('oh my god', '00:05:27', 2),
('myself', '00:02:37', 2),
('by myself', '00:02:47', 4),
('bemy self', '00:02:57', 4),
('myself by', '00:02:17', 3),
('by myself by', '00:02:39', 3),
('beemy', '00:02:39', 1),
('premyne', '00:02:39', 2);

INSERT INTO  compilation (title, release_year) VALUES 
('Greatest Hits of the 70s', 2000),
('Pop Classics', 2010),
('Hip-Hop Essentials', 2015),
('Jazz Legends', 1995);

INSERT INTO artist_genre (artist_id, genre_id) VALUES
(1, 1), -- Queen -> Rock
(2, 2), -- Michael Jackson -> Pop
(3, 3), -- Eminem -> Hip-Hop
(4, 4); -- Louis Armstrong -> Jazz

INSERT INTO artist_genre (artist_id, genre_id) VALUES (1, 2)
ON CONFLICT (artist_id, genre_id) DO NOTHING;

INSERT INTO album_artist (album_id, artist_id) VALUES
(1, 1), -- A Night at the Opera -> Queen
(2, 2), -- Thriller -> Michael Jackson
(3, 3), -- The Marshall Mathers LP -> Eminem
(4, 4); -- What a Wonderful World -> Louis Armstrong

INSERT INTO compilation_track (compilation_id, track_id) VALUES 
(1, 1), -- Greatest Hits of the 70s -> Bohemian Rhapsody
(1, 2), -- Greatest Hits of the 70s -> Love of My Life
(2, 3), -- Pop Classics -> Thriller
(2, 4), -- Pop Classics -> Beat It
(3, 5), -- Hip-Hop Essentials -> Stan
(3, 6), -- Hip-Hop Essentials -> The Real Slim Shady
(4, 7), -- Jazz Legends -> What a Wonderful World
(4, 8); -- Jazz Legends -> Hello Dolly










