CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  privileges TEXT NOT NULL
);
-- privileges:
-- guest - no permisions,
-- user - read,
-- privileged - read, write, delete
-- admin - read, write, delete and chaning others privileges
CREATE TABLE companies (
  'id' INTEGER PRIMARY KEY AUTOINCREMENT,
  'Company name' TEXT NOT NULL,
  'Field of work' TEXT NOT NULL,
  'Address' TEXT NOT NULL,
  'Name of Mentor/ Contact person' TEXT NOT NULL,
  'Phone number' TEXT NOT NULL,
  'Email' TEXT NOT NULL,
  'Website' TEXT NOT NULL,
  'Max number of students' INTEGER NOT NULL,
  'Current student count' INTEGER NOT NULL,
  'Status' TEXT NOT NULL,
  'Commute' TEXT NOT NULL,
  'Required additional equipment/ clothes' TEXT NOT NULL,
  'Important information' TEXT NOT NULL,
  'Creation date' datetime NOT NULL,
  'Last update' datetime NOT NULL
);
CREATE TABLE comments (
  'id' INTEGER PRIMARY KEY AUTOINCREMENT,
  'Content' TEXT NOT NULL,
  'Author' TEXT NOT NULL,
  'Creation date' datetime NOT NULL,
  'company_id' INTEGER NOT NULL,
  FOREIGN KEY (company_id) REFERENCES companies(id)
);