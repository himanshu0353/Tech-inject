import React from 'react';
import '../../styles/tokens.css';
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
};
