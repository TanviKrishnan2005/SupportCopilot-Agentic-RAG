import { useEffect, useRef, useState } from "react";

import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import LoadingMessage from "./components/LoadingMessage";
import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import WelcomeScreen from "./components/WelcomeScreen";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Automatically scroll to the newest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // Send message to FastAPI backend
  const sendMessage = async (text = message) => {
    const question = text.trim();

    if (!question || loading) return;

    // Add user message immediately
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        content: question,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response
      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          content: data.response,
          intent: data.intent,
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          type: "error",
          content:
            "I couldn't connect to NovaCart AI right now. Please make sure the backend is running and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Enter = send
  // Shift + Enter = new line
  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  // Auto-growing textarea
  const handleInputChange = (event) => {
    setMessage(event.target.value);

    event.target.style.height = "auto";

    event.target.style.height = `${Math.min(
      event.target.scrollHeight,
      128
    )}px`;
  };

  // Start a new conversation
  const startNewConversation = () => {
    setMessages([]);
    setMessage("");
  };

  const isConversationStarted = messages.length > 0;

  return (
    <div className="min-h-screen bg-[#08090c] text-white">
      <div className="flex h-screen overflow-hidden">

        {/* SIDEBAR */}
        <Sidebar
          onNewConversation={startNewConversation}
          onOrderClick={() =>
            sendMessage("Where is my order ORD1005?")
          }
          onRefundClick={() =>
            sendMessage("Can I get a refund for ORD1005?")
          }
        />

        {/* MAIN */}
        <main className="flex min-w-0 flex-1 flex-col">

          {/* TOP BAR */}
          <TopBar
            isConversationStarted={isConversationStarted}
          />

          {/* CHAT AREA */}
          <section className="relative flex flex-1 flex-col overflow-hidden">

            {/* Background glow */}
            <div className="pointer-events-none absolute left-1/2 top-[18%] h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-white/[0.025] blur-[100px]" />

            {/* CHAT CONTENT */}
            <div className="relative flex-1 overflow-y-auto">

              {/* WELCOME SCREEN */}
              {!isConversationStarted ? (
                <WelcomeScreen
                  onSuggestionClick={sendMessage}
                  loading={loading}
                />
              ) : (

                /* CONVERSATION */
                <div className="relative mx-auto w-full max-w-3xl px-5 py-8 sm:px-6">

                  <div className="space-y-6">

                    {/* MESSAGES */}
                    {messages.map((item, index) => (
                      <div
                        key={index}
                        className="animate-[fadeIn_0.25s_ease-out]"
                      >
                        <ChatMessage item={item} />
                      </div>
                    ))}

                    {/* LOADING */}
                    {loading && <LoadingMessage />}

                    {/* AUTO-SCROLL TARGET */}
                    <div ref={messagesEndRef} />

                  </div>
                </div>
              )}
            </div>

            {/* CHAT INPUT */}
            <ChatInput
              message={message}
              loading={loading}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onSend={() => sendMessage()}
            />

          </section>
        </main>
      </div>

      {/* MESSAGE ANIMATION */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(6px);
          }

          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}

export default App;