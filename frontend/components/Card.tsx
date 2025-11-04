import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  glassmorphic?: boolean;
  hover?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  glassmorphic = false,
  hover = true,
  ...props
}) => {
  const baseClass = glassmorphic ? 'glass-card' : 'card';
  const hoverClass = hover && !glassmorphic ? '' : '';
  const classes = [baseClass, hoverClass, className].filter(Boolean).join(' ');

  return <div className={classes} {...props}>{children}</div>;
};

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ children, className = '', ...props }) => {
  return <div className={`card-header ${className}`} {...props}>{children}</div>;
};

interface CardTitleProps extends React.HTMLAttributes<HTMLHeadingElement> {
  children: React.ReactNode;
  className?: string;
}

export const CardTitle: React.FC<CardTitleProps> = ({ children, className = '', ...props }) => {
  return <h2 className={`card-title ${className}`} {...props}>{children}</h2>;
};

interface CardBodyProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

export const CardBody: React.FC<CardBodyProps> = ({ children, className = '', ...props }) => {
  return <div className={`card-body ${className}`} {...props}>{children}</div>;
};
