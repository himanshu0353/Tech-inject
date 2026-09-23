# Tech Inject Design Library — Complete Copilot Build Specification

> **Purpose:** This file is the single working specification for implementing the Tech Inject Design Library assignment.
>
> **Source of truth:** The assignment PDF supplied for this task. Recommendations in this file are clearly marked as implementation decisions/recommendations where the assignment leaves choices open.
>
> **Important:** Do not invent verification results. Only mark something as verified after actually testing it.

---

# 1. Assignment Goal

Build a reusable, documented, dependable **React/Next.js + TypeScript component library** with two separately runnable web applications:

1. **Public Component Catalogue**
   - Developers discover free and premium components.
   - Search and browse components.
   - View live previews and useful variants/states.
   - Read props and usage documentation.
   - Copy actual source code.
   - Copy a working `npx` installation command.
   - Copy a specific AI-agent integration prompt.
   - Premium content must be protected server-side.

2. **Admin Dashboard**
   - Admin uploads component source/supporting files/preview data.
   - Admin creates and edits drafts.
   - Admin validates and previews components.
   - Admin publishes/unpublishes components.
   - Admin marks components free/premium.
   - Admin manages customer premium access.
   - Published components must appear in the public catalogue without editing catalogue source or redeploying the frontend.

The result must be treated as a **production-ready application for the stated scope**, not a static prototype.

---

# 2. Critical Reference Rules

There are two references and they have different jobs.

## 2.1 Sales CRM = Visual Source of Truth

Use the **Sales CRM reference** to decide:

- Component visual language
- Typography
- Colors
- Borders
- Border radii
- Spacing
- Sizing
- Icons
- Visible interaction states
- Theme tokens
- Reusable component boundaries

Do NOT copy the CRM as an application.

Do NOT rebuild:
- CRM business logic
- Deal management
- Contact management
- Email sequences
- Forecasting logic
- Full CRM pages

Instead:

> Extract reusable UI components from the Sales CRM.

Reference URL:

`https://sales-crm-kargulstudio.vercel.app/`

---

## 2.2 Astryx = Public Catalogue UX Reference

Use Astryx to understand how a developer should:

- Discover components
- Search components
- Navigate documentation
- Inspect previews
- Understand variants
- Read props/usage
- Access source code
- Get installation instructions
- Get AI-agent instructions

Astryx is NOT the visual source for our components.

Do NOT copy:
- Astryx branding
- Astryx styling
- Astryx identity
- Meta branding/affiliation

Use:

> **Sales CRM theme + our own Tech Inject identity + Astryx-style developer documentation/discovery experience.**

Astryx reference:

`https://astryx.atmeta.com/`

---

# 3. Core Product Mental Model

The product relationship should be:

```text
                    SALES CRM
                       |
                       | Analyze UI
                       v
             Reusable UI Components
                       |
                       v
              TECH INJECT LIBRARY
                       |
                       v
                PUBLIC CATALOGUE
                       |
       +---------------+----------------+
       |               |                |
       v               v                v
    Preview          Source          Install
                                         |
                                         v
                                  AI Agent Prompt
```

In simple words:

- **Sales CRM tells us WHAT to build and how it should look.**
- **Astryx tells us HOW developers should discover and consume it.**
- **Tech Inject is our own product identity.**

---

# 4. Recommended Component Inventory

The assignment intentionally does not prescribe a component count. The following is the recommended implementation scope for the 8-hour timebox.

Build approximately **10 reusable components** well rather than many weak components.

## 4.1 Component List

### 1. Sidebar / Navigation

Extract from Sales CRM's left navigation.

Responsibilities:
- Navigation items
- Icons
- Active state
- Collapsed/expanded behavior if implemented
- Sections/groups if appropriate

Example:

```tsx
<Sidebar
  items={navigationItems}
  activeItem="companies"
/>
```

States:
- Default
- Active
- Hover
- Focus

---

### 2. Button

Extract the CRM actions such as:
- Export
- New Company
- Add Calculation

Do NOT create separate components for every action.

Use one reusable Button with variants.

Example:

```tsx
<Button variant="primary">
  New Company
</Button>

<Button variant="secondary">
  Export
</Button>

<Button variant="ghost">
  Add Calculation
</Button>
```

Suggested props:

```ts
type ButtonProps = {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  loading?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
};
```

States:
- Default
- Hover
- Focus
- Disabled
- Loading if applicable

---

### 3. Tabs

Extract the CRM tabs:

- Companies
- Deals
- Forecast

Example:

```tsx
<Tabs
  items={[
    { id: "companies", label: "Companies" },
    { id: "deals", label: "Deals" },
    { id: "forecast", label: "Forecast" }
  ]}
  value="companies"
  onChange={setTab}
/>
```

States:
- Active
- Inactive
- Hover
- Focus

---

### 4. Avatar

Extract account-owner avatars.

Example:

```tsx
<Avatar
  src="/avatars/alex.png"
  name="Alex Santos"
/>
```

Support:
- Image
- Fallback initials
- Accessible alt/name
- Sizes

---

### 5. Badge / Status

Extract CRM segment/stage/status presentation.

Example:

```tsx
<Badge variant="success">
  Pilot
</Badge>

<Badge variant="neutral">
  SMB
</Badge>
```

Suggested variants:

```ts
"success" | "warning" | "neutral" | "danger" | "info"
```

Do not hardcode CRM-specific meanings inside the component.

---

### 6. Filter / Select

Extract CRM filtering controls such as:

- Pipeline Value
- Owner
- Stage
- Last Activity

Example:

```tsx
<FilterSelect
  label="Owner"
  value={owner}
  options={owners}
  onChange={setOwner}
/>
```

