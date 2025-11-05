import { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle2, MessageSquare, Image, BarChart3, ArrowLeft, Calendar, Clock, Trash2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { toast } from "@/hooks/use-toast";

const API_BASE = "http://localhost:8000";

interface FinishedSchedule {
  type: "message" | "image" | "poll";
  group_name: string;
  message?: string;
  image_path?: string;
  caption?: string;
  question?: string;
  options?: string[];
  allow_multiple?: boolean;
  time: string;
  scheduled_time?: string;
  created_at?: string;
  completed_at?: string;
  status: string;
}

const FinishedSchedules = () => {
  const [finishedSchedules, setFinishedSchedules] = useState<FinishedSchedule[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchFinishedSchedules();
  }, []);

  const fetchFinishedSchedules = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/finished-schedules`);
      if (!response.ok) throw new Error("Failed to fetch");
      const data = await response.json();
      setFinishedSchedules(data);
    } catch (error) {
      toast({
        title: "Failed to load finished schedules",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (index: number) => {
    try {
      const response = await fetch(`${API_BASE}/finished-schedules/${index}`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to delete");

      toast({
        title: "Schedule deleted",
        description: "Finished schedule removed successfully",
      });

      // Refresh the list
      fetchFinishedSchedules();
    } catch (error) {
      toast({
        title: "Failed to delete schedule",
        variant: "destructive",
      });
    }
  };

  const handleClearAll = async () => {
    if (!confirm("Are you sure you want to delete all finished schedules? This cannot be undone.")) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/finished-schedules`, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Failed to clear");

      toast({
        title: "All schedules cleared",
        description: "All finished schedules have been removed",
      });

      // Refresh the list
      fetchFinishedSchedules();
    } catch (error) {
      toast({
        title: "Failed to clear schedules",
        variant: "destructive",
      });
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "message":
        return <MessageSquare className="h-5 w-5" />;
      case "image":
        return <Image className="h-5 w-5" />;
      case "poll":
        return <BarChart3 className="h-5 w-5" />;
      default:
        return <MessageSquare className="h-5 w-5" />;
    }
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString();
    } catch {
      return dateString;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 mb-2">Finished Schedules</h1>
            <p className="text-gray-600">View all completed WhatsApp schedules</p>
          </div>
          <div className="flex gap-2">
            {finishedSchedules.length > 0 && (
              <Button onClick={handleClearAll} variant="destructive">
                <Trash2 className="h-4 w-4 mr-2" />
                Clear All
              </Button>
            )}
            <Button onClick={() => navigate("/")} variant="outline">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Dashboard
            </Button>
          </div>
        </div>

        {loading ? (
          <Card>
            <CardContent className="p-8 text-center">
              <p className="text-gray-500">Loading finished schedules...</p>
            </CardContent>
          </Card>
        ) : finishedSchedules.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <CheckCircle2 className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No finished schedules yet</p>
              <p className="text-sm text-gray-400 mt-2">Completed schedules will appear here</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {finishedSchedules.map((schedule, index) => (
              <Card key={index} className="shadow-lg hover:shadow-xl transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 flex-1">
                      <div className="p-2 rounded-lg bg-green-100 text-green-600">
                        {getIcon(schedule.type)}
                      </div>
                      <div className="flex-1">
                        <CardTitle className="text-lg flex items-center gap-2">
                          {schedule.group_name}
                          <CheckCircle2 className="h-5 w-5 text-green-500" />
                        </CardTitle>
                        <CardDescription className="flex items-center gap-4 mt-1">
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            Scheduled: {formatDate(schedule.time || schedule.scheduled_time || "")}
                          </span>
                          {schedule.completed_at && (
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              Completed: {formatDate(schedule.completed_at)}
                            </span>
                          )}
                        </CardDescription>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                        {schedule.type}
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(index)}
                        className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {schedule.type === "message" && schedule.message && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm font-medium text-gray-700 mb-1">Message:</p>
                      <p className="text-gray-600">{schedule.message}</p>
                    </div>
                  )}

                  {schedule.type === "image" && (
                    <div className="space-y-2">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-700 mb-1">Image Path:</p>
                        <p className="text-gray-600 text-sm break-all">{schedule.image_path}</p>
                      </div>
                      {schedule.caption && (
                        <div className="bg-gray-50 p-4 rounded-lg">
                          <p className="text-sm font-medium text-gray-700 mb-1">Caption:</p>
                          <p className="text-gray-600">{schedule.caption}</p>
                        </div>
                      )}
                    </div>
                  )}

                  {schedule.type === "poll" && (
                    <div className="space-y-2">
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-700 mb-2">Question:</p>
                        <p className="text-gray-600 mb-3">{schedule.question}</p>
                        <p className="text-sm font-medium text-gray-700 mb-2">Options:</p>
                        <ul className="list-disc list-inside space-y-1">
                          {schedule.options?.map((option, i) => (
                            <li key={i} className="text-gray-600">{option}</li>
                          ))}
                        </ul>
                        {schedule.allow_multiple && (
                          <p className="text-sm text-blue-600 mt-2">✓ Multiple answers allowed</p>
                        )}
                      </div>
                    </div>
                  )}

                  {schedule.created_at && (
                    <div className="mt-4 pt-4 border-t">
                      <p className="text-xs text-gray-500">
                        Created: {formatDate(schedule.created_at)}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FinishedSchedules;
