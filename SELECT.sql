-- Задание 2
--Название и продолжительность самого длительного трека.
SELECT title, MAX(duration) FROM track 
GROUP BY title 
ORDER BY MAX(duration) DESC
LIMIT 1;

--Название треков, продолжительность которых не менее 3,5 минут.
SELECT title 
FROM track
WHERE duration >= '00:03:30';

--Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT title
FROM compilation
WHERE release_year BETWEEN 2018 AND 2020;

--Исполнители, чьё имя состоит из одного слова.
SELECT name 
FROM artist
WHERE name NOT LIKE '% %';

--Название треков, которые содержат слово «мой» или «my».
SELECT DISTINCT title 
FROM track
WHERE lower(title) ~* '\mмой\M' OR lower(title) ~* '\mmy\M';

-- Задание 3
--Количество исполнителей в каждом жанре.
SELECT g.name, count(ag.artist_id) AS artist_count 
FROM genre g 
LEFT JOIN artist_genre ag ON g.id = ag.genre_id 
GROUP BY g.name;

--Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT count(t.id) AS track_count
FROM track t 
JOIN album a ON t.album_id = a.id 
WHERE a.release_year BETWEEN 2019 AND 2020;

--Средняя продолжительность треков по каждому альбому.
SELECT a.title, avg(t.duration) AS avg_track_duration
FROM album a 
JOIN track t ON a.id = t.album_id 
GROUP BY a.title;

--Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT DISTINCT ar.name
FROM artist ar
WHERE ar.id NOT IN (
	SELECT aa.artist_id
	FROM album_artist aa 
	JOIN album al ON aa.album_id = al.id
	WHERE al.release_year = 2020
);

--Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT DISTINCT c.title
FROM compilation c 
JOIN compilation_track ct ON c.id = ct.compilation_id 
JOIN track t ON ct.track_id = t.id 
JOIN album a ON t.album_id = a.id 
JOIN album_artist aa ON a.id = aa.album_id 
JOIN artist ar ON aa.artist_id = ar.id
WHERE ar.name = 'Queen';

-- Задание 4
--Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT a.title
FROM album a
JOIN album_artist aa ON a.id = aa.album_id 
JOIN artist_genre ag ON aa.artist_id  = ag.artist_id 
GROUP BY a.id, aa.artist_id
HAVING count(DISTINCT ag.genre_id ) > 1;

-- второй вариант - с подзапросом:
SELECT DISTINCT a.title
FROM album a 
JOIN album_artist aa ON a.id = aa.album_id 
WHERE aa.artist_id IN (
	SELECT ag.artist_id
	FROM artist_genre ag 
	GROUP BY ag.artist_id
	HAVING count(DISTINCT ag.genre_id) > 1
);

--Наименования треков, которые не входят в сборники.
SELECT t.title
FROM track t 
LEFT JOIN compilation_track ct ON t.id = ct.track_id 
WHERE ct.compilation_id IS NULL;

--Исполнитель или исполнители, написавшие самый короткий по продолжительности трек,
-- — теоретически таких треков может быть несколько.
SELECT ar.name
FROM artist ar 
JOIN album_artist aa ON ar.id = aa.artist_id 
JOIN album al ON aa.album_id = al.id 
JOIN track t ON al.id = t.album_id 
WHERE t.duration = (SELECT min(duration) FROM track);

--Названия альбомов, содержащих наименьшее количество треков.
SELECT a.title
FROM album a
JOIN track t ON a.id = t.album_id 
GROUP BY a.id
HAVING count(t.id) = (
	SELECT count(t.id)
	FROM album a
	JOIN track t ON a.id = t.album_id 
	GROUP BY a.id
	ORDER BY count(t.id)
	LIMIT 1
);







