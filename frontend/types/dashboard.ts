export type RecommendationExplanation = {
  label: string;
  weight: number;
  source: string;
};

export type Recommendation = {
  job_id: string;
  title: string;
  location: string | null;
  score: number;
  bm25_score: number;
  vector_score: number;
  skills: string[];
  snippet: string | null;
  explanations: RecommendationExplanation[];
};

export type UserRole = "seeker" | "employer";

export type InboxItem = {
  id: string;
  job_title: string;
  candidate_email: string | null;
  status: string;
  updated_at: string;
};

export type InboxCounts = Record<"applied" | "viewed" | "shortlisted" | "interview" | "rejected", number>;

export const INBOX_STATUSES = ["all", "applied", "viewed", "shortlisted", "interview", "rejected"] as const;

export type InboxStatusWithAll = (typeof INBOX_STATUSES)[number];

export type InboxStatus = Exclude<InboxStatusWithAll, "all">;
