'use client';

import { Job } from '@/types/job';

interface JobCardProps {
  job: Job;
  onClick?: () => void;
}

export default function JobCard({ job, onClick }: JobCardProps) {
  // Format salary
  const formatSalary = () => {
    if (!job.salary_min && !job.salary_max) return null;
    
    const format = (amount: number) => {
      if (amount >= 1000) {
        return `$${(amount / 1000).toFixed(0)}k`;
      }
      return `$${amount.toLocaleString()}`;
    };
    
    if (job.salary_min && job.salary_max) {
      return `${format(job.salary_min)} - ${format(job.salary_max)}`;
    } else if (job.salary_min) {
      return `${format(job.salary_min)}+`;
    } else if (job.salary_max) {
      return `Up to ${format(job.salary_max)}`;
    }
    return null;
  };
  
  // Format posted date
  const formatPostedDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 24) {
      return `${diffInHours} hours ago`;
    } else if (diffInHours < 48) {
      return '1 day ago';
    } else if (diffInHours < 168) {
      return `${Math.floor(diffInHours / 24)} days ago`;
    } else if (diffInHours < 720) {
      return `${Math.floor(diffInHours / 168)} weeks ago`;
    } else {
      return `${Math.floor(diffInHours / 720)} months ago`;
    }
  };
  
  // Format work type
  const formatWorkType = (workType: string) => {
    const types: Record<string, string> = {
      remote: 'Remote',
      hybrid: 'Hybrid',
      onsite: 'On-site'
    };
    return types[workType] || workType;
  };
  
  // Get work type color
  const getWorkTypeBadgeColor = (workType: string) => {
    const colors: Record<string, string> = {
      remote: 'bg-green-100 text-green-800 border-green-200',
      hybrid: 'bg-blue-100 text-blue-800 border-blue-200',
      onsite: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[workType] || 'bg-gray-100 text-gray-800 border-gray-200';
  };
  
  const salary = formatSalary();
  
  return (
    <div
      className="bg-white border border-gray-200 rounded-lg p-5 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1 hover:text-blue-600">
            {job.title}
          </h3>
          <div className="flex items-center gap-2 text-sm text-gray-600">
            {job.company_name && (
              <span className="font-medium">{job.company_name}</span>
            )}
            {job.company_rating && (
              <div className="flex items-center gap-1">
                <svg className="h-4 w-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
                  <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                </svg>
                <span>{job.company_rating.toFixed(1)}</span>
              </div>
            )}
          </div>
        </div>
        
        {job.easy_apply && (
          <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-medium rounded border border-blue-200">
            Easy Apply
          </span>
        )}
      </div>
      
      {/* Location and Work Type */}
      <div className="flex items-center gap-3 mb-3 text-sm">
        {job.location && (
          <div className="flex items-center gap-1 text-gray-600">
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{job.location}</span>
          </div>
        )}
        
        <span className={`px-2 py-0.5 text-xs font-medium rounded border ${getWorkTypeBadgeColor(job.work_type)}`}>
          {formatWorkType(job.work_type)}
        </span>
      </div>
      
      {/* Salary */}
      {salary && (
        <div className="mb-3 text-sm">
          <span className="font-medium text-gray-900">{salary}</span>
          <span className="text-gray-600"> / year</span>
        </div>
      )}
      
      {/* Skills */}
      {job.skills && job.skills.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {job.skills.slice(0, 5).map((skill, idx) => (
            <span
              key={idx}
              className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded border border-gray-200"
            >
              {skill}
            </span>
          ))}
          {job.skills.length > 5 && (
            <span className="px-2 py-1 text-gray-500 text-xs">
              +{job.skills.length - 5} more
            </span>
          )}
        </div>
      )}
      
      {/* Footer */}
      <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
        <span>{formatPostedDate(job.posted_at)}</span>
        {job.industry && <span>{job.industry}</span>}
      </div>
    </div>
  );
}

