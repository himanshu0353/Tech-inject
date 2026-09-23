import React from 'react';
import '../../styles/tokens.css';
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
};
