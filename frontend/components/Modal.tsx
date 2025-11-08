import React from 'react';
import { Button } from './Button';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
  confirmVariant?: 'primary' | 'danger' | 'success';
  isLoading?: boolean;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  onConfirm,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmVariant = 'primary',
  isLoading = false,
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="modal-overlay"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        className="modal-content"
        style={{
          backgroundColor: 'white',
          borderRadius: 'var(--radius-lg)',
          padding: 'var(--space-6)',
          maxWidth: '500px',
          width: '90%',
          maxHeight: '90vh',
          overflow: 'auto',
          boxShadow: 'var(--shadow-2xl)',
        }}
      >
        <div
          className="modal-header"
          style={{
            marginBottom: 'var(--space-4)',
            paddingBottom: 'var(--space-4)',
            borderBottom: '1px solid var(--neutral-200)',
          }}
        >
          <h2
            style={{
              margin: 0,
              fontSize: 'var(--text-xl)',
              fontWeight: 'var(--font-semibold)',
              color: 'var(--neutral-900)',
            }}
          >
            {title}
          </h2>
        </div>

        <div
          className="modal-body"
          style={{
            marginBottom: 'var(--space-6)',
            color: 'var(--neutral-700)',
          }}
        >
          {children}
        </div>

        <div
          className="modal-footer"
          style={{
            display: 'flex',
            gap: 'var(--space-3)',
            justifyContent: 'flex-end',
          }}
        >
          <Button
            variant="secondary"
            onClick={onClose}
            disabled={isLoading}
          >
            {cancelText}
          </Button>
          {onConfirm && (
            <Button
              variant={confirmVariant}
              onClick={onConfirm}
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : confirmText}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};