Include:
- Label
- Trigger
- Options
- Selected state
- Clear/reset if appropriate

---

### 7. Data Table — FLAGSHIP COMPONENT

This should be the strongest component because the CRM has a substantial reusable data table.

Example CRM-style columns:

```text
Company
Segment / Stage
Account Owner
Open Deals
Pipeline Value
Win Probability
Activity Trend
Last Interaction
Action
```

Build a generic table, NOT a `CompanyTable`.

Example:

```tsx
<DataTable
  columns={columns}
  data={companies}
  selectable
  sortable
  pagination
/>
```

Possible props:

```ts
type DataTableProps<T> = {
  columns: ColumnDef<T>[];
  data: T[];
  selectable?: boolean;
  sortable?: boolean;
  pagination?: boolean;
  loading?: boolean;
  emptyMessage?: string;
};
```

The component must be reusable with other datasets.

Example:

```tsx
<DataTable
  columns={userColumns}
  data={users}
/>
```

Do not hardcode CRM business logic into DataTable.

---

### 8. Metric / Stat Card

Extract CRM summary metrics/KPI presentation.

Example:

```tsx
<MetricCard
  label="Pipeline Value"
  value="$1.2M"
  trend="+12%"
/>
```

Suggested data:
- Label
- Value
- Optional trend
- Optional description
- Optional icon

---

### 9. Action Menu / Dropdown

Extract the row-level action behavior.

Example:

```tsx
<ActionMenu
  items={[
    { id: "edit", label: "Edit" },
    { id: "duplicate", label: "Duplicate" },
    { id: "delete", label: "Delete", destructive: true }
  ]}
/>
```

States:
- Closed
- Open
- Hover
- Focus
- Disabled
- Destructive action

---

### 10. Probability / Progress Indicator

Extract the CRM Win Probability representation.

Example:

```tsx
<Probability value={82} />
```

Support:
- 0–100
- Accessible label
- Visual progress
- Optional compact mode

Do not hardcode "win probability" into the component.

---

# 5. Suggested Free/Premium Split

The assignment requires examples of both free and premium components, but it does not prescribe which components must be premium.

Recommended split:

## Free

- Button
- Badge
- Avatar
- Tabs
- Filter / Select
- Sidebar

## Premium

- Data Table
- Metric Card
- Action Menu
- Probability / Progress

This is an implementation decision, not a requirement from the reference.

The exact split can change if implementation constraints require it.

---

# 6. Component Design Rules

## 6.1 Reuse Through Props and Variants

Do NOT create:

```text
ExportButton
NewCompanyButton
AddCalculationButton
```

Create:

```text
Button
```

with variants.

Do NOT create:

```text
CompanyBadge
DealBadge
CustomerBadge
```

Create:

```text
Badge
```

with variants.

The goal is a reusable design library.

---

# 7. Sales CRM Theme Extraction

Before implementation:

1. Open the Sales CRM reference.
2. Capture reference screenshots.
3. Inspect visual details.
4. Create shared design tokens.
5. Build components using those tokens.

Extract tokens for:

```text
Typography
Colors
Backgrounds
Borders
Border radius
Spacing
Sizing
Shadows
Icon sizing
Control heights
Table row heights
```

Example token structure:

```ts
export const theme = {
  colors: {
    background: "...",
    foreground: "...",
    muted: "...",
    border: "...",
    primary: "...",
    success: "...",
    warning: "...",
    danger: "..."
  },

  radius: {
    sm: "...",
    md: "...",
    lg: "..."
  },

  spacing: {
    xs: "...",
    sm: "...",
    md: "...",
    lg: "...",
    xl: "..."
  }
};
```

IMPORTANT:

Do not invent generic "CRM-inspired" styling.

The assignment expects close recreation of the reference theme.

---

# 8. Reference/Recreation Verification

For each important component:

1. Capture the reference screenshot.
2. Capture the recreated component at a comparable size.
3. Compare:
   - Typography
   - Spacing
   - Colors
   - Borders
   - Radius
   - Icons
   - Dimensions
   - Interaction states
4. Document remaining differences.

README should include side-by-side reference/recreation screenshots.

---

# 9. Public Catalogue UX

The public catalogue should be a **developer documentation product**.

It must NOT look like:
- A sales dashboard
- A static marketing landing page
- A copy of Astryx

Recommended routes:

```text
/
├── /get-started
├── /components
├── /components/[slug]
└── /login
```

---

# 10. Public Home / Get Started Page

Purpose:

Quickly explain:

> Tech Inject is a reusable React + TypeScript component library based on a consistent design system.

Include:

- Short introduction
- What the library provides
- How to install
- Supported consumer setup
- Free/premium explanation
- Link to components
- Basic usage example

Example:

```text
Tech Inject

Reusable React components for building
consistent interfaces faster.

[Browse Components]
[Get Started]

Supported:
React + TypeScript
```

Keep this concise.

---

# 11. Component Catalogue Page

Recommended structure:

```text
------------------------------------------------
Tech Inject

Search components...
------------------------------------------------

Categories

All
Actions
Data Display
Navigation
Forms
Feedback
People

------------------------------------------------

Components

Button
Reusable action control

Badge
Status and category indicator

Avatar
User representation

Data Table
Reusable structured data table

...
------------------------------------------------
```

Must support:

- Search
- Component categories/navigation
- Published components
- Free/premium status
- Responsive layout

---

# 12. Component Detail Page

This is one of the most important pages.

Example:

