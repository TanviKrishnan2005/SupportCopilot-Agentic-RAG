import {
  Headphones,
  MessageSquare,
  PackageSearch,
  RefreshCcw,
  Sparkles,
} from "lucide-react";

function Sidebar({ onNewConversation, onOrderClick, onRefundClick }) {
  return (
    <aside className="hidden w-[270px] shrink-0 border-r border-white/[0.07] bg-[#0b0c10] lg:flex lg:flex-col">

      {/* Brand */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-black shadow-lg">
          <Sparkles size={18} strokeWidth={2.2} />
        </div>

        <div>
          <div className="text-[15px] font-semibold tracking-tight">
            NovaCart
          </div>

          <div className="text-[11px] text-white/35">
            AI Support
          </div>
        </div>
      </div>

      {/* New conversation */}
      <div className="px-4">
        <button
          onClick={onNewConversation}
          className="flex w-full items-center gap-3 rounded-xl border border-white/[0.08] bg-white/[0.04] px-4 py-3 text-sm font-medium transition hover:bg-white/[0.07]"
        >
          <MessageSquare size={16} />
          New conversation
        </button>
      </div>

      {/* Recent */}
      <div className="mt-8 px-4">
        <div className="mb-3 px-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/25">
          Recent
        </div>

        <button
          onClick={onOrderClick}
          className="group flex w-full items-start gap-3 rounded-xl px-3 py-3 text-left transition hover:bg-white/[0.04]"
        >
          <PackageSearch
            size={16}
            className="mt-0.5 shrink-0 text-white/35"
          />

          <div className="min-w-0">
            <div className="truncate text-sm text-white/70">
              Order ORD1005
            </div>

            <div className="mt-1 truncate text-xs text-white/25">
              Order status
            </div>
          </div>
        </button>

        <button
          onClick={onRefundClick}
          className="group flex w-full items-start gap-3 rounded-xl px-3 py-3 text-left transition hover:bg-white/[0.04]"
        >
          <RefreshCcw
            size={16}
            className="mt-0.5 shrink-0 text-white/35"
          />

          <div className="min-w-0">
            <div className="truncate text-sm text-white/70">
              Refund eligibility
            </div>

            <div className="mt-1 truncate text-xs text-white/25">
              Order ORD1005
            </div>
          </div>
        </button>
      </div>

      {/* Human support */}
      <div className="mt-auto border-t border-white/[0.06] p-4">
        <div className="flex items-center gap-3 rounded-xl bg-white/[0.025] px-3 py-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.06]">
            <Headphones size={15} className="text-white/50" />
          </div>

          <div>
            <div className="text-xs font-medium text-white/60">
              Human support
            </div>

            <div className="mt-0.5 text-[10px] text-white/25">
              Available if you need us
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;