import { useState, useEffect } from "react";
import { SchedulerHeader } from "@/components/SchedulerHeader";
import { ScheduleCard } from "@/components/ScheduleCard";
import { AddScheduleForm } from "@/components/AddScheduleForm";
import { EditScheduleDialog } from "@/components/EditScheduleDialog";
import { toast } from "@/hooks/use-toast";

const API_BASE = "http://localhost:8000";

interface Schedule {
  type: "message" | "image" | "poll";
  group_name: string;
  message?: string;
  image_path?: string;
  caption?: string;
  question?: string;
  options?: string[];
  allow_multiple?: boolean;
  time: string;
  status?: "pending" | "done";
  completed_at?: string;
  profile_name?: string;
}

// Example schedules to demonstrate the UI
const exampleSchedules: Schedule[] = [
  {
    type: "message",
    group_name: "Cairo",
    message: "Good morning team! Hope everyone has a great day ahead.",
    time: "2025-10-30 09:00"
  },
  {
    type: "image",
    group_name: "Family Group",
    image_path: "/path/to/photo.jpg",
    caption: "Check out this amazing sunset!",
    time: "2025-10-30 18:30"
  },
  {
    type: "poll",
    group_name: "Cairo",
    question: "What's your favorite food?",
    options: ["Pizza", "Burger", "Pasta", "Sushi"],
    allow_multiple: false,
    time: "2025-10-30 12:00"
  },
  {
    type: "message",
    group_name: "Work Team",
    message: "Reminder: Team meeting in 30 minutes!",
    time: "2025-10-30 14:30"
  }
];

const Index = () => {
  const [schedules, setSchedules] = useState<Schedule[]>(exampleSchedules);
  const [loading, setLoading] = useState(true);
  const [editingSchedule, setEditingSchedule] = useState<{ schedule: Schedule; index: number } | null>(null);

  const fetchSchedules = async () => {
    try {
      const response = await fetch(`${API_BASE}/schedules`);
      const data = await response.json();
      // Sort schedules by time
      const sortedSchedules = data.sort((a: Schedule, b: Schedule) => {
        const timeA = new Date(a.time.replace(" ", "T")).getTime();
        const timeB = new Date(b.time.replace(" ", "T")).getTime();
        return timeA - timeB;
      });
      setSchedules(sortedSchedules);
    } catch (error) {
      toast({ title: "Failed to fetch schedules", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, []);

  const handleDelete = async (index: number) => {
    try {
      const newSchedules = schedules.filter((_, i) => i !== index);
      await fetch(`${API_BASE}/schedules/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entries: newSchedules }),
      });
      toast({ title: "Schedule deleted" });
      fetchSchedules();
    } catch (error) {
      toast({ title: "Failed to delete schedule", variant: "destructive" });
    }
  };

  const handleEdit = (index: number) => {
    setEditingSchedule({ schedule: schedules[index], index });
  };

  const handleSaveEdit = async (editedSchedule: Schedule) => {
    if (editingSchedule === null) return;
    
    try {
      const newSchedules = [...schedules];
      newSchedules[editingSchedule.index] = editedSchedule;
      
      await fetch(`${API_BASE}/schedules/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entries: newSchedules }),
      });
      
      toast({ title: "Schedule updated successfully" });
      fetchSchedules();
    } catch (error) {
      toast({ title: "Failed to update schedule", variant: "destructive" });
    }
  };

  return (
    <div className="min-h-screen bg-[var(--gradient-subtle)]">
      <SchedulerHeader />
      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <AddScheduleForm onScheduleAdded={fetchSchedules} />
          </div>
          <div className="lg:col-span-2">
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-2">Scheduled Messages</h2>
              <p className="text-muted-foreground">
                {schedules.length} {schedules.length === 1 ? "schedule" : "schedules"} configured
              </p>
            </div>
            {loading ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Loading schedules...</p>
              </div>
            ) : schedules.length === 0 ? (
              <div className="text-center py-12 bg-card rounded-lg border shadow-[var(--shadow-card)]">
                <p className="text-muted-foreground">No schedules yet. Add your first schedule to get started!</p>
              </div>
            ) : (
              <div className="grid gap-4">
                {schedules.map((schedule, index) => (
                  <ScheduleCard 
                    key={index} 
                    schedule={schedule} 
                    onDelete={() => handleDelete(index)}
                    onEdit={() => handleEdit(index)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>

      <EditScheduleDialog
        schedule={editingSchedule?.schedule || null}
        open={editingSchedule !== null}
        onOpenChange={(open) => !open && setEditingSchedule(null)}
        onSave={handleSaveEdit}
      />
    </div>
  );
};

export default Index;
