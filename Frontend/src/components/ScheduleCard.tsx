import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { MessageSquare, Image, BarChart3, Trash2, Calendar, Edit, Video } from "lucide-react";
import { format } from "date-fns";

interface Schedule {
  type: "message" | "image" | "video" | "poll";
  group_name: string;
  message?: string;
  image_path?: string;
  video_path?: string;
  caption?: string;
  question?: string;
  options?: string[];
  allow_multiple?: boolean;
  time: string;
  status?: "pending" | "done";
  completed_at?: string;
}

interface ScheduleCardProps {
  schedule: Schedule;
  onDelete: () => void;
  onEdit: () => void;
}

export const ScheduleCard = ({ schedule, onDelete, onEdit }: ScheduleCardProps) => {
  const getIcon = () => {
    switch (schedule.type) {
      case "message":
        return <MessageSquare className="h-5 w-5" />;
      case "image":
        return <Image className="h-5 w-5" />;
      case "video":
        return <Video className="h-5 w-5" />;
      case "poll":
        return <BarChart3 className="h-5 w-5" />;
    }
  };

  const getContent = () => {
    switch (schedule.type) {
      case "message":
        return schedule.message;
      case "image":
        return schedule.caption || "Image message";
      case "video":
        return schedule.caption || "Video message";
      case "poll":
        return schedule.question;
    }
  };

  return (
    <Card className="transition-all hover:shadow-[var(--shadow-hover)] hover:scale-[1.02] border-l-4 border-l-primary">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-secondary text-secondary-foreground">{getIcon()}</div>
            <div>
              <CardTitle className="text-lg">{schedule.group_name}</CardTitle>
              <CardDescription className="flex items-center gap-2 mt-1">
                <Calendar className="h-3 w-3" />
                {format(new Date(schedule.time.replace(" ", "T")), "MMM dd, yyyy - hh:mm a")}
              </CardDescription>
            </div>
          </div>
          <div className="flex gap-2 items-center">
            {schedule.status === "done" ? (
              <Badge variant="default" className="bg-green-600 hover:bg-green-600">Done</Badge>
            ) : (
              <Badge variant="outline" className="text-amber-700 border-amber-300 bg-amber-50">Pending</Badge>
            )}
            <Button variant="ghost" size="icon" onClick={onEdit}>
              <Edit className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={onDelete} className="text-destructive hover:text-destructive">
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{getContent()}</p>
        {schedule.type === "poll" && schedule.options && (
          <div className="flex flex-wrap gap-1 mb-3">
            {schedule.options.map((option, i) => (
              <Badge key={i} variant="outline" className="text-xs">
                {option}
              </Badge>
            ))}
          </div>
        )}
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs capitalize">
            {schedule.type}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
};
