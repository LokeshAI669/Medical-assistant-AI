"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState<any[]>([]);

  // 🔐 Check login
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please login first");
      window.location.href = "/login";
    }
  }, []);

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

      const res = await fetch("http://127.0.0.1:8000/api/v1/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ message: userMessage.text }),
      });

      const data = await res.json();

      const aiMessage = { role: "ai", text: data.response };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ Error connecting to server" },
      ]);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>🏥 Medical AI Assistant</h1>

      {/* Logout */}
      <button onClick={handleLogout} style={styles.logoutBtn}>
        Logout 🚪
      </button>

      {/* Chat */}
      <div style={styles.chatBox}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={
              m.role === "user" ? styles.userMessage : styles.aiMessage
            }
          >
            {m.text}
          </div>
        ))}
      </div>

      {/* Input */}
      <div style={styles.inputBox}>
        <input
          value={msg}
          onChange={(e) => setMsg(e.target.value)}
          placeholder="Enter symptoms..."
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
    padding: 20,
    fontFamily: "Arial",
    maxWidth: 600,
    margin: "auto",
    backgroundColor: "#000",
    color: "#fff",
    minHeight: "100vh",
  },

  title: {
    textAlign: "center",
  },

  logoutBtn: {
    marginBottom: 10,
    padding: "8px 12px",
    backgroundColor: "red",
    color: "#fff",
    border: "none",
    borderRadius: 5,
    cursor: "pointer",
  },

  chatBox: {
    border: "1px solid #444",
    backgroundColor: "#121212",
    height: "400px",
    overflowY: "auto",
    padding: 10,
    marginBottom: 10,
    display: "flex",
    flexDirection: "column",
  },

  userMessage: {
    backgroundColor: "#007bff",
    color: "#fff",
    padding: 10,
    borderRadius: 10,
    marginBottom: 8,
    alignSelf: "flex-end",
    maxWidth: "70%",
  },

  aiMessage: {
    backgroundColor: "#2d2d2d",
    color: "#fff",
    padding: 10,
    borderRadius: 10,
    marginBottom: 8,
    alignSelf: "flex-start",
    maxWidth: "70%",
  },

  inputBox: {
    display: "flex",
    gap: 10,
  },

  input: {
    flex: 1,
    padding: 10,
    borderRadius: 5,
    border: "none",
  },

  button: {
    padding: "10px 15px",
    borderRadius: 5,
    border: "none",
    backgroundColor: "#007bff",
    color: "#fff",
    cursor: "pointer",
  },
};