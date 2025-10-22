import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState([]);
  const [progress, setProgress] = useState(0);
  const [logs, setLogs] = useState(["> Console ready..."]);
  const [isRunning, setIsRunning] = useState(false);
  const [taskStatus, setTaskStatus] = useState({
    Build: "idle",
    Push: "idle",
    Pull: "idle",
  });

  // Simulated boot-up loader
  useEffect(() => {
    const bootMessages = [
      "Initializing system...",
      "Loading assets...",
      "Fetching configurations...",
      "Connecting to build servers...",
      "Almost done...",
      "All systems ready ✅"
    ];

    let index = 0;
    const interval = setInterval(() => {
      setLoadingMessages((prev) => [...prev, bootMessages[index]]);
      index++;
      if (index === bootMessages.length) {
        clearInterval(interval);
        setTimeout(() => setIsLoaded(true), 1000); // Delay for smooth transition
      }
    }, 800);
  }, []);

  // Dashboard logic
  const simulateProgress = (taskName) => {
    if (isRunning) return;
    setIsRunning(true);
    setLogs((prev) => [...prev, `> ${taskName} started...`]);
    setProgress(0);
    setTaskStatus((prev) => ({ ...prev, [taskName]: "running" }));

    let value = 0;
    const interval = setInterval(() => {
      value += 10;
      setProgress(value);

      if (value === 50)
        setLogs((prev) => [...prev, `> ${taskName} is halfway done...`]);
      if (value >= 100) {
        clearInterval(interval);
        setLogs((prev) => [
          ...prev,
          `> ${taskName} completed successfully! ✅`,
        ]);
        setTaskStatus((prev) => ({ ...prev, [taskName]: "done" }));
        setTimeout(() => {
          setTaskStatus((prev) => ({ ...prev, [taskName]: "idle" }));
        }, 2500);
        setIsRunning(false);
      }
    }, 300);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "running":
        return <span className="spinner" />;
      case "done":
        return <span className="status-icon done">✅</span>;
      default:
        return <span className="status-icon idle">⏸️</span>;
    }
  };

  // If not loaded, show loading screen
  if (!isLoaded) {
    return (
      <div className="loading-screen">
        <div className="loading-terminal">
          <h2>🚀 Initializing Build Console...</h2>
          <div className="loading-messages">
            {loadingMessages.map((msg, i) => (
              <p key={i}> {msg}</p>
            ))}
          </div>
          <div className="loading-bar">
            <div
              className="loading-bar-progress"
              style={{ width: `${(loadingMessages.length / 6) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>
    );
  }

  // Main dashboard after loading completes
  return (
    <div className="app-container">
      <h1 className="title">🚀 Build & Deployment Console</h1>

      <div className="button-group">
        {["Build", "Push", "Pull"].map((task) => (
          <button
            key={task}
            onClick={() => simulateProgress(task)}
            disabled={isRunning}
            className={`task-button ${
              taskStatus[task] === "running" ? "running" : ""
            }`}
          >
            {getStatusIcon(taskStatus[task])} {task}
          </button>
        ))}
      </div>

      <div className="progress-container">
        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
      </div>

      <div className="console-output">
        {logs.map((log, i) => (
          <p key={i}>{log}</p>
        ))}
      </div>
    </div>
  );
}

export default App;
