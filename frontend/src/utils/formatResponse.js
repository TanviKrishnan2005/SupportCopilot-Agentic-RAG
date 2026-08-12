export function formatAssistantResponse(content) {
  const parts = content.split(/\n\s*Sources:\s*/i);

  const answer = parts[0].trim();
  const sourcesText = parts[1] || "";

  const lines = answer
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const sources = sourcesText
    .split("\n")
    .map((line) => line.replace(/^[-•]\s*/, "").trim())
    .filter(Boolean);

  return {
    lines,
    sources,
  };
}