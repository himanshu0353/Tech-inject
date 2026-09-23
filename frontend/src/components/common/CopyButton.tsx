import React, { useState } from 'react';
import { Copy, Check, AlertCircle } from 'lucide-react';
import './CopyButton.css';

export interface CopyButtonProps {
  textToCopy: string;
  label?: string;
  className?: string;
}

export const CopyButton: React.FC<CopyButtonProps> = ({ textToCopy, label = 'Copy', className = '' }) => {
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setError(false);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setError(true);
      setTimeout(() => setError(false), 3000);
    }
  };

  return (
    <button
      type="button"
      className={`tech-copy-btn ${copied ? 'tech-copy-btn--copied' : ''} ${error ? 'tech-copy-btn--error' : ''} ${className}`}
      onClick={handleCopy}
    >
      {copied ? (
        <>
          <Check size={14} />
          <span>Copied!</span>
        </>
      ) : error ? (
        <>
          <AlertCircle size={14} />
          <span>Unable to copy</span>
        </>
      ) : (
        <>
          <Copy size={14} />
          <span>{label}</span>
        </>
      )}
    </button>
  );
};
