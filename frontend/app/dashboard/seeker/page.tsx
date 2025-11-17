'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { seekerAPI, jobsAPI, applicationsAPI } from '@/lib/api'

export default function SeekerDashboard() {
  const router = useRouter()
  const [profile, setProfile] = useState<any>(null)
  const [jobs, setJobs] = useState<any[]>([])
  const [applications, setApplications] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setError(null)
        const [profileRes, jobsRes, appsRes] = await Promise.all([
          seekerAPI.getProfile(),
          jobsAPI.search({ limit: 5 }),
          applicationsAPI.getMyApplications(),
        ])

        if (profileRes?.data) {
          setProfile(profileRes.data)
        }
        if (jobsRes?.data) {
          setJobs(Array.isArray(jobsRes.data) ? jobsRes.data : [])
        }
        if (appsRes?.data) {
          setApplications(Array.isArray(appsRes.data) ? appsRes.data : [])
        }
      } catch (error: any) {
        console.error('Failed to fetch data:', error)
        const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load dashboard data'
        setError(errorMessage)

        // Only redirect if it's an authentication error
        if (error?.response?.status === 401) {
          router.push('/auth/login')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
          <div className="text-center">
            <svg
              className="mx-auto h-12 w-12 text-red-500 mb-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Unable to Load Dashboard</h3>
            <p className="text-gray-600 mb-6">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">JobPortal</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/dashboard/seeker" className="text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
              <Link href="/jobs" className="text-gray-700 hover:text-primary-600">
                Browse Jobs
              </Link>
              <button onClick={handleLogout} className="btn-secondary">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">
            Welcome back, {profile?.first_name || 'Job Seeker'}!
          </h2>
          <p className="text-gray-600 mt-2">Here's what's happening with your job search</p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Applications</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">{applications.length}</p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Profile Complete</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">
              {profile?.resume ? '100%' : '50%'}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">New Matches</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">{jobs.length}</p>
          </div>
        </div>

        {/* Recent Applications */}
        <div className="card mb-8">
          <h3 className="text-xl font-semibold mb-4">Recent Applications</h3>
          {applications.length > 0 ? (
            <div className="space-y-4">
              {applications.slice(0, 5).map((app: any) => (
                <div key={app._id} className="flex justify-between items-center border-b pb-4">
                  <div>
                    <p className="font-medium">Application #{app._id.slice(-6)}</p>
                    <p className="text-sm text-gray-600">
                      Status: <span className="font-medium">{app.status}</span>
                    </p>
                  </div>
                  <Link href={`/applications/${app._id}`} className="text-primary-600 hover:underline">
                    View
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No applications yet. Start applying to jobs!</p>
          )}
        </div>

        {/* Recommended Jobs */}
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">Recommended Jobs</h3>
          {jobs.length > 0 ? (
            <div className="space-y-4">
              {jobs.map((job: any) => (
                <div key={job._id} className="border-b pb-4 last:border-0">
                  <h4 className="font-semibold text-lg">{job.title}</h4>
                  <p className="text-gray-600 text-sm mt-1">{job.location?.city}</p>
                  <p className="text-gray-700 mt-2 line-clamp-2">{job.description}</p>
                  <Link href={`/jobs/${job._id}`} className="text-primary-600 hover:underline text-sm mt-2 inline-block">
                    View Details →
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">No job recommendations yet. Complete your profile to get matches!</p>
          )}
        </div>
      </div>
    </div>
  )
}
