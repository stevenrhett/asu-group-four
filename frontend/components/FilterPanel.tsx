'use client';

import { useState } from 'react';
import { SearchFilters } from '@/types/job';

interface FilterPanelProps {
  filters: SearchFilters;
  onChange: (filters: Partial<SearchFilters>) => void;
}

export default function FilterPanel({ filters, onChange }: FilterPanelProps) {
  const [salaryMin, setSalaryMin] = useState(filters.salary_min || 0);
  const [salaryMax, setSalaryMax] = useState(filters.salary_max || 300000);
  
  const handleToggle = (key: 'easy_apply' | 'remote_only') => {
    onChange({ [key]: !filters[key] });
  };
  
  const handleSalaryChange = () => {
    // Validate salary range
    if (salaryMin > salaryMax && salaryMax > 0) {
      alert('Minimum salary cannot be greater than maximum salary');
      return;
    }
    onChange({ salary_min: salaryMin, salary_max: salaryMax });
  };
  
  const handleCheckboxGroup = (key: keyof SearchFilters, value: string) => {
    const currentValues = (filters[key] as string[]) || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    
    onChange({ [key]: newValues.length > 0 ? newValues : undefined });
  };
  
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-6">
      <h3 className="text-lg font-semibold text-gray-900">Filter Jobs</h3>
      
      {/* Easy Apply Toggle */}
      <div className="space-y-2">
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={filters.easy_apply || false}
            onChange={() => handleToggle('easy_apply')}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            aria-label="Filter for easy apply jobs only"
          />
          <span className="ml-2 text-sm text-gray-700">Easy Apply only</span>
        </label>
        
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={filters.remote_only || false}
            onChange={() => handleToggle('remote_only')}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            aria-label="Filter for remote jobs only"
          />
          <span className="ml-2 text-sm text-gray-700">Remote only</span>
        </label>
      </div>
      
      {/* Salary Range */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Salary Range</h4>
        <div className="space-y-3">
          <div>
            <label htmlFor="salary-min" className="block text-xs text-gray-600 mb-1">Minimum</label>
            <input
              id="salary-min"
              type="number"
              value={salaryMin}
              onChange={(e) => setSalaryMin(parseInt(e.target.value) || 0)}
              onBlur={handleSalaryChange}
              min="0"
              step="1000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="$0"
              aria-label="Minimum salary"
            />
          </div>
          <div>
            <label htmlFor="salary-max" className="block text-xs text-gray-600 mb-1">Maximum</label>
            <input
              id="salary-max"
              type="number"
              value={salaryMax}
              onChange={(e) => setSalaryMax(parseInt(e.target.value) || 0)}
              onBlur={handleSalaryChange}
              min="0"
              step="1000"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="$300,000"
              aria-label="Maximum salary"
            />
          </div>
          <button
            onClick={handleSalaryChange}
            className="w-full px-3 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 transition-colors"
            aria-label="Apply salary filters"
          >
            Apply
          </button>
        </div>
      </div>
      
      {/* Date Posted */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Date Posted</h4>
        <div className="space-y-2">
          {[
            { value: '24h', label: 'Last 24 hours' },
            { value: '7d', label: 'Last 7 days' },
            { value: '30d', label: 'Last 30 days' },
            { value: 'any', label: 'Any time' },
          ].map((option) => (
            <label key={option.value} className="flex items-center cursor-pointer">
              <input
                type="radio"
                name="posted_within"
                value={option.value}
                checked={filters.posted_within === option.value || (option.value === 'any' && !filters.posted_within)}
                onChange={(e) => onChange({ posted_within: e.target.value as any })}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span className="ml-2 text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>
      
      {/* Work Type */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Work Type</h4>
        <div className="space-y-2">
          {[
            { value: 'remote', label: 'Remote' },
            { value: 'hybrid', label: 'Hybrid' },
            { value: 'onsite', label: 'On-site' },
          ].map((option) => (
            <label key={option.value} className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={(filters.work_types || []).includes(option.value)}
                onChange={() => handleCheckboxGroup('work_types', option.value)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>
      
      {/* Job Type */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Job Type</h4>
        <div className="space-y-2">
          {[
            { value: 'full_time', label: 'Full-time' },
            { value: 'part_time', label: 'Part-time' },
            { value: 'contract', label: 'Contract' },
            { value: 'internship', label: 'Internship' },
          ].map((option) => (
            <label key={option.value} className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={(filters.job_types || []).includes(option.value)}
                onChange={() => handleCheckboxGroup('job_types', option.value)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>
      
      {/* Experience Level */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Experience Level</h4>
        <div className="space-y-2">
          {[
            { value: 'entry', label: 'Entry Level' },
            { value: 'mid', label: 'Mid-Level' },
            { value: 'senior', label: 'Senior' },
            { value: 'lead', label: 'Lead/Principal' },
          ].map((option) => (
            <label key={option.value} className="flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={(filters.experience_levels || []).includes(option.value)}
                onChange={() => handleCheckboxGroup('experience_levels', option.value)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="ml-2 text-sm text-gray-700">{option.label}</span>
            </label>
          ))}
        </div>
      </div>
      
      {/* Company Rating */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-900 mb-3">Company Rating</h4>
        <select
          value={filters.min_rating || ''}
          onChange={(e) => onChange({ min_rating: e.target.value ? parseFloat(e.target.value) : undefined })}
          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Any rating</option>
          <option value="3.0">3.0+ stars</option>
          <option value="3.5">3.5+ stars</option>
          <option value="4.0">4.0+ stars</option>
          <option value="4.5">4.5+ stars</option>
        </select>
      </div>
    </div>
  );
}