```text
Components / Data Table

# Data Table

A reusable table for displaying structured data
with sorting, selection and pagination.

[ Free / Premium ]

------------------------------------------------

Preview | Code

[Working component preview]

------------------------------------------------

Variants

Default
Selectable
Sortable
Compact

------------------------------------------------

Props

columns       Column[]
data          T[]
selectable    boolean
sortable      boolean
pagination    boolean

------------------------------------------------

Usage

<DataTable
  columns={columns}
  data={data}
/>

[Copy Code]

------------------------------------------------

Installation

npx tech-inject add data-table

[Copy]

------------------------------------------------

Source Code

button.tsx
theme.css
types.ts

[Copy Code]

------------------------------------------------

Dependencies

React
TypeScript
...
------------------------------------------------

AI Agent Prompt

[Copy Prompt]
```

---

# 13. Every Component Detail Page Must Provide

For authorized users:

## 13.1 Working Preview

Not a static screenshot.

The component must actually work.

Example:

- Button can be clicked
- Tabs change
- Filter opens
- Table can interact
- Action menu opens

---

## 13.2 Useful Variants/States

Examples:

Button:

```text
Primary
Secondary
Ghost
Danger
Disabled
Loading
```

Tabs:

```text
Active
Inactive
Hover
Focus
```

Data Table:

```text
Default
Sortable
Selectable
Empty
Loading
```

Only include states applicable to the component.

---

## 13.3 Props Documentation

Use actual implementation types.

Example:

```text
variant
type: "primary" | "secondary" | "ghost"

default: "primary"

description:
Controls the visual style of the button.
```

Do not create documentation that disagrees with the source code.

---

# 14. Copy Source Code

The catalogue must provide actual source.

Do not return:

```tsx
// example only
```

Return actual component source.

Source may include:

```text
component.tsx
types.ts
theme.css
utils.ts
```

where required.

The copyable integration must include:

- Actual source
- Example usage
- Required imports
- Required theme/style files
- Dependency instructions

---

# 15. Installation Command

Every component should have a working command such as:

```bash
npx tech-inject add button
```

or:

```bash
npx tech-inject add data-table
```

The exact command format is an implementation decision.

IMPORTANT:

The displayed command must actually work on the reviewer's machine.

It must NOT depend on:

- Candidate's laptop
- localhost
- Local-only files
- Cloning the entire catalogue

Publishing to npm is NOT required.

A publicly downloadable package/CLI or compatible installer is acceptable.

---

# 16. Consumer Project Requirement

Support one documented setup.

Recommended:

```text
React + TypeScript + Vite
```

Document prerequisites:

```text
Node.js version
npm
React
TypeScript
```

Example clean consumer:

```text
consumer-demo/
├── src/
├── package.json
├── tsconfig.json
└── ...
```

Install:

```bash
npx tech-inject add button
```

Then:

```tsx
import { Button } from "./components/button";
```

or whatever the installer generates.

The consumer must:

- Build
- Render
- Work independently
- Not import from the catalogue app
- Not require catalogue-only aliases
- Not require missing theme files

---

# 17. AI Agent Prompt

Every component needs a specific copyable AI prompt.

Example:

```text
Add the Tech Inject Button component to this React +
TypeScript project.

Use the supplied Button source and preserve the Tech Inject
theme tokens and required styles.

Install or add all required dependencies.

Do not replace the component with an unrelated UI library.

Use the component in the existing project using this example:

<Button variant="primary">
  Create Project
</Button>

After integration:
1. Run the project.
2. Verify the component renders.
3. Verify styles are loaded.
4. Verify TypeScript passes.
5. Verify the button interaction works.

If the existing project structure differs, adapt imports
without changing the component behavior or theme.
```

The prompt must:

- Identify the component
- Explain how to integrate it
- Preserve theme
- Preserve dependencies
- Explain required files
- Explain verification

Do not include credentials.

Do not expose secrets.

---

# 18. Copy Feedback

Every copy action must provide visible feedback.

Example:

```text
[Copy Code]

-> Copied!
```

On failure:

```text
Unable to copy.
Please select and copy manually.
```

Use accessible status feedback where practical.

---

# 19. Responsive / Narrow Screen Requirement

The public catalogue must work on narrow screens.

Check:

- Sidebar/navigation
- Search
- Component cards/list
- Preview
- Code blocks
- Tables
- Copy buttons
- Tabs

Avoid horizontal overflow where possible.

Code blocks may scroll horizontally when necessary.

---

# 20. Admin Dashboard

The admin app can be simple.

It does NOT need to look as polished as the public catalogue.

Admin must be server-protected.

Recommended routes:

```text
/admin/login
/admin
/admin/components
/admin/components/new
/admin/components/[id]
/admin/customers
```

---

# 21. Admin Authentication

One administrator configured through environment variables is sufficient.

Example:

```env
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD_HASH=...
```

Do not expose admin secrets in frontend code.

Every admin write API must verify authentication server-side.

Do not trust:

```text
isAdmin=true
```

from frontend requests.

---

# 22. Admin Component Workflow

The admin must support:

```text
Create Draft
     |
     v
Upload Source
     |
     v
Upload Supporting Files
     |
     v
Add Preview/Example Data
     |
     v
Set Metadata
     |
     v
Validate
     |
     v
Preview
     |
     v
Publish
     |
     v
Public Catalogue
```

Admin must also support:

```text
Published
    |
    v
Unpublish
```

---

# 23. Component Metadata

Each component should have:

```ts
type ComponentRecord = {
  id: string;
  name: string;
  slug: string;
  description: string;
  category: string;
  version: string;
  access: "free" | "premium";

  props: PropDefinition[];
  dependencies: Dependency[];

  sourceFiles: SourceFile[];
  previewData?: unknown;

  status: "draft" | "published";

  createdAt: string;
  updatedAt: string;
};
```

Use runtime validation as well as TypeScript.

---

# 24. Draft Privacy

Draft components must never be publicly accessible.

