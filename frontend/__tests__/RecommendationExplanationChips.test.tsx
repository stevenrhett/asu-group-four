import { render, screen } from "@testing-library/react";

import RecommendationExplanationChips, {
  getExplanationStyles,
} from "../components/RecommendationExplanationChips";
import { RecommendationExplanation } from "../types/dashboard";

describe("RecommendationExplanationChips", () => {
  const explanations: RecommendationExplanation[] = [
    { label: "python", weight: 0.9, source: "skill" },
    { label: "backend engineer", weight: 0.8, source: "title" },
    { label: "semantic match", weight: 0.7, source: "vector" },
    { label: "api", weight: 0.6, source: "token" },
  ];

  it("renders explanation chips with formatted labels and weights", () => {
    render(<RecommendationExplanationChips explanations={explanations} />);

    const chips = screen.getAllByText(/\(/);
    expect(chips).toHaveLength(explanations.length);
    expect(chips[0]).toHaveTextContent("python (skill: 0.90)");
    expect(chips[1]).toHaveTextContent("backend engineer (title: 0.80)");
  });

  it("limits chips when maxChips is provided", () => {
    render(<RecommendationExplanationChips explanations={explanations} maxChips={2} />);
    const chips = screen.getAllByText(/\(/);
    expect(chips).toHaveLength(2);
  });

  it("returns default styles for unknown sources", () => {
    const styles = getExplanationStyles("unknown");
    expect(styles.background).toBe("#f3f4f6");
    expect(styles.color).toBe("#111827");
  });
});
