import { Sparkles } from "lucide-react";
import { formatAssistantResponse } from "../utils/formatResponse";

function ChatMessage({ item }) {
  // USER MESSAGE
  if (item.type === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-white px-4 py-3 text-sm text-black shadow-lg">
          {item.content}
        </div>
      </div>
    );
  }

  // ERROR MESSAGE
  if (item.type === "error") {
    return (
      <div className="rounded-2xl border border-red-400/10 bg-red-400/[0.04] px-4 py-3 text-sm text-red-200/70">
        {item.content}
      </div>
    );
  }

  // AI MESSAGE
  if (item.type === "assistant") {
    const { lines, sources } = formatAssistantResponse(
      item.content
    );

    return (
      <div className="flex items-start gap-3">

        {/* AI ICON */}
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.05]">
          <Sparkles
            size={14}
            className="text-white/70"
          />
        </div>

        <div className="max-w-[82%]">

          {/* AI NAME */}
          <div className="mb-2 text-[10px] uppercase tracking-[0.15em] text-white/25">
            NovaCart AI
          </div>

          {/* ANSWER */}
          <div className="rounded-2xl rounded-tl-md border border-white/[0.08] bg-white/[0.035] px-5 py-4 text-sm leading-6 text-white/75">

            <div className="space-y-2">

              {lines.map((line, lineIndex) => {
                const isBullet =
                  line.startsWith("- ") ||
                  line.startsWith("• ");

                return isBullet ? (
                  <div
                    key={lineIndex}
                    className="flex items-start gap-3"
                  >
                    <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-white/40" />

                    <span>
                      {line.replace(
                        /^[-•]\s*/,
                        ""
                      )}
                    </span>
                  </div>
                ) : (
                  <p key={lineIndex}>
                    {line}
                  </p>
                );
              })}

            </div>

            {/* SOURCES */}
            {sources.length > 0 && (
              <div className="mt-5 border-t border-white/[0.07] pt-4">

                <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-white/25">
                  Sources
                </div>

                <div className="flex flex-wrap gap-2">

                  {sources.map(
                    (source, sourceIndex) => (
                      <span
                        key={sourceIndex}
                        className="rounded-lg border border-white/[0.07] bg-white/[0.035] px-2.5 py-1 text-[10px] text-white/35"
                      >
                        {source}
                      </span>
                    )
                  )}

                </div>
              </div>
            )}

          </div>

          {/* INTENT */}
          {item.intent && (
            <div className="mt-2 inline-flex rounded-full border border-white/[0.06] bg-white/[0.025] px-2.5 py-1 text-[10px] capitalize text-white/25">
              {item.intent.replace("_", " ")}
            </div>
          )}

        </div>
      </div>
    );
  }

  return null;
}

export default ChatMessage;