import { Sparkles } from "lucide-react";

function TopBar({ isConversationStarted }) {
  return (
    <header className="flex h-[68px] shrink-0 items-center justify-between border-b border-white/[0.07] px-5 sm:px-8">

      {/* Mobile brand */}
      <div className="flex items-center gap-3 lg:hidden">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-black">
          <Sparkles size={15} />
        </div>

        <span className="text-sm font-semibold">
          NovaCart AI
        </span>
      </div>

      {/* Breadcrumb */}
      <div className="hidden items-center gap-2 text-xs text-white/35 lg:flex">
        <span>Support</span>

        <span className="text-white/15">/</span>

        <span className="text-white/60">
          {isConversationStarted
            ? "Conversation"
            : "New conversation"}
        </span>
      </div>

      {/* Status */}
      <div className="ml-auto flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-full border border-white/[0.07] bg-white/[0.025] px-3 py-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.7)]" />

          <span className="text-[11px] text-white/45">
            AI online
          </span>
        </div>
      </div>
    </header>
  );
}

export default TopBar;