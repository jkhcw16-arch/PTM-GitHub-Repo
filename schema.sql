CREATE TABLE IF NOT EXISTS contact_inquiries (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  name TEXT NOT NULL,
  organization TEXT NOT NULL DEFAULT '',
  email TEXT NOT NULL,
  use_case TEXT NOT NULL DEFAULT '',
  integration_interest TEXT NOT NULL DEFAULT '',
  message TEXT NOT NULL
) STRICT;
CREATE INDEX IF NOT EXISTS idx_contact_inquiries_created_at ON contact_inquiries(created_at);
