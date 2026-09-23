# Tech Inject Design Library — Technical Interview Answers (answers.md)

### Question 1 — Reference Analysis
I identified reusable UI elements by systematically inspecting visual patterns, typography, color tokens, and repeated controls in the Sales CRM reference (https://sales-crm-kargulstudio.vercel.app/). I grouped repetitive interface patterns into 10 distinct, self-contained components with configurable variants (e.g. Button primary/secondary/ghost/danger) rather than creating single-purpose buttons. Component boundaries were strictly defined to extract UI representation while stripping out CRM-specific business logic. Visual fidelity was verified by capturing reference screenshots and comparing padding, borders, status colors, and hover states directly against the design token CSS specifications.

---

### Question 2 — Architecture and Clean Code
We selected React (Vite + TypeScript) for a responsive frontend and Python FastAPI (SQLAlchemy + SQLite) for a performant, typed backend API. The system strictly separates responsibilities into presentation, authentication, component registry, and installer endpoints. Following DRY and SOLID principles, theme tokens and authorization guards (`require_admin`, `require_premium`) are centralized to prevent logic duplication. To maintain simplicity (KISS/YAGNI), we intentionally avoided complex RBAC frameworks, payment gateways, and heavy monorepo tooling in favor of a clean, maintainable architecture.

---

### Question 3 — Publishing Consistency
A single published database record powers all component artifacts—live previews, props documentation, copyable source code, CLI installer payloads, and AI agent prompts—ensuring complete consistency across channels. When an administrator publishes or updates a component, the changes are stored in the SQLite database and served dynamically via `/api/components`, requiring zero frontend code modification or redeployment. If an update fails, database transactions rollback to preserve stability; unpublishing a component immediately revokes its listing and access endpoints from future requests.

---

### Question 4 — Security
Security risks around uploaded component source, dynamic previews, and installer scripts include path traversal attacks, secret leakage, and unauthorized access to premium code. We mitigated these risks by enforcing strict server-side authorization guards on all source/install endpoints, sanitizing filenames to block path traversal (e.g., rejecting `../` and absolute paths), and restricting installer writes strictly to the consumer workspace. We explicitly document that while sandboxed iFrames and path sanitization protect against common vector attacks, complete client-side execution isolation has structural boundaries.

---

### Question 5 — AI Ownership
During development, AI coding assistants were leveraged to draft initial component templates and API boilerplate. When AI suggested hardcoding published component lists into static frontend files, I challenged this assumption and refactored the catalogue to fetch components dynamically from the FastAPI backend to satisfy requirement #48. All AI-generated code was strictly reviewed, typed with TypeScript interfaces, tested with Pytest suites, and verified in an independent React consumer project (`consumer-demo`).

---

### Question 6 — Production Ownership
Production releases undergo strict automated checks: TypeScript type-checking (`tsc -b`), production Vite bundling, and Pytest API verification. If a breaking release occurs, I would inspect Uvicorn application logs and database error tracebacks, immediately roll back to the previous stable release, and verify database integrity. After resolving the issue, I would document the root cause, update automated integration test suites to prevent regression, and communicate the incident and fix timeline to the team.

---

### Question 7 — Premium Access
Premium access enforcement is strictly handled on the FastAPI server by validating user identity and premium status on every protected request (`/source`, `/install`, `/agent-prompt`). Direct API requests for locked premium components return HTTP 403 Forbidden and withhold source code bundles from public JS payloads. When an admin revokes a customer's premium access, subsequent API calls are instantly denied regardless of old session state. While revocation prevents future downloads and installer commands, it structurally cannot delete code already copied into local customer repositories.
