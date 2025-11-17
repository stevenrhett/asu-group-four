"use client";

import { useState, useEffect, FormEvent, ChangeEvent } from "react";
import { Card, CardHeader, CardTitle, CardBody } from "../../components/Card";
import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Alert } from "../../components/Alert";
import { Modal } from "../../components/Modal";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ?? "http://localhost:8000/api/v1";

interface UserProfile {
  id: string;
  email: string;
  role: "seeker" | "employer";
  phone: string | null;
  linkedin_url: string | null;
  website_url: string | null;
  is_active: boolean;
  created_at: string;
}

export default function SettingsPage() {
  // Auth state
  const [token, setToken] = useState<string | null>(null);
  const [userRole, setUserRole] = useState<"seeker" | "employer" | null>(null);

  // Profile state
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [phone, setPhone] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [websiteUrl, setWebsiteUrl] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setMessage] = useState<string | null>(null);

  // Modal state
  const [showDeactivateModal, setShowDeactivateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deletePassword, setDeletePassword] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  // Resume upload state (seekers only)
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Load token and profile on mount
  useEffect(() => {
    // In a real app, get token from localStorage or session
    const storedToken = localStorage.getItem("token");
    if (!storedToken) {
      window.location.href = "/";
      return;
    }

    setToken(storedToken);

    // Decode role from token
    try {
      const [, payloadSegment] = storedToken.split(".");
      if (payloadSegment) {
        const normalized = payloadSegment.replace(/-/g, "+").replace(/_/g, "/");
        const decoded = atob(normalized.padEnd(normalized.length + (4 - (normalized.length % 4)) % 4, "="));
        const payload = JSON.parse(decoded);
        setUserRole(payload.role);
      }
    } catch (err) {
      console.error("Failed to decode token", err);
    }

    // Fetch profile
    fetchProfile(storedToken);
  }, []);

  const fetchProfile = async (authToken: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/users/me`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Session expired or invalid token
          localStorage.removeItem("token");
          throw new Error("Your session has expired. Please log in again.");
        }
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || "Failed to load profile");
      }

      const data = await response.json();
      setProfile(data);
      setPhone(data.phone || "");
      setLinkedinUrl(data.linkedin_url || "");
      setWebsiteUrl(data.website_url || "");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to load profile";
      setError(errorMessage);
      
      // If authentication failed, redirect to home after showing error
      if (errorMessage.includes("session has expired")) {
        setTimeout(() => {
          window.location.href = "/";
        }, 2000);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateProfile = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!token) return;

    setIsSaving(true);
    setMessage(null);
    setError(null);

    try {
      const response = await fetch(`${API_BASE}/users/me`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          phone: phone.trim() || null,
          linkedin_url: linkedinUrl.trim() || null,
          website_url: websiteUrl.trim() || null,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail || "Failed to update profile");
      }

      const updated = await response.json();
      setProfile(updated);
      setMessage("Profile updated successfully!");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update profile");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDeactivate = async () => {
    if (!token) return;

    setIsProcessing(true);

    try {
      const response = await fetch(`${API_BASE}/users/me/deactivate`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to deactivate account");
      }

      // Clear session and redirect
      localStorage.removeItem("token");
      window.location.href = "/";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to deactivate account");
      setIsProcessing(false);
      setShowDeactivateModal(false);
    }
  };

  const handleDeletePermanently = async () => {
    if (!token || !deletePassword) return;

    setIsProcessing(true);

    try {
      const response = await fetch(`${API_BASE}/users/me`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ password: deletePassword }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail || "Failed to delete account");
      }

      // Clear session and redirect
      localStorage.removeItem("token");
      window.location.href = "/";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete account");
      setIsProcessing(false);
      setDeletePassword("");
    }
  };

  const handleResumeUpload = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!token || !selectedFile) return;

    setIsUploading(true);
    setUploadMessage(null);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_BASE}/uploads/resume`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail || "Failed to upload resume");
      }

      setUploadMessage("Resume uploaded and parsed successfully!");
      setSelectedFile(null);
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Failed to upload resume");
    } finally {
      setIsUploading(false);
    }
  };

  const getAccountAge = (createdAt: string): string => {
    const created = new Date(createdAt);
    const now = new Date();
    const diffMs = now.getTime() - created.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "1 day";
    if (diffDays < 30) return `${diffDays} days`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months`;
    return `${Math.floor(diffDays / 365)} years`;
  };

  if (loading) {
    return (
      <div className="container" style={{ paddingTop: "var(--space-12)" }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container" style={{ paddingTop: "var(--space-12)" }}>
        {error && <Alert variant="error">{error}</Alert>}
        <p>Failed to load profile</p>
      </div>
    );
  }

  return (
    <div className="container" style={{ paddingTop: "var(--space-12)", paddingBottom: "var(--space-12)" }}>
      {/* Back to Dashboard Button */}
      <div style={{ marginBottom: "var(--space-6)" }}>
        <Button
          variant="secondary"
          onClick={() => {
            window.location.href = "/";
          }}
          style={{ display: "flex", alignItems: "center", gap: "var(--space-2)" }}
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          Back to Dashboard
        </Button>
      </div>

      <h1 style={{ marginBottom: "var(--space-8)", color: "var(--neutral-900)" }}>Account Settings</h1>

      {error && <div style={{ marginBottom: "var(--space-6)" }}><Alert variant="error">{error}</Alert></div>}
      {saveMessage && <div style={{ marginBottom: "var(--space-6)" }}><Alert variant="success">{saveMessage}</Alert></div>}

      {/* Account Info */}
      <Card glassmorphic style={{ marginBottom: "var(--space-6)" }}>
        <CardHeader>
          <CardTitle>Account Information</CardTitle>
        </CardHeader>
        <CardBody>
          <div style={{ display: "grid", gap: "var(--space-4)" }}>
            <div>
              <strong style={{ color: "var(--neutral-900)" }}>Email:</strong>
              <p style={{ margin: 0, color: "var(--neutral-700)" }}>{profile.email}</p>
            </div>
            <div>
              <strong style={{ color: "var(--neutral-900)" }}>Role:</strong>
              <p style={{ margin: 0, color: "var(--neutral-700)", textTransform: "capitalize" }}>
                {profile.role}
              </p>
            </div>
            <div>
              <strong style={{ color: "var(--neutral-900)" }}>Account Age:</strong>
              <p style={{ margin: 0, color: "var(--neutral-700)" }}>
                {getAccountAge(profile.created_at)}
              </p>
            </div>
            <div>
              <strong style={{ color: "var(--neutral-900)" }}>Status:</strong>
              <p style={{ margin: 0, color: profile.is_active ? "var(--success-600)" : "var(--danger-600)" }}>
                {profile.is_active ? "Active" : "Inactive"}
              </p>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Contact Information */}
      <Card glassmorphic style={{ marginBottom: "var(--space-6)" }}>
        <CardHeader>
          <CardTitle>Contact Information</CardTitle>
        </CardHeader>
        <CardBody>
          <form onSubmit={handleUpdateProfile}>
            <Input
              label="Phone Number"
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+1 (555) 123-4567"
              helper="Optional - Your phone number"
            />
            <Input
              label="LinkedIn URL"
              type="url"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/yourprofile"
              helper="Optional - Your LinkedIn profile"
            />
            <Input
              label="Website/Portfolio URL"
              type="url"
              value={websiteUrl}
              onChange={(e) => setWebsiteUrl(e.target.value)}
              placeholder="https://yourwebsite.com"
              helper="Optional - Your personal website or portfolio"
            />
            <Button type="submit" variant="primary" disabled={isSaving} style={{ marginTop: "var(--space-4)" }}>
              {isSaving ? "Saving..." : "Save Changes"}
            </Button>
          </form>
        </CardBody>
      </Card>

      {/* Resume Upload (Seekers Only) */}
      {userRole === "seeker" && (
        <Card glassmorphic style={{ marginBottom: "var(--space-6)" }}>
          <CardHeader>
            <CardTitle>Resume</CardTitle>
          </CardHeader>
          <CardBody>
            {uploadMessage && <div style={{ marginBottom: "var(--space-4)" }}><Alert variant="success">{uploadMessage}</Alert></div>}
            {uploadError && <div style={{ marginBottom: "var(--space-4)" }}><Alert variant="error">{uploadError}</Alert></div>}
            <form onSubmit={handleResumeUpload}>
              <Input
                label="Upload New Resume"
                type="file"
                accept=".pdf,.docx"
                onChange={(e: ChangeEvent<HTMLInputElement>) => setSelectedFile(e.target.files?.[0] || null)}
                helper="Upload a new resume to replace your existing one (PDF or DOCX)"
              />
              <Button
                type="submit"
                variant="primary"
                disabled={!selectedFile || isUploading}
                style={{ marginTop: "var(--space-4)" }}
              >
                {isUploading ? "Uploading..." : "Upload Resume"}
              </Button>
            </form>
          </CardBody>
        </Card>
      )}

      {/* Employer Settings Placeholder */}
      {userRole === "employer" && (
        <Card glassmorphic style={{ marginBottom: "var(--space-6)" }}>
          <CardHeader>
            <CardTitle>Employer Settings</CardTitle>
          </CardHeader>
          <CardBody>
            <p style={{ color: "var(--neutral-600)", margin: 0 }}>
              Additional employer-specific settings will be available here in a future update.
            </p>
          </CardBody>
        </Card>
      )}

      {/* Account Management */}
      <Card glassmorphic>
        <CardHeader>
          <CardTitle>Account Management</CardTitle>
        </CardHeader>
        <CardBody>
          <div style={{ display: "flex", gap: "var(--space-4)", flexDirection: "column" }}>
            <div>
              <h3 style={{ fontSize: "var(--text-lg)", marginBottom: "var(--space-2)" }}>Deactivate Account</h3>
              <p style={{ color: "var(--neutral-600)", marginBottom: "var(--space-4)" }}>
                Temporarily deactivate your account. You can reactivate it by contacting support.
              </p>
              <Button variant="secondary" onClick={() => setShowDeactivateModal(true)}>
                Deactivate Account
              </Button>
            </div>

            <div style={{ paddingTop: "var(--space-6)", borderTop: "1px solid var(--neutral-200)" }}>
              <h3 style={{ fontSize: "var(--text-lg)", marginBottom: "var(--space-2)", color: "var(--danger-700)" }}>
                Delete Account Permanently
              </h3>
              <p style={{ color: "var(--neutral-600)", marginBottom: "var(--space-4)" }}>
                Permanently delete your account and all associated data. This action cannot be undone.
              </p>
              <Button variant="danger" onClick={() => setShowDeleteModal(true)}>
                Delete Account Permanently
              </Button>
            </div>
          </div>
        </CardBody>
      </Card>

      {/* Deactivate Modal */}
      <Modal
        isOpen={showDeactivateModal}
        onClose={() => setShowDeactivateModal(false)}
        title="Deactivate Account"
        onConfirm={handleDeactivate}
        confirmText="Deactivate"
        confirmVariant="secondary"
        isLoading={isProcessing}
      >
        <p>Are you sure you want to deactivate your account?</p>
        <p style={{ marginTop: "var(--space-4)" }}>
          Your account will be temporarily disabled. You can reactivate it by contacting support.
        </p>
      </Modal>

      {/* Delete Permanently Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => {
          setShowDeleteModal(false);
          setDeletePassword("");
        }}
        title="Delete Account Permanently"
        onConfirm={handleDeletePermanently}
        confirmText="Delete Forever"
        confirmVariant="danger"
        isLoading={isProcessing}
      >
        <p style={{ color: "var(--danger-700)", fontWeight: "var(--font-semibold)" }}>
          ⚠️ This action cannot be undone!
        </p>
        <p style={{ marginTop: "var(--space-4)" }}>
          All your personal data, applications, and resume will be permanently deleted.
        </p>
        <Input
          label="Confirm Password"
          type="password"
          value={deletePassword}
          onChange={(e) => setDeletePassword(e.target.value)}
          placeholder="Enter your password to confirm"
          required
          helper="For security, please enter your password"
        />
      </Modal>
    </div>
  );
}