Test:

```text
/admin draft -> accessible
/public draft -> denied/not found
```

Direct API requests must also fail.

Do not rely only on hiding the component from the UI.

---

# 25. Publishing

When admin publishes:

```text
DB/storage
   |
   v
Published component
   |
   +--> Public listing
   +--> Detail page
   +--> Preview
   +--> Source
   +--> Install
   +--> AI prompt
```

No manual code changes.

No per-component import into the frontend.

No frontend redeployment.

A normal page refresh is acceptable.

---

# 26. Unpublishing

When admin unpublishes:

- Remove from public listing
- Direct detail route should no longer expose it
- New source requests denied
- New installation requests denied
- New agent-prompt requests denied

Existing copied/installed files do not need to be removed.

Document this limitation.

---

# 27. Premium Access Model

There are three user states.

## State A — Signed Out

### Free component

Full access:

```text
Preview
Source
Install
Agent Prompt
```

### Premium component

Only:

```text
Public description
Static thumbnail/preview
Sign in / premium access message
```

No premium source.

No premium install.

No premium prompt.

---

## State B — Signed In Without Premium

### Free component

Full access.

### Premium component

Locked.

Display something like:

```text
Premium component

Premium access is required to use this component.
Contact the administrator to request access.
```

Do NOT build fake payment/checkout.

---

## State C — Signed In With Premium

Full access:

```text
Preview
Source
Install
Agent Prompt
```

---

# 28. Customer Authentication

Required:

- Sign in
- Sign out
- Visible account state
- Free/premium status

Not required:

- Public signup
- Password recovery
- Payments
- Subscriptions
- Invoices

Seed:

```text
Free test customer
Premium test customer
```

Credentials must be shared privately, never committed to Git.

---

# 29. Premium Access Backend Enforcement

This is CRITICAL.

Do not only hide buttons.

Every protected request must check:

```text
Is user authenticated?
        |
        v
Does user have premium access?
        |
        v
Is component published?
        |
        v
Allow / deny
```

Protect:

- Preview
- Source
- Download
- Installer
- Agent prompt
- Supporting files
- Dependencies containing premium code

Also protect direct URLs.

---

# 30. Revocation

Example:

```text
Customer has premium
        |
        v
Can access premium source
        |
Admin revokes
        |
        v
Customer still signed in
        |
        v
New request
        |
        v
DENIED
```

Do not rely on old frontend session state.

Check current access on every protected request.

Important limitation:

> Revocation cannot remove code the customer already copied or installed.

Document this.

---

# 31. Publication vs Premium Access

These are separate concepts.

```text
Publication:
draft -> published/unpublished

Access:
free/premium
```

A premium customer must NOT be able to retrieve:

```text
draft
unpublished component
```

Premium status never means admin status.

A customer cannot grant themselves premium.

---

# 32. No Premium Source Leakage

Premium source must NOT appear in:

- Public JS bundles
- Public Git repository
- Unrestricted storage
- Public cache responses
- Static frontend source
- Public API responses

For locked preview:

> Use static thumbnail/preview representation instead of exposing executable premium source.

Test with a **new premium component uploaded through admin that does not exist in the repository**.

This is an important proof of the access-control design.

---

# 33. Installer Security

Installer must:

- Write only inside selected consumer directory.
- Reject unsafe paths.
- Reject path traversal.
- Avoid silently overwriting existing files.
- Not run component-provided shell commands.
- Not execute uploaded code.
- Validate component metadata/source.
- Fail clearly on unauthorized premium access.

Unsafe examples to reject:

```text
../../package.json
../../../etc/passwd
/absolute/path
```

Never allow a component source package to tell the installer:

```bash
rm -rf ...
npm install random-command && ...
```

The installer should control what operations are allowed.

---

# 34. Uploaded Component Security

Admin uploads must be validated.

Validate:

- Required fields
- Slug
- Version
- File type
- File size
- File count
- File path
- Dependency format
- JSON structure
- Metadata structure

Do NOT execute uploaded component code in:

- Backend
- Admin server context
- Authenticated server context

---

# 35. Preview Isolation

Uploaded component previews must not have access to:

- Backend credentials
- Admin secrets
- Environment variables
- Customer tokens
- Internal APIs

A restricted component format is acceptable.

IMPORTANT:

> An ordinary unsandboxed iframe is NOT secure isolation.

If using iframe preview, document its limitations and use the safest practical restrictions for the implementation.

---

# 36. Recommended Architecture

A practical architecture:

```text
tech-inject/
│
├── apps/
│   ├── catalogue/
│   │   ├── app/
│   │   ├── components/
│   │   ├── lib/
│   │   └── ...
│   │
│   └── admin/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── ...
│
├── packages/
│   ├── ui/
│   ├── types/
│   ├── validation/
│   └── installer/
│
├── backend/
│   ├── api/
│   ├── auth/
│   ├── components/
│   ├── customers/
│   ├── storage/
│   └── ...
│
├── consumer-demo/
│
├── tests/
│
├── README.md
├── answers.md
└── package.json
```

A monorepo/TurboRepo is optional.

Do not introduce TurboRepo just to demonstrate architecture.

Use it only if it genuinely helps.

---

# 37. Backend Responsibilities

Backend should own:

- Authentication
- Authorization
- Component registry
- Publication state
- Premium access
- Source retrieval
- Installer package retrieval
- Agent prompt retrieval
- Admin writes
- Validation
- Storage access
- Error handling

Frontend should not be the authority for security.

---

# 38. Data Model

A practical database model:

## components

```text
id
name
slug
description
category
version
access_level
status
props_json
dependencies_json
preview_data_json
source_bundle_location
created_at
updated_at
published_at
```

## users

