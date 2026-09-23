import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import '../../styles/tokens.css';
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
};
