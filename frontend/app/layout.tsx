import './globals.css';

export const metadata = {
  title: 'Job Portal - Connect Talent with Opportunity',
  description: 'AI-powered job matching platform connecting seekers and employers efficiently',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
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
          </div>
        </nav>
        <main className="container" style={{ paddingTop: 'var(--space-8)', paddingBottom: 'var(--space-8)' }}>
          {children}
        </main>
      </body>
    </html>
  );
}

