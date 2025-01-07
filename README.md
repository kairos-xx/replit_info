
# Replit Info API

A simple API to fetch information about Replit repls using GraphQL.

## Features

- Get detailed information about a repl using its ID
- Optional title-only response
- Error handling for invalid requests

## Endpoints

- `/get` - Get repl information
  - Query parameters:
    - `replit_id` (optional): The ID of the repl. If not provided, uses current repl's ID
    - `title` (optional): If present, returns only the repl's title

## Usage

```python
# Example request
GET /get?replit_id=your-repl-id

# Get only title
GET /get?replit_id=your-repl-id&title=1
```

## Repository
For more information, visit: [GitHub Repository](https://github.com/kairos-xx/replit_info.git)
