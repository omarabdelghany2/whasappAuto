import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from concurrent.futures import ThreadPoolExecutor
import os
import json
import shutil
from pathlib import Path

from whatsapp_bot import WhatsAppBot
from scheduler import MessageScheduler

logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp Scheduler API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend origin(s) for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Single bot instance and scheduler
bot: Optional[WhatsAppBot] = None
scheduler: Optional[MessageScheduler] = None
executor = ThreadPoolExecutor(max_workers=4)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Group names file
GROUP_NAMES_FILE = "group_names.json"


class LoadSchedulesBody(BaseModel):
    entries: Optional[list] = None


class GroupNameBody(BaseModel):
    name: str


@app.on_event("startup")
def startup_event():
    global bot, scheduler
    logger.info("API server startup: initializing components without launching WhatsApp")
    # Create bot instance but do NOT start Chrome yet
    bot = WhatsAppBot(headless=False)
    # Create scheduler bound to bot
    scheduler = MessageScheduler(bot)
    # Load schedules if present (no execution until /scheduler/start)
    schedules_path = os.path.join(os.getcwd(), 'schedules.json')
    try:
        scheduler.load_schedules_from_file(schedules_path)
    except Exception as e:
        logger.warning(f"Could not load schedules: {e}")
    logger.info("API server startup complete (WhatsApp not launched; scheduler not running)")


@app.on_event("shutdown")
def shutdown_event():
    global bot, scheduler
    if scheduler:
        scheduler.stop_background()
    if bot:
        bot.close()


"""Immediate send endpoints removed; scheduling-only API."""


"""Per-type schedule endpoints removed; use /schedules/load with entries list."""


