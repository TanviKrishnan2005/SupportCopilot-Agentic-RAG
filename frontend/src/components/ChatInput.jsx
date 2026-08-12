import { ArrowUp, ShieldCheck } from "lucide-react";

function ChatInput({
  message,
  loading,
  onChange,
  onKeyDown,
  onSend,
}) {
  return (
    <div className="relative mx-auto w-full max-w-3xl px-5 pb-5 sm:px-6">

      <div className="rounded-2xl border border-white/[0.1] bg-[#101116]/95 p-2 shadow-2xl shadow-black/30 backdrop-blur-xl">

        <div className="flex items-end gap-2">

          <textarea
            value={message}
            onChange={onChange}
            onKeyDown={onKeyDown}
            rows={1}
            placeholder="Ask NovaCart anything..."
            disabled={loading}
            className="max-h-32 min-h-[44px] flex-1 resize-none overflow-y-auto bg-transparent px-3 py-3 text-sm text-white outline-none placeholder:text-white/20 disabled:cursor-not-allowed disabled:opacity-50"
          />

          <button
            onClick={onSend}
            disabled={!message.trim() || loading}
            aria-label="Send message"
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:bg-white/[0.08] disabled:text-white/20"
          >
            <ArrowUp
              size={17}
              strokeWidth={2.2}
            />
          </button>

        </div>

        <div className="flex items-center justify-between px-3 pb-1 pt-1">

          <div className="flex items-center gap-2 text-[10px] text-white/20">
            <ShieldCheck size={12} />
            Your support conversation is secure
          </div>

          <div className="hidden text-[10px] text-white/15 sm:block">
            Enter to send · Shift + Enter for new line
          </div>

        </div>
      </div>

      <p className="mt-3 text-center text-[10px] text-white/15">
        NovaCart AI can make mistakes. Check important order details.
      </p>

    </div>
  );
}

export default ChatInput;