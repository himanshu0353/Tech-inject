import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, ShieldCheck, Terminal, Cpu, Layers } from 'lucide-react';
import './Home.css';

export const Home: React.FC = () => {
  return (
    <div className="tech-home">
      {/* Hero Section */}
      <section className="tech-home__hero">
        <div className="tech-home__hero-badge">
          <Sparkles size={14} />
          <span>Production-Ready React + TypeScript Component System</span>
        </div>
        <h1 className="tech-home__hero-title">
          Tech Inject <span className="tech-home__hero-highlight">Design Library</span>
        </h1>
        <p className="tech-home__hero-sub">
          A reusable, documented, dependable React & TypeScript design system extracted from Sales CRM interaction patterns. Built for speed, precision, and AI agent copilot integration.
        </p>

        <div className="tech-home__hero-actions">
          <Link to="/components" className="tech-home__btn-primary">
            <span>Browse Components</span>
            <ArrowRight size={16} />
          </Link>
          <a href="#installation" className="tech-home__btn-secondary">
            <span>Quick Install</span>
          </a>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="tech-home__features">
        <div className="tech-home__feature-card">
          <div className="tech-home__feature-icon"><Layers size={24} /></div>
          <h3>10 Core Components</h3>
          <p>Carefully engineered UI components (Button, Badge, Avatar, Sidebar, Tabs, FilterSelect, Data Table, MetricCard, ActionMenu, Probability) with exact Sales CRM aesthetic fidelity.</p>
        </div>

        <div className="tech-home__feature-card">
          <div className="tech-home__feature-icon"><Terminal size={24} /></div>
          <h3>npx CLI Installer</h3>
          <p>Install components directly into your clean React + TypeScript project with a single command: <code>npx tech-inject add &lt;slug&gt;</code>.</p>
        </div>

        <div className="tech-home__feature-card">
          <div className="tech-home__feature-icon"><Cpu size={24} /></div>
          <h3>AI Agent Integration</h3>
          <p>Every component provides a structured, copyable prompt tailored for AI coding assistants like Copilot and Antigravity.</p>
        </div>

        <div className="tech-home__feature-card">
          <div className="tech-home__feature-icon"><ShieldCheck size={24} /></div>
          <h3>Dynamic & Secure</h3>
          <p>Admin dynamic publishing without redeploying frontend code, backed by server-side premium access enforcement.</p>
        </div>
      </section>

      {/* Getting Started Guide */}
      <section id="installation" className="tech-home__guide">
        <h2 className="tech-home__section-title">Getting Started</h2>
        <div className="tech-home__guide-box">
          <div className="tech-home__step">
            <div className="tech-home__step-num">1</div>
            <div className="tech-home__step-content">
              <h4>Prerequisites</h4>
              <p>React 18+, TypeScript strict mode, and Node.js v18+ in your target application.</p>
            </div>
          </div>

          <div className="tech-home__step">
            <div className="tech-home__step-num">2</div>
            <div className="tech-home__step-content">
              <h4>Install Component</h4>
              <p>Run the installer command in your project directory:</p>
              <pre className="tech-home__code">npx tech-inject add data-table</pre>
            </div>
          </div>

          <div className="tech-home__step">
            <div className="tech-home__step-num">3</div>
            <div className="tech-home__step-content">
              <h4>Import & Render</h4>
              <p>Import the component into your app:</p>
              <pre className="tech-home__code">import {"{ DataTable }"} from './components/DataTable';</pre>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
