CREATE TABLE Employee (
	id serial PRIMARY KEY,
	name varchar(100) NOT NULL,
	department varchar(100) NOT NULL,
	manager_id int REFERENCES Employee(id) ON DELETE SET NULL
);

