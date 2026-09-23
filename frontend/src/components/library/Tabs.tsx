import React from 'react';
import '../../styles/tokens.css';
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
};
