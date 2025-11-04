import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import EmployerInbox from "../components/EmployerInbox";
import { InboxCounts, InboxItem, InboxStatusWithAll } from "../types/dashboard";

const formatDate = (value: string | null) => (value ? `Formatted ${value}` : "–");

const baseCounts: InboxCounts = {
  applied: 2,
  viewed: 1,
  shortlisted: 0,
  interview: 0,
  rejected: 0,
};

const baseItems: InboxItem[] = [
  {
    id: "app-1",
    job_title: "Backend Engineer",
    candidate_email: "candidate@example.com",
    status: "applied",
    updated_at: "2025-01-01T00:00:00.000Z",
  },
];

describe("EmployerInbox", () => {
  it("renders counts and notifies when filter buttons are clicked", async () => {
    const user = userEvent.setup();
    const handleSelectStatus = jest.fn();

    render(
      <EmployerInbox
        activeStatus={"all"}
        counts={baseCounts}
        items={baseItems}
        isLoading={false}
        onSelectStatus={handleSelectStatus}
        onUpdateStatus={jest.fn()}
        formatDate={formatDate}
      />
    );

    const shortlistedButton = screen.getByRole("button", { name: /Shortlisted/i });
    await user.click(shortlistedButton);

    expect(handleSelectStatus).toHaveBeenCalledWith("shortlisted");
  });

  it("allows status updates from the select control", async () => {
    const user = userEvent.setup();
    const handleUpdateStatus = jest.fn();

    render(
      <EmployerInbox
        activeStatus={"all"}
        counts={baseCounts}
        items={baseItems}
        isLoading={false}
        onSelectStatus={jest.fn()}
        onUpdateStatus={handleUpdateStatus}
        formatDate={formatDate}
      />
    );

    const select = screen.getByLabelText(/candidate@example.com/i);
    await user.selectOptions(select, "shortlisted");

    expect(handleUpdateStatus).toHaveBeenCalledWith("app-1", "shortlisted");
  });

  it("renders loading and empty states", () => {
    const { rerender } = render(
      <EmployerInbox
        activeStatus={"all"}
        counts={baseCounts}
        items={[]}
        isLoading={true}
        onSelectStatus={jest.fn()}
        onUpdateStatus={jest.fn()}
        formatDate={formatDate}
      />
    );

    expect(screen.getByText(/Loading inbox…/i)).toBeInTheDocument();

    rerender(
      <EmployerInbox
        activeStatus={"all"}
        counts={{ applied: 0, viewed: 0, shortlisted: 0, interview: 0, rejected: 0 }}
        items={[]}
        isLoading={false}
        onSelectStatus={jest.fn()}
        onUpdateStatus={jest.fn()}
        formatDate={formatDate}
      />
    );

    expect(screen.getByTestId("inbox-empty")).toBeInTheDocument();
  });
});
