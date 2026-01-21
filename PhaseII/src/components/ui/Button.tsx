import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  type?: 'button' | 'submit' | 'reset';
  className?: string;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
  className = ''
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-md border';

  const variantClasses = {
    primary: disabled
      ? 'bg-indigo-400 text-white border-transparent cursor-not-allowed'
      : 'bg-indigo-600 text-white border-transparent hover:bg-indigo-700 focus:ring-indigo-500',
    secondary: disabled
      ? 'bg-gray-200 text-gray-500 border-gray-300 cursor-not-allowed'
      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 focus:ring-indigo-500',
    success: disabled
      ? 'bg-green-400 text-white border-transparent cursor-not-allowed'
      : 'bg-green-600 text-white border-transparent hover:bg-green-700 focus:ring-green-500',
    danger: disabled
      ? 'bg-red-400 text-white border-transparent cursor-not-allowed'
      : 'bg-red-600 text-white border-transparent hover:bg-red-700 focus:ring-red-500',
    ghost: disabled
      ? 'text-gray-400 cursor-not-allowed'
      : 'text-gray-600 hover:bg-gray-100 focus:ring-gray-500'
  };

  const sizeClasses = {
    sm: 'text-xs px-2.5 py-1.5',
    md: 'text-sm px-3 py-2',
    lg: 'text-base px-4 py-2'
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`;

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled}
      aria-disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;