import datetime
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import User, Component
from .auth import hash_password

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Users if not existing
        if not db.query(User).filter(User.email == "admin@techinject.com").first():
            admin = User(
                email="admin@techinject.com",
                password_hash=hash_password("admin123"),
                role="admin",
                is_premium=True
            )
            db.add(admin)

        if not db.query(User).filter(User.email == "free@example.com").first():
            free_user = User(
                email="free@example.com",
                password_hash=hash_password("customer123"),
                role="customer",
                is_premium=False
            )
            db.add(free_user)

        # Requirement #2: Seed TWO users who can use premium components
        if not db.query(User).filter(User.email == "premium@example.com").first():
            premium_user1 = User(
                email="premium@example.com",
                password_hash=hash_password("customer123"),
                role="customer",
                is_premium=True
            )
            db.add(premium_user1)

        if not db.query(User).filter(User.email == "premium2@example.com").first():
            premium_user2 = User(
                email="premium2@example.com",
                password_hash=hash_password("customer123"),
                role="customer",
                is_premium=True
            )
            db.add(premium_user2)

        db.commit()

        # 2. Seed 10 Core Components if database is empty
        if db.query(Component).count() == 0:
            now = datetime.datetime.utcnow()

            components_data = [
                # --- FREE COMPONENTS ---
                {
                    "slug": "button",
                    "name": "Button",
                    "description": "Flexible action button component derived from Sales CRM controls.",
                    "category": "Actions",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "variant", "type": "'primary' | 'secondary' | 'ghost' | 'danger'", "default": "'primary'", "description": "Visual style variant."},
                        {"name": "size", "type": "'sm' | 'md' | 'lg'", "default": "'md'", "description": "Button size padding and font."},
                        {"name": "disabled", "type": "boolean", "default": "false", "description": "Disables interaction."},
                        {"name": "loading", "type": "boolean", "default": "false", "description": "Shows loading spinner."},
                        {"name": "children", "type": "React.ReactNode", "default": "None", "description": "Button label or icon content."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "variants": ["primary", "secondary", "ghost", "danger"],
                        "sizes": ["sm", "md", "lg"],
                        "states": ["default", "hover", "disabled", "loading"]
                    },
                    "source_files_json": {
                        "Button.tsx": """import React from 'react';
import './Button.css';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  children,
  className = '',
  ...props
}) => {
  return (
    <button
      className={`tech-btn tech-btn--${variant} tech-btn--${size} ${loading ? 'tech-btn--loading' : ''} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className="tech-btn__spinner" />}
      <span className="tech-btn__content">{children}</span>
    </button>
  );
};""",
                        "Button.css": """.tech-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: inherit;
  font-weight: 500;
  border-radius: var(--radius-md, 6px);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-fast, 150ms ease-in-out);
  outline: none;
  position: relative;
  white-space: nowrap;
}

.tech-btn:focus-visible {
  box-shadow: 0 0 0 2px var(--bg-app, #090d16), 0 0 0 4px var(--primary, #3b82f6);
}

.tech-btn--sm {
  padding: 4px 10px;
  font-size: var(--font-xs, 0.75rem);
  height: 28px;
}

.tech-btn--md {
  padding: 6px 14px;
  font-size: var(--font-sm, 0.875rem);
  height: 36px;
}

.tech-btn--lg {
  padding: 8px 18px;
  font-size: var(--font-base, 1rem);
  height: 44px;
}

.tech-btn--primary {
  background-color: var(--primary, #3b82f6);
  color: var(--primary-text, #ffffff);
}

.tech-btn--primary:hover:not(:disabled) {
  background-color: var(--primary-hover, #2563eb);
}

.tech-btn--secondary {
  background-color: var(--bg-surface, #111827);
  color: var(--text-main, #f8fafc);
  border-color: var(--border-subtle, #1e293b);
}

.tech-btn--secondary:hover:not(:disabled) {
  background-color: var(--bg-surface-hover, #1f2937);
  border-color: var(--border-medium, #334155);
}

.tech-btn--ghost {
  background-color: transparent;
  color: var(--text-muted, #94a3b8);
}

.tech-btn--ghost:hover:not(:disabled) {
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-main, #f8fafc);
}

.tech-btn--danger {
  background-color: var(--danger-bg, rgba(239, 68, 68, 0.15));
  color: var(--danger-text, #f87171);
  border-color: var(--danger-border, rgba(239, 68, 68, 0.3));
}

.tech-btn--danger:hover:not(:disabled) {
  background-color: rgba(239, 68, 68, 0.25);
}

.tech-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tech-btn__spinner {
  width: 14px;
  height: 14px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: tech-spin 0.6s linear infinite;
  margin-right: 6px;
}

@keyframes tech-spin {
  to { transform: rotate(360deg); }
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "badge",
                    "name": "Badge",
                    "description": "Status and category pill badge component.",
                    "category": "Data Display",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "variant", "type": "'success' | 'warning' | 'neutral' | 'danger' | 'info'", "default": "'neutral'", "description": "Color theme indicator."},
                        {"name": "children", "type": "React.ReactNode", "default": "None", "description": "Badge text label."}
                    ],
                    "dependencies_json": [],
                    "preview_data_json": {
                        "variants": ["success", "warning", "neutral", "danger", "info"]
                    },
                    "source_files_json": {
                        "Badge.tsx": """import React from 'react';
import './Badge.css';

export interface BadgeProps {
  variant?: 'success' | 'warning' | 'neutral' | 'danger' | 'info';
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'neutral', children, className = '' }) => {
  return (
    <span className={`tech-badge tech-badge--${variant} ${className}`}>
      {children}
    </span>
  );
};""",
                        "Badge.css": """.tech-badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: var(--radius-full, 9999px);
  font-size: var(--font-xs, 0.75rem);
  font-weight: 500;
  line-height: 1.25;
  border: 1px solid transparent;
}

