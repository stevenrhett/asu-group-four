'use client';

import { SearchFilters } from '@/types/job';

interface ActiveFiltersProps {
  filters: SearchFilters;
  totalResults: number;
  onRemove: (filterKey: string) => void;
  onClearAll: () => void;
}

export default function ActiveFilters({ filters, totalResults, onRemove, onClearAll }: ActiveFiltersProps) {
  const activeFilters: { key: string; label: string; value: string }[] = [];
  
  // Build list of active filters
  if (filters.q) {
    activeFilters.push({ key: 'q', label: 'Keywords', value: filters.q });
  }
  if (filters.location) {
    activeFilters.push({ key: 'location', label: 'Location', value: filters.location });
  }
  if (filters.remote_only) {
    activeFilters.push({ key: 'remote_only', label: 'Remote Only', value: 'Yes' });
  }
  if (filters.easy_apply) {
    activeFilters.push({ key: 'easy_apply', label: 'Easy Apply', value: 'Yes' });
  }
  if (filters.salary_min || filters.salary_max) {
    const min = filters.salary_min ? `$${(filters.salary_min / 1000).toFixed(0)}k` : '$0';
    const max = filters.salary_max ? `$${(filters.salary_max / 1000).toFixed(0)}k` : '∞';
    activeFilters.push({ key: 'salary', label: 'Salary', value: `${min} - ${max}` });
  }
  if (filters.posted_within) {
    const labels: Record<string, string> = {
      '24h': 'Last 24 hours',
      '7d': 'Last 7 days',
      '30d': 'Last 30 days',
      'any': 'Any time'
    };
    activeFilters.push({ key: 'posted_within', label: 'Posted', value: labels[filters.posted_within] || filters.posted_within });
  }
  if (filters.min_rating) {
    activeFilters.push({ key: 'min_rating', label: 'Rating', value: `${filters.min_rating}+ stars` });
  }
  if (filters.work_types && filters.work_types.length > 0) {
    activeFilters.push({ key: 'work_types', label: 'Work Type', value: filters.work_types.join(', ') });
  }
  if (filters.job_types && filters.job_types.length > 0) {
    activeFilters.push({ key: 'job_types', label: 'Job Type', value: filters.job_types.join(', ') });
  }
  if (filters.experience_levels && filters.experience_levels.length > 0) {
    activeFilters.push({ key: 'experience_levels', label: 'Experience', value: filters.experience_levels.join(', ') });
  }
  if (filters.cities && filters.cities.length > 0) {
    activeFilters.push({ key: 'cities', label: 'Cities', value: filters.cities.join(', ') });
  }
  
  // Don't show if no filters
  if (activeFilters.length === 0) {
    return (
      <div className="mb-6">
        <p className="text-gray-600">
          <span className="font-semibold text-gray-900">{totalResults.toLocaleString()}</span> jobs found
        </p>
      </div>
    );
  }
  
  return (
    <div className="mb-6 bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <p className="text-gray-600">
          <span className="font-semibold text-gray-900">{totalResults.toLocaleString()}</span> jobs matching your filters
        </p>
        <button
          onClick={onClearAll}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          Clear all
        </button>
      </div>
      
      <div className="flex flex-wrap gap-2">
        {activeFilters.map((filter) => (
          <div
            key={filter.key}
            className="inline-flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-full text-sm border border-blue-200"
          >
            <span className="font-medium">{filter.label}:</span>
            <span>{filter.value}</span>
            <button
              onClick={() => onRemove(filter.key)}
              className="ml-1 hover:bg-blue-100 rounded-full p-0.5 transition-colors"
              aria-label={`Remove ${filter.label} filter`}
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

