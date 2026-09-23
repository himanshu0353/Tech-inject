import React, { useState, useRef, useEffect } from 'react';
import { MoreHorizontal } from 'lucide-react';
import '../../styles/tokens.css';
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
};
