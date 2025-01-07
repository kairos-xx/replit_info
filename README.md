
<div align="center">
  <img src="https://github.com/kairos-xx/replit_info/raw/main/assets/icon_raster.png" alt="Replit Info API Logo" width="150"/>
  <h1>Replit Info API</h1>
  <p><em>Access Replit repl information through a simple GraphQL API</em></p>

  <a href="https://replit.com/@kairos/replitinfo">
    <img src="https://github.com/kairos-xx/replit_info/raw/main/assets/replit.png" alt="Try it on Replit" width="150"/>
  </a>
</div>

## Quick Start
```python
# Get repl title
GET /get?replit_id=your-repl-id&title=1

# Get full repl info
GET /get?replit_id=your-repl-id
```

## Features
- 🚀 Fast and simple GraphQL-based API
- 📦 Get detailed repl information
- 🎯 Optional title-only responses
- ⚡ Automatic error handling

## API Reference
### GET /get
Query Parameters:
- `replit_id` (optional): Target repl ID
- `title` (optional): Return only the title

## Links
- [GitHub Repository](https://github.com/kairos-xx/replit_info.git)
- [Live Demo](https://replit.com/@kairos/replitinfo)
