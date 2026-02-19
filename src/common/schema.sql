CREATE TABLE IF NOT EXISTS titles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  genre TEXT[],
  year INT,
  description TEXT
);

CREATE TABLE IF NOT EXISTS watch_history (
  user_id TEXT NOT NULL,
  title_id TEXT NOT NULL REFERENCES titles(id),
  last_position_seconds INT NOT NULL DEFAULT 0,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, title_id)
);

-- Trending events aggregation (optional if you store trending only in Redis)
CREATE TABLE IF NOT EXISTS title_events (
  title_id TEXT NOT NULL REFERENCES titles(id),
  event_type TEXT NOT NULL,
  ts TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for the resume bullet
CREATE INDEX IF NOT EXISTS idx_watch_history_user_updated
  ON watch_history (user_id, updated_at DESC);

CREATE INDEX IF NOT EXISTS idx_title_events_title_ts
  ON title_events (title_id, ts DESC);

