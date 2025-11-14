import React from 'react';

type BadgeVariant = 'primary' | 'success' | 'warning' | 'error' | 'neutral';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  className = '',
}) => {
  const variantClass = `badge-${variant}`;
  const classes = ['badge', variantClass, className].filter(Boolean).join(' ');

  return <span className={classes}>{children}</span>;
};
