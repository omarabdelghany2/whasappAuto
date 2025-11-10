import { useState, useRef, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { toast } from "@/hooks/use-toast";
import { MessageSquare, Image, BarChart3, Plus, Upload, Video } from "lucide-react";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Check, ChevronsUpDown, Users2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const API_BASE = "http://localhost:8000";

interface AddScheduleFormProps {
  onScheduleAdded: () => void;
  refreshGroupNames?: number;
}

export const AddScheduleForm = ({ onScheduleAdded, refreshGroupNames }: AddScheduleFormProps) => {
  const [activeTab, setActiveTab] = useState("message");
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoInputRef = useRef<HTMLInputElement>(null);
  const [groupNames, setGroupNames] = useState<string[]>([]);
  const [openMessageGroup, setOpenMessageGroup] = useState(false);
  const [openImageGroup, setOpenImageGroup] = useState(false);
  const [openVideoGroup, setOpenVideoGroup] = useState(false);
  const [openPollGroup, setOpenPollGroup] = useState(false);
  const [multiGroupMode, setMultiGroupMode] = useState(false);
  const [selectedGroups, setSelectedGroups] = useState<string[]>([]);

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

  const [videoForm, setVideoForm] = useState({
    group_name: "",
    video_path: "",
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

  const fetchGroupNames = async () => {
    try {
      const response = await fetch(`${API_BASE}/group-names`);
      const data = await response.json();
      setGroupNames(data);
    } catch (error) {
      console.error("Failed to fetch group names:", error);
    }
  };

  useEffect(() => {
    fetchGroupNames();
  }, [refreshGroupNames]);

  const handleAddSchedule = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/schedules`, { method: "GET" });
      const currentSchedules = await response.json();

      let newSchedule;
      let newScheduleTime;

      if (activeTab === "message") {
        newScheduleTime = messageForm.time;
        newSchedule = {
          type: "message",
          ...messageForm,
          time: messageForm.time.replace("T", " ")
        };
      } else if (activeTab === "image") {
        newScheduleTime = imageForm.time;
        newSchedule = {
          type: "image",
          ...imageForm,
          time: imageForm.time.replace("T", " ")
        };
      } else if (activeTab === "video") {
        newScheduleTime = videoForm.time;
        newSchedule = {
          type: "video",
          ...videoForm,
          time: videoForm.time.replace("T", " ")
        };
      } else {
        newScheduleTime = pollForm.time;
        newSchedule = {
          type: "poll",
          ...pollForm,
          time: pollForm.time.replace("T", " "),
          options: pollForm.options.split(",").map((s) => s.trim()),
        };
      }

      // Validate minimum 1-minute gap between schedules
      // Normalize times to ignore seconds
      const newTime = new Date(newScheduleTime);
      newTime.setSeconds(0, 0); // Set seconds and milliseconds to 0
      const newTimeMs = newTime.getTime();

      for (const schedule of currentSchedules) {
        const existingTime = new Date(schedule.time.replace(" ", "T"));
        existingTime.setSeconds(0, 0); // Set seconds and milliseconds to 0
        const existingTimeMs = existingTime.getTime();
        const timeDiffMinutes = Math.abs(newTimeMs - existingTimeMs) / (1000 * 60);

        if (timeDiffMinutes < 1) {
          const secondsNeeded = ((1 - timeDiffMinutes) * 60).toFixed(0);
          toast({
            title: "Schedule too close",
            description: `Minimum time between schedules is 1 minute. This schedule is ${secondsNeeded} second(s) too close to another schedule at ${schedule.time}.`,
            variant: "destructive"
          });
          setLoading(false);
          return;
        }
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
      setVideoForm({ group_name: "", video_path: "", caption: "", time: "" });
      setPollForm({ group_name: "", question: "", options: "", allow_multiple: false, time: "" });
    } catch (error) {
      toast({ title: "Failed to add schedule", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleMultiGroupSchedule = async () => {
    if (selectedGroups.length === 0) {
      toast({ title: "Please select at least one group", variant: "destructive" });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/schedules`, { method: "GET" });
      const currentSchedules = await response.json();

      const newSchedules = [];
      let baseTime;

      // Get the base schedule data
      if (activeTab === "message") {
        baseTime = messageForm.time;
        if (!messageForm.message.trim()) {
          toast({ title: "Message is required", variant: "destructive" });
          setLoading(false);
          return;
        }
      } else if (activeTab === "image") {
        baseTime = imageForm.time;
        if (!imageForm.image_path.trim()) {
          toast({ title: "Image path is required", variant: "destructive" });
          setLoading(false);
          return;
        }
      } else if (activeTab === "video") {
        baseTime = videoForm.time;
        if (!videoForm.video_path.trim()) {
          toast({ title: "Video path is required", variant: "destructive" });
          setLoading(false);
          return;
        }
      } else {
        baseTime = pollForm.time;
        if (!pollForm.question.trim()) {
          toast({ title: "Poll question is required", variant: "destructive" });
          setLoading(false);
          return;
        }
      }

      const baseTimeMs = new Date(baseTime).getTime();
      // Generate unique batch ID for this multi-group send
      const batchId = `batch_${Date.now()}`;

      // Create a schedule for each selected group with 1-minute intervals
      for (let i = 0; i < selectedGroups.length; i++) {
        const scheduleTimeMs = baseTimeMs + (i * 60 * 1000); // Add 60 seconds (1 minute) per group
        const scheduleDate = new Date(scheduleTimeMs);
        // Format as local time, not UTC
        const year = scheduleDate.getFullYear();
        const month = String(scheduleDate.getMonth() + 1).padStart(2, '0');
        const day = String(scheduleDate.getDate()).padStart(2, '0');
        const hours = String(scheduleDate.getHours()).padStart(2, '0');
        const minutes = String(scheduleDate.getMinutes()).padStart(2, '0');
        const scheduleTime = `${year}-${month}-${day} ${hours}:${minutes}`;

        let newSchedule;
        if (activeTab === "message") {
          newSchedule = {
            type: "message",
            group_name: selectedGroups[i],
            message: messageForm.message,
            time: scheduleTime,
            batch_id: batchId
          };
        } else if (activeTab === "image") {
          newSchedule = {
            type: "image",
            group_name: selectedGroups[i],
            image_path: imageForm.image_path,
            caption: imageForm.caption,
            time: scheduleTime,
            batch_id: batchId
          };
        } else if (activeTab === "video") {
          newSchedule = {
            type: "video",
            group_name: selectedGroups[i],
            video_path: videoForm.video_path,
            caption: videoForm.caption,
            time: scheduleTime,
            batch_id: batchId
          };
        } else {
          newSchedule = {
            type: "poll",
            group_name: selectedGroups[i],
            question: pollForm.question,
            options: pollForm.options.split(",").map((s) => s.trim()),
            allow_multiple: pollForm.allow_multiple,
            time: scheduleTime,
            batch_id: batchId
          };
        }

        newSchedules.push(newSchedule);
      }

      await fetch(`${API_BASE}/schedules/load`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entries: [...currentSchedules, ...newSchedules] }),
      });

      toast({
        title: `${selectedGroups.length} schedules added successfully`,
        description: `Scheduled at 1 minute intervals starting from ${new Date(baseTime).toLocaleString()}`
      });
      onScheduleAdded();

      // Reset forms and selections
      setMessageForm({ group_name: "", message: "", time: "" });
      setImageForm({ group_name: "", image_path: "", caption: "", time: "" });
      setVideoForm({ group_name: "", video_path: "", caption: "", time: "" });
      setPollForm({ group_name: "", question: "", options: "", allow_multiple: false, time: "" });
      setSelectedGroups([]);
      setMultiGroupMode(false);
    } catch (error) {
      toast({ title: "Failed to add schedules", variant: "destructive" });
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

  const handleVideoSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      // Upload the file to the backend
      const formData = new FormData();
      formData.append("file", file);

      toast({ title: "Uploading video...", description: file.name });

      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const data = await response.json();

      // Use the real absolute path returned by the server
      setVideoForm({ ...videoForm, video_path: data.path });
      toast({
        title: "Video uploaded successfully",
        description: `Saved to: ${data.path}`
      });
    } catch (error) {
      toast({
        title: "Upload failed",
        description: "Could not upload video to server",
        variant: "destructive"
      });
    }
  };

  return (
    <Card className="shadow-[var(--shadow-card)]">
      <CardHeader>
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              {multiGroupMode ? "Add Multiple Schedules" : "Add New Schedule"}
            </CardTitle>
          </div>
          <div className="flex items-center justify-between">
            <CardDescription>
              {multiGroupMode ? "Select multiple groups - schedules will be 1 minute apart" : "Schedule a new WhatsApp message, image, video, or poll"}
            </CardDescription>
            <Button
              variant={multiGroupMode ? "default" : "outline"}
              size="sm"
              className="h-8 whitespace-nowrap"
              onClick={() => {
                setMultiGroupMode(!multiGroupMode);
                setSelectedGroups([]);
              }}
            >
              <Users2 className="h-3.5 w-3.5 mr-1.5" />
              {multiGroupMode ? "Single" : "Multi Group"}
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="message">
              <MessageSquare className="h-4 w-4 mr-2" />
              Text
            </TabsTrigger>
            <TabsTrigger value="image">
              <Image className="h-4 w-4 mr-2" />
              Image
            </TabsTrigger>
            <TabsTrigger value="video">
              <Video className="h-4 w-4 mr-2" />
              Video
            </TabsTrigger>
            <TabsTrigger value="poll">
              <BarChart3 className="h-4 w-4 mr-2" />
              Poll
            </TabsTrigger>
          </TabsList>

          <TabsContent value="message" className="space-y-4">
            {multiGroupMode ? (
              <div className="space-y-2">
                <Label>Select Groups</Label>
                {groupNames.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No groups available. Add groups first.</p>
                ) : (
                  <div className="border rounded-md p-3 space-y-2 max-h-[200px] overflow-y-auto">
                    {groupNames.map((name) => (
                      <div key={name} className="flex items-center space-x-2">
                        <Checkbox
                          id={`msg-multi-${name}`}
                          checked={selectedGroups.includes(name)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedGroups([...selectedGroups, name]);
                            } else {
                              setSelectedGroups(selectedGroups.filter((g) => g !== name));
                            }
                          }}
                        />
                        <label
                          htmlFor={`msg-multi-${name}`}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                        >
                          {name}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
                {selectedGroups.length > 0 && (
                  <p className="text-xs text-muted-foreground">
                    {selectedGroups.length} group{selectedGroups.length !== 1 ? 's' : ''} selected
                  </p>
                )}
              </div>
            ) : (
              <div className="space-y-2">
                <Label>Group Name</Label>
                <Popover open={openMessageGroup} onOpenChange={setOpenMessageGroup}>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={openMessageGroup}
                      className="w-full justify-between"
                    >
                      {messageForm.group_name || "Select or type group name..."}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-full p-0">
                    <Command>
                      <CommandInput
                        placeholder="Search or type group name..."
                        value={messageForm.group_name}
                        onValueChange={(value) => setMessageForm({ ...messageForm, group_name: value })}
                      />
                      <CommandList>
                        <CommandEmpty>
                          <div className="p-2 text-sm text-muted-foreground">
                            Type to enter custom group name
                          </div>
                        </CommandEmpty>
                        <CommandGroup>
                          {groupNames.map((name) => (
                            <CommandItem
                              key={name}
                              value={name}
                              onSelect={(currentValue) => {
                                setMessageForm({ ...messageForm, group_name: currentValue });
                                setOpenMessageGroup(false);
                              }}
                            >
                              <Check
                                className={cn(
                                  "mr-2 h-4 w-4",
                                  messageForm.group_name === name ? "opacity-100" : "opacity-0"
                                )}
                              />
                              {name}
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      </CommandList>
                    </Command>
                  </PopoverContent>
                </Popover>
              </div>
            )}
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
            {multiGroupMode ? (
              <div className="space-y-2">
                <Label>Select Groups</Label>
                {groupNames.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No groups available. Add groups first.</p>
                ) : (
                  <div className="border rounded-md p-3 space-y-2 max-h-[200px] overflow-y-auto">
                    {groupNames.map((name) => (
                      <div key={name} className="flex items-center space-x-2">
                        <Checkbox
                          id={`img-multi-${name}`}
                          checked={selectedGroups.includes(name)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedGroups([...selectedGroups, name]);
                            } else {
                              setSelectedGroups(selectedGroups.filter((g) => g !== name));
                            }
                          }}
                        />
                        <label
                          htmlFor={`img-multi-${name}`}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                        >
                          {name}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
                {selectedGroups.length > 0 && (
                  <p className="text-xs text-muted-foreground">
                    {selectedGroups.length} group{selectedGroups.length !== 1 ? 's' : ''} selected
                  </p>
                )}
              </div>
            ) : (
              <div className="space-y-2">
                <Label>Group Name</Label>
                <Popover open={openImageGroup} onOpenChange={setOpenImageGroup}>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={openImageGroup}
                      className="w-full justify-between"
                    >
                      {imageForm.group_name || "Select or type group name..."}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-full p-0">
                    <Command>
                      <CommandInput
                        placeholder="Search or type group name..."
                        value={imageForm.group_name}
                        onValueChange={(value) => setImageForm({ ...imageForm, group_name: value })}
                      />
                      <CommandList>
                        <CommandEmpty>
                          <div className="p-2 text-sm text-muted-foreground">
                            Type to enter custom group name
                          </div>
                        </CommandEmpty>
                        <CommandGroup>
                          {groupNames.map((name) => (
                            <CommandItem
                              key={name}
                              value={name}
                              onSelect={(currentValue) => {
                                setImageForm({ ...imageForm, group_name: currentValue });
                                setOpenImageGroup(false);
                              }}
                            >
                              <Check
                                className={cn(
                                  "mr-2 h-4 w-4",
                                  imageForm.group_name === name ? "opacity-100" : "opacity-0"
                                )}
                              />
                              {name}
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      </CommandList>
                    </Command>
                  </PopoverContent>
                </Popover>
              </div>
            )}
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

          <TabsContent value="video" className="space-y-4">
            {multiGroupMode ? (
              <div className="space-y-2">
                <Label>Select Groups</Label>
                {groupNames.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No groups available. Add groups first.</p>
                ) : (
                  <div className="border rounded-md p-3 space-y-2 max-h-[200px] overflow-y-auto">
                    {groupNames.map((name) => (
                      <div key={name} className="flex items-center space-x-2">
                        <Checkbox
                          id={`video-multi-${name}`}
                          checked={selectedGroups.includes(name)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedGroups([...selectedGroups, name]);
                            } else {
                              setSelectedGroups(selectedGroups.filter((g) => g !== name));
                            }
                          }}
                        />
                        <label
                          htmlFor={`video-multi-${name}`}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                        >
                          {name}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
                {selectedGroups.length > 0 && (
                  <p className="text-xs text-muted-foreground">
                    {selectedGroups.length} group{selectedGroups.length !== 1 ? 's' : ''} selected
                  </p>
                )}
              </div>
            ) : (
              <div className="space-y-2">
                <Label>Group Name</Label>
                <Popover open={openVideoGroup} onOpenChange={setOpenVideoGroup}>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={openVideoGroup}
                      className="w-full justify-between"
                    >
                      {videoForm.group_name || "Select or type group name..."}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-full p-0">
                    <Command>
                      <CommandInput
                        placeholder="Search or type group name..."
                        value={videoForm.group_name}
                        onValueChange={(value) => setVideoForm({ ...videoForm, group_name: value })}
                      />
                      <CommandList>
                        <CommandEmpty>
                          <div className="p-2 text-sm text-muted-foreground">
                            Type to enter custom group name
                          </div>
                        </CommandEmpty>
                        <CommandGroup>
                          {groupNames.map((name) => (
                            <CommandItem
                              key={name}
                              value={name}
                              onSelect={(currentValue) => {
                                setVideoForm({ ...videoForm, group_name: currentValue });
                                setOpenVideoGroup(false);
                              }}
                            >
                              <Check
                                className={cn(
                                  "mr-2 h-4 w-4",
                                  videoForm.group_name === name ? "opacity-100" : "opacity-0"
                                )}
                              />
                              {name}
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      </CommandList>
                    </Command>
                  </PopoverContent>
                </Popover>
              </div>
            )}
            <div className="space-y-2">
              <Label>Video Path</Label>
              <div className="flex gap-2">
                <Input
                  placeholder="/path/to/video.mp4"
                  value={videoForm.video_path}
                  onChange={(e) => setVideoForm({ ...videoForm, video_path: e.target.value })}
                />
                <input
                  ref={videoInputRef}
                  type="file"
                  accept="video/*"
                  onChange={handleVideoSelect}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => videoInputRef.current?.click()}
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Browse
                </Button>
              </div>
            </div>
            <div className="space-y-2">
              <Label>Caption (optional)</Label>
              <Input
                placeholder="Caption for the video"
                value={videoForm.caption}
                onChange={(e) => setVideoForm({ ...videoForm, caption: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Time</Label>
              <Input
                type="datetime-local"
                value={videoForm.time}
                onChange={(e) => setVideoForm({ ...videoForm, time: e.target.value })}
              />
            </div>
          </TabsContent>

          <TabsContent value="poll" className="space-y-4">
            {multiGroupMode ? (
              <div className="space-y-2">
                <Label>Select Groups</Label>
                {groupNames.length === 0 ? (
                  <p className="text-sm text-muted-foreground">No groups available. Add groups first.</p>
                ) : (
                  <div className="border rounded-md p-3 space-y-2 max-h-[200px] overflow-y-auto">
                    {groupNames.map((name) => (
                      <div key={name} className="flex items-center space-x-2">
                        <Checkbox
                          id={`poll-multi-${name}`}
                          checked={selectedGroups.includes(name)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setSelectedGroups([...selectedGroups, name]);
                            } else {
                              setSelectedGroups(selectedGroups.filter((g) => g !== name));
                            }
                          }}
                        />
                        <label
                          htmlFor={`poll-multi-${name}`}
                          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                        >
                          {name}
                        </label>
                      </div>
                    ))}
                  </div>
                )}
                {selectedGroups.length > 0 && (
                  <p className="text-xs text-muted-foreground">
                    {selectedGroups.length} group{selectedGroups.length !== 1 ? 's' : ''} selected
                  </p>
                )}
              </div>
            ) : (
              <div className="space-y-2">
                <Label>Group Name</Label>
                <Popover open={openPollGroup} onOpenChange={setOpenPollGroup}>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      role="combobox"
                      aria-expanded={openPollGroup}
                      className="w-full justify-between"
                    >
                      {pollForm.group_name || "Select or type group name..."}
                      <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-full p-0">
                    <Command>
                      <CommandInput
                        placeholder="Search or type group name..."
                        value={pollForm.group_name}
                        onValueChange={(value) => setPollForm({ ...pollForm, group_name: value })}
                      />
                      <CommandList>
                        <CommandEmpty>
                          <div className="p-2 text-sm text-muted-foreground">
                            Type to enter custom group name
                          </div>
                        </CommandEmpty>
                        <CommandGroup>
                          {groupNames.map((name) => (
                            <CommandItem
                              key={name}
                              value={name}
                              onSelect={(currentValue) => {
                                setPollForm({ ...pollForm, group_name: currentValue });
                                setOpenPollGroup(false);
                              }}
                            >
                              <Check
                                className={cn(
                                  "mr-2 h-4 w-4",
                                  pollForm.group_name === name ? "opacity-100" : "opacity-0"
                                )}
                              />
                              {name}
                            </CommandItem>
                          ))}
                        </CommandGroup>
                      </CommandList>
                    </Command>
                  </PopoverContent>
                </Popover>
              </div>
            )}
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

        <Button
          onClick={multiGroupMode ? handleMultiGroupSchedule : handleAddSchedule}
          disabled={loading || (multiGroupMode && selectedGroups.length === 0)}
          className="w-full mt-6"
        >
          <Plus className="h-4 w-4 mr-2" />
          {multiGroupMode ? `Add ${selectedGroups.length} Schedule${selectedGroups.length !== 1 ? 's' : ''}` : 'Add Schedule'}
        </Button>
      </CardContent>
    </Card>
  );
};