```text
id
email
password_hash
role
premium
created_at
updated_at
```

Suggested roles:

```text
admin
customer
```

No general-purpose RBAC system is required.

## component_versions

Optional but recommended if implementation can support it:

```text
id
component_id
version
metadata
source_location
dependencies
preview_data
created_at
```

If time is limited, a single current published version can be implemented cleanly.

---

# 39. Consistent Published Version

This is critical.

Preview, source, installer and AI prompt must all come from the SAME published component version.

Avoid:

```text
Preview -> hardcoded source A
Source -> manually copied source B
CLI -> manually copied source C
AI prompt -> manually written source D
```

Instead:

```text
Published Component Version
        |
        +--> Preview
        +--> Source
        +--> Installer
        +--> AI Prompt
        +--> Dependencies
```

One source of truth.

---

# 40. Suggested API Design

Exact implementation may differ.

## Public

```http
GET /api/components
GET /api/components/:slug
GET /api/components/:slug/preview
GET /api/components/:slug/source
GET /api/components/:slug/install
GET /api/components/:slug/agent-prompt
```

Premium endpoints must verify access.

---

## Auth

```http
POST /api/auth/login
POST /api/auth/logout
GET /api/auth/me
```

---

## Admin

```http
GET /api/admin/components
POST /api/admin/components
PATCH /api/admin/components/:id
POST /api/admin/components/:id/validate
POST /api/admin/components/:id/publish
POST /api/admin/components/:id/unpublish

GET /api/admin/customers
POST /api/admin/customers/:id/grant-premium
POST /api/admin/customers/:id/revoke-premium
```

These are suggested endpoints, not mandatory names.

---

# 41. Authorization Helper

Create one reusable authorization function.

Conceptually:

```ts
requireAdmin(request)
```

and:

```ts
requirePremium(request, component)
```

Do not duplicate access logic across 10 endpoints.

But don't over-engineer the authorization layer.

---

# 42. Runtime Validation

TypeScript does not replace runtime validation.

Use a validation library such as Zod if appropriate.

Validate:

```text
Component metadata
Admin request bodies
Upload manifests
Props definitions
Dependencies
Installer package metadata
Authentication input
```

---

# 43. TypeScript Rules

Use:

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

Avoid:

```ts
any
```

unless genuinely justified.

Avoid:

```ts
as any
```

Avoid:

```ts
// @ts-ignore
```

Do not disable strict checking globally.

---

# 44. Clean Code Rules

Use:

- Meaningful names
- Focused functions
- Focused components
- Consistent structure
- No dead code
- Shared types
- Shared validation
- Shared design tokens
- Clear API boundaries

Separate:

```text
Presentation
Publishing
Storage
Authentication
Authorization
Installation
Validation
```

Do not mix everything into one component/page.

---

# 45. SOLID

Apply only where useful.

Example:

Instead of one huge service:

```text
ComponentService
  -> upload
  -> validate
  -> publish
  -> install
  -> authenticate
  -> customer management
```

Prefer focused responsibilities where complexity warrants it.

But do NOT create:

```text
IComponentFactory
IComponentFactoryProvider
ComponentFactoryManager
ComponentRepositoryAbstraction
```

just to demonstrate SOLID.

---

# 46. DRY

Share:

- Theme tokens
- Types
- Validation
- Authorization
- Component registry logic
- Installer safety rules

Do not maintain separate copies of:

```text
Button styles
Component metadata schema
Premium authorization logic
```

Frontend validation can improve UX.

Backend validation remains mandatory.

---

# 47. KISS / YAGNI

Do NOT build:

- Payments
- Subscription billing
- Public signup
- Password recovery
- Multi-framework support
- Marketplace
- Public uploads
- npm publishing
- General-purpose code execution
- Enterprise RBAC
- Complex analytics

Unless explicitly required.

---

# 48. Admin Publishing Without Redeploy

This is a major acceptance criterion.

Test:

```text
1. Open public catalogue.
2. Confirm component does not exist.
3. Admin creates new component.
4. Upload files.
5. Validate.
6. Preview.
7. Publish.
8. Refresh public catalogue.
9. New component appears.
10. Open detail page.
11. Preview works.
12. Source works.
13. Install command works.
14. Agent prompt works.
```

No frontend code changes.

No redeployment.

---

# 49. End-to-End Demo Flow

The assignment specifically expects this.

## Flow A — Free/reference-derived component

```text
Admin
  |
  v
Upload additional reference-derived component
  |
  v
Preview
  |
  v
Publish
  |
  v
Public catalogue
  |
  +--> Preview
  +--> Source
  +--> Installer
  +--> Agent Prompt
```

The component should not already exist in the catalogue before this test.

---

## Flow B — Premium

```text
Publish Premium Component
        |
        v
Free Customer
        |
        v
LOCKED
        |
        v
Admin Grants Premium
        |
        v
Customer Refreshes
        |
        +--> Preview works
        +--> Source works
        +--> Installer works
        +--> Agent Prompt works
        |
        v
Admin Revokes Premium
        |
        v
Customer remains signed in
        |
        v
New protected requests
        |
        v
DENIED
```

Free components remain usable.

---

# 50. Automated Tests

Automate checks for:

## 1. Admin security

- Unauthenticated admin write denied
- Customer admin write denied
- Premium customer cannot perform admin action

## 2. Draft privacy

- Draft not visible publicly
- Direct draft API denied

## 3. Publication

- Valid component publishes
- Invalid upload rejected

## 4. Metadata/source consistency

- Published metadata matches source
- Correct version returned
- Installer uses same published version

## 5. Installer security

- Path traversal rejected
- Absolute path rejected
- Existing file not silently overwritten
- Unauthorized premium install rejected

