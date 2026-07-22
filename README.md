# Job Hunt Tracker

A personal practice project that will help me learn how to use a common real data 
architecture pattern: an API layer, an MCP (Model Context Protocol)
server, a database, and an AI agent, all working together.

This project is a hands-on way to learn how these pieces connect,
not a production tool.

## Status

Database schema designed and reviewd (six related tabels: compnaies, postings, requirements, applications, tasks, communications) and version controlled in 'schema.sql'. A local SQLite database had been built from that schema using a small Python script ('init_bd.py). 

A Learning log has been created within a Claude.ai project relating to this project. This tracks specific moments where a dicision or mistake beings up taching points. This is kept seperate from the repo itself.

Next: Populate the database with data, then build the MCP server layer