import { Sparkles } from "lucide-react";

function LoadingMessage() {
  return (
    <div className="flex items-start gap-3">

      {/* AI ICON */}
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.05]">
        <Sparkles
          size={14}
          className="animate-pulse text-white/70"
        />
      </div>

      {/* LOADING DOTS */}
      <div className="rounded-2xl rounded-tl-md border border-white/[0.08] bg-white/[0.035] px-5 py-4">

        <div className="flex items-center gap-1.5">

          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/40 [animation-delay:-0.3s]" />

          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/40 [animation-delay:-0.15s]" />

          <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-white/40" />

        </div>

      </div>
    </div>
  );
}

export default LoadingMessage;