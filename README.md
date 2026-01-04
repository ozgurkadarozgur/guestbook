# Guestbook API

A simple Guestbook service where users can create entries, view all entries, and retrieve user-based summary information.

## Features

- Create a guestbook entry
- List all entries (ordered from newest to oldest)
- Retrieve user summaries including last entry and total entry count

## Running the Project

> ⚠️ Important  
> Before running the project, make sure to delete the existing `db.sqlite3` file if it exists.  
> Then start the application using Docker Compose.

```bash

rm -f db.sqlite3
docker compose up -d
```

## API Access

The API runs on port 8000.


## Endpoints

### Get Entries

Retrieves guestbook entries with pagination support.  
Entries are returned in reverse chronological order (newest first).

- **Method:** `GET`
- **Endpoint:** `/api/entry`

---

### Create Entry

Creates a new guestbook entry.

- **Method:** `POST`
- **Endpoint:** `/api/entry`
- **Headers:**
  - `Content-Type: application/json`

**Request Body:**
```json
{
  "subject": "...",
  "message": "...",
  "name": "..."
}
```

### Get User Entry Statuses

Retrieves a summary of all users. Including username, last entry information and total number of entries created by each user.

- **Method:** `GET`
- **Endpoint:** `/api/users`
