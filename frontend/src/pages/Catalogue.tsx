import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import type { ComponentSummary } from '../services/api';
import { Search, Lock, ArrowRight } from 'lucide-react';
import './Catalogue.css';

const CATEGORIES = ['All', 'Actions', 'Data Display', 'Navigation', 'Forms', 'People'];

export const Catalogue: React.FC = () => {
  const [components, setComponents] = useState<ComponentSummary[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadComponents = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getComponents(selectedCategory, search);
        setComponents(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch components');
      } finally {
        setLoading(false);
      }
    };

    const timer = setTimeout(loadComponents, 200);
    return () => clearTimeout(timer);
  }, [selectedCategory, search]);

  return (
    <div className="tech-catalogue">
      {/* Search Header */}
      <div className="tech-catalogue__header">
        <h1 className="tech-catalogue__title">Component Catalogue</h1>
        <p className="tech-catalogue__sub">
          Explore reusable Sales CRM components. Inspect variants, props documentation, source code, and copy AI prompts.
        </p>

        <div className="tech-catalogue__search-box">
          <Search size={18} className="tech-catalogue__search-icon" />
          <input
            type="text"
            placeholder="Search components by name, description, or category..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="tech-catalogue__search-input"
          />
        </div>
      </div>

      {/* Categories Bar */}
      <div className="tech-catalogue__categories">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            className={`tech-catalogue__cat-btn ${selectedCategory === cat ? 'tech-catalogue__cat-btn--active' : ''}`}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Component Grid */}
      {loading ? (
        <div className="tech-catalogue__loading">Loading component registry...</div>
      ) : error ? (
        <div className="tech-catalogue__error">{error}</div>
      ) : components.length === 0 ? (
        <div className="tech-catalogue__empty">No components found matching your filter criteria.</div>
      ) : (
        <div className="tech-catalogue__grid">
          {components.map((comp) => (
            <Link key={comp.id} to={`/components/${comp.slug}`} className="tech-catalogue__card">
              <div className="tech-catalogue__card-header">
                <div className="tech-catalogue__card-badge-row">
                  <span className="tech-catalogue__card-cat">{comp.category}</span>
                  {comp.access_level === 'premium' ? (
                    <span className="tech-catalogue__card-tag tech-catalogue__card-tag--premium">
                      <Lock size={12} />
                      Premium
                    </span>
                  ) : (
                    <span className="tech-catalogue__card-tag tech-catalogue__card-tag--free">
                      Free
                    </span>
                  )}
                </div>
                <h3 className="tech-catalogue__card-title">{comp.name}</h3>
              </div>

              <p className="tech-catalogue__card-desc">{comp.description}</p>

              <div className="tech-catalogue__card-footer">
                <span className="tech-catalogue__card-ver">v{comp.version}</span>
                <span className="tech-catalogue__card-link">
                  <span>View Details</span>
                  <ArrowRight size={14} />
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
