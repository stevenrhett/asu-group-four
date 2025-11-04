export const metadata = {
  title: 'Job Portal',
  description: 'Connect seekers and employers fast',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav style={{ padding: 12, borderBottom: '1px solid #eee' }}>
          <strong>Job Portal</strong>
        </nav>
        <main style={{ padding: 16 }}>{children}</main>
      </body>
    </html>
  );
}

