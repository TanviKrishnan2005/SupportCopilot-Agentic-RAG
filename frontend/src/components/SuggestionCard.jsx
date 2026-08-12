function SuggestionCard({
  icon: Icon,
  title,
  description,
  onClick,
  disabled = false,
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="group rounded-2xl border border-white/[0.08] bg-white/[0.025] p-4 text-left transition duration-200 hover:-translate-y-0.5 hover:border-white/[0.14] hover:bg-white/[0.045] disabled:cursor-not-allowed disabled:opacity-50"
    >
      <div className="mb-7 flex h-9 w-9 items-center justify-center rounded-xl bg-white/[0.06] text-white/55 transition group-hover:bg-white/[0.1] group-hover:text-white">
        <Icon size={17} />
      </div>

      <div className="text-sm font-medium text-white/75">
        {title}
      </div>

      <div className="mt-1 text-xs leading-5 text-white/25">
        {description}
      </div>
    </button>
  );
}

export default SuggestionCard;