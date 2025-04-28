# Cybersecurity-API

This is the backend for my Intro to Cybersecurity final project, it uses FastAPI and PostgreSQL. It is made to briefly mimic Canvas and show off potential vulnerabilities and their patches.

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

1. SQL Injection

---

Vulnerability:

- An attacker could manipulate a database query by injecting malicious SQL code into a form (e.g., login form, search box).

Patch:

- We used SQLAlchemy ORM for all database queries, which automatically parameterizes inputs and prevents raw SQL execution.

Demo:

- "In a vulnerable system, an attacker could log in without a real account by injecting code like ' OR 1=1 --.
  In our system, because we use SQLAlchemy's safe filter() and query() methods, user inputs are never inserted directly into SQL queries, blocking this kind of attack."
- (Try entering ' OR 1=1 -- into a login field — it will fail properly.)

2. Arbitrary File Upload

---

Vulnerability:

- An attacker might upload a malicious file like a .exe or a script instead of a safe document.

Patch:

- We restricted file uploads to only allow .doc and .docx Word documents.
- Any other file types are rejected on the backend.

Demo Script:

- "If a system accepts any file, attackers could upload viruses or server scripts.
  Here, if we try uploading a .png or .exe, the server immediately blocks it because only .doc and .docx are whitelisted."

3. Path Traversal / Filename Collision

---

Vulnerability:

- Attackers could try uploading files with names like ../../etc/passwd.
- They could also try overwriting other users' files by uploading the same filename.

Patch:

- Every uploaded file is renamed with a random UUID and correct extension, so no unsafe filenames are used.
- Uploading the same filename twice saves it under two unique names.

Demo Script:

- "By using a random UUID for every file upload, even if the original filename is malicious, it cannot affect the server.
  Here we upload files with the same name — you'll see they are saved separately, preventing overwriting."

4. Insecure File Execution

---

Vulnerability:

- If uploaded or requested files are executed rather than safely handled, an attacker could run arbitrary code on the server.

Patch:

- We use a strict whitelist for reading files, only allowing specific known scripts.

Demo Script:

- "We don't allow users to choose any file path. Only specific scripts on a safe list can be accessed safely.
  If I try to access an unauthorized script or system file, the server returns a 404 error."

5. Cross-Site Scripting (XSS)

---

Vulnerability:

- An attacker injects malicious JavaScript into a form field (e.g., <script>alert('XSS')</script>) and the browser executes it.

Patch:

- We sanitize all user input on the backend using bleach, and again on the frontend using DOMPurify to clean any HTML before saving or displaying.

Demo Script:

- "In a vulnerable app, posting <script>alert('XSS')</script> would pop up an alert or run malicious code.
  Here, user input is sanitized so the script is treated as plain text and never executed."

6. Rate Limiting

---

Vulnerability:

- Without limits, attackers could spam the server with rapid requests, overwhelming it (brute force, upload spam, etc.).

Patch:

- We implemented request rate limiting using slowapi, allowing only 3 uploads per minute per IP address.

Demo Script:

- "To prevent spamming attacks, if I try uploading more than 3 files very quickly, the server automatically blocks the fourth upload and responds with a 429 'Too Many Requests' error."

7. Frontend Script Injection Prevention

---

Vulnerability:

- If the frontend does not escape user input, malicious HTML or JavaScript could still run even if backend protection exists.

Patch:

- React automatically escapes variables when rendering.
- We additionally sanitize discussion post input with DOMPurify on the frontend before it is sent to the server.

Demo Script:

- "Even if an attacker tries to inject something like an <img> tag with an onerror JavaScript payload, it will display harmlessly as text because React escapes it and DOMPurify sanitizes it."

---

## Mock bad attempts for demo

SQL Injection Test (Login)

- Input: username'--
- Expected Result: Login fails — input is safely handled through ORM.

Arbitrary Upload Test

- Try uploading .exe, .png, .jpg, or .pdf.
- Expected Result: Upload blocked — 400 error "Unsupported file type."

Path Traversal Filename Test

- Rename your upload file to ../../server/secret.txt
- Expected Result: Server saves the file with a random UUID — no directory traversal.

Insecure File Read Attempt

- Visit: http://localhost:5173/safe-script/?script=../../../etc/passwd
- Expected Result: 404 Error — Only whitelisted files can be read.

Cross-Site Scripting (XSS) Test

- Post: <script>alert('You got hacked!')</script> in the discussion board text box
- Expected Result: No popup alert. The text is displayed safely.

Rate Limiting Test

- Spam 4 file uploads rapidly within a minute.
- Expected Result: The server returns a 429 Too Many Requests error after 3 uploads.

Frontend Script Injection Test

- Post: <img src="x" onerror="alert('hacked')"/> in the discussion board text box
- Expected Result: No alert. The text is displayed safely.
