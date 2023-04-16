CREATE TABLE IF NOT EXISTS violations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  remote_id INTEGER NOT NULL,
  business_id INTEGER NOT NULL,
  date DATE NOT NULL,
  description TEXT NOT NULL,
  address TEXT NOT NULL,
  judgement_date DATE NOT NULL,
  establishment TEXT NOT NULL,
  amount NUMERIC(10,2) NOT NULL,
  owner TEXT NOT NULL,
  city TEXT NOT NULL,
  status TEXT NOT NULL,
  status_date DATE NOT NULL,
  category TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_violations_remote_id ON violations (remote_id);
