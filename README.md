# Cybersecurity-API

To install our necessary packages, run the following:
pip install fastapi[all]
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install psycopg2
pip install bleach
pip install slowapi

Next, to get the server running, run:
fastapi dev main.py

Visit the following to see the local webserver:
http://localhost:8000/

To test routes, visit:
http://localhost:8000/docs


What we have:
Vulnerability                          Fix Implemented                        Location                   How It Fixes the Issue

SQL Injection                          SQLAlchemy ORM                         crud.py (db queries)       Uses parameterized queries instead of raw SQL
Arbitrary File Upload                  Extension whitelist                    main.py                    Only allows .doc/.docx uploads
Filename Collisions / Path Traversal   uuid + Path().suffix                   main.py                    Prevents unsafe filenames and overwriting
Insecure File Execution                Whitelist-based file access            main.py                    Only reads safe, predefined script files
Cross-Site Scripting (XSS)             bleach + DOMPurify                     crud.py, Discussion.jsx    Sanitizes user input to remove harmful HTML/JS
Rate Limiting                          slowapi (3/minute per IP)              main.py                    Prevents brute force by limiting request frequency
Frontend Script Injection Prevention   React auto-escaping + DOMPurify        Discussion.jsx             Prevents execution of embedded scripts in UI
