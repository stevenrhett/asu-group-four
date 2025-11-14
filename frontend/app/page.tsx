"use client";

import { ChangeEvent, FormEvent, useEffect, useMemo, useState } from "react";

import EmployerInbox from "../components/EmployerInbox";
import RecommendationExplanationChips from "../components/RecommendationExplanationChips";
import { AuthForm } from "../components/AuthForm";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { Alert } from "../components/Alert";
import { Card, CardHeader, CardTitle, CardBody } from "../components/Card";
import { Badge } from "../components/Badge";
import {
  INBOX_STATUSES,
  InboxCounts,
  InboxItem,
  InboxStatus,
  InboxStatusWithAll,
  Recommendation,
  UserRole,
} from "../types/dashboard";

type Profile = {
  id: string;
  user_id: string;
  skills: string[];
  titles: string[];
  raw_text: string | null;
  parsed_at: string | null;
};

type AuthMode = "login" | "register";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000/api/v1";
const MAX_FILE_SIZE_MB = Number(process.env.NEXT_PUBLIC_MAX_RESUME_MB ?? "5");
const ACCEPTED_EXTENSIONS = (process.env.NEXT_PUBLIC_RESUME_EXTENSIONS ?? ".pdf,.docx")
  .split(",")
  .map((ext) => ext.trim().toLowerCase())
  .filter(Boolean);

const EXTENSION_MIME_MAP: Record<string, string> = {
  ".pdf": "application/pdf",
  ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
};

const formatDate = (value: string | null) => {
  if (!value) return "–";
  try {
    return new Date(value).toLocaleString();
  } catch {
    return value;
  }
};

const decodeRoleFromToken = (jwt: string): UserRole | null => {
  try {
    const [, payloadSegment] = jwt.split(".");
    if (!payloadSegment) return null;
    const normalized = payloadSegment.replace(/-/g, "+").replace(/_/g, "/");
    const decoded = atob(normalized.padEnd(normalized.length + (4 - (normalized.length % 4)) % 4, "="));
    const payload = JSON.parse(decoded);
    return payload.role === "employer" ? "employer" : payload.role === "seeker" ? "seeker" : null;
  } catch (error) {
    console.warn("Unable to decode token", error);
    return null;
  }
};

