import React, { useState } from 'react';
import '../../styles/tokens.css';
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
};
