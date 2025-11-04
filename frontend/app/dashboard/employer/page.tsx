'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { employerAPI, jobsAPI } from '@/lib/api'

export default function EmployerDashboard() {
  const router = useRouter()
  const [profile, setProfile] = useState<any>(null)
  const [jobs, setJobs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profileRes, jobsRes] = await Promise.all([
          employerAPI.getProfile(),
          jobsAPI.getMyJobs(),
        ])
        setProfile(profileRes.data)
        setJobs(jobsRes.data)
      } catch (error) {
        console.error('Failed to fetch data:', error)
        router.push('/auth/login')
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
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
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
              <Link href="/dashboard/employer" className="text-gray-700 hover:text-primary-600">
                Dashboard
              </Link>
              <Link href="/dashboard/employer/jobs/new" className="btn-primary">
                Post a Job
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
            Welcome, {profile?.company_name || 'Employer'}!
          </h2>
          <p className="text-gray-600 mt-2">Manage your job postings and review applicants</p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Active Jobs</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">
              {jobs.filter((j: any) => j.status === 'active').length}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Total Applications</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">
              {jobs.reduce((sum: number, j: any) => sum + (j.applications_count || 0), 0)}
            </p>
          </div>
          <div className="card">
            <h3 className="text-sm font-medium text-gray-500">Total Views</h3>
            <p className="text-3xl font-bold text-primary-600 mt-2">
              {jobs.reduce((sum: number, j: any) => sum + (j.views_count || 0), 0)}
            </p>
          </div>
        </div>

        {/* Job Postings */}
        <div className="card">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold">Your Job Postings</h3>
            <Link href="/dashboard/employer/jobs/new" className="btn-primary">
              + New Job
            </Link>
          </div>

          {jobs.length > 0 ? (
            <div className="space-y-4">
              {jobs.map((job: any) => (
                <div key={job._id} className="border rounded-lg p-4 hover:border-primary-300">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="font-semibold text-lg">{job.title}</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {job.location?.city} • {job.job_type}
                      </p>
                      <div className="flex space-x-4 mt-2 text-sm">
                        <span className="text-gray-600">
                          📊 {job.applications_count || 0} applications
                        </span>
                        <span className="text-gray-600">
                          👁️ {job.views_count || 0} views
                        </span>
                        <span className={`font-medium ${job.status === 'active' ? 'text-green-600' : 'text-gray-600'}`}>
                          {job.status}
                        </span>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Link href={`/jobs/${job._id}`} className="text-primary-600 hover:underline text-sm">
                        View
                      </Link>
                      <Link href={`/dashboard/employer/jobs/${job._id}/edit`} className="text-primary-600 hover:underline text-sm">
                        Edit
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600 mb-4">You haven't posted any jobs yet.</p>
              <Link href="/dashboard/employer/jobs/new" className="btn-primary">
                Post Your First Job
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