## 6. Premium

- Signed-out premium source denied
- Free customer premium source denied
- Premium customer premium source allowed
- Revoked customer denied
- Customer cannot self-grant premium

## 7. Free components

- Signed-out access works
- Free customer access works
- Premium customer access works

---

# 51. Consumer Project Verification

Create a clean consumer project.

Example:

```bash
npm create vite@latest tech-inject-consumer -- --template react-ts
cd tech-inject-consumer
npm install
```

Then run your installer.

Example:

```bash
npx tech-inject add button
```

Verify:

```text
Build succeeds
Component renders
Styles render
No catalogue imports
No missing theme files
No localhost dependency
```

Repeat with at least one more meaningful component if time permits.

---

# 52. AI Prompt Verification

Use the copied AI prompt in a clean consumer project.

Record:

```text
AI tool used:
Prompt:
Initial result:
Problem found:
Correction:
Final result:
Verification:
```

Do not claim success unless actually tested.

---

# 53. Deployment

Deploy:

- Public catalogue
- Admin dashboard
- Backend/API
- Database
- Storage

Everything required must work remotely.

Do not depend on:

```text
localhost
Laptop files
Local database
Local storage
```

Use HTTPS.

---

# 54. Environment Variables

Use `.env.example`.

Example:

```env
DATABASE_URL=
AUTH_SECRET=
ADMIN_EMAIL=
ADMIN_PASSWORD_HASH=

STORAGE_ENDPOINT=
STORAGE_BUCKET=
STORAGE_ACCESS_KEY=
STORAGE_SECRET_KEY=

PUBLIC_API_URL=
```

Use only variables actually required by the implementation.

Never commit real values.

Never put secrets in frontend bundles.

---

# 55. Logging and Errors

Useful errors:

```text
Component not found
Component unpublished
Premium access required
Authentication required
Invalid component package
Invalid file type
File too large
Unsafe file path
File already exists
Unauthorized admin action
```

Do not expose secrets in errors/logs.

---

# 56. UI Usability

Verify:

- Keyboard navigation
- Visible focus
- Labels
- Loading state
- Empty state
- Error state
- Disabled state
- Copy feedback
- Responsive layout

Do not only test the happy path.

---

# 57. README Requirements

README must contain:

## Project

Short explanation.

## Links

```text
Public Catalogue:
Admin Dashboard:
Repository:
```

## Architecture

Explain:

```text
Frontend
Backend
Database
Storage
Installer
```

## Local Setup

Actual commands.

Example:

```bash
npm install
npm run dev
```

Use actual project commands.

## Build

```bash
npm run build
```

## Checks

```bash
npm run lint
npm run typecheck
npm test
```

Only report commands/results that actually exist and were run.

## Environment Variables

List names only.

Provide `.env.example`.

Never include real secrets.

## Deployment

Explain where and how each service is deployed.

## Screenshots

Include:

- Sales CRM reference
- Recreation
- Catalogue
- Component detail
- Admin
- Premium locked
- Premium unlocked
- Consumer project

## Tests

Document actual results.

## Time Spent

Record actual approximate time.

## Known Gaps

Be honest.

Incomplete core functionality must be reported as incomplete.

---

# 58. README Component Inventory

Use a table similar to:

| Component | CRM Reference | Implemented | Priority | Reason |
|---|---|---:|---|---|
| Button | CRM actions | Yes | High | Common reusable action |
| Badge | Status/segment | Yes | High | Reusable status UI |
| Avatar | Account owner | Yes | High | Common identity UI |
| Tabs | CRM tabs | Yes | High | Navigation |
| Filter | CRM filters | Yes | High | Reusable data filtering |
| Sidebar | CRM navigation | Yes | High | Application navigation |
| Data Table | Companies table | Yes | Very High | Main reusable data component |
| Metric Card | Summary metrics | Yes | High | KPI presentation |
| Action Menu | Action column | Yes | Medium | Row actions |
| Probability | Win probability | Yes | Medium | Data visualization |

Modify this table to reflect the actual final implementation.

---

# 59. Important Omissions to Explain

Possible omissions:

```text
Full CRM pages
Deal management
Contact management
Email sequences
Forecasting business logic
```

Reason:

> These are product-specific business features rather than reusable UI components required for the component library.

Only claim an omission if it is actually omitted.

---

# 60. answers.md

Create:

```text
answers.md
```

Answer all seven questions in **2–4 sentences each**, based on the real implementation.

---

## Question 1 — Reference Analysis

Explain:

- How reusable components were identified.
- How variants were decided.
- How theme tokens were extracted.
- One component boundary decision.
- How recreation was verified against the reference.

Example structure:

```text
I identified reusable elements by comparing repeated interaction
patterns and visual structures in the Sales CRM. I grouped...
```

Do not invent details.

---

## Question 2 — Architecture and Clean Code

Explain:

- Why this stack was chosen.
- Separation of responsibilities.
- One SOLID/DRY decision.
- One abstraction/feature intentionally avoided.

Mention actual implementation.

---

## Question 3 — Publishing Consistency

Explain:

- How one published version powers:
  - Preview
  - Source
  - Installer
  - Agent prompt
- What happens if update fails.
- What happens after unpublish.

---

## Question 4 — Security

Explain risks around:

- Uploaded code
- Preview
- Admin APIs
- Installation

Then explain:

- Implemented protections
- Tests
- Remaining limitations

Do not claim ordinary iframe isolation is secure.

---

## Question 5 — AI Ownership

Explain:

- AI tools used.
- One AI suggestion/assumption challenged.
- Why you changed/accepted it.
- Evidence.
- Consumer-project verification.

---

## Question 6 — Production Ownership

Explain:

