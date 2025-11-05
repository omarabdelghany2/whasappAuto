import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Play, Pause, RefreshCw, Save, Upload, CheckCircle2, LogIn } from "lucide-react";
import { toast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

const API_BASE = "http://localhost:8000";

interface SchedulerStatus {
  running: boolean;
  count: number;
}

export const SchedulerHeader = () => {
  const [status, setStatus] = useState<SchedulerStatus>({ running: false, count: 0 });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE}/scheduler/status`);
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error("Failed to fetch status:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStart = async () => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/scheduler/start`, { method: "POST" });
      toast({ title: "Scheduler started" });
      fetchStatus();
    } catch (error) {
      toast({ title: "Failed to start scheduler", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/scheduler/stop`, { method: "POST" });
      toast({ title: "Scheduler stopped" });
      fetchStatus();
    } catch (error) {
      toast({ title: "Failed to stop scheduler", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/schedules/save`, { method: "POST" });
      toast({ title: "Schedules saved successfully" });
    } catch (error) {
      toast({ title: "Failed to save schedules", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleLoad = async () => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/schedules/load`, { method: "POST" });
      toast({ title: "Schedules loaded successfully" });
      window.location.reload();
    } catch (error) {
      toast({ title: "Failed to load schedules", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/whatsapp/login`, { method: "POST" });
      const data = await response.json();
      toast({ title: data.message || "WhatsApp Web opened for login" });
    } catch (error) {
      toast({ title: "Failed to open WhatsApp Web", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <header className="border-b bg-card shadow-[var(--shadow-card)]">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold bg-[var(--gradient-primary)] bg-clip-text text-transparent">
              WhatsApp Scheduler
            </h1>
            <Badge variant={status.running ? "default" : "secondary"} className="px-3 py-1">
              {status.running ? "Running" : "Stopped"} • {status.count} schedules
            </Badge>
          </div>
          <div className="flex gap-2">
            <Button onClick={handleLogin} disabled={loading} variant="default" className="flex flex-col h-auto py-1.5 px-3">
              <div className="flex items-center gap-1.5">
                <LogIn className="h-4 w-4" />
                <span>Open WhatsApp</span>
              </div>
              <span className="text-[10px] font-normal opacity-70">For login or logout</span>
            </Button>
            {status.running ? (
              <Button onClick={handleStop} disabled={loading} variant="destructive" className="h-auto py-1.5 px-3">
                <Pause className="h-4 w-4" />
                Stop
              </Button>
            ) : (
              <Button onClick={handleStart} disabled={loading} className="h-auto py-1.5 px-3">
                <Play className="h-4 w-4" />
                Start
              </Button>
            )}
            <Button onClick={handleSave} disabled={loading} variant="outline" className="h-auto py-1.5 px-3">
              <Save className="h-4 w-4" />
              Save
            </Button>
            <Button onClick={handleLoad} disabled={loading} variant="outline" className="h-auto py-1.5 px-3">
              <Upload className="h-4 w-4" />
              Load
            </Button>
            <Button onClick={() => navigate("/finished")} variant="outline" className="h-auto py-1.5 px-3">
              <CheckCircle2 className="h-4 w-4" />
              Finished
            </Button>
            <Button onClick={fetchStatus} disabled={loading} variant="ghost" className="h-auto py-1.5 px-3">
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};
