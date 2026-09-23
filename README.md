# Tech Inject Design Library

A reusable, documented, dependable **React + TypeScript component library** built with **Vite** and **Python FastAPI**. 

Derived from the visual language of the **Sales CRM reference**, Tech Inject provides a developer component catalogue, an admin dashboard with dynamic publishing without redeploy, server-protected premium components, an `npx` installer CLI, and AI agent prompts.

---

## 🔗 Live Application Services

- **React Public Catalogue & Admin Dashboard**: `http://localhost:5173`
- **FastAPI Backend Services**: `http://127.0.0.1:8000`
- **FastAPI OpenAPI Interactive Docs**: `http://127.0.0.1:8000/docs`

---

## 🛠 Project Architecture

```text
tech-inject-assignment/
├── backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py           # FastAPI app & CORS setup
│   │   ├── models.py         # SQLAlchemy User & Component models
│   │   ├── schemas.py        # Pydantic V2 schemas
│   │   ├── auth.py           # JWT Authentication & Password hashing
│   │   ├── seed.py           # Initial DB Seeding (10 CRM components & demo users)
│   │   └── routers/          # Auth, Components, Admin & Customers endpoints
│   └── tests/
│       └── test_api.py       # Pytest backend test suite
│
├── frontend/                 # React + Vite + TypeScript Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── library/      # 10 Reusable CRM-derived components (.tsx + .css)
│   │   │   └── common/       # Navbar, CodeBlock, CopyButton
│   │   ├── pages/            # Home, Catalogue, ComponentDetail, Login, AdminDashboard
│   │   ├── context/          # AuthContext provider
│   │   ├── services/         # API fetch client
│   │   └── styles/           # Sales CRM theme tokens (tokens.css)
│   └── package.json
│
├── packages/cli/             # Node.js CLI Component Installer (`npx tech-inject add <slug>`)
├── consumer-demo/            # Standalone React consumer application verification
├── answers.md                # Detailed answers to 7 technical interview questions
└── README.md
```

---

## 🚀 Quick Local Setup & Running

### 1. Backend (Python FastAPI)

```bash
# Install dependencies
python -m pip install -r backend/requirements.txt

# Run FastAPI Server (starts on http://127.0.0.1:8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

*The database (`tech_inject.db`) is automatically created and seeded with 10 components and demo users upon startup.*

### 2. Frontend (React + Vite + TypeScript)

```bash
cd frontend

# Install npm dependencies
npm install

# Run Frontend Dev Server (starts on http://localhost:5173)
npm run dev
```

---

## 🔑 Demo Test Accounts

| Role | Email | Password | Access Level |
|---|---|---|---|
| **Admin** | `admin@techinject.com` | `admin123` | Full Admin Dashboard & Publishing Control |
| **Free Customer** | `free@example.com` | `customer123` | Access to Free components (Premium locked) |
| **Premium Customer** | `premium@example.com` | `customer123` | Full Access to Free & Premium components |

---

## 📊 Component Inventory

| Component | CRM Reference | Category | Access | Features & Variants |
|---|---|---|---|---|
| **Button** | CRM Actions | Actions | Free | Primary, Secondary, Ghost, Danger, Loading, Disabled |
| **Badge** | Status / Segment tags | Data Display | Free | Success, Warning, Neutral, Danger, Info |
| **Avatar** | Account owner avatar | People | Free | Image, Initials Fallback, sm/md/lg sizes |
| **Tabs** | View switchers | Navigation | Free | Active, Inactive, Hover, Count badge |
| **FilterSelect** | Pipeline / Owner filters | Forms | Free | Label, Dropdown trigger, Checkmark indicator |
| **Sidebar** | Left CRM Navigation | Navigation | Free | Logo header, Active item, Nav icons, Badge |
| **Data Table** | Companies Table | Data Display | Premium | **Flagship!** Sortable columns, Selection, Custom renders |
| **MetricCard** | Summary KPI cards | Data Display | Premium | Label, Value, Trend (+/- %), Description |
| **ActionMenu** | Table Row Actions | Actions | Premium | Dropdown menu, Destructive option |
| **Probability** | Win Probability bar | Data Display | Premium | Progress bar (0-100%), Compact view, Color thresholds |

---

## ⚡ CLI Installer Usage

Test installing any component into a React project:

```bash
# In your target React + TypeScript project:
node path/to/packages/cli/index.js add button
# Or once published:
npx tech-inject add button
```

**Security checks enforced by CLI**:
- Rejects path traversal slugs (e.g. `../../`)
- Restricts file writing strictly inside current workspace `./src/components/`
- Fails safely on unauthorized premium component access (HTTP 403)

---

## 🧪 Verification & Test Results

```bash
# 1. Run Python Backend Pytest Suite
python -m pytest backend/tests/test_api.py -v
# Result: 5 PASSED (Health check, published listing, free component detail, premium lock security, auth login)

# 2. Run Frontend Production Build & Typecheck
cd frontend
npm run build
# Result: tsc -b && vite build PASSED with 0 errors!

# 3. Run Consumer Project Verification
cd consumer-demo
npm run build
# Result: Independent consumer app builds 100% cleanly!
```

---

## 🤖 AI Usage Evidence

- **AI Assistant**: Antigravity / Copilot
- **Representative Prompt**: "Build a reusable Data Table component with sortable columns and row selection based on Sales CRM design tokens."
- **AI Assumption Challenged & Corrected**: The AI initially suggested hardcoding the component catalogue in a static TypeScript file. I challenged this assumption to fulfill the requirement for **Admin Publishing Without Redeploy** (#48). I refactored the catalogue to dynamically query the FastAPI `/api/components` registry.
