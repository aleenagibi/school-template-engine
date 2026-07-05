## Setup

### Backend

1. Open backend folder

2. Create virtual environment:

python -m venv venv
`

3. Activate virtual environment:

Windows:

PS E:\Projects\school-template-engine\backend> venv\Scripts\activate


4. Install dependencies:

(venv) PS E:\Projects\school-template-engine\backend> pip install -r requirements.txt


5. Run backend:

(venv) PS E:\Projects\school-template-engine\backend> uvicorn app:app 


Backend runs on:


http://127.0.0.1:8000


---

### Frontend

1. Open frontend folder

2. Install dependencies:

PS E:\Projects\school-template-engine\frontend> npm install


3. Run frontend:

PS E:\Projects\school-template-engine\frontend> npm run dev


Frontend runs on:


http://localhost:5173


---

## Before Testing

Put sample school repositories inside:


school_repos/



## How to Test

1. Start backend
2. Start frontend
3. Open frontend
4. Select school
5. Browse sections
6. Preview section
7. Add sections
8. Reorder/remove sections
9. Assemble template

---

## Important

To load repositories into the system:

Use:

http
POST /scan


in FastAPI docs:


http://127.0.0.1:8000/docs


This scans all school repos and builds the reusable section library.

Run scan whenever new school repos are added.

---


