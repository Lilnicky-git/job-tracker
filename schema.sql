CREATE TABLE companies (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  industry TEXT,
  notes TEXT
);

CREATE TABLE postings (
  id INTEGER PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  title TEXT NOT NULL,
  location TEXT,
  salary_min INTEGER,
  salary_max INTEGER,
  source_url TEXT,
  date_found TEXT,
  status TEXT DEFAULT 'new' -- new, matched, dismissed
);

CREATE TABLE requirements (
  id INTEGER PRIMARY KEY,
  posting_id INTEGER REFERENCES postings(id),
  requirement TEXT,
  must_have BOOLEAN
);

CREATE TABLE applications (
  id INTEGER PRIMARY KEY,
  posting_id INTEGER REFERENCES postings(id),
  date_applied TEXT,
  stage TEXT DEFAULT 'applied', -- applied, interview, offer, rejected
  notes TEXT
);

CREATE TABLE tasks (
  id INTEGER PRIMARY KEY,
  application_id INTEGER REFERENCES applications(id),
  type TEXT,
  due_date TEXT,
  status TEXT DEFAULT 'open', -- open, complete, overdue
  notes TEXT
);

CREATE TABLE communications (
  id INTEGER PRIMARY KEY,
  application_id INTEGER REFERENCES applications(id),
  date TEXT,
  type TEXT,               -- email, call, message
  direction TEXT,           -- inbound, outbound
  summary TEXT,
  follow_up_required BOOLEAN DEFAULT 0,
  related_task_id INTEGER REFERENCES tasks(id)
);