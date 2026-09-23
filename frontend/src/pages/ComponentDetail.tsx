import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import type { ComponentDetail as ComponentDetailType } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { CodeBlock } from '../components/common/CodeBlock';
import { CopyButton } from '../components/common/CopyButton';

// Import our 10 reusable components for live rendering previews!
import { Button } from '../components/library/Button';
import { Badge } from '../components/library/Badge';
import { Avatar } from '../components/library/Avatar';
import { Tabs } from '../components/library/Tabs';
import { FilterSelect } from '../components/library/FilterSelect';
import { Sidebar } from '../components/library/Sidebar';
import { DataTable } from '../components/library/DataTable';
import { MetricCard } from '../components/library/MetricCard';
import { ActionMenu } from '../components/library/ActionMenu';
import { Probability } from '../components/library/Probability';

import { Lock, ArrowLeft, Terminal, Cpu, FileCode, CheckCircle2, ShieldAlert } from 'lucide-react';
import './ComponentDetail.css';

export const ComponentDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { user } = useAuth();
  const [component, setComponent] = useState<ComponentDetailType | null>(null);
  const [agentPrompt, setAgentPrompt] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Live preview interactive state controls
  const [btnVariant, setBtnVariant] = useState<'primary' | 'secondary' | 'ghost' | 'danger'>('primary');
  const [btnSize, setBtnSize] = useState<'sm' | 'md' | 'lg'>('md');
  const [btnLoading, setBtnLoading] = useState(false);
  const [btnDisabled, setBtnDisabled] = useState(false);

  const [activeTab, setActiveTab] = useState('companies');
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [sidebarActive, setSidebarActive] = useState('companies');
  const [probValue, setProbValue] = useState(85);

  useEffect(() => {
    const loadDetail = async () => {
      if (!slug) return;
      setLoading(true);
      setError(null);
      try {
        const data = await api.getComponent(slug);
        setComponent(data);

        // Load AI prompt if unlocked
        if (!data.is_locked) {
          try {
            const p = await api.getAgentPrompt(slug);
            setAgentPrompt(p.prompt);
          } catch {
            setAgentPrompt(null);
          }
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load component details');
      } finally {
        setLoading(false);
      }
    };

    loadDetail();
  }, [slug, user]);

  if (loading) return <div className="tech-detail__loading">Loading component details...</div>;
  if (error || !component) return <div className="tech-detail__error">{error || 'Component not found'}</div>;

  const installCommand = `npx tech-inject add ${component.slug}`;

  // Helper to render live component previews
  const renderLivePreview = () => {
    switch (component.slug) {
      case 'button':
        return (
          <div className="tech-preview__container">
            <div className="tech-preview__controls">
              <label>Variant:
                <select value={btnVariant} onChange={(e: any) => setBtnVariant(e.target.value)}>
                  <option value="primary">Primary</option>
                  <option value="secondary">Secondary</option>
                  <option value="ghost">Ghost</option>
                  <option value="danger">Danger</option>
                </select>
              </label>
              <label>Size:
                <select value={btnSize} onChange={(e: any) => setBtnSize(e.target.value)}>
                  <option value="sm">Small</option>
                  <option value="md">Medium</option>
                  <option value="lg">Large</option>
                </select>
              </label>
              <label>
                <input type="checkbox" checked={btnLoading} onChange={(e) => setBtnLoading(e.target.checked)} /> Loading
              </label>
              <label>
                <input type="checkbox" checked={btnDisabled} onChange={(e) => setBtnDisabled(e.target.checked)} /> Disabled
              </label>
            </div>
            <div className="tech-preview__stage">
              <Button
                variant={btnVariant}
                size={btnSize}
                loading={btnLoading}
                disabled={btnDisabled}
                onClick={() => alert('Button Clicked!')}
              >
                Action Button
              </Button>
            </div>
          </div>
        );

      case 'badge':
        return (
          <div className="tech-preview__stage tech-preview__stage--row">
            <Badge variant="success">Success</Badge>
            <Badge variant="warning">Warning</Badge>
            <Badge variant="neutral">Neutral</Badge>
            <Badge variant="danger">Danger</Badge>
            <Badge variant="info">Info</Badge>
          </div>
        );

      case 'avatar':
        return (
          <div className="tech-preview__stage tech-preview__stage--row">
            <Avatar size="sm" name="Alex Santos" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100" />
            <Avatar size="md" name="Alex Santos" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100" />
            <Avatar size="lg" name="Alex Santos" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100" />
            <Avatar size="md" name="Jordan Lee" src="" />
          </div>
        );

      case 'tabs':
        return (
          <div className="tech-preview__stage">
            <Tabs
              items={[
                { id: 'companies', label: 'Companies', count: 24 },
                { id: 'deals', label: 'Deals', count: 12 },
                { id: 'forecast', label: 'Forecast' }
              ]}
              value={activeTab}
              onChange={setActiveTab}
            />
          </div>
        );

      case 'filter-select':
        return (
          <div className="tech-preview__stage">
            <FilterSelect
              label="Pipeline Owner"
              options={[
                { label: 'All Owners', value: 'all' },
                { label: 'Alex Santos', value: 'alex' },
                { label: 'Jordan Lee', value: 'jordan' }
              ]}
              value={selectedFilter}
              onChange={setSelectedFilter}
            />
          </div>
        );

      case 'sidebar':
        return (
          <div className="tech-preview__stage tech-preview__stage--height">
            <Sidebar
              title="Sales CRM"
              items={[
                { id: 'overview', label: 'Overview' },
                { id: 'companies', label: 'Companies', badge: 24 },
                { id: 'deals', label: 'Deals Pipeline' },
                { id: 'forecast', label: 'Sales Forecast' }
              ]}
              activeItem={sidebarActive}
              onSelect={setSidebarActive}
            />
          </div>
        );

      case 'data-table':
        return (
          <div className="tech-preview__stage">
            <DataTable
              columns={[
                { key: 'company', header: 'Company' },
                { key: 'segment', header: 'Segment', render: (r: any) => <Badge variant="info">{r.segment}</Badge> },
                { key: 'owner', header: 'Account Owner', render: (r: any) => <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><Avatar size="sm" name={r.owner} /><span>{r.owner}</span></div> },
                { key: 'pipeline', header: 'Pipeline Value' },
                { key: 'win', header: 'Win %', render: (r: any) => <Probability value={r.win} /> }
              ]}
              data={component.preview_data?.sample_data || []}
              selectable
            />
          </div>
        );

      case 'metric-card':
        return (
          <div className="tech-preview__stage tech-preview__stage--grid">
            <MetricCard label="Pipeline Value" value="$1,420,000" trend="+14.2%" trendType="up" description="Compared to last month" />
            <MetricCard label="Open Deals" value="38" trend="-3.5%" trendType="down" description="Active pipeline stage" />
          </div>
        );

      case 'action-menu':
        return (
          <div className="tech-preview__stage">
            <ActionMenu
              items={[
                { id: 'edit', label: 'Edit Record' },
                { id: 'duplicate', label: 'Duplicate Record' },
                { id: 'delete', label: 'Delete Record', destructive: true }
              ]}
              onSelect={(id) => alert(`Action Selected: ${id}`)}
            />
          </div>
        );

      case 'probability':
        return (
          <div className="tech-preview__stage" style={{ width: '300px' }}>
            <div style={{ marginBottom: 12 }}>
              <input type="range" min="0" max="100" value={probValue} onChange={(e) => setProbValue(Number(e.target.value))} />
            </div>
            <Probability value={probValue} />
          </div>
        );

      default:
        return <div className="tech-preview__stage">Live preview available.</div>;
    }
  };

  return (
    <div className="tech-detail">
      {/* Breadcrumb Header */}
      <div className="tech-detail__breadcrumb">
        <Link to="/components" className="tech-detail__back">
          <ArrowLeft size={16} />
          <span>Back to Catalogue</span>
        </Link>
      </div>

      <div className="tech-detail__header">
        <div className="tech-detail__title-row">
          <h1 className="tech-detail__title">{component.name}</h1>
          <span className="tech-detail__ver">v{component.version}</span>
          {component.access_level === 'premium' ? (
            <span className="tech-detail__tag tech-detail__tag--premium">
              <Lock size={12} /> Premium Component
            </span>
          ) : (
            <span className="tech-detail__tag tech-detail__tag--free">
              <CheckCircle2 size={12} /> Free Component
            </span>
          )}
        </div>
        <p className="tech-detail__desc">{component.description}</p>
      </div>

      {/* Live Preview Section */}
      <section className="tech-detail__section">
        <h2 className="tech-detail__section-title">Working Live Preview</h2>
        {renderLivePreview()}
      </section>

      {/* Installation Command */}
      <section className="tech-detail__section">
        <h2 className="tech-detail__section-title">
          <Terminal size={18} />
          <span>npx Installation Command</span>
        </h2>
        <div className="tech-detail__install-box">
          <code>{installCommand}</code>
          <CopyButton textToCopy={installCommand} label="Copy Command" />
        </div>
      </section>

      {/* Props Documentation Table */}
      <section className="tech-detail__section">
        <h2 className="tech-detail__section-title">Props Documentation</h2>
        {component.props.length === 0 ? (
          <p className="tech-detail__empty-text">No props required.</p>
        ) : (
          <table className="tech-detail__props-table">
            <thead>
              <tr>
                <th>Prop</th>
                <th>Type</th>
                <th>Default</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {component.props.map((p) => (
                <tr key={p.name}>
                  <td className="tech-detail__prop-name"><code>{p.name}</code></td>
                  <td className="tech-detail__prop-type"><code>{p.type}</code></td>
                  <td className="tech-detail__prop-def"><code>{p.default || '-'}</code></td>
                  <td className="tech-detail__prop-desc">{p.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Source Code Section or Premium Lock Card */}
      <section className="tech-detail__section">
        <h2 className="tech-detail__section-title">
          <FileCode size={18} />
          <span>Source Code</span>
        </h2>

        {component.is_locked ? (
          <div className="tech-detail__lock-card">
            <div className="tech-detail__lock-icon">
              <ShieldAlert size={32} />
            </div>
            <h3>Premium Component Locked</h3>
            <p>
              Source code and CLI installer access for this component require a Premium Customer account.
            </p>
            {user ? (
              <div className="tech-detail__lock-notice">
                Logged in as <strong>{user.email}</strong> (Free Account). Contact Administrator to request Premium access.
              </div>
            ) : (
              <Link to="/login" className="tech-detail__btn-lock-login">
                Sign In with Premium Account
              </Link>
            )}
          </div>
        ) : (
          <div>
            {Object.entries(component.source_files || {}).map(([filename, code]) => (
              <CodeBlock key={filename} filename={filename} code={code} />
            ))}
          </div>
        )}
      </section>

      {/* AI Agent Integration Prompt */}
      {!component.is_locked && agentPrompt && (
        <section className="tech-detail__section">
          <h2 className="tech-detail__section-title">
            <Cpu size={18} />
            <span>Copyable AI Agent Integration Prompt</span>
          </h2>
          <CodeBlock filename="ai-prompt.txt" code={agentPrompt} language="markdown" />
        </section>
      )}
    </div>
  );
};
