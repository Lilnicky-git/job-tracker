# Job Hunt Tracker

A personal practice project that will help me learn how to use a common
real data architecture pattern: an API layer, an MCP server, a database, and an AI agent, all working together.

This project is a way to learn how these pieces connect,
not a production tool.

## Status

Database schema designed and reviewed (six related tables: companies,
postings, requirements, applications, tasks, communications) and
version-controlled in `schema.sql`. A local SQLite database has been
built from that schema using a small Python script (`init_db.py`). 
Sample data has been created in `seed_data.py` to populate the database.  

A learning log has been created within a Claude.ai project relating to
this project. This tracks specific moments where a decision or mistake
brings up teaching points. This is kept separate from the repo itself.



Next: build the MCP server layer.