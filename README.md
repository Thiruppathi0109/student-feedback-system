# Student Feedback System (Flask + Docker + GitHub Actions CI/CD)

Students submit feedback for courses; admin views ratings & comments.

## Tech
Flask, Flask-SQLAlchemy, SQLite, Docker, GitHub Actions.

---

## 1. Run Locally (without Docker)

```bash
cd student-feedback-system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Open **http://localhost:5000**

Run tests:
```bash
pytest -v
```

---

## 2. Run with Docker

```bash
docker build -t student-feedback-system .
docker run -p 5000:5000 student-feedback-system
```
or with docker-compose:
```bash
docker-compose up --build
```
Open **http://localhost:5000**

---

## 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Student Feedback System"
git branch -M main
git remote add origin https://github.com/<your-username>/student-feedback-system.git
git push -u origin main
```

---

## 4. CI/CD Setup (GitHub Actions)

Workflow file already included: `.github/workflows/ci-cd.yml`

**What it does on every push/PR to `main`:**
1. **CI job** — installs deps, runs `pytest`, builds Docker image (checks nothing is broken).
2. **CD job** (only on push to `main`, after CI passes) — logs into Docker Hub, builds & pushes the image.

### Required GitHub Secrets (Repo → Settings → Secrets and variables → Actions):
| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (Docker Hub → Account Settings → Security → New Access Token) |

If you don't want Docker Hub push, delete the `deploy` job — CI (test + build) will still run.

### Deploying automatically (simplest option)
- Create a free account on **Render** or **Railway**.
- Connect your GitHub repo → it auto-builds using the `Dockerfile` and redeploys on every push to `main`. No extra YAML needed for this part.
- Add the same environment variables (`SECRET_KEY`, `DATABASE_URL`) there.

### Deploying to your own VM/server (optional, advanced)
Uncomment the SSH deploy step at the bottom of `ci-cd.yml` and add these secrets:
`SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`.

---

## 5. What to say in interview
- "Built a CI/CD pipeline with GitHub Actions: every push runs automated pytest tests and builds a Docker image before deployment — so broken code never reaches production."
- "Used Docker to containerize the Flask app for consistent environments across dev and prod."
- "Deployment is automatic on Render/Docker Hub push, triggered only when tests pass on `main`."

## Project Structure
```
student-feedback-system/
├── app.py                     # Flask app (routes, models)
├── requirements.txt
├── templates/                 # HTML pages
├── static/style.css
├── tests/test_app.py          # pytest tests (run in CI)
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
└── README.md
```
