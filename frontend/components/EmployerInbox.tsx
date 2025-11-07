import { INBOX_STATUSES, InboxCounts, InboxItem, InboxStatus, InboxStatusWithAll } from "../types/dashboard";
import { Alert } from "./Alert";
import { Badge } from "./Badge";
import { Card, CardHeader, CardTitle, CardBody } from "./Card";

type EmployerInboxProps = {
  activeStatus: InboxStatusWithAll;
  counts: InboxCounts;
  items: InboxItem[];
  isLoading: boolean;
  error?: string | null;
  onSelectStatus: (status: InboxStatusWithAll) => void;
  onUpdateStatus: (applicationId: string, status: InboxStatus) => void;
  formatDate: (value: string | null) => string;
};

const formatStatusLabel = (value: string) =>
  `${value.charAt(0).toUpperCase()}${value.slice(1)}`;

const getTotalCount = (counts: InboxCounts) =>
  Object.values(counts).reduce((total, value) => total + value, 0);

const getStatusBadgeVariant = (status: InboxStatus): "primary" | "success" | "warning" | "error" | "neutral" => {
  switch (status) {
    case "interview": return "success";
    case "shortlisted": return "primary";
    case "rejected": return "error";
    case "viewed": return "warning";
    case "applied": return "neutral";
    default: return "neutral";
  }
};

const EmployerInbox = ({
  activeStatus,
  counts,
  items,
  isLoading,
  error,
  onSelectStatus,
  onUpdateStatus,
  formatDate,
}: EmployerInboxProps) => {
  const totalCount = getTotalCount(counts);

  return (
    <div style={{ display: "grid", gap: "var(--space-6)" }}>
      {error && <Alert variant="error">{error}</Alert>}

      <Card glassmorphic>
        <CardHeader>
          <CardTitle>Candidate Inbox</CardTitle>
        </CardHeader>
        <CardBody>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "var(--space-2)", marginBottom: "var(--space-6)" }}>
            {INBOX_STATUSES.map((status) => {
              const isActive = activeStatus === status;
              const count = status === "all" ? totalCount : counts[status as InboxStatus] ?? 0;
              return (
                <button
                  key={status}
                  type="button"
                  onClick={() => onSelectStatus(status)}
                  disabled={isLoading}
                  style={{
                    padding: "var(--space-2) var(--space-4)",
                    borderRadius: "var(--radius-full)",
                    border: `1px solid ${isActive ? 'var(--primary-500)' : 'var(--neutral-300)'}`,
                    background: isActive ? "var(--primary-600)" : "white",
                    color: isActive ? "white" : "var(--neutral-900)",
                    cursor: isLoading ? "not-allowed" : "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: "var(--space-2)",
                    fontWeight: "var(--font-medium)",
                    fontSize: "var(--text-sm)",
                    transition: "var(--transition-all)",
                  }}
                >
                  <span>{status === "all" ? "All" : formatStatusLabel(status)}</span>
                  <span
                    style={{
                      background: isActive ? "rgba(255,255,255,0.2)" : "var(--neutral-200)",
                      color: isActive ? "white" : "var(--neutral-900)",
                      borderRadius: "var(--radius-full)",
                      padding: "0 var(--space-2)",
                      fontSize: "var(--text-xs)",
                      minWidth: "24px",
                      textAlign: "center",
                    }}
                  >
                    {count}
                  </span>
                </button>
              );
            })}
          </div>

          {isLoading && (
            <div style={{ display: "flex", alignItems: "center", gap: "var(--space-2)", color: "var(--neutral-500)" }}>
              <span className="spinner" />
              <span>Loading inbox…</span>
            </div>
          )}

          {!isLoading && items.length === 0 && (
            <p style={{ color: "var(--neutral-500)", textAlign: "center", padding: "var(--space-8)" }} data-testid="inbox-empty">
              No applications in this filter yet. Encourage seekers to apply!
            </p>
          )}

          {!isLoading && items.length > 0 && (
            <ul style={{ listStyle: "none", paddingLeft: 0, display: "grid", gap: "var(--space-3)" }}>
              {items.map((item) => (
                <li key={item.id}>
                  <Card>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--space-3)" }}>
                      <div>
                        <h3 style={{ fontSize: "var(--text-lg)", fontWeight: "var(--font-semibold)", color: "var(--neutral-900)", margin: 0 }}>
                          {item.job_title}
                        </h3>
                        <p style={{ margin: "var(--space-1) 0 0", color: "var(--neutral-600)", fontSize: "var(--text-sm)" }}>
                          {item.candidate_email ?? "Unknown candidate"}
                        </p>
                      </div>
                      <Badge variant={getStatusBadgeVariant(item.status as InboxStatus)}>
                        {formatStatusLabel(item.status)}
                      </Badge>
                    </div>
                    <p style={{ margin: "0 0 var(--space-3)", color: "var(--neutral-500)", fontSize: "var(--text-sm)" }}>
                      Updated {formatDate(item.updated_at)}
                    </p>
                    <div className="form-group" style={{ marginBottom: 0 }}>
                      <label style={{ fontSize: "var(--text-sm)", fontWeight: "var(--font-medium)", color: "var(--neutral-700)", marginBottom: "var(--space-2)", display: "block" }}>
                        Update Status
                      </label>
                      <select
                        aria-label={`Update status for ${item.candidate_email ?? item.id}`}
                        value={item.status}
                        onChange={(event) => onUpdateStatus(item.id, event.target.value as InboxStatus)}
                        disabled={isLoading}
                        className="form-select"
                      >
                        {INBOX_STATUSES.filter((statusOption) => statusOption !== "all").map((statusOption) => (
                          <option key={statusOption} value={statusOption}>
                            {formatStatusLabel(statusOption)}
                          </option>
                        ))}
                      </select>
                    </div>
                  </Card>
                </li>
              ))}
            </ul>
          )}
        </CardBody>
      </Card>
    </div>
  );
};

export default EmployerInbox;
