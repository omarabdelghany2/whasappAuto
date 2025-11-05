import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { toast } from "@/hooks/use-toast";
import { MessageSquare, Image, BarChart3, Plus, Upload } from "lucide-react";

const API_BASE = "http://localhost:8000";

interface AddScheduleFormProps {
  onScheduleAdded: () => void;
}

export const AddScheduleForm = ({ onScheduleAdded }: AddScheduleFormProps) => {
  const [activeTab, setActiveTab] = useState("message");
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [messageForm, setMessageForm] = useState({
    group_name: "",
    message: "",
    time: "",
  });

  const [imageForm, setImageForm] = useState({
    group_name: "",
    image_path: "",
    caption: "",
    time: "",
  });

  const [pollForm, setPollForm] = useState({
    group_name: "",
    question: "",
    options: "",
    allow_multiple: false,
    time: "",
  });

  const handleAddSchedule = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/schedules`, { method: "GET" });
      const currentSchedules = await response.json();

      let newSchedule;
      if (activeTab === "message") {
        newSchedule = { 
          type: "message", 
          ...messageForm,
          time: messageForm.time.replace("T", " ")
        };
      } else if (activeTab === "image") {
        newSchedule = { 
          type: "image", 
          ...imageForm,
          time: imageForm.time.replace("T", " ")
        };
      } else {
        newSchedule = {
          type: "poll",
          ...pollForm,
          time: pollForm.time.replace("T", " "),
          options: pollForm.options.split(",").map((s) => s.trim()),
        };
      }

      await fetch(`${API_BASE}/schedules/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entries: [...currentSchedules, newSchedule] }),
      });

      toast({ title: "Schedule added successfully" });
      onScheduleAdded();

      // Reset forms
      setMessageForm({ group_name: "", message: "", time: "" });
      setImageForm({ group_name: "", image_path: "", caption: "", time: "" });
      setPollForm({ group_name: "", question: "", options: "", allow_multiple: false, time: "" });
    } catch (error) {
      toast({ title: "Failed to add schedule", variant: "destructive" });
    } finally {
      setLoading(false);
    }
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
      setImageForm({ ...imageForm, image_path: data.path });
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

  return (
    <Card className="shadow-[var(--shadow-card)]">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Plus className="h-5 w-5" />
          Add New Schedule
        </CardTitle>
        <CardDescription>Schedule a new WhatsApp message, image, or poll</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="message">
              <MessageSquare className="h-4 w-4 mr-2" />
              Text
            </TabsTrigger>
            <TabsTrigger value="image">
              <Image className="h-4 w-4 mr-2" />
              Image
            </TabsTrigger>
            <TabsTrigger value="poll">
              <BarChart3 className="h-4 w-4 mr-2" />
              Poll
            </TabsTrigger>
          </TabsList>

          <TabsContent value="message" className="space-y-4">
            <div className="space-y-2">
              <Label>Group Name</Label>
              <Input
                placeholder="Cairo"
                value={messageForm.group_name}
                onChange={(e) => setMessageForm({ ...messageForm, group_name: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Message</Label>
              <Input
                placeholder="Good morning!"
                value={messageForm.message}
                onChange={(e) => setMessageForm({ ...messageForm, message: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Time</Label>
              <Input
                type="datetime-local"
                value={messageForm.time}
                onChange={(e) => setMessageForm({ ...messageForm, time: e.target.value })}
              />
            </div>
          </TabsContent>

          <TabsContent value="image" className="space-y-4">
            <div className="space-y-2">
              <Label>Group Name</Label>
              <Input
                placeholder="Cairo"
                value={imageForm.group_name}
                onChange={(e) => setImageForm({ ...imageForm, group_name: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Image Path</Label>
              <div className="flex gap-2">
                <Input
                  placeholder="/path/to/image.jpg"
                  value={imageForm.image_path}
                  onChange={(e) => setImageForm({ ...imageForm, image_path: e.target.value })}
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
            <div className="space-y-2">
              <Label>Caption (optional)</Label>
              <Input
                placeholder="Caption for the image"
                value={imageForm.caption}
                onChange={(e) => setImageForm({ ...imageForm, caption: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Time</Label>
              <Input
                type="datetime-local"
                value={imageForm.time}
                onChange={(e) => setImageForm({ ...imageForm, time: e.target.value })}
              />
            </div>
          </TabsContent>

          <TabsContent value="poll" className="space-y-4">
            <div className="space-y-2">
              <Label>Group Name</Label>
              <Input
                placeholder="Cairo"
                value={pollForm.group_name}
                onChange={(e) => setPollForm({ ...pollForm, group_name: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Question</Label>
              <Input
                placeholder="What's your favorite food?"
                value={pollForm.question}
                onChange={(e) => setPollForm({ ...pollForm, question: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Options (comma-separated)</Label>
              <Input
                placeholder="Pizza, Burger, Pasta"
                value={pollForm.options}
                onChange={(e) => setPollForm({ ...pollForm, options: e.target.value })}
              />
            </div>
            <div className="flex items-center space-x-2">
              <Switch
                id="allow-multiple"
                checked={pollForm.allow_multiple}
                onCheckedChange={(checked) => setPollForm({ ...pollForm, allow_multiple: checked })}
              />
              <Label htmlFor="allow-multiple" className="cursor-pointer">
                Allow multiple answers
              </Label>
            </div>
            <div className="space-y-2">
              <Label>Time</Label>
              <Input
                type="datetime-local"
                value={pollForm.time}
                onChange={(e) => setPollForm({ ...pollForm, time: e.target.value })}
              />
            </div>
          </TabsContent>
        </Tabs>

        <Button onClick={handleAddSchedule} disabled={loading} className="w-full mt-6">
          <Plus className="h-4 w-4 mr-2" />
          Add Schedule
        </Button>
      </CardContent>
    </Card>
  );
};
