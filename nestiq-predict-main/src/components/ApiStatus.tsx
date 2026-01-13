import { useEffect, useState } from "react";
import { Wifi, WifiOff } from "lucide-react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const ApiStatus = () => {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkHealth = async () => {
    setIsChecking(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/health/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setIsOnline(data.status === "ok");
      } else {
        setIsOnline(false);
      }
    } catch (error) {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <button
      onClick={checkHealth}
      disabled={isChecking}
      className="flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs font-medium transition-all duration-200 hover:scale-105"
      title={isOnline ? "API Connected" : "API Disconnected"}
    >
      <div className={`status-dot ${isOnline ? "status-dot-online" : "status-dot-offline"} ${isChecking ? "animate-pulse" : ""}`} />
      {isOnline === null ? (
        <span className="text-muted-foreground">Checking...</span>
      ) : isOnline ? (
        <>
          <Wifi className="w-3 h-3 text-emerald-400" />
          <span className="text-emerald-400 hidden sm:inline">Online</span>
        </>
      ) : (
        <>
          <WifiOff className="w-3 h-3 text-red-400" />
          <span className="text-red-400 hidden sm:inline">Offline</span>
        </>
      )}
    </button>
  );
};

export default ApiStatus;
