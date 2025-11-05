import { useState, useEffect, useRef } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "@/hooks/use-toast";
import { Plus, Trash2, Upload } from "lucide-react";

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
}

interface EditScheduleDialogProps {
  schedule: Schedule | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSave: (schedule: Schedule) => void;
}

export const EditScheduleDialog = ({ schedule, open, onOpenChange, onSave }: EditScheduleDialogProps) => {
  const [editedSchedule, setEditedSchedule] = useState<Schedule | null>(null);
  const [newOption, setNewOption] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (schedule) {
      setEditedSchedule({ ...schedule });
    }
  }, [schedule]);

  if (!editedSchedule) return null;

  const handleSave = () => {
    if (!editedSchedule.group_name.trim()) {
      toast({ title: "Group name is required", variant: "destructive" });
      return;
    }

    if (editedSchedule.type === "message" && !editedSchedule.message?.trim()) {
      toast({ title: "Message is required", variant: "destructive" });
      return;
    }

    if (editedSchedule.type === "poll") {
      if (!editedSchedule.question?.trim()) {
        toast({ title: "Poll question is required", variant: "destructive" });
        return;
      }
      if (!editedSchedule.options || editedSchedule.options.length < 2) {
        toast({ title: "Poll needs at least 2 options", variant: "destructive" });
        return;
      }
    }

    onSave(editedSchedule);
    onOpenChange(false);
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      // Upload the file to the backend
      const formData = new FormData();
      formData.append("file", file);

      toast({ title: "Uploading file...", description: file.name });

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      // Use the real absolute path returned by the server
      setEditedSchedule({ ...editedSchedule, image_path: data.path });
      toast({
        title: "File uploaded successfully",
        description: `Saved to: ${data.path}`
      });
    } catch (error) {
      toast({
        title: "Upload failed",
        description: "Could not upload file to server",
        variant: "destructive"
      });
    }
  };

  const addOption = () => {
    if (newOption.trim() && editedSchedule.options) {
      setEditedSchedule({
        ...editedSchedule,
        options: [...editedSchedule.options, newOption.trim()]
      });
      setNewOption("");
    }
  };

  const removeOption = (index: number) => {
    if (editedSchedule.options) {
      setEditedSchedule({
        ...editedSchedule,
        options: editedSchedule.options.filter((_, i) => i !== index)
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Edit Schedule</DialogTitle>
          <DialogDescription>Modify the schedule details below</DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label htmlFor="group_name">Group Name</Label>
            <Input
              id="group_name"
              value={editedSchedule.group_name}
              onChange={(e) => setEditedSchedule({ ...editedSchedule, group_name: e.target.value })}
              placeholder="Cairo"
            />
          </div>
          
          <div>
            <Label htmlFor="time">Time</Label>
            <Input
              id="time"
              type="datetime-local"
              value={editedSchedule.time.replace(" ", "T").slice(0, 16)}
              onChange={(e) => setEditedSchedule({ ...editedSchedule, time: e.target.value.replace("T", " ") })}
            />
          </div>

          {editedSchedule.type === "message" && (
            <div>
              <Label htmlFor="message">Message</Label>
              <Textarea
                id="message"
                value={editedSchedule.message || ""}
                onChange={(e) => setEditedSchedule({ ...editedSchedule, message: e.target.value })}
                placeholder="Enter your message"
                rows={4}
              />
            </div>
          )}

          {editedSchedule.type === "image" && (
            <>
              <div>
                <Label htmlFor="image_path">Image Path</Label>
                <div className="flex gap-2">
                  <Input
                    id="image_path"
                    value={editedSchedule.image_path || ""}
                    onChange={(e) => setEditedSchedule({ ...editedSchedule, image_path: e.target.value })}
                    placeholder="/absolute/path/to/image.jpg"
                  />
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <Upload className="h-4 w-4 mr-2" />
                    Browse
                  </Button>
                </div>
              </div>
              <div>
                <Label htmlFor="caption">Caption (Optional)</Label>
                <Textarea
                  id="caption"
                  value={editedSchedule.caption || ""}
                  onChange={(e) => setEditedSchedule({ ...editedSchedule, caption: e.target.value })}
                  placeholder="Image caption"
                  rows={2}
                />
              </div>
            </>
          )}

          {editedSchedule.type === "poll" && (
            <>
              <div>
                <Label htmlFor="question">Poll Question</Label>
                <Input
                  id="question"
                  value={editedSchedule.question || ""}
                  onChange={(e) => setEditedSchedule({ ...editedSchedule, question: e.target.value })}
                  placeholder="What's your question?"
                />
              </div>
              <div>
                <Label>Poll Options</Label>
                <div className="space-y-2 mt-2">
                  {editedSchedule.options?.map((option, index) => (
                    <div key={index} className="flex gap-2">
                      <Input value={option} disabled />
                      <Button variant="ghost" size="icon" onClick={() => removeOption(index)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                  <div className="flex gap-2">
                    <Input
                      value={newOption}
                      onChange={(e) => setNewOption(e.target.value)}
                      placeholder="Add new option"
                      onKeyPress={(e) => e.key === "Enter" && addOption()}
                    />
                    <Button variant="outline" onClick={addOption}>
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="allow_multiple"
                  checked={editedSchedule.allow_multiple || false}
                  onChange={(e) => setEditedSchedule({ ...editedSchedule, allow_multiple: e.target.checked })}
                  className="rounded"
                />
                <Label htmlFor="allow_multiple">Allow multiple answers</Label>
              </div>
            </>
          )}

          <div className="flex justify-end gap-2 pt-4">
            <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
            <Button onClick={handleSave}>Save Changes</Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};