.tech-badge--success {
  background-color: var(--success-bg, rgba(16, 185, 129, 0.15));
  color: var(--success-text, #34d399);
  border-color: var(--success-border, rgba(16, 185, 129, 0.3));
}

.tech-badge--warning {
  background-color: var(--warning-bg, rgba(245, 158, 11, 0.15));
  color: var(--warning-text, #fbbf24);
  border-color: var(--warning-border, rgba(245, 158, 11, 0.3));
}

.tech-badge--danger {
  background-color: var(--danger-bg, rgba(239, 68, 68, 0.15));
  color: var(--danger-text, #f87171);
  border-color: var(--danger-border, rgba(239, 68, 68, 0.3));
}

.tech-badge--info {
  background-color: var(--info-bg, rgba(59, 130, 246, 0.15));
  color: var(--info-text, #60a5fa);
  border-color: var(--info-border, rgba(59, 130, 246, 0.3));
}

.tech-badge--neutral {
  background-color: var(--neutral-bg, rgba(100, 116, 139, 0.15));
  color: var(--neutral-text, #cbd5e1);
  border-color: var(--neutral-border, rgba(100, 116, 139, 0.3));
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "avatar",
                    "name": "Avatar",
                    "description": "User profile avatar with image and initials fallback.",
                    "category": "People",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "src", "type": "string", "default": "undefined", "description": "Image URL."},
                        {"name": "name", "type": "string", "default": "'User'", "description": "User full name for initials fallback and alt text."},
                        {"name": "size", "type": "'sm' | 'md' | 'lg'", "default": "'md'", "description": "Avatar dimension size."}
                    ],
                    "dependencies_json": [],
                    "preview_data_json": {
                        "sizes": ["sm", "md", "lg"],
                        "examples": [
                          {"name": "Alex Santos", "src": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100"},
                          {"name": "Jordan Lee", "src": ""}
                        ]
                    },
                    "source_files_json": {
                        "Avatar.tsx": """import React, { useState } from 'react';
import './Avatar.css';

export interface AvatarProps {
  src?: string;
  name?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Avatar: React.FC<AvatarProps> = ({
  src,
  name = 'User',
  size = 'md',
  className = ''
}) => {
  const [imageError, setImageError] = useState(false);

  const getInitials = (str: string) => {
    const parts = str.trim().split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    }
    return str.slice(0, 2).toUpperCase();
  };

  return (
    <div className={`tech-avatar tech-avatar--${size} ${className}`}>
      {src && !imageError ? (
        <img
          src={src}
          alt={name}
          className="tech-avatar__img"
          onError={() => setImageError(true)}
        />
      ) : (
        <span className="tech-avatar__fallback">{getInitials(name)}</span>
      )}
    </div>
  );
};""",
                        "Avatar.css": """.tech-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full, 9999px);
  background-color: var(--bg-surface-active, #374151);
  color: var(--text-main, #f8fafc);
  font-weight: 600;
  overflow: hidden;
  user-select: none;
  border: 1px solid var(--border-subtle, #1e293b);
}

.tech-avatar--sm {
  width: 24px;
  height: 24px;
  font-size: 10px;
}

.tech-avatar--md {
  width: 36px;
  height: 36px;
  font-size: var(--font-xs, 0.75rem);
}

.tech-avatar--lg {
  width: 48px;
  height: 48px;
  font-size: var(--font-sm, 0.875rem);
}

.tech-avatar__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tech-avatar__fallback {
  letter-spacing: 0.5px;
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "tabs",
                    "name": "Tabs",
                    "description": "Navigation tab bar component extracted from CRM view switchers.",
                    "category": "Navigation",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "items", "type": "Array<{ id: string; label: string }>", "default": "[]", "description": "Tab items definition."},
                        {"name": "value", "type": "string", "default": "None", "description": "Active tab id."},
                        {"name": "onChange", "type": "(id: string) => void", "default": "None", "description": "Callback when tab changes."}
                    ],
                    "dependencies_json": [],
                    "preview_data_json": {
                        "tabs": [
                            {"id": "companies", "label": "Companies"},
                            {"id": "deals", "label": "Deals"},
                            {"id": "forecast", "label": "Forecast"}
                        ]
                    },
                    "source_files_json": {
                        "Tabs.tsx": """import React from 'react';
import './Tabs.css';

export interface TabItem {
  id: string;
  label: string;
  count?: number;
}

export interface TabsProps {
  items: TabItem[];
  value: string;
  onChange: (id: string) => void;
  className?: string;
}

export const Tabs: React.FC<TabsProps> = ({ items, value, onChange, className = '' }) => {
  return (
    <div className={`tech-tabs ${className}`} role="tablist">
      {items.map((tab) => {
        const isActive = tab.id === value;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            className={`tech-tabs__item ${isActive ? 'tech-tabs__item--active' : ''}`}
            onClick={() => onChange(tab.id)}
          >
            <span>{tab.label}</span>
            {tab.count !== undefined && (
              <span className="tech-tabs__count">{tab.count}</span>
            )}
          </button>
        );
      })}
    </div>
  );
};""",
                        "Tabs.css": """.tech-tabs {
  display: inline-flex;
  align-items: center;
  background-color: var(--bg-surface, #111827);
  padding: 3px;
  border-radius: var(--radius-md, 6px);
  border: 1px solid var(--border-subtle, #1e293b);
}

.tech-tabs__item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: var(--radius-sm, 4px);
  border: none;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  font-size: var(--font-sm, 0.875rem);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast, 150ms ease-in-out);
}

.tech-tabs__item:hover:not(.tech-tabs__item--active) {
  color: var(--text-main, #f8fafc);
  background-color: var(--bg-surface-hover, #1f2937);
}

.tech-tabs__item--active {
  background-color: var(--bg-card, #131b2e);
  color: var(--primary, #3b82f6);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.tech-tabs__count {
  font-size: var(--font-xs, 0.75rem);
  padding: 1px 6px;
  border-radius: var(--radius-full, 9999px);
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-muted, #94a3b8);
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "filter-select",
                    "name": "Filter Select",
                    "description": "Dropdown filter selector derived from CRM data filtering controls.",
                    "category": "Forms",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "label", "type": "string", "default": "None", "description": "Filter field label."},
                        {"name": "options", "type": "Array<{ label: string; value: string }>", "default": "[]", "description": "List of selectable options."},
                        {"name": "value", "type": "string", "default": "''", "description": "Currently selected value."},
                        {"name": "onChange", "type": "(val: string) => void", "default": "None", "description": "Selection change callback."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "label": "Pipeline Owner",
                        "options": [
                            {"label": "All Owners", "value": "all"},
                            {"label": "Alex Santos", "value": "alex"},
                            {"label": "Jordan Lee", "value": "jordan"},
                            {"label": "Taylor Reed", "value": "taylor"}
                        ]
                    },
                    "source_files_json": {
                        "FilterSelect.tsx": """import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import './FilterSelect.css';

export interface Option {
  label: string;
  value: string;
}

export interface FilterSelectProps {
  label: string;
  options: Option[];
  value: string;
  onChange: (value: string) => void;
  className?: string;
}

export const FilterSelect: React.FC<FilterSelectProps> = ({
  label,
  options,
  value,
  onChange,
  className = ''
}) => {
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const selectedOption = options.find((o) => o.value === value) || options[0];

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`tech-filter-select ${className}`} ref={containerRef}>
      <button
        type="button"
        className={`tech-filter-select__trigger ${open ? 'tech-filter-select__trigger--open' : ''}`}
        onClick={() => setOpen(!open)}
      >
        <span className="tech-filter-select__label">{label}:</span>
        <span className="tech-filter-select__value">{selectedOption?.label}</span>
        <ChevronDown className="tech-filter-select__icon" size={14} />
      </button>

      {open && (
        <div className="tech-filter-select__menu">
          {options.map((option) => {
            const isSelected = option.value === value;
            return (
              <button
                key={option.value}
                type="button"
                className={`tech-filter-select__item ${isSelected ? 'tech-filter-select__item--selected' : ''}`}
                onClick={() => {
                  onChange(option.value);
                  setOpen(false);
                }}
              >
                <span>{option.label}</span>
                {isSelected && <Check size={14} className="tech-filter-select__check" />}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};""",
                        "FilterSelect.css": """.tech-filter-select {
  position: relative;
  display: inline-block;
}

.tech-filter-select__trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background-color: var(--bg-surface, #111827);
  border: 1px solid var(--border-subtle, #1e293b);
  border-radius: var(--radius-md, 6px);
  color: var(--text-main, #f8fafc);
  font-size: var(--font-sm, 0.875rem);
  cursor: pointer;
  transition: all var(--transition-fast, 150ms ease-in-out);
}

.tech-filter-select__trigger:hover {
  background-color: var(--bg-surface-hover, #1f2937);
  border-color: var(--border-medium, #334155);
}

.tech-filter-select__label {
  color: var(--text-muted, #94a3b8);
  font-weight: 500;
}

.tech-filter-select__value {
  color: var(--text-main, #f8fafc);
  font-weight: 600;
}

.tech-filter-select__icon {
  color: var(--text-subtle, #64748b);
}

.tech-filter-select__menu {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  min-width: 180px;
  background-color: var(--bg-card, #131b2e);
  border: 1px solid var(--border-medium, #334155);
  border-radius: var(--radius-md, 6px);
  box-shadow: var(--shadow-lg);
  padding: 4px;
  z-index: 50;
}

.tech-filter-select__item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 10px;
  border-radius: var(--radius-sm, 4px);
  border: none;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  font-size: var(--font-sm, 0.875rem);
  text-align: left;
  cursor: pointer;
}

.tech-filter-select__item:hover {
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-main, #f8fafc);
}

.tech-filter-select__item--selected {
  color: var(--primary, #3b82f6);
  font-weight: 600;
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "sidebar",
                    "name": "Sidebar Navigation",
                    "description": "Left application navigation bar extracted from Sales CRM.",
                    "category": "Navigation",
                    "access_level": "free",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "items", "type": "Array<{ id: string; label: string; icon: string }>", "default": "[]", "description": "Navigation links list."},
                        {"name": "activeItem", "type": "string", "default": "''", "description": "Active item ID."},
                        {"name": "onSelect", "type": "(id: string) => void", "default": "None", "description": "Navigation click handler."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "activeItem": "companies",
                        "items": [
                            {"id": "overview", "label": "Overview", "icon": "LayoutDashboard"},
                            {"id": "companies", "label": "Companies", "icon": "Building2"},
                            {"id": "deals", "label": "Deals Pipeline", "icon": "Kanban"},
                            {"id": "forecast", "label": "Sales Forecast", "icon": "TrendingUp"}
                        ]
                    },
                    "source_files_json": {
                        "Sidebar.tsx": """import React from 'react';
import './Sidebar.css';

export interface SidebarItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  badge?: string | number;
}

export interface SidebarProps {
  title?: string;
  items: SidebarItem[];
  activeItem: string;
  onSelect: (id: string) => void;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  title = 'Tech Inject',
  items,
  activeItem,
  onSelect,
  className = ''
}) => {
  return (
    <aside className={`tech-sidebar ${className}`}>
      {title && (
        <div className="tech-sidebar__header">
          <div className="tech-sidebar__logo-mark" />
          <span className="tech-sidebar__title">{title}</span>
        </div>
      )}
      <nav className="tech-sidebar__nav">
        {items.map((item) => {
          const isActive = item.id === activeItem;
          return (
            <button
              key={item.id}
              className={`tech-sidebar__item ${isActive ? 'tech-sidebar__item--active' : ''}`}
              onClick={() => onSelect(item.id)}
            >
              {item.icon && <span className="tech-sidebar__icon">{item.icon}</span>}
              <span className="tech-sidebar__label">{item.label}</span>
              {item.badge !== undefined && (
                <span className="tech-sidebar__badge">{item.badge}</span>
              )}
            </button>
          );
        })}
      </nav>
    </aside>
  );
};""",
                        "Sidebar.css": """.tech-sidebar {
  width: 240px;
  height: 100%;
  background-color: var(--bg-surface, #111827);
  border-right: 1px solid var(--border-subtle, #1e293b);
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
}

.tech-sidebar__header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px 20px 12px;
}

.tech-sidebar__logo-mark {
  width: 20px;
  height: 20px;
  border-radius: var(--radius-sm, 4px);
  background: linear-gradient(135deg, var(--primary, #3b82f6), #1d4ed8);
}

.tech-sidebar__title {
  font-weight: 700;
  font-size: var(--font-base, 1rem);
  color: var(--text-main, #f8fafc);
  letter-spacing: -0.02em;
}

.tech-sidebar__nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tech-sidebar__item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: var(--radius-md, 6px);
  border: none;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  font-size: var(--font-sm, 0.875rem);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast, 150ms ease-in-out);
  text-align: left;
  width: 100%;
}

.tech-sidebar__item:hover:not(.tech-sidebar__item--active) {
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-main, #f8fafc);
}

.tech-sidebar__item--active {
  background-color: var(--primary-light, rgba(59, 130, 246, 0.12));
  color: var(--primary, #3b82f6);
  font-weight: 600;
}

.tech-sidebar__icon {
  display: flex;
  align-items: center;
  color: currentColor;
}

.tech-sidebar__label {
  flex: 1;
}

.tech-sidebar__badge {
  font-size: var(--font-xs, 0.75rem);
  padding: 1px 6px;
  border-radius: var(--radius-full, 9999px);
  background-color: var(--bg-surface-active, #374151);
  color: var(--text-main, #f8fafc);
}"""
                    },
                    "published_at": now
                },

                # --- PREMIUM COMPONENTS (FLAGSHIP & ADVANCED UI) ---
                {
                    "slug": "data-table",
                    "name": "Data Table (Flagship)",
                    "description": "Comprehensive, reusable data table with sorting, row selection, and pagination extracted from the Sales CRM Companies table.",
                    "category": "Data Display",
                    "access_level": "premium",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "columns", "type": "ColumnDef<T>[]", "default": "[]", "description": "Column definitions with key, label, and render functions."},
                        {"name": "data", "type": "T[]", "default": "[]", "description": "Array of row data objects."},
                        {"name": "selectable", "type": "boolean", "default": "false", "description": "Enables row checkbox selection."},
                        {"name": "sortable", "type": "boolean", "default": "false", "description": "Enables column header sorting."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "sample_data": [
                            {"id": "1", "company": "Acme Corp", "segment": "Enterprise", "owner": "Alex Santos", "deals": 3, "pipeline": "$450,000", "win": 85},
                            {"id": "2", "company": "Starlight AI", "segment": "Pilot", "owner": "Jordan Lee", "deals": 1, "pipeline": "$120,000", "win": 60},
                            {"id": "3", "company": "Nexus Systems", "segment": "SMB", "owner": "Taylor Reed", "deals": 4, "pipeline": "$280,000", "win": 90}
                        ]
                    },
                    "source_files_json": {
                        "DataTable.tsx": """import React, { useState } from 'react';
import { ChevronUp, ChevronDown } from 'lucide-react';
import './DataTable.css';

export interface ColumnDef<T> {
  key: string;
  header: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
}

export interface DataTableProps<T extends { id: string | number }> {
  columns: ColumnDef<T>[];
  data: T[];
  selectable?: boolean;
  onSelectionChange?: (selectedIds: (string | number)[]) => void;
  className?: string;
}

export function DataTable<T extends { id: string | number }>({
  columns,
  data,
  selectable = false,
  onSelectionChange,
  className = ''
}: DataTableProps<T>) {
  const [selectedIds, setSelectedIds] = useState<Set<string | number>>(new Set());
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const toggleSelectAll = () => {
    if (selectedIds.size === data.length) {
      setSelectedIds(new Set());
      onSelectionChange?.([]);
    } else {
      const all = new Set(data.map((d) => d.id));
      setSelectedIds(all);
      onSelectionChange?.(Array.from(all));
    }
  };

  const toggleSelectRow = (id: string | number) => {
    const updated = new Set(selectedIds);
    if (updated.has(id)) {
      updated.delete(id);
    } else {
      updated.add(id);
    }
    setSelectedIds(updated);
    onSelectionChange?.(Array.from(updated));
  };

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  const sortedData = [...data].sort((a: any, b: any) => {
    if (!sortKey) return 0;
    const valA = a[sortKey];
    const valB = b[sortKey];
    if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
    if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <div className={`tech-datatable-wrapper ${className}`}>
      <table className="tech-datatable">
        <thead>
          <tr>
            {selectable && (
              <th className="tech-datatable__th tech-datatable__th--check">
                <input
                  type="checkbox"
                  checked={data.length > 0 && selectedIds.size === data.length}
                  onChange={toggleSelectAll}
                />
              </th>
            )}
            {columns.map((col) => (
              <th
                key={col.key}
                className={`tech-datatable__th ${col.sortable !== false ? 'tech-datatable__th--sortable' : ''}`}
                onClick={() => col.sortable !== false && handleSort(col.key)}
              >
                <div className="tech-datatable__th-content">
                  <span>{col.header}</span>
                  {sortKey === col.key && (
                    sortOrder === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row) => {
            const isSelected = selectedIds.has(row.id);
            return (
              <tr
                key={row.id}
                className={`tech-datatable__tr ${isSelected ? 'tech-datatable__tr--selected' : ''}`}
              >
                {selectable && (
                  <td className="tech-datatable__td tech-datatable__td--check">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => toggleSelectRow(row.id)}
                    />
                  </td>
                )}
                {columns.map((col) => (
                  <td key={col.key} className="tech-datatable__td">
                    {col.render ? col.render(row) : (row as any)[col.key]}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}""",
                        "DataTable.css": """.tech-datatable-wrapper {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border-subtle, #1e293b);
  border-radius: var(--radius-lg, 8px);
  background-color: var(--bg-surface, #111827);
}

.tech-datatable {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: var(--font-sm, 0.875rem);
}

.tech-datatable__th {
  padding: 10px 16px;
  background-color: var(--bg-card, #131b2e);
  color: var(--text-muted, #94a3b8);
  font-weight: 600;
  border-bottom: 1px solid var(--border-subtle, #1e293b);
  user-select: none;
}

.tech-datatable__th--sortable {
  cursor: pointer;
}

.tech-datatable__th--sortable:hover {
  color: var(--text-main, #f8fafc);
}

.tech-datatable__th-content {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tech-datatable__td {
  padding: 12px 16px;
  color: var(--text-main, #f8fafc);
  border-bottom: 1px solid var(--border-subtle, #1e293b);
}

.tech-datatable__tr:last-child .tech-datatable__td {
  border-bottom: none;
}

.tech-datatable__tr:hover {
  background-color: var(--bg-surface-hover, #1f2937);
}

.tech-datatable__tr--selected {
  background-color: var(--primary-light, rgba(59, 130, 246, 0.12));
}

.tech-datatable__td--check, .tech-datatable__th--check {
  width: 40px;
  text-align: center;
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "metric-card",
                    "name": "Metric Stat Card",
                    "description": "KPI summary card extracted from Sales CRM executive dashboard metrics.",
                    "category": "Data Display",
                    "access_level": "premium",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "label", "type": "string", "default": "None", "description": "Metric name."},
                        {"name": "value", "type": "string | number", "default": "None", "description": "Primary display value."},
                        {"name": "trend", "type": "string", "default": "undefined", "description": "Trend percentage e.g. +12%."},
                        {"name": "trendType", "type": "'up' | 'down' | 'neutral'", "default": "'up'", "description": "Visual color of trend."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "label": "Pipeline Value",
                        "value": "$1,420,000",
                        "trend": "+14.2%",
                        "trendType": "up"
                    },
                    "source_files_json": {
                        "MetricCard.tsx": """import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import './MetricCard.css';

export interface MetricCardProps {
  label: string;
  value: string | number;
  trend?: string;
  trendType?: 'up' | 'down' | 'neutral';
  description?: string;
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  trend,
  trendType = 'up',
  description,
  icon,
  className = ''
}) => {
  return (
    <div className={`tech-metric-card ${className}`}>
      <div className="tech-metric-card__header">
        <span className="tech-metric-card__label">{label}</span>
        {icon && <span className="tech-metric-card__icon">{icon}</span>}
      </div>
      <div className="tech-metric-card__body">
        <span className="tech-metric-card__value">{value}</span>
        {trend && (
          <span className={`tech-metric-card__trend tech-metric-card__trend--${trendType}`}>
            {trendType === 'up' && <TrendingUp size={14} />}
            {trendType === 'down' && <TrendingDown size={14} />}
            <span>{trend}</span>
          </span>
        )}
      </div>
      {description && <p className="tech-metric-card__desc">{description}</p>}
    </div>
  );
};""",
                        "MetricCard.css": """.tech-metric-card {
  padding: 16px 20px;
  background-color: var(--bg-card, #131b2e);
  border: 1px solid var(--border-subtle, #1e293b);
  border-radius: var(--radius-lg, 8px);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tech-metric-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tech-metric-card__label {
  font-size: var(--font-xs, 0.75rem);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted, #94a3b8);
}

.tech-metric-card__icon {
  color: var(--primary, #3b82f6);
}

.tech-metric-card__body {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.tech-metric-card__value {
  font-size: var(--font-2xl, 1.5rem);
  font-weight: 700;
  color: var(--text-main, #f8fafc);
  letter-spacing: -0.02em;
}

.tech-metric-card__trend {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-xs, 0.75rem);
  font-weight: 600;
}

.tech-metric-card__trend--up {
  color: var(--success-text, #34d399);
}

.tech-metric-card__trend--down {
  color: var(--danger-text, #f87171);
}

.tech-metric-card__desc {
  font-size: var(--font-xs, 0.75rem);
  color: var(--text-subtle, #64748b);
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "action-menu",
                    "name": "Action Menu Dropdown",
                    "description": "Row-level context menu dropdown component.",
                    "category": "Actions",
                    "access_level": "premium",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "items", "type": "Array<{ id: string; label: string; destructive?: boolean }>", "default": "[]", "description": "Action menu options."},
                        {"name": "onSelect", "type": "(id: string) => void", "default": "None", "description": "Menu selection callback."}
                    ],
                    "dependencies_json": [
                        {"name": "lucide-react", "version": "^0.344.0", "is_dev": False}
                    ],
                    "preview_data_json": {
                        "items": [
                            {"id": "edit", "label": "Edit Company"},
                            {"id": "duplicate", "label": "Duplicate Record"},
                            {"id": "delete", "label": "Delete Company", "destructive": True}
                        ]
                    },
                    "source_files_json": {
                        "ActionMenu.tsx": """import React, { useState, useRef, useEffect } from 'react';
import { MoreHorizontal } from 'lucide-react';
import './ActionMenu.css';

export interface ActionMenuItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  destructive?: boolean;
}

export interface ActionMenuProps {
  items: ActionMenuItem[];
  onSelect: (id: string) => void;
  className?: string;
}

export const ActionMenu: React.FC<ActionMenuProps> = ({ items, onSelect, className = '' }) => {
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`tech-action-menu ${className}`} ref={menuRef}>
      <button
        type="button"
        className="tech-action-menu__trigger"
        onClick={() => setOpen(!open)}
      >
        <MoreHorizontal size={16} />
      </button>

      {open && (
        <div className="tech-action-menu__dropdown">
          {items.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`tech-action-menu__item ${item.destructive ? 'tech-action-menu__item--destructive' : ''}`}
              onClick={() => {
                onSelect(item.id);
                setOpen(false);
              }}
            >
              {item.icon && <span className="tech-action-menu__icon">{item.icon}</span>}
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};""",
                        "ActionMenu.css": """.tech-action-menu {
  position: relative;
  display: inline-block;
}

.tech-action-menu__trigger {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm, 4px);
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  cursor: pointer;
  transition: all var(--transition-fast, 150ms ease-in-out);
}

.tech-action-menu__trigger:hover {
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-main, #f8fafc);
}

.tech-action-menu__dropdown {
  position: absolute;
  right: 0;
  top: calc(100% + 4px);
  min-width: 160px;
  background-color: var(--bg-card, #131b2e);
  border: 1px solid var(--border-medium, #334155);
  border-radius: var(--radius-md, 6px);
  box-shadow: var(--shadow-lg);
  padding: 4px;
  z-index: 60;
}

.tech-action-menu__item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: var(--radius-sm, 4px);
  border: none;
  background: transparent;
  color: var(--text-muted, #94a3b8);
  font-size: var(--font-sm, 0.875rem);
  cursor: pointer;
  text-align: left;
}

.tech-action-menu__item:hover {
  background-color: var(--bg-surface-hover, #1f2937);
  color: var(--text-main, #f8fafc);
}

.tech-action-menu__item--destructive {
  color: var(--danger-text, #f87171);
}

.tech-action-menu__item--destructive:hover {
  background-color: var(--danger-bg, rgba(239, 68, 68, 0.15));
}"""
                    },
                    "published_at": now
                },
                {
                    "slug": "probability",
                    "name": "Probability Indicator",
                    "description": "Progress bar component extracted from CRM deal win probability representation.",
                    "category": "Data Display",
                    "access_level": "premium",
                    "status": "published",
                    "version": "1.0.0",
                    "props_json": [
                        {"name": "value", "type": "number", "default": "0", "description": "Percentage value between 0 and 100."},
                        {"name": "showLabel", "type": "boolean", "default": "true", "description": "Displays percentage text."}
                    ],
                    "dependencies_json": [],
                    "preview_data_json": {
                        "value": 85
                    },
                    "source_files_json": {
                        "Probability.tsx": """import React from 'react';
import './Probability.css';

export interface ProbabilityProps {
  value: number; // 0 to 100
  showLabel?: boolean;
  className?: string;
}

export const Probability: React.FC<ProbabilityProps> = ({ value, showLabel = true, className = '' }) => {
  const safeValue = Math.min(100, Math.max(0, value));

  const getColor = (val: number) => {
    if (val >= 75) return 'var(--success-text, #34d399)';
    if (val >= 40) return 'var(--primary, #3b82f6)';
    return 'var(--warning-text, #fbbf24)';
  };

  return (
    <div className={`tech-probability ${className}`}>
      <div className="tech-probability__bar-bg">
        <div
          className="tech-probability__bar-fill"
          style={{ width: `${safeValue}%`, backgroundColor: getColor(safeValue) }}
        />
      </div>
      {showLabel && <span className="tech-probability__label">{safeValue}%</span>}
    </div>
  );
};""",
                        "Probability.css": """.tech-probability {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.tech-probability__bar-bg {
  flex: 1;
  height: 6px;
  background-color: var(--bg-surface-active, #374151);
  border-radius: var(--radius-full, 9999px);
  overflow: hidden;
}

.tech-probability__bar-fill {
  height: 100%;
  border-radius: var(--radius-full, 9999px);
  transition: width 300ms ease-in-out;
}

.tech-probability__label {
  font-size: var(--font-xs, 0.75rem);
  font-weight: 600;
  color: var(--text-muted, #94a3b8);
  min-width: 32px;
}"""
                    },
                    "published_at": now
                }
            ]

            for comp_dict in components_data:
                comp = Component(**comp_dict)
                db.add(comp)
            db.commit()

        print("Database seeding completed successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
