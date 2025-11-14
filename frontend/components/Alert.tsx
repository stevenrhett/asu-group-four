import React from 'react';

type AlertVariant = 'success' | 'error' | 'info' | 'warning';

interface AlertProps {
  children: React.ReactNode;
  variant?: AlertVariant;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  children,
  variant = 'info',
  className = '',
}) => {
  const variantClass = `alert-${variant}`;
  const classes = ['alert', variantClass, className].filter(Boolean).join(' ');

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  return (
    <div className={classes}>
      <span style={{ fontSize: '1.25em' }}>{icons[variant]}</span>
      <div style={{ flex: 1 }}>{children}</div>
    </div>
  );
};
