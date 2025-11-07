import { RecommendationExplanation } from "../types/dashboard";

type RecommendationExplanationChipsProps = {
  explanations: RecommendationExplanation[];
  maxChips?: number;
};

const SOURCE_STYLE_MAP: Record<string, { background: string; color: string }> = {
  skill: { background: "#dcfce7", color: "#166534" },
  title: { background: "#ede9fe", color: "#5b21b6" },
  vector: { background: "#fee2e2", color: "#991b1b" },
  token: { background: "#e0f2fe", color: "#0c4a6e" },
};

export const getExplanationStyles = (source: string) =>
  SOURCE_STYLE_MAP[source] ?? { background: "#f3f4f6", color: "#111827" };

const RecommendationExplanationChips = ({ explanations, maxChips = 6 }: RecommendationExplanationChipsProps) => {
  if (!explanations.length) {
    return null;
  }

  return (
    <div
      data-testid="explanation-chips"
      style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}
    >
      {explanations.slice(0, maxChips).map((explanation, index) => {
        const styles = getExplanationStyles(explanation.source);
        return (
          <span
            key={`${explanation.label}-${index}`}
            style={{
              padding: "4px 8px",
              borderRadius: 999,
              fontSize: 12,
              background: styles.background,
              color: styles.color,
              whiteSpace: "nowrap",
            }}
          >
            {explanation.label} ({explanation.source}: {explanation.weight.toFixed(2)})
          </span>
        );
      })}
    </div>
  );
};

export default RecommendationExplanationChips;