- What deployment checks were performed.
- What you would inspect after a broken release.
- Recovery strategy.
- How stored data would be protected.
- What would be communicated to the team.

---

## Question 7 — Premium Access

Explain:

- Account access
- Publication state
- Admin permissions
- Premium checks
- Direct API protection
- Installer protection
- Agent prompt protection
- Revocation
- What revocation cannot undo

---

# 61. Required AI Documentation

The assignment requires extensive AI use.

Document:

```text
AI Tool:
Example Prompt:
What AI Generated:
What I Reviewed:
What I Changed:
How I Verified It:
```

At least one representative prompt should be in README.

Also include:

> One AI suggestion/assumption that was verified or corrected, with code/test evidence.

Do not provide the full chat history.

---

# 62. Recommended AI Development Workflow

Use AI like a senior engineering assistant, not as a blind code generator.

For every major feature:

```text
1. Understand requirement
2. Design
3. Ask AI for implementation
4. Review generated code
5. Run type check
6. Run lint
7. Run tests
8. Manually test
9. Fix issues
10. Document important decision
```

Never accept:

```text
"It looks correct"
```

as verification.

---

# 63. Copilot Working Rules

When implementing this project, Copilot should follow these rules:

### Rule 1

Do not implement features outside the assignment unless explicitly requested.

### Rule 2

Prefer the simplest maintainable implementation.

### Rule 3

Do not create fake functionality.

If an install command is shown, it must actually work.

If a button says "Publish", it must actually publish.

If premium content is locked, backend enforcement must exist.

### Rule 4

Do not hardcode published components into the public frontend.

Newly published components must be discovered dynamically.

### Rule 5

Do not expose premium source in public bundles.

### Rule 6

Do not put secrets in code.

### Rule 7

Use strict TypeScript.

### Rule 8

Use runtime validation at trust boundaries.

### Rule 9

Do not suppress TypeScript/lint/test errors just to get a green build.

### Rule 10

Before implementing a major feature, inspect the existing architecture and reuse existing utilities.

### Rule 11

Do not duplicate component source between preview/source/installer.

### Rule 12

Every new component must fit the same theme/token system.

### Rule 13

Every public component page must support:

```text
Preview
Variants
Props
Source
Install
Agent Prompt
```

where access allows.

### Rule 14

Premium access must be checked server-side.

### Rule 15

Do not assume UI hiding equals authorization.

---

# 64. Recommended Build Order

Use vertical slices.

## Phase 1 — Analyze Reference

- Open Sales CRM
- Capture screenshots
- Identify components
- Extract theme tokens
- Decide variants

Output:

```text
Component inventory
Theme tokens
Reference screenshots
```

---

## Phase 2 — Project Setup

Create:

```text
Next.js/React
TypeScript strict
Styling system
Backend/API
Database
Storage
```

Run:

```text
Install
Build
Lint
Typecheck
```

---

## Phase 3 — Build Design System

Implement:

```text
Tokens
Button
Badge
Avatar
Tabs
Filter
Sidebar
```

Then:

```text
Data Table
Metric Card
Action Menu
Probability
```

---

## Phase 4 — Database + Component Registry

Implement:

```text
Component
User
Publication
Access
Source storage
```

---

## Phase 5 — Public Catalogue

Build:

```text
Home
Get Started
Component search
Categories
Component detail
Preview
Props
Source
Install
AI prompt
```

---

## Phase 6 — Admin

Build:

```text
Admin auth
Component list
Create draft
Upload
Edit metadata
Validate
Preview
Publish
Unpublish
Customer list
Grant premium
Revoke premium
```

---

## Phase 7 — Premium

Implement:

```text
Free customer
Premium customer
Signed out
Direct API protection
Source protection
Installer protection
Agent prompt protection
Revocation
```

---

## Phase 8 — Installer

Implement:

```text
npx tech-inject add <slug>
```

Security:

```text
Safe paths
No overwrite
No shell execution
Authentication
Premium check
Published check
```

---

## Phase 9 — Verification

Run:

```text
Build
Lint
Typecheck
Tests
Consumer build
CLI install
AI prompt
Admin publish
Admin unpublish
Premium grant
Premium revoke
```

---

## Phase 10 — Deployment

Deploy:

```text
Catalogue
Admin
Backend
Database
Storage
```

Verify remotely.

---

## Phase 11 — Documentation

Complete:

```text
README.md
answers.md
Screenshots
Test results
AI evidence
Recovery plan
Known gaps
```

---

# 65. Acceptance Checklist

Before submission, all applicable boxes should be true.

## Component Library

- [ ] Sales CRM analyzed
- [ ] Reference screenshots captured
- [ ] Theme tokens extracted
- [ ] Reusable components selected
- [ ] Components visually match reference
- [ ] Props typed
- [ ] Variants implemented
- [ ] Hover/focus/selected/disabled states where applicable
- [ ] Realistic data used
- [ ] No CRM business logic rebuilt

## Public Catalogue

- [ ] Intro/get-started
- [ ] Search
- [ ] Component navigation
- [ ] Component detail pages
- [ ] Working previews
- [ ] Variants/states
- [ ] Props docs
- [ ] Actual source
- [ ] Example usage
- [ ] Theme/style dependencies
- [ ] Install command
- [ ] AI prompt
- [ ] Copy success feedback
- [ ] Copy error handling
- [ ] Responsive layout

## Admin

- [ ] Admin auth
- [ ] Server-side admin verification
- [ ] Draft creation
- [ ] Source upload
- [ ] Supporting file upload
- [ ] Preview data
- [ ] Metadata editing
- [ ] Validation
- [ ] Preview
- [ ] Publish
- [ ] Unpublish
- [ ] Customer list
- [ ] Grant premium
- [ ] Revoke premium
- [ ] Persistent storage
- [ ] Newly published components appear without redeploy

