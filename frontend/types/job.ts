/**
 * Job-related TypeScript types for the Job Portal
 */

export enum WorkType {
  REMOTE = 'remote',
  HYBRID = 'hybrid',
  ONSITE = 'onsite',
}

export enum JobType {
  FULL_TIME = 'full_time',
  PART_TIME = 'part_time',
  CONTRACT = 'contract',
  INTERNSHIP = 'internship',
}

export enum ExperienceLevel {
  ENTRY = 'entry',
  MID = 'mid',
  SENIOR = 'senior',
  LEAD = 'lead',
}

export enum CompanySize {
  STARTUP = 'startup',
  SMALL = 'small',
  MEDIUM = 'medium',
  LARGE = 'large',
  ENTERPRISE = 'enterprise',
}

export enum JobStatus {
  ACTIVE = 'active',
  ARCHIVED = 'archived',
  DRAFT = 'draft',
}

export interface Job {
  id: string;
  title: string;
  description: string;
  skills: string[];
  employer_id?: string;
  status: JobStatus;
  
  // Location
  location?: string;
  city?: string;
  state?: string;
  country: string;
  
  // Work arrangement
  work_type: WorkType;
  job_type: JobType;
  experience_level: ExperienceLevel;
  easy_apply: boolean;
  
  // Salary
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  
  // Company
  company_name?: string;
  company_rating?: number;
  company_size?: CompanySize;
  industry?: string;
  
  // Timestamps
  posted_at: string;
  created_at: string;
  updated_at: string;
  archived_at?: string;
}

export interface SearchFilters {
  // Keyword search
  q?: string;
  location?: string;
  radius?: number;
  
  // Toggle filters
  easy_apply?: boolean;
  remote_only?: boolean;
  
  // Salary
  salary_min?: number;
  salary_max?: number;
  hide_without_salary?: boolean;
  
  // Date posted
  posted_within?: '24h' | '7d' | '30d' | 'any';
  
  // Company
  min_rating?: number;
  company_sizes?: string[];
  companies?: string[];
  industries?: string[];
  
  // Job details
  work_types?: string[];
  job_types?: string[];
  experience_levels?: string[];
  
  // Location
  cities?: string[];
  states?: string[];
  
  // Skills
  skills?: string[];
  
  // Pagination
  page?: number;
  page_size?: number;
  
  // Sort
  sort_by?: 'relevance' | 'newest' | 'salary';
}

export interface PaginationMetadata {
  page: number;
  page_size: number;
  total_results: number;
  total_pages: number;
  has_more: boolean;
}

export interface FilterCount {
  value: string;
  label: string;
  count: number;
}

export interface FilterOptions {
  work_types: FilterCount[];
  job_types: FilterCount[];
  experience_levels: FilterCount[];
  company_sizes: FilterCount[];
  cities: FilterCount[];
  states: FilterCount[];
  salary_ranges: {
    min: number;
    max: number | null;
    label: string;
  }[];
}

export interface SearchResponse {
  jobs: Job[];
  pagination: PaginationMetadata;
  filters_applied: Record<string, any>;
}

