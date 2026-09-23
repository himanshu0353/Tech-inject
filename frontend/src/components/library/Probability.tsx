import React from 'react';
import '../../styles/tokens.css';
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
};
