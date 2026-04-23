"use client";

import { useState, useEffect, useRef } from "react";

export default function ChatPage() {
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // 🔐 Check login
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) window.location.href = "/login";
  }, []);

  // 🔄 Auto scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🚪 Logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  // 💬 Send message
  const sendMessage = async () => {
    if (!msg) return;

    const userMessage = { role: "user", text: msg };
    setMessages((prev) => [...prev, userMessage]);
    setMsg("");

    try {
      const token = localStorage.getItem("token");

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/chat/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ message: userMessage.text }),
        }
      );

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.response || "No response ❌" },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ Server error" },
      ]);
    }
  };

  return (
    <div style={styles.container}>
      
      {/* Header */}
      <div style={styles.header}>
        <h2>🤖 Medical AI Assistant</h2>
        <button onClick={handleLogout} style={styles.logout}>
          Logout
        </button>
      </div>

      {/* Chat */}
      <div style={styles.chatBox}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={m.role === "user" ? styles.userMessage : styles.aiMessage}
          >
            {m.role === "ai" ? (
              <div style={styles.aiCard}>
                
                <div style={styles.aiHeader}>🩺 AI Assistant</div>

                {/* Response */}
                <div style={styles.section}>
                  <div style={styles.label}>💬 Response</div>
                  <div style={styles.text}>
                    {m.text.split("Risk:")[0]}
                  </div>
                </div>

                {/* Risk */}
                {m.text.includes("Risk:") && (
                  <div style={styles.section}>
                    <div style={styles.label}>📊 Risk Level</div>
                    <div
                      style={{
                        ...styles.risk,
                        color:
                          m.text.includes("HIGH")
                            ? "#ef4444"
                            : m.text.includes("MEDIUM")
                            ? "#f59e0b"
                            : "#22c55e",
                      }}
                    >
                      {m.text.split("Risk:")[1]?.split("Advice:")[0]}
                    </div>
                  </div>
                )}

                {/* Advice */}
                {m.text.includes("Advice:") && (
                  <div style={styles.section}>
                    <div style={styles.label}>🧠 Advice</div>
                    <div style={styles.text}>
                      {m.text.split("Advice:")[1]}
                    </div>
                  </div>
                )}

              </div>
            ) : (
              m.text
            )}
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div style={styles.inputBox}>
        <input
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          placeholder="Type your symptoms..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles: any = {
  container: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    background: "#0f172a",
    color: "#fff",
  },

  header: {
    padding: "15px 20px",
    borderBottom: "1px solid #1e293b",
    display: "flex",
    justifyContent: "space-between",
  },

  logout: {
    background: "#ef4444",
    border: "none",
    padding: "6px 12px",
    borderRadius: 6,
    color: "#fff",
  },

  chatBox: {
    flex: 1,
    padding: 20,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },

  userMessage: {
    alignSelf: "flex-end",
    background: "#2563eb",
    padding: "10px 14px",
    borderRadius: 12,
    maxWidth: "70%",
  },

  aiMessage: {
    alignSelf: "flex-start",
    maxWidth: "75%",
  },

  aiCard: {
    background: "linear-gradient(135deg, #1e293b, #0f172a)",
    padding: 15,
    borderRadius: 12,
    boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
  },

  aiHeader: {
    fontWeight: "bold",
    marginBottom: 10,
    color: "#38bdf8",
  },

  section: {
    marginBottom: 10,
  },

  label: {
    fontSize: 12,
    color: "#94a3b8",
  },

  text: {
    fontSize: 14,
    lineHeight: 1.5,
  },

  risk: {
    fontWeight: "bold",
    fontSize: 15,
  },

  inputBox: {
    display: "flex",
    padding: 15,
    borderTop: "1px solid #1e293b",
    gap: 10,
  },

  input: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    border: "none",
    background: "#1e293b",
    color: "#fff",
  },

  button: {
    padding: "10px 18px",
    background: "#3b82f6",
    border: "none",
    borderRadius: 8,
    color: "#fff",
  },
};