export default function HomePage() {
  const [mode, setMode] = useState<AuthMode>("register");
  const [registerRole, setRegisterRole] = useState<UserRole>("seeker");
  const [userRole, setUserRole] = useState<UserRole | null>(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [authMessage, setAuthMessage] = useState<string | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);
  const [isRestoringSession, setIsRestoringSession] = useState(true);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const [profile, setProfile] = useState<Profile | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [recommendationError, setRecommendationError] = useState<string | null>(null);
  const [isFetchingRecommendations, setIsFetchingRecommendations] = useState(false);
  const [inboxItems, setInboxItems] = useState<InboxItem[]>([]);
  const [inboxCounts, setInboxCounts] = useState<InboxCounts>({
    applied: 0,
    viewed: 0,
    shortlisted: 0,
    interview: 0,
    rejected: 0,
  });
  const [inboxStatus, setInboxStatus] = useState<InboxStatusWithAll>("all");
  const [isLoadingInbox, setIsLoadingInbox] = useState(false);
  const [inboxError, setInboxError] = useState<string | null>(null);

  const isSeeker = userRole === "seeker";
  const isEmployer = userRole === "employer";

  // Restore session from localStorage on mount
  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      const decodedRole = decodeRoleFromToken(storedToken);
      setToken(storedToken);
      setUserRole(decodedRole);
      
      // Try to restore email from token
      try {
        const [, payloadSegment] = storedToken.split(".");
        if (payloadSegment) {
          const normalized = payloadSegment.replace(/-/g, "+").replace(/_/g, "/");
          const decoded = atob(normalized.padEnd(normalized.length + (4 - (normalized.length % 4)) % 4, "="));
          const payload = JSON.parse(decoded);
          if (payload.sub) {
            setEmail(payload.sub);
          }
        }
      } catch (err) {
        console.warn("Could not extract email from token", err);
      }
    }
    setIsRestoringSession(false);
  }, []);

  const acceptAttribute = useMemo(() => {
    const mimeList = ACCEPTED_EXTENSIONS.map((ext) => EXTENSION_MIME_MAP[ext] ?? ext).join(",");
    const extensionsList = ACCEPTED_EXTENSIONS.join(",");
    return [mimeList, extensionsList].filter(Boolean).join(",");
  }, []);

  const resetUploadState = () => {
    setUploadMessage(null);
    setUploadError(null);
    setFileError(null);
  };

  const fetchInbox = async (
    statusParam: InboxStatusWithAll = inboxStatus,
    overrideToken?: string,
    overrideRole?: UserRole | null,
  ) => {
    const authToken = overrideToken ?? token;
    const role = overrideRole ?? userRole;
    if (!authToken) {
      setInboxError("Log in as an employer to view the inbox.");
      return;
    }
    if (role !== "employer") {
      setInboxError("Employer access required for the smart inbox.");
      return;
    }

    setInboxError(null);
    setIsLoadingInbox(true);
    try {
      const response = await fetch(`${API_BASE}/inbox/applications?status=${statusParam}`, {
        method: "GET",
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Unable to load inbox.");
      }
      const payload = await response.json();
      const counts = payload.counts ?? {};
      setInboxStatus(statusParam);
      setInboxCounts({
        applied: counts.applied ?? 0,
        viewed: counts.viewed ?? 0,
        shortlisted: counts.shortlisted ?? 0,
        interview: counts.interview ?? 0,
        rejected: counts.rejected ?? 0,
      });
      setInboxItems(payload.items ?? []);
    } catch (error) {
      setInboxError(error instanceof Error ? error.message : "Unable to load inbox.");
    } finally {
      setIsLoadingInbox(false);
    }
  };

  const updateInboxStatus = async (applicationId: string, nextStatus: InboxStatus) => {
    if (!token || userRole !== "employer") {
      setInboxError("Employer authentication required to update applications.");
      return;
    }
    try {
      const response = await fetch(`${API_BASE}/inbox/applications/${applicationId}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: nextStatus }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Unable to update status.");
      }
      await fetchInbox(inboxStatus);
    } catch (error) {
      setInboxError(error instanceof Error ? error.message : "Unable to update status.");
    }
  };

  const handleAuthSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setAuthMessage(null);
    setAuthError(null);

    const trimmedEmail = email.trim().toLowerCase();
    if (!trimmedEmail || !password) {
      setAuthError("Enter both email and password.");
      return;
    }

    try {
      if (mode === "register") {
        const registerResponse = await fetch(`${API_BASE}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: trimmedEmail, password, role: registerRole }),
        });
        if (!registerResponse.ok) {
          const body = await registerResponse.json().catch(() => null);
          throw new Error(body?.detail ?? "Unable to register. Try logging in.");
        }
        setAuthMessage("Registration successful. Logging you in…");
      }

      const loginResponse = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: trimmedEmail,
          password,
        }).toString(),
      });

      if (!loginResponse.ok) {
        const body = await loginResponse.json().catch(() => null);
        throw new Error(body?.detail ?? "Login failed. Check credentials.");
      }

      const payload = (await loginResponse.json()) as { access_token: string };
      
      // Save token to localStorage for persistence
      localStorage.setItem("token", payload.access_token);
      
      setToken(payload.access_token);
      const decodedRole = decodeRoleFromToken(payload.access_token);
      setUserRole(decodedRole);
      setAuthMessage(mode === "register" ? "Registered and logged in!" : "Logged in successfully.");
      
      if (decodedRole === "seeker") {
        setRecommendations([]);
        setRecommendationError(null);
        setProfile(null);
        setInboxItems([]);
        // Auto-fetch recommendations if user has a profile
        setTimeout(() => fetchRecommendations(), 500);
      } else if (decodedRole === "employer") {
        setProfile(null);
        setRecommendations([]);
        await fetchInbox("all", payload.access_token, decodedRole);
      } else {
        setAuthMessage("Logged in. Role not recognized; limited features available.");
      }
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : "Unexpected auth error.");
      setToken(null);
      setUserRole(null);
    }
  };

  const validateFile = (file: File) => {
    const extension = `.${file.name.split(".").pop()?.toLowerCase() ?? ""}`;
    if (!ACCEPTED_EXTENSIONS.includes(extension)) {
      throw new Error(
        `Unsupported file type. Allowed: ${ACCEPTED_EXTENSIONS.join(", ")}.`,
      );
    }

    const maxBytes = MAX_FILE_SIZE_MB * 1024 * 1024;
    if (file.size > maxBytes) {
      throw new Error(`File too large. Max size is ${MAX_FILE_SIZE_MB} MB.`);
    }
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    resetUploadState();
    const file = event.target.files?.[0];
    if (!file) {
      setSelectedFile(null);
      return;
    }
    try {
      validateFile(file);
      setSelectedFile(file);
    } catch (error) {
      setSelectedFile(null);
      setFileError(error instanceof Error ? error.message : "Invalid file.");
    }
  };

  const fetchRecommendations = async () => {
    if (userRole !== "seeker") {
      setRecommendationError("Log in as a seeker to request recommendations.");
      return;
    }
    if (!token) {
      setRecommendationError("Log in to request recommendations.");
      return;
    }
    setRecommendationError(null);
    setIsFetchingRecommendations(true);
    try {
      const response = await fetch(`${API_BASE}/recommendations`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Unable to retrieve recommendations.");
      }
      const payload = (await response.json()) as { results: Recommendation[] };
      setRecommendations(payload.results);
      if (!payload.results.length) {
        setRecommendationError("No recommendations available yet. Try refining your profile or query.");
      }
    } catch (error) {
      setRecommendationError(error instanceof Error ? error.message : "Unable to fetch recommendations.");
    } finally {
      setIsFetchingRecommendations(false);
    }
  };

  const handleUpload = async () => {
    resetUploadState();
    if (!token) {
      setUploadError("You must be logged in as a seeker to upload a resume.");
      return;
    }
    if (userRole !== "seeker") {
      setUploadError("Resume uploads are only available to seeker accounts.");
      return;
    }
    if (!selectedFile) {
      setUploadError("Choose a resume before uploading.");
      return;
    }
    try {
      validateFile(selectedFile);
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : "Invalid file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    setIsUploading(true);
    try {
      const response = await fetch(`${API_BASE}/uploads/resume`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });
      if (!response.ok) {
        const body = await response.json().catch(() => null);
        throw new Error(body?.detail ?? "Upload failed.");
      }
      const payload = (await response.json()) as Profile;
      setProfile(payload);
      setUploadMessage("Resume processed! Review the parsed skills and titles below.");
      setSelectedFile(null);
      await fetchRecommendations();
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  };

  // Show loading while restoring session
  if (isRestoringSession) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", minHeight: "50vh" }}>
        <p style={{ color: "var(--neutral-600)" }}>Loading...</p>
      </div>
    );
  }

  // Not authenticated - show auth form
  if (!token) {
    return (
      <AuthForm
        mode={mode}
        email={email}
        password={password}
        registerRole={registerRole}
        authMessage={authMessage}
        authError={authError}
        onModeChange={setMode}
        onEmailChange={setEmail}
        onPasswordChange={setPassword}
        onRegisterRoleChange={setRegisterRole}
        onSubmit={handleAuthSubmit}
      />
    );
  }

  return (
    <div style={{ display: "grid", gap: "var(--space-8)" }}>
      {/* User Info Header */}
      <Card glassmorphic>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h2 style={{ margin: 0, fontSize: "var(--text-xl)", fontWeight: "var(--font-semibold)", color: "var(--neutral-900)" }}>
              Welcome, {email}
            </h2>
            <div style={{ display: "flex", gap: "var(--space-2)", marginTop: "var(--space-2)" }}>
              <Badge variant="primary">{userRole}</Badge>
              <Badge variant="success">Authenticated</Badge>
            </div>
          </div>
          <Button
            variant="secondary"
            onClick={() => {
              setToken(null);
              setUserRole(null);
              setProfile(null);
              setRecommendations([]);
              setInboxItems([]);
              localStorage.removeItem("token");
            }}
          >
            Sign Out
          </Button>
        </div>
      </Card>

      {/* Resume Upload Section - Seeker Only */}
      {isSeeker && (
        <Card glassmorphic>
          <CardHeader>
            <CardTitle>Resume Upload</CardTitle>
            <p style={{ color: "var(--neutral-600)", fontSize: "var(--text-sm)", margin: "var(--space-2) 0 0" }}>
              Accepted formats: {ACCEPTED_EXTENSIONS.join(", ")} (max {MAX_FILE_SIZE_MB} MB)
            </p>
          </CardHeader>
          <CardBody>
            {uploadMessage && <Alert variant="success">{uploadMessage}</Alert>}
            {uploadError && <Alert variant="error">{uploadError}</Alert>}
            
            <div style={{ display: "grid", gap: "var(--space-4)" }}>
              <div className="form-group">
                <input
                  type="file"
                  accept={acceptAttribute}
                  onChange={handleFileChange}
                  className="form-input"
                  style={{ padding: "var(--space-2) 0" }}
                />
                {selectedFile && (
                  <span className="form-helper">
                    Selected: <strong>{selectedFile.name}</strong> ({(selectedFile.size / 1024).toFixed(0)} KB)
                  </span>
                )}
                {fileError && <span className="form-error">{fileError}</span>}
              </div>

              <div style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap" }}>
                <Button
                  variant="primary"
                  onClick={handleUpload}
                  disabled={isUploading || !selectedFile}
                  isLoading={isUploading}
                >
                  {isUploading ? "Uploading…" : "Upload & Parse"}
                </Button>
                <Button
                  variant="secondary"
                  onClick={fetchRecommendations}
                  disabled={isFetchingRecommendations}
                  isLoading={isFetchingRecommendations}
                >
                  {isFetchingRecommendations ? "Fetching…" : "Get Recommendations"}
                </Button>
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Profile Preview - Seeker Only */}
      {isSeeker && (
        <Card glassmorphic>
          <CardHeader>
            <CardTitle>Parsed Profile Preview</CardTitle>
          </CardHeader>
          <CardBody>
            {!profile && (
              <p style={{ color: "var(--neutral-500)", textAlign: "center", padding: "var(--space-8)" }}>
                Upload a resume to see parsed data.
              </p>
            )}
            {profile && (
              <div style={{ display: "grid", gap: "var(--space-4)" }}>
                <div>
                  <strong style={{ color: "var(--neutral-700)", fontSize: "var(--text-sm)" }}>Last Parsed:</strong>
                  <span style={{ marginLeft: "var(--space-2)", color: "var(--neutral-600)" }}>
                    {formatDate(profile.parsed_at)}
                  </span>
                </div>

                <div>
                  <strong style={{ color: "var(--neutral-700)", fontSize: "var(--text-sm)" }}>
                    Skills ({profile.skills.length}):
                  </strong>
                  {profile.skills.length ? (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-2)", marginTop: "var(--space-2)" }}>
                      {profile.skills.map((skill) => (
                        <Badge key={skill} variant="primary">{skill}</Badge>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "var(--neutral-500)", margin: "var(--space-1) 0 0" }}>No skills detected.</p>
                  )}
                </div>

                <div>
                  <strong style={{ color: "var(--neutral-700)", fontSize: "var(--text-sm)" }}>
                    Titles ({profile.titles.length}):
                  </strong>
                  {profile.titles.length ? (
                    <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-2)", marginTop: "var(--space-2)" }}>
                      {profile.titles.map((title) => (
                        <Badge key={title} variant="neutral">{title}</Badge>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: "var(--neutral-500)", margin: "var(--space-1) 0 0" }}>No titles detected.</p>
                  )}
                </div>

                {profile.raw_text && (
                  <details className="card" style={{ background: "var(--neutral-50)", padding: "var(--space-3)" }}>
                    <summary style={{ cursor: "pointer", fontWeight: "var(--font-semibold)", color: "var(--neutral-700)" }}>
                      View raw extracted text
                    </summary>
                    <p style={{ whiteSpace: "pre-wrap", marginTop: "var(--space-3)", color: "var(--neutral-600)", fontSize: "var(--text-sm)" }}>
                      {profile.raw_text}
                    </p>
                  </details>
                )}
              </div>
            )}
          </CardBody>
        </Card>
      )}

      {/* Recommendations - Seeker Only */}
      {isSeeker && (
        <Card glassmorphic>
          <CardHeader>
            <CardTitle>Recommended Jobs</CardTitle>
          </CardHeader>
          <CardBody>
            {recommendationError && <Alert variant="error">{recommendationError}</Alert>}
            {!recommendationError && !recommendations.length && (
              <p style={{ color: "var(--neutral-500)", textAlign: "center", padding: "var(--space-8)" }}>
                No recommendations yet. Upload a resume or adjust your profile details to personalize results.
              </p>
            )}
            {recommendations.length > 0 && (
              <ul style={{ display: "grid", gap: "var(--space-4)", paddingLeft: 0, listStyle: "none" }}>
                {recommendations.map((item) => (
                  <li key={item.job_id}>
                    <Card hover>
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--space-3)" }}>
                        <h3 style={{ margin: 0, fontSize: "var(--text-xl)", fontWeight: "var(--font-semibold)", color: "var(--neutral-900)" }}>
                          {item.title}
                        </h3>
                        <Badge variant="primary">
                          Score {item.score.toFixed(3)}
                        </Badge>
                      </div>
                      {item.location && (
                        <p style={{ margin: "0 0 var(--space-2)", color: "var(--neutral-600)", fontSize: "var(--text-sm)" }}>
                          📍 {item.location}
                        </p>
                      )}
                      <p style={{ margin: "0 0 var(--space-3)", color: "var(--neutral-500)", fontSize: "var(--text-sm)" }}>
                        BM25 {item.bm25_score.toFixed(3)} • Vector {item.vector_score.toFixed(3)}
                      </p>
                      {item.snippet && (
                        <p style={{ margin: "0 0 var(--space-3)", color: "var(--neutral-700)" }}>
                          {item.snippet}
                        </p>
                      )}
                      <RecommendationExplanationChips explanations={item.explanations} />
                      {item.skills.length > 0 && (
                        <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-2)", marginTop: "var(--space-3)" }}>
                          {item.skills.map((skill) => (
                            <Badge key={skill} variant="primary">{skill}</Badge>
                          ))}
                        </div>
                      )}
                    </Card>
                  </li>
                ))}
              </ul>
            )}
          </CardBody>
        </Card>
      )}

      {/* Employer Inbox - Employer Only */}
      {isEmployer && (
        <EmployerInbox
          activeStatus={inboxStatus}
          counts={inboxCounts}
          items={inboxItems}
          isLoading={isLoadingInbox}
          error={inboxError}
          onSelectStatus={(status) => fetchInbox(status)}
          onUpdateStatus={updateInboxStatus}
          formatDate={formatDate}
        />
      )}
    </div>
  );
}
