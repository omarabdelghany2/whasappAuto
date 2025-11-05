import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Plus, Trash2, Users, ChevronDown } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const API_BASE = "http://localhost:8000";

interface ManageGroupNamesProps {
  onGroupNamesChange?: () => void;
}

export const ManageGroupNames = ({ onGroupNamesChange }: ManageGroupNamesProps) => {
  const [groupNames, setGroupNames] = useState<string[]>([]);
  const [newGroupName, setNewGroupName] = useState("");
  const [loading, setLoading] = useState(false);
  const [showScrollIndicator, setShowScrollIndicator] = useState(false);

  const fetchGroupNames = async () => {
    try {
      const response = await fetch(`${API_BASE}/group-names`);
      const data = await response.json();
      setGroupNames(data);
      // Check if we need to show scroll indicator (more than 3 items)
      setShowScrollIndicator(data.length > 3);
    } catch (error) {
      console.error("Failed to fetch group names:", error);
    }
  };

  useEffect(() => {
    fetchGroupNames();
  }, []);

  const handleAdd = async () => {
    if (!newGroupName.trim()) {
      toast({ title: "Please enter a group name", variant: "destructive" });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/group-names`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newGroupName.trim() }),
      });
      const data = await response.json();

      if (data.status === "exists") {
        toast({ title: "Group name already exists", variant: "destructive" });
      } else {
        toast({ title: "Group name added successfully" });
        setNewGroupName("");
        fetchGroupNames();
        onGroupNamesChange?.();
      }
    } catch (error) {
      toast({ title: "Failed to add group name", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (name: string) => {
    setLoading(true);
    try {
      await fetch(`${API_BASE}/group-names/${encodeURIComponent(name)}`, {
        method: "DELETE",
      });
      toast({ title: "Group name deleted successfully" });
      fetchGroupNames();
      onGroupNamesChange?.();
    } catch (error) {
      toast({ title: "Failed to delete group name", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-[var(--shadow-card)]">
      <CardHeader className="pb-2 pt-4">
        <CardTitle className="flex items-center gap-1.5 text-base">
          <Users className="h-3.5 w-3.5" />
          Group Names
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex gap-1.5">
          <Input
            placeholder="Add group..."
            value={newGroupName}
            onChange={(e) => setNewGroupName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
            disabled={loading}
            className="h-8 text-sm"
          />
          <Button onClick={handleAdd} disabled={loading} size="icon" className="h-8 w-8">
            <Plus className="h-3.5 w-3.5" />
          </Button>
        </div>

        <div className="space-y-1">
          {groupNames.length === 0 ? (
            <p className="text-xs text-muted-foreground text-center py-1">
              No groups yet
            </p>
          ) : (
            <>
              <div className="flex items-center justify-between">
                <div className="text-[10px] text-muted-foreground">
                  {groupNames.length} group{groupNames.length !== 1 ? 's' : ''}
                </div>
                {showScrollIndicator && (
                  <div className="flex items-center gap-0.5 text-[10px] text-muted-foreground animate-bounce">
                    <span>scroll</span>
                    <ChevronDown className="h-2.5 w-2.5" />
                  </div>
                )}
              </div>
              <div className="max-h-[120px] overflow-y-auto space-y-1 pr-1 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
                {groupNames.map((name) => (
                  <div
                    key={name}
                    className="flex items-center justify-between p-1 rounded border bg-card hover:bg-accent/50 transition-colors"
                  >
                    <span className="text-xs px-1.5">{name}</span>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleDelete(name)}
                      disabled={loading}
                      className="h-6 w-6 text-destructive hover:text-destructive"
                    >
                      <Trash2 className="h-2.5 w-2.5" />
                    </Button>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