## Premium

- [ ] Signed-out free access
- [ ] Signed-out premium locked
- [ ] Free customer premium locked
- [ ] Premium customer premium access
- [ ] Backend enforcement
- [ ] Direct URL protection
- [ ] Source protection
- [ ] Installer protection
- [ ] Agent prompt protection
- [ ] Supporting files protected
- [ ] Revocation works for future requests
- [ ] No premium source leakage
- [ ] Customer cannot self-grant
- [ ] Premium customer cannot access drafts

## Installer

- [ ] Works using deployed source
- [ ] Clean consumer project tested
- [ ] Safe paths
- [ ] Path traversal rejected
- [ ] Existing files not silently overwritten
- [ ] No component shell commands
- [ ] Premium auth enforced
- [ ] Published status enforced

## Engineering

- [ ] Persistent database
- [ ] Persistent storage
- [ ] HTTPS
- [ ] Secrets protected
- [ ] Runtime validation
- [ ] Safe queries/ORM
- [ ] Useful errors/logging
- [ ] TypeScript strict
- [ ] Lint passes
- [ ] Typecheck passes
- [ ] Tests pass
- [ ] No suppressed failures

## Deployment

- [ ] Catalogue deployed
- [ ] Admin deployed
- [ ] Backend deployed
- [ ] Database deployed
- [ ] Storage deployed
- [ ] Remote publish tested
- [ ] Remote unpublish tested
- [ ] Data survives restart/redeploy

## Documentation

- [ ] README
- [ ] answers.md
- [ ] Public URL
- [ ] Admin URL
- [ ] Repository
- [ ] Deployed commit
- [ ] Setup commands
- [ ] Build/check commands
- [ ] Environment variable names
- [ ] Screenshots
- [ ] Test results
- [ ] Time spent
- [ ] Known gaps
- [ ] AI tool
- [ ] Representative AI prompt
- [ ] AI verification/correction
- [ ] Recovery plan
- [ ] Premium setup/testing

---

# 66. Final Product Structure

The final product should feel like:

```text
                 TECH INJECT
              DESIGN LIBRARY
                    |
       +------------+-------------+
       |                          |
       v                          v
 PUBLIC CATALOGUE            ADMIN DASHBOARD
       |                          |
       |                          |
       v                          v
 Discover                  Manage Components
 Search                    Upload
 Preview                   Draft
 Props                     Validate
 Source                    Publish
 Install                   Unpublish
 AI Prompt                 Customers
       |                   Premium access
       |
       v
 Consumer React + TS App
```

---

# 67. What the Reviewer Should Be Able to Do

A reviewer should be able to:

### As visitor

```text
Open catalogue
Search component
Open component
See preview
See premium/free status
```

### As free customer

```text
Sign in
Use free component
See premium locked
```

### As premium customer

```text
Sign in
See premium component
Preview
Copy source
Install
Copy AI prompt
```

### As admin

```text
Login
Upload new component
Preview
Publish
See it publicly
Grant premium
Revoke premium
Unpublish
```

### As developer

```text
Create clean React + TS app
Run npx command
Build
Render component
```

---

# 68. Most Important Implementation Principle

The project should not be:

```text
Beautiful UI
+
Fake install button
+
Hardcoded components
+
Fake premium lock
```

It must be:

```text
Reusable components
+
Dynamic publishing
+
Persistent storage
+
Real authentication
+
Real authorization
+
Real installer
+
Real source delivery
+
Real AI prompt
+
Real consumer verification
```

The assignment explicitly values dependable reusable systems over attractive examples.

---

# 69. Timebox Strategy

The assignment timebox is **up to 8 hours**.

Do not spend the entire time polishing one page.

Recommended priority:

```text
1. Reference analysis
2. Core components
3. Dynamic component registry
4. Public catalogue
5. Admin publish
6. Premium access
7. Installer
8. Security tests
9. Deployment
10. Documentation
```

If time becomes short:

Prioritize:

```text
Dynamic publishing
Premium enforcement
Working installer
Consumer verification
```

over:

```text
Extra animations
Extra components
Fancy marketing sections
Advanced admin UI
```

---

# 70. Final Rule for Copilot

Before saying a feature is complete, ask:

```text
1. Is it implemented?
2. Is it typed?
3. Is it validated?
4. Is it secure?
5. Is it actually connected to persistence?
6. Is it tested?
7. Does it work after deployment?
8. Does the consumer project work independently?
9. Does it match the reference?
10. Can I explain the implementation in an interview?
```

If the answer to any required item is "no", do not mark the feature as complete.

---

# 71. Interview Ownership

The reviewer may ask about:

- Component boundaries
- Theme tokens
- Architecture
- Database
- Publishing
- Version consistency
- Premium access
- Authentication
- Authorization
- Installer security
- Preview security
- AI usage
- Deployment
- Recovery
- Clean code
- SOLID
- DRY
- KISS
- YAGNI
- Testing

Be able to point to the actual implementation.

The goal is not to memorize definitions.

The goal is to understand and own the system.

---

# 72. Final Source-of-Truth Summary

```text
SALES CRM
= visual reference
= component extraction
= theme
= reusable UI boundaries

ASTRYX
= catalogue/discovery reference
= developer documentation UX
= search/navigation/documentation inspiration

TECH INJECT
= our brand
= our implementation
= our component library
= our admin/publishing system
= our premium system
= our installer
= our AI integration
```

**Do not mix these responsibilities.**

Build a Tech Inject developer component library whose components visually derive from the Sales CRM and whose developer catalogue experience follows the useful discovery/documentation patterns demonstrated by Astryx.
