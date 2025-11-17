import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">JobPortal</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/auth/login" className="text-gray-700 hover:text-primary-600">
                Login
              </Link>
              <Link href="/auth/register" className="btn-primary">
                Sign Up
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Find Your Dream Job with AI
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Intelligent matching between job seekers and employers
            </p>
            <div className="flex justify-center space-x-4">
              <Link href="/auth/register?role=job_seeker" className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
                I'm Looking for a Job
              </Link>
              <Link href="/auth/register?role=employer" className="bg-primary-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-900 transition border-2 border-white">
                I'm Hiring
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose JobPortal?</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="card text-center">
            <h3 className="text-xl font-semibold mb-2">AI-Powered Matching</h3>
            <p className="text-gray-600">
              Advanced algorithms match candidates with the perfect opportunities
            </p>
          </div>
          <div className="card text-center">
            <h3 className="text-xl font-semibold mb-2">Quick & Easy</h3>
            <p className="text-gray-600">
              Apply to jobs or review candidates with just a few clicks
            </p>
          </div>
          <div className="card text-center">
            <h3 className="text-xl font-semibold mb-2">Real-time Updates</h3>
            <p className="text-gray-600">
              Track application status and get instant notifications
            </p>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600">10K+</div>
              <div className="text-gray-600 mt-2">Active Jobs</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">50K+</div>
              <div className="text-gray-600 mt-2">Job Seekers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">5K+</div>
              <div className="text-gray-600 mt-2">Companies</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600">95%</div>
              <div className="text-gray-600 mt-2">Success Rate</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p>&copy; 2024 JobPortal. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
