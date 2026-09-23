import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import '../../styles/tokens.css';
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
};
