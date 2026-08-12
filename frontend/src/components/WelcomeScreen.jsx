import {
  PackageSearch,
  RefreshCcw,
  Sparkles,
  Ticket,
} from "lucide-react";

import SuggestionCard from "./SuggestionCard";

function WelcomeScreen({ onSuggestionClick, loading }) {
  const suggestions = [
    {
      icon: PackageSearch,
      title: "Track my order",
      description: "Check the status of an order",
      prompt: "Where is my order?",
    },
    {
      icon: RefreshCcw,
      title: "Refund eligibility",
      description: "Check if an order can be refunded",
      prompt: "Can I get a refund?",
    },
    {
      icon: Ticket,
      title: "Report an issue",
      description: "Get help with a damaged order",
      prompt: "I want to report an issue",
    },
  ];

  return (
    <div className="mx-auto flex min-h-full w-full max-w-4xl flex-col items-center justify-center px-5 pb-8 pt-10">

      {/* AI Icon */}
      <div className="mb-7 flex h-14 w-14 items-center justify-center rounded-2xl border border-white/[0.1] bg-white/[0.045] shadow-2xl">
        <Sparkles
          size={25}
          strokeWidth={1.7}
          className="text-white/80"
        />
      </div>

      {/* Heading */}
      <div className="text-center">
        <p className="mb-3 text-xs font-medium uppercase tracking-[0.22em] text-white/25">
          NovaCart Intelligence
        </p>

        <h1 className="text-3xl font-semibold tracking-[-0.04em] text-white sm:text-4xl">
          How can we help?
        </h1>

        <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-white/35">
          Ask about an order, refunds, delivery, returns,
          or anything else you need help with.
        </p>
      </div>

      {/* Suggestion Cards */}
      <div className="mt-10 grid w-full max-w-3xl gap-3 sm:grid-cols-3">
        {suggestions.map((suggestion) => (
          <SuggestionCard
            key={suggestion.title}
            icon={suggestion.icon}
            title={suggestion.title}
            description={suggestion.description}
            disabled={loading}
            onClick={() =>
              onSuggestionClick(suggestion.prompt)
            }
          />
        ))}
      </div>
    </div>
  );
}

export default WelcomeScreen;