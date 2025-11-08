"use client";

import { useState } from 'react';
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <html lang="en">
      <head>
        <title>Job Portal - Connect Talent with Opportunity</title>
        <meta name="description" content="AI-powered job matching platform connecting seekers and employers efficiently" />
      </head>
      <body>
        <nav className="nav">
          <div className="nav-container">
            <a href="/" className="nav-brand">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 7H4C2.9 7 2 7.9 2 9V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V9C22 7.9 21.1 7 20 7Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M16 21V5C16 4.46957 15.7893 3.96086 15.4142 3.58579C15.0391 3.21071 14.5304 3 14 3H10C9.46957 3 8.96086 3.21071 8.58579 3.58579C8.21071 3.96086 8 4.46957 8 5V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Job Portal
            </a>
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="hamburger-btn"
              aria-label="Toggle menu"
              style={{
                marginLeft: "auto",
                background: menuOpen ? "var(--neutral-100)" : "transparent",
                border: "none",
                cursor: "pointer",
                padding: "var(--space-2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: menuOpen ? "var(--primary-600)" : "var(--neutral-700)",
                transition: "all 0.2s ease",
                borderRadius: "var(--radius-md)"
              }}
              onMouseEnter={(e) => {
                if (!menuOpen) {
                  e.currentTarget.style.background = "var(--neutral-100)";
                  e.currentTarget.style.color = "var(--primary-600)";
                }
              }}
              onMouseLeave={(e) => {
                if (!menuOpen) {
                  e.currentTarget.style.background = "transparent";
                  e.currentTarget.style.color = "var(--neutral-700)";
                }
              }}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </nav>

        {/* Hamburger Menu Dropdown */}
        {menuOpen && (
          <>
            {/* Backdrop */}
            <div
              onClick={() => setMenuOpen(false)}
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: "rgba(0, 0, 0, 0.3)",
                zIndex: 999,
              }}
            />
            {/* Menu Panel */}
            <div
              style={{
                position: "fixed",
                top: "64px",
                right: "var(--space-4)",
                background: "var(--glass-bg)",
                backdropFilter: "blur(20px)",
                WebkitBackdropFilter: "blur(20px)",
                border: "1px solid var(--neutral-200)",
                borderRadius: "var(--radius-lg)",
                boxShadow: "var(--shadow-xl)",
                zIndex: 1000,
                minWidth: "200px",
                overflow: "hidden"
              }}
            >
              <div style={{ display: "flex", flexDirection: "column" }}>
                <a
                  href="/"
                  onClick={() => setMenuOpen(false)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "var(--space-3)",
                    padding: "var(--space-4)",
                    color: "var(--neutral-700)",
                    textDecoration: "none",
                    fontSize: "var(--text-base)",
                    fontWeight: "var(--font-medium)",
                    transition: "background 0.2s ease, color 0.2s ease",
                    borderBottom: "1px solid var(--neutral-200)"
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "var(--neutral-50)";
                    e.currentTarget.style.color = "var(--primary-600)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "transparent";
                    e.currentTarget.style.color = "var(--neutral-700)";
                  }}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <polyline points="9 22 9 12 15 12 15 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Dashboard
                </a>
                <a
                  href="/settings"
                  onClick={() => setMenuOpen(false)}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "var(--space-3)",
                    padding: "var(--space-4)",
                    color: "var(--neutral-700)",
                    textDecoration: "none",
                    fontSize: "var(--text-base)",
                    fontWeight: "var(--font-medium)",
                    transition: "background 0.2s ease, color 0.2s ease"
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = "var(--neutral-50)";
                    e.currentTarget.style.color = "var(--primary-600)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = "transparent";
                    e.currentTarget.style.color = "var(--neutral-700)";
                  }}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 1v6m0 6v6m8.66-15L17 7.5M7 16.5l-3.66 3.66M23 12h-6m-6 0H1m20.66 8.66L17 16.5M7 7.5l-3.66-3.66" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Account Settings
                </a>
              </div>
            </div>
          </>
        )}

        <main className="container" style={{ paddingTop: 'var(--space-8)', paddingBottom: 'var(--space-8)' }}>
          {children}
        </main>
      </body>
    </html>
  );
}

