import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { ComponentSummary, User } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Plus, Globe, EyeOff, Shield, Star, Layers, Users, Trash2 } from 'lucide-react';
import './AdminDashboard.css';

export const AdminDashboard: React.FC = () => {
  const { user } = useAuth();
  const [tab, setTab] = useState<'components' | 'customers'>('components');

  // Component states
  const [components, setComponents] = useState<ComponentSummary[]>([]);
  const [loadingComps, setLoadingComps] = useState(true);

  // Customer states
  const [customers, setCustomers] = useState<User[]>([]);
  const [loadingCust, setLoadingCust] = useState(false);

  // Create Draft Form Modal State
  const [showModal, setShowModal] = useState(false);
  const [slug, setSlug] = useState('');
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('Actions');
  const [accessLevel, setAccessLevel] = useState<'free' | 'premium'>('free');
  const [version] = useState('1.0.0');
  const [fileName, setFileName] = useState('CustomWidget.tsx');
  const [fileCode, setFileCode] = useState(`import React from 'react';\n\nexport const CustomWidget = () => {\n  return <div style={{ padding: 16, background: '#1e293b', color: '#fff', borderRadius: 8 }}>Dynamic Admin Uploaded Component!</div>;\n};`);
  const [formError, setFormError] = useState<string | null>(null);

  const loadComponents = async () => {
    setLoadingComps(true);
    try {
      const data = await api.getComponents();
      setComponents(data);
    } catch {
      //
    } finally {
      setLoadingComps(false);
    }
  };

  const loadCustomers = async () => {
    setLoadingCust(true);
    try {
      const data = await api.getCustomers();
      setCustomers(data);
    } catch {
      //
    } finally {
      setLoadingCust(false);
    }
  };

  useEffect(() => {
    loadComponents();
  }, []);

  useEffect(() => {
    if (tab === 'customers') loadCustomers();
  }, [tab]);

  const handlePublish = async (id: number) => {
    try {
      await api.publishComponent(id);
      loadComponents();
    } catch (err: any) {
      alert(err.message || 'Failed to publish');
    }
  };

  const handleUnpublish = async (id: number) => {
    try {
      await api.unpublishComponent(id);
      loadComponents();
    } catch (err: any) {
      alert(err.message || 'Failed to unpublish');
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete component "${name}"?`)) return;
    try {
      await api.deleteComponent(id);
      loadComponents();
    } catch (err: any) {
      alert(err.message || 'Failed to delete component');
    }
  };

  const handleGrantPremium = async (userId: number) => {
    try {
      await api.grantPremium(userId);
      loadCustomers();
    } catch (err: any) {
      alert(err.message || 'Failed to grant premium');
    }
  };

  const handleRevokePremium = async (userId: number) => {
    try {
      await api.revokePremium(userId);
      loadCustomers();
    } catch (err: any) {
      alert(err.message || 'Failed to revoke premium');
    }
  };

  const handleCreateDraft = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    try {
      await api.createComponent({
        slug: slug.trim().toLowerCase(),
        name,
        description,
        category,
        access_level: accessLevel,
        version,
        props: [],
        dependencies: [],
        preview_data: {},
        source_files: {
          [fileName]: fileCode
        }
      });
      setShowModal(false);
      // Reset form
      setSlug('');
      setName('');
      setDescription('');
      loadComponents();
    } catch (err: any) {
      setFormError(err.message || 'Failed to create component');
    }
  };

  if (!user || user.role !== 'admin') {
    return (
      <div className="tech-admin__unauthorized">
        <Shield size={36} />
        <h2>Access Denied</h2>
        <p>You must be signed in as an Administrator to view this dashboard.</p>
      </div>
    );
  }

  return (
    <div className="tech-admin">
      <div className="tech-admin__header">
        <div>
          <h1 className="tech-admin__title">Admin Control Dashboard</h1>
          <p className="tech-admin__sub">Manage components, draft uploads, dynamic publishing, and customer premium access.</p>
        </div>
        <button onClick={() => setShowModal(true)} className="tech-admin__btn-new">
          <Plus size={16} />
          <span>Upload New Component</span>
        </button>
      </div>

      {/* Admin Nav Tabs */}
      <div className="tech-admin__tabs">
        <button
          className={`tech-admin__tab-btn ${tab === 'components' ? 'tech-admin__tab-btn--active' : ''}`}
          onClick={() => setTab('components')}
        >
          <Layers size={16} />
          <span>Component Registry ({components.length})</span>
        </button>
        <button
          className={`tech-admin__tab-btn ${tab === 'customers' ? 'tech-admin__tab-btn--active' : ''}`}
          onClick={() => setTab('customers')}
        >
          <Users size={16} />
          <span>Customer Accounts</span>
        </button>
      </div>

      {/* Component Registry Tab */}
      {tab === 'components' && (
        <div className="tech-admin__table-card">
          {loadingComps ? (
            <div className="tech-admin__loading">Loading component registry...</div>
          ) : (
            <table className="tech-admin__table">
              <thead>
                <tr>
                  <th>Slug / Name</th>
                  <th>Category</th>
                  <th>Access</th>
                  <th>Status</th>
                  <th>Version</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {components.map((comp) => (
                  <tr key={comp.id}>
                    <td>
                      <div className="tech-admin__comp-name">{comp.name}</div>
                      <div className="tech-admin__comp-slug"><code>{comp.slug}</code></div>
                    </td>
                    <td><span className="tech-admin__cat-pill">{comp.category}</span></td>
                    <td>
                      <span className={`tech-admin__access-pill tech-admin__access-pill--${comp.access_level}`}>
                        {comp.access_level}
                      </span>
                    </td>
                    <td>
                      <span className={`tech-admin__status-pill tech-admin__status-pill--${comp.status}`}>
                        {comp.status === 'published' ? <Globe size={12} /> : <EyeOff size={12} />}
                        {comp.status}
                      </span>
                    </td>
                    <td><code>v{comp.version}</code></td>
                    <td>
                      <div className="tech-admin__action-row">
                        {comp.status === 'draft' ? (
                          <button
                            onClick={() => handlePublish(comp.id)}
                            className="tech-admin__btn-publish"
                          >
                            <Globe size={14} />
                            <span>Publish</span>
                          </button>
                        ) : (
                          <button
                            onClick={() => handleUnpublish(comp.id)}
                            className="tech-admin__btn-unpublish"
                          >
                            <EyeOff size={14} />
                            <span>Unpublish</span>
                          </button>
                        )}
                        <button
                          onClick={() => handleDelete(comp.id, comp.name)}
                          className="tech-admin__btn-delete"
                          title="Delete component"
                        >
                          <Trash2 size={14} />
                          <span>Delete</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Customer Management Tab */}
      {tab === 'customers' && (
        <div className="tech-admin__table-card">
          {loadingCust ? (
            <div className="tech-admin__loading">Loading customer list...</div>
          ) : (
            <table className="tech-admin__table">
              <thead>
                <tr>
                  <th>User ID</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Premium Access</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {customers.map((cust) => (
                  <tr key={cust.id}>
                    <td><code>#{cust.id}</code></td>
                    <td><strong>{cust.email}</strong></td>
                    <td><code>{cust.role}</code></td>
                    <td>
                      {cust.is_premium ? (
                        <span className="tech-admin__access-pill tech-admin__access-pill--premium">
                          <Star size={12} /> Premium Active
                        </span>
                      ) : (
                        <span className="tech-admin__access-pill tech-admin__access-pill--free">
                          Free Account
                        </span>
                      )}
                    </td>
                    <td>
                      {cust.is_premium ? (
                        <button
                          onClick={() => handleRevokePremium(cust.id)}
                          className="tech-admin__btn-revoke"
                        >
                          Revoke Premium
                        </button>
                      ) : (
                        <button
                          onClick={() => handleGrantPremium(cust.id)}
                          className="tech-admin__btn-grant"
                        >
                          Grant Premium Access
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Create Draft Modal */}
      {showModal && (
        <div className="tech-modal__overlay">
          <div className="tech-modal__card">
            <div className="tech-modal__header">
              <h3>Upload & Register New Component Draft</h3>
              <button onClick={() => setShowModal(false)} className="tech-modal__close">✕</button>
            </div>

            {formError && <div className="tech-admin__error">{formError}</div>}

            <form onSubmit={handleCreateDraft} className="tech-modal__form">
              <div className="tech-modal__grid">
                <div className="tech-modal__field">
                  <label>Component Name</label>
                  <input required type="text" placeholder="Custom Card" value={name} onChange={(e) => setName(e.target.value)} />
                </div>
                <div className="tech-modal__field">
                  <label>URL Slug</label>
                  <input required type="text" placeholder="custom-card" value={slug} onChange={(e) => setSlug(e.target.value)} />
                </div>
              </div>

              <div className="tech-modal__field">
                <label>Description</label>
                <textarea required placeholder="Short description..." value={description} onChange={(e) => setDescription(e.target.value)} />
              </div>

              <div className="tech-modal__grid">
                <div className="tech-modal__field">
                  <label>Category</label>
                  <select value={category} onChange={(e) => setCategory(e.target.value)}>
                    <option value="Actions">Actions</option>
                    <option value="Data Display">Data Display</option>
                    <option value="Navigation">Navigation</option>
                    <option value="Forms">Forms</option>
                    <option value="People">People</option>
                  </select>
                </div>

                <div className="tech-modal__field">
                  <label>Access Level</label>
                  <select value={accessLevel} onChange={(e: any) => setAccessLevel(e.target.value)}>
                    <option value="free">Free</option>
                    <option value="premium">Premium</option>
                  </select>
                </div>
              </div>

              <div className="tech-modal__field">
                <label>Source File Name</label>
                <input required type="text" value={fileName} onChange={(e) => setFileName(e.target.value)} />
              </div>

              <div className="tech-modal__field">
                <label>React Source Code</label>
                <textarea required rows={8} className="tech-modal__code-area" value={fileCode} onChange={(e) => setFileCode(e.target.value)} />
              </div>

              <div className="tech-modal__footer">
                <button type="button" onClick={() => setShowModal(false)} className="tech-modal__btn-cancel">Cancel</button>
                <button type="submit" className="tech-modal__btn-submit">Create Draft</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