@app.get("/schedules")
def list_schedules():
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    # Prefer returning the persisted JSON as-is if available
    try:
        with open('schedules.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        # Fallback to in-memory normalized entries
        return scheduler.scheduled_messages


@app.post("/schedules/save")
def save_schedules():
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    scheduler.save_schedules_to_file('schedules.json')
    return {"status": "saved"}


@app.post("/schedules/load")
def load_schedules(body: Optional[LoadSchedulesBody] = None):
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    # If entries provided, replace in-memory and persist; otherwise load from file
    if body and body.entries is not None:
        scheduler.reset_with_entries(body.entries)
        try:
            with open('schedules.json', 'w', encoding='utf-8') as f:
                json.dump(body.entries, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed saving schedules.json: {e}")
        return {"status": "loaded", "source": "body", "count": len(body.entries)}
    else:
        scheduler.load_schedules_from_file('schedules.json', replace=True)
        return {"status": "loaded", "source": "file"}


@app.get("/scheduler/status")
def scheduler_status():
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    return {"running": scheduler.is_running(), "count": len(scheduler.scheduled_messages)}


@app.post("/scheduler/start")
def scheduler_start():
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    if scheduler.is_running():
        return {"running": True, "message": "Scheduler already running"}
    # Do NOT launch WhatsApp here; jobs will start the bot lazily when due
    scheduler.start_background()
    return {"running": True}


@app.post("/scheduler/stop")
def scheduler_stop():
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")
    if not scheduler.is_running():
        return {"running": False, "message": "Scheduler already stopped"}
    scheduler.stop_background()
    return {"running": False}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an image file and return the absolute path.
    This allows the frontend to upload files and get a real path for scheduling.
    """
    try:
        # Create a safe filename
        safe_filename = file.filename.replace(" ", "_")
        file_path = UPLOADS_DIR / safe_filename

        # If file already exists, add a number to make it unique
        counter = 1
        original_path = file_path
        while file_path.exists():
            stem = original_path.stem
            suffix = original_path.suffix
            file_path = UPLOADS_DIR / f"{stem}_{counter}{suffix}"
            counter += 1

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the absolute path
        absolute_path = str(file_path.absolute())
        logger.info(f"File uploaded successfully: {absolute_path}")

        return {
            "status": "success",
            "filename": file.filename,
            "path": absolute_path
        }
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@app.get("/finished-schedules")
def get_finished_schedules():
    """
    Get all completed schedules from finishedSchedules.json
    """
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")

    try:
        finished = scheduler.get_finished_schedules()
        return finished
    except Exception as e:
        logger.error(f"Error getting finished schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting finished schedules: {str(e)}")


@app.delete("/finished-schedules/{index}")
def delete_finished_schedule(index: int):
    """
    Delete a finished schedule by index
    """
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")

    try:
        success = scheduler.delete_finished_schedule(index)
        if success:
            return {"status": "deleted", "index": index}
        else:
            raise HTTPException(status_code=404, detail="Schedule not found or invalid index")
    except Exception as e:
        logger.error(f"Error deleting finished schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting finished schedule: {str(e)}")


@app.delete("/finished-schedules")
def clear_all_finished_schedules():
    """
    Clear all finished schedules
    """
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")

    try:
        success = scheduler.clear_all_finished_schedules()
        if success:
            return {"status": "cleared"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear schedules")
    except Exception as e:
        logger.error(f"Error clearing finished schedules: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error clearing finished schedules: {str(e)}")


@app.get("/whatsapp/status")
def whatsapp_status():
    """
    Check if WhatsApp session exists (logged in previously).
    Note: Browser is closed between messages, but session is saved.
    """
    global bot
    if not bot:
        return {"connected": False, "message": "Bot not initialized"}

    try:
        import os
        # Check if chrome_data profile exists (indicates previous login)
        chrome_data_path = "./chrome_data"
        if os.path.exists(chrome_data_path) and os.path.isdir(chrome_data_path):
            # Check if there's actual session data
            session_files = os.listdir(chrome_data_path)
            if len(session_files) > 0:
                return {"connected": True, "message": "Session saved (logged in)"}

        return {"connected": False, "message": "Not logged in - Click Login button"}
    except Exception as e:
        return {"connected": False, "message": f"Error: {str(e)}"}


@app.post("/whatsapp/login")
def whatsapp_login():
    """
    Simply open WhatsApp Web for login.
    User will manually scan QR code and close browser when done.
    """
    global bot
    if not bot:
        raise HTTPException(status_code=500, detail="Bot not initialized")

    try:
        logger.info("Opening WhatsApp Web for login...")

        # Just start the bot (opens Chrome with WhatsApp Web)
        bot.start()

        return {
            "status": "opened",
            "message": "WhatsApp Web opened. Scan QR code and close browser when done."
        }

    except Exception as e:
        logger.error(f"Error opening WhatsApp Web: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error opening WhatsApp Web: {str(e)}")


@app.get("/group-names")
def get_group_names():
    """
    Get list of saved group names
    """
    try:
        if os.path.exists(GROUP_NAMES_FILE):
            with open(GROUP_NAMES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("groups", [])
        return []
    except Exception as e:
        logger.error(f"Error getting group names: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting group names: {str(e)}")


@app.post("/group-names")
def add_group_name(body: GroupNameBody):
    """
    Add a new group name
    """
    try:
        groups = []
        if os.path.exists(GROUP_NAMES_FILE):
            with open(GROUP_NAMES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                groups = data.get("groups", [])

        # Check if group name already exists
        if body.name in groups:
            return {"status": "exists", "message": "Group name already exists"}

        # Add new group name
        groups.append(body.name)

        # Save to file
        with open(GROUP_NAMES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"groups": groups}, f, indent=2, ensure_ascii=False)

        return {"status": "added", "groups": groups}
    except Exception as e:
        logger.error(f"Error adding group name: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error adding group name: {str(e)}")


@app.delete("/group-names/{name}")
def delete_group_name(name: str):
    """
    Delete a group name
    """
    try:
        if not os.path.exists(GROUP_NAMES_FILE):
            raise HTTPException(status_code=404, detail="No group names found")

        with open(GROUP_NAMES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            groups = data.get("groups", [])

        if name not in groups:
            raise HTTPException(status_code=404, detail="Group name not found")

        # Remove group name
        groups.remove(name)

        # Save to file
        with open(GROUP_NAMES_FILE, 'w', encoding='utf-8') as f:
            json.dump({"groups": groups}, f, indent=2, ensure_ascii=False)

        return {"status": "deleted", "groups": groups}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting group name: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting group name: {str(e)}")


# For local running: uvicorn server:app --reload

