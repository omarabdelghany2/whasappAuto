import schedule
import time
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
import threading
from whatsapp_bot import WhatsAppBot

logger = logging.getLogger(__name__)


class MessageScheduler:
    """Scheduler for WhatsApp messages"""

    def __init__(self, bot: WhatsAppBot):
        """
        Initialize the scheduler

        Args:
            bot (WhatsAppBot): Instance of WhatsAppBot
        """
        self.bot = bot
        self.scheduled_messages = []
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.finished_schedules_file = 'finishedSchedules.json'

    def schedule_message(self, group_name: str, message: str, scheduled_time: str, repeat: str = "once", profile_name: str = None, batch_id: str = None):
        """
        Schedule a message to be sent

        Args:
            group_name (str): Name of the WhatsApp group
            message (str): Message to send
            scheduled_time (str): Time to send message (format: "HH:MM" for time, or "2023-12-25 14:30" for specific date)
            repeat (str): Repeat frequency ("once", "daily", "hourly", or specific day like "monday")
            profile_name (str): Chrome profile name to use (optional)
            batch_id (str): Batch ID for multi-group schedules (optional)
        """
        entry = {
            "group_name": group_name,
            "message": message,
            "scheduled_time": scheduled_time,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "message",
            "status": "pending",
            "profile_name": profile_name,
            "batch_id": batch_id
        }

        self.scheduled_messages.append(entry)

        # Create the job
        def job():
            self._ensure_bot_ready(profile_name)
            logger.info(f"Executing scheduled message to '{group_name}'")
            success = self.bot.send_message_to_group(group_name, message)
            if success:
                logger.info(f"Scheduled message sent successfully to '{group_name}'")
                try:
                    entry["status"] = "done"
                    entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Save to finished schedules
                    self.save_to_finished_schedules(entry)

                    # persist current schedules
                    self.save_schedules_to_file('schedules.json')
                    if repeat == "once":
                        try:
                            self.scheduled_messages.remove(entry)
                            self.save_schedules_to_file('schedules.json')
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Could not mark schedule as done: {e}")

                # Close browser only if no upcoming schedules in same batch
                try:
                    if self.bot and self.bot.driver:
                        if entry.get("batch_id") and self._has_upcoming_schedules(within_minutes=10, batch_id=entry.get("batch_id")):
                            logger.info(f"Keeping browser open - more schedules in batch {entry.get('batch_id')} coming up soon")
                        else:
                            logger.info("Closing browser after successful scheduled job...")
                            self.bot.close()
                except Exception as e:
                    logger.warning(f"Error closing browser after scheduled job: {e}")
            else:
                logger.error(f"Failed to send scheduled message to '{group_name}'")
                logger.warning(f"Browser kept open for debugging. Please check WhatsApp Web.")

        # Schedule using unified helper (supports absolute datetime or time-only)
        self._schedule_by_repeat(job, repeat, scheduled_time)

        logger.info(f"Message scheduled: {group_name} at {scheduled_time} ({repeat})")

    def schedule_image(self, group_name: str, image_path: str, caption: Optional[str], scheduled_time: str, repeat: str = "once", profile_name: str = None, batch_id: str = None):
        """Schedule an image to be sent."""
        entry = {
            "type": "image",
            "group_name": group_name,
            "image_path": image_path,
            "caption": caption,
            "scheduled_time": scheduled_time,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",
            "profile_name": profile_name,
            "batch_id": batch_id
        }
        self.scheduled_messages.append(entry)

        def job():
            self._ensure_bot_ready(profile_name)
            logger.info(f"Executing scheduled image to '{group_name}'")
            success = self.bot.send_image_to_group(group_name, image_path, caption)
            if success:
                logger.info(f"Scheduled image sent successfully to '{group_name}'")
                try:
                    entry["status"] = "done"
                    entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Save to finished schedules
                    self.save_to_finished_schedules(entry)

                    self.save_schedules_to_file('schedules.json')
                    if repeat == "once":
                        try:
                            self.scheduled_messages.remove(entry)
                            self.save_schedules_to_file('schedules.json')
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Could not mark schedule as done: {e}")

                # Close browser only if no upcoming schedules
                try:
                    if self.bot and self.bot.driver:
                        # Check for upcoming schedules in the same batch first (within 2 minutes for batch jobs)
                        if batch_id and self._has_upcoming_schedules(within_minutes=2, batch_id=batch_id):
                            logger.info(f"Keeping browser open - more schedules in batch '{batch_id}' coming up soon")
                        elif self._has_upcoming_schedules(within_minutes=10):
                            logger.info("Keeping browser open - more schedules coming up soon")
                        else:
                            logger.info("Closing browser after successful scheduled job...")
                            self.bot.close()
                except Exception as e:
                    logger.warning(f"Error closing browser after scheduled job: {e}")
            else:
                logger.error(f"Failed to send scheduled image to '{group_name}'")
                logger.warning(f"Browser kept open for debugging. Please check WhatsApp Web.")

        self._schedule_by_repeat(job, repeat, scheduled_time)
        logger.info(f"Image scheduled: {group_name} at {scheduled_time} ({repeat})")

    def schedule_video(self, group_name: str, video_path: str, caption: Optional[str], scheduled_time: str, repeat: str = "once", profile_name: str = None, batch_id: str = None):
        """Schedule a video to be sent."""
        entry = {
            "type": "video",
            "group_name": group_name,
            "video_path": video_path,
            "caption": caption,
            "scheduled_time": scheduled_time,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",
            "profile_name": profile_name,
            "batch_id": batch_id
        }
        self.scheduled_messages.append(entry)

        def job():
            self._ensure_bot_ready(profile_name)
            logger.info(f"Executing scheduled video to '{group_name}'")
            success = self.bot.send_video_to_group(group_name, video_path, caption)
            if success:
                logger.info(f"Scheduled video sent successfully to '{group_name}'")
                try:
                    entry["status"] = "done"
                    entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Save to finished schedules
                    self.save_to_finished_schedules(entry)

                    self.save_schedules_to_file('schedules.json')
                    if repeat == "once":
                        try:
                            self.scheduled_messages.remove(entry)
                            self.save_schedules_to_file('schedules.json')
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Could not mark schedule as done: {e}")

                # Close browser only if no upcoming schedules
                try:
                    if self.bot and self.bot.driver:
                        # Check for upcoming schedules in the same batch first (within 2 minutes for batch jobs)
                        if batch_id and self._has_upcoming_schedules(within_minutes=2, batch_id=batch_id):
                            logger.info(f"Keeping browser open - more schedules in batch '{batch_id}' coming up soon")
                        elif self._has_upcoming_schedules(within_minutes=10):
                            logger.info("Keeping browser open - more schedules coming up soon")
                        else:
                            logger.info("Closing browser after successful scheduled job...")
                            self.bot.close()
                except Exception as e:
                    logger.warning(f"Error closing browser after scheduled job: {e}")
            else:
                logger.error(f"Failed to send scheduled video to '{group_name}'")
                logger.warning(f"Browser kept open for debugging. Please check WhatsApp Web.")

        self._schedule_by_repeat(job, repeat, scheduled_time)
        logger.info(f"Video scheduled: {group_name} at {scheduled_time} ({repeat})")

    def schedule_poll(self, group_name: str, question: str, options: List[str], allow_multiple: bool, scheduled_time: str, repeat: str = "once", profile_name: str = None, batch_id: str = None):
        """Schedule a poll to be sent."""
        entry = {
            "type": "poll",
            "group_name": group_name,
            "question": question,
            "options": options,
            "allow_multiple": allow_multiple,
            "scheduled_time": scheduled_time,
            "repeat": repeat,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending",
            "profile_name": profile_name,
            "batch_id": batch_id
        }
        self.scheduled_messages.append(entry)

        def job():
            self._ensure_bot_ready(profile_name)
            logger.info(f"Executing scheduled poll to '{group_name}'")
            success = self.bot.send_poll_to_group(group_name, question, options, allow_multiple)
            if success:
                logger.info(f"Scheduled poll sent successfully to '{group_name}'")
                try:
                    entry["status"] = "done"
                    entry["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Save to finished schedules
                    self.save_to_finished_schedules(entry)

                    self.save_schedules_to_file('schedules.json')
                    if repeat == "once":
                        try:
                            self.scheduled_messages.remove(entry)
                            self.save_schedules_to_file('schedules.json')
                        except Exception:
                            pass
                except Exception as e:
                    logger.warning(f"Could not mark schedule as done: {e}")

                # Close browser only if no upcoming schedules
                try:
                    if self.bot and self.bot.driver:
                        # Check for upcoming schedules in the same batch first (within 2 minutes for batch jobs)
                        if batch_id and self._has_upcoming_schedules(within_minutes=2, batch_id=batch_id):
                            logger.info(f"Keeping browser open - more schedules in batch '{batch_id}' coming up soon")
                        elif self._has_upcoming_schedules(within_minutes=10):
                            logger.info("Keeping browser open - more schedules coming up soon")
                        else:
                            logger.info("Closing browser after successful scheduled job...")
                            self.bot.close()
                except Exception as e:
                    logger.warning(f"Error closing browser after scheduled job: {e}")
            else:
                logger.error(f"Failed to send scheduled poll to '{group_name}'")
                logger.warning(f"Browser kept open for debugging. Please check WhatsApp Web.")

        self._schedule_by_repeat(job, repeat, scheduled_time)
        logger.info(f"Poll scheduled: {group_name} at {scheduled_time} ({repeat})")

    def _schedule_by_repeat(self, job: Callable[[], None], repeat: str, scheduled_time: str):
        # Support absolute datetime strings like "2025-10-29 15:30" (or with seconds)
        absolute_dt: Optional[datetime] = None
        time_only: Optional[str] = None
        if scheduled_time:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    absolute_dt = datetime.strptime(scheduled_time, fmt)
                    break
                except ValueError:
                    continue
            if absolute_dt is None:
                # treat as time-only
                time_only = scheduled_time

        if repeat == "once":
            if absolute_dt is not None:
                # Normalize both times to ignore seconds for comparison
                absolute_dt_normalized = absolute_dt.replace(second=0, microsecond=0)
                now_normalized = datetime.now().replace(second=0, microsecond=0)
                delta = (absolute_dt_normalized - now_normalized)
                delay_seconds = int(delta.total_seconds())

                # Allow schedules in the current minute (delay_seconds == 0) to run immediately
                if delay_seconds < 0:
                    logger.warning(f"Scheduled time {absolute_dt} is in the past; skipping job")
                    return

                job_ref = None
                def wrapper():
                    nonlocal job_ref
                    job()
                    try:
                        schedule.cancel_job(job_ref)  # type: ignore
                    except Exception:
                        pass

                # If delay is 0 (current minute), run immediately
                if delay_seconds == 0:
                    logger.info(f"Schedule for {absolute_dt} is in current minute ({datetime.now()}), running immediately")
                    # Schedule to run in the next second to ensure bot is ready
                    job_ref = schedule.every(1).seconds.do(wrapper).tag(f"once-{len(self.scheduled_messages)}")
                else:
                    job_ref = schedule.every(delay_seconds).seconds.do(wrapper).tag(f"once-{len(self.scheduled_messages)}")
            else:
                job_ref = None
                def wrapper():
                    nonlocal job_ref
                    job()
                    try:
                        schedule.cancel_job(job_ref)  # type: ignore
                    except Exception:
                        pass
                job_ref = schedule.every().day.at(time_only or scheduled_time).do(wrapper).tag(f"once-{len(self.scheduled_messages)}")
        elif repeat == "daily":
            schedule.every().day.at((absolute_dt.strftime("%H:%M:%S") if absolute_dt else (time_only or scheduled_time))).do(job)
        elif repeat == "hourly":
            schedule.every().hour.do(job)
        elif repeat in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            getattr(schedule.every(), repeat).at((absolute_dt.strftime("%H:%M:%S") if absolute_dt else (time_only or scheduled_time))).do(job)
        else:
            logger.warning(f"Unknown repeat type: {repeat}. Defaulting to 'once'")
            if absolute_dt is not None:
                # Normalize both times to ignore seconds for comparison
                absolute_dt_normalized = absolute_dt.replace(second=0, microsecond=0)
                now_normalized = datetime.now().replace(second=0, microsecond=0)
                delta = (absolute_dt_normalized - now_normalized)
                delay_seconds = int(delta.total_seconds())
                if delay_seconds < 0:
                    logger.warning(f"Scheduled time {absolute_dt} is in the past; skipping job")
                elif delay_seconds == 0:
                    # Run in next second if in current minute
                    logger.info(f"Schedule for {absolute_dt} is in current minute ({datetime.now()}), scheduling for immediate execution")
                    schedule.every(1).seconds.do(job).tag(f"once-{len(self.scheduled_messages)}")
                else:
                    schedule.every(delay_seconds).seconds.do(job).tag(f"once-{len(self.scheduled_messages)}")
            else:
                schedule.every().day.at(time_only or scheduled_time).do(job).tag(f"once-{len(self.scheduled_messages)}")

    def add_immediate_message(self, group_name: str, message: str, delay_seconds: int = 0):
        """
        Send a message immediately or after a short delay

        Args:
            group_name (str): Name of the WhatsApp group
            message (str): Message to send
            delay_seconds (int): Delay before sending (in seconds)
        """
        def job():
            logger.info(f"Sending immediate message to '{group_name}'")
            self.bot.send_message_to_group(group_name, message)

        if delay_seconds > 0:
            schedule.every(delay_seconds).seconds.do(job).tag("immediate")
            logger.info(f"Immediate message scheduled with {delay_seconds}s delay to '{group_name}'")
        else:
            job()

    def load_schedules_from_file(self, file_path: str, replace: bool = True):
        """
        Load scheduled messages from a JSON file

        Args:
            file_path (str): Path to JSON file with scheduled messages
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                schedules = json.load(f)

            if replace:
                # Clear in-memory list and pending jobs
                self.clear_all()

            for schedule_data in schedules:
                typ = schedule_data.get("type", "message")
                profile_name = schedule_data.get("profile_name")
                batch_id = schedule_data.get("batch_id")
                if typ == "image":
                    self.schedule_image(
                        group_name=schedule_data.get("group_name"),
                        image_path=schedule_data.get("image_path"),
                        caption=schedule_data.get("caption"),
                        scheduled_time=schedule_data.get("time") or schedule_data.get("scheduled_time"),
                        repeat=schedule_data.get("repeat", "once"),
                        profile_name=profile_name,
                        batch_id=batch_id
                    )
                elif typ == "video":
                    self.schedule_video(
                        group_name=schedule_data.get("group_name"),
                        video_path=schedule_data.get("video_path"),
                        caption=schedule_data.get("caption"),
                        scheduled_time=schedule_data.get("time") or schedule_data.get("scheduled_time"),
                        repeat=schedule_data.get("repeat", "once"),
                        profile_name=profile_name,
                        batch_id=batch_id
                    )
                elif typ == "poll":
                    self.schedule_poll(
                        group_name=schedule_data.get("group_name"),
                        question=schedule_data.get("question"),
                        options=schedule_data.get("options", []),
                        allow_multiple=bool(schedule_data.get("allow_multiple", False)),
                        scheduled_time=schedule_data.get("time") or schedule_data.get("scheduled_time"),
                        repeat=schedule_data.get("repeat", "once"),
                        profile_name=profile_name,
                        batch_id=batch_id
                    )
                else:
                    self.schedule_message(
                        group_name=schedule_data.get("group_name"),
                        message=schedule_data.get("message"),
                        scheduled_time=schedule_data.get("time") or schedule_data.get("scheduled_time"),
                        repeat=schedule_data.get("repeat", "once"),
                        profile_name=profile_name,
                        batch_id=batch_id
                    )

            logger.info(f"Loaded {len(schedules)} scheduled messages from {file_path}")

        except FileNotFoundError:
            logger.warning(f"Schedule file not found: {file_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from {file_path}: {str(e)}")

    def save_schedules_to_file(self, file_path: str):
        """
        Save scheduled messages to a JSON file

        Args:
            file_path (str): Path to save the JSON file
        """
        try:
            # Ensure a stable schema
            normalized: List[Dict] = []
            for entry in self.scheduled_messages:
                e = dict(entry)
                # unify time key
                if 'scheduled_time' in e and 'time' not in e:
                    e['time'] = e['scheduled_time']
                normalized.append(e)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(normalized, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved {len(self.scheduled_messages)} scheduled messages to {file_path}")

        except Exception as e:
            logger.error(f"Error saving schedules to {file_path}: {str(e)}")

    def save_to_finished_schedules(self, entry: Dict):
        """
        Save a completed schedule to the finished schedules file

        Args:
            entry (Dict): The completed schedule entry
        """
        try:
            # Load existing finished schedules
            finished_schedules = []
            try:
                with open(self.finished_schedules_file, 'r', encoding='utf-8') as f:
                    finished_schedules = json.load(f)
            except FileNotFoundError:
                pass  # File doesn't exist yet, that's fine

            # Add the new finished schedule
            finished_entry = dict(entry)
            # Ensure it has the time key
            if 'scheduled_time' in finished_entry and 'time' not in finished_entry:
                finished_entry['time'] = finished_entry['scheduled_time']

            finished_schedules.append(finished_entry)

            # Save back to file
            with open(self.finished_schedules_file, 'w', encoding='utf-8') as f:
                json.dump(finished_schedules, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved finished schedule to {self.finished_schedules_file}")

        except Exception as e:
            logger.error(f"Error saving to finished schedules: {str(e)}")

    def get_finished_schedules(self) -> List[Dict]:
        """
        Get all finished schedules, ordered by latest first

        Returns:
            List[Dict]: List of finished schedules (newest first)
        """
        try:
            with open(self.finished_schedules_file, 'r', encoding='utf-8') as f:
                schedules = json.load(f)
                # Sort by completed_at timestamp, newest first
                schedules.sort(key=lambda x: x.get('completed_at', ''), reverse=True)
                return schedules
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"Error reading finished schedules: {str(e)}")
            return []

    def delete_finished_schedule(self, index: int) -> bool:
        """
        Delete a finished schedule by index

        Args:
            index (int): Index of the schedule to delete

        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            finished_schedules = self.get_finished_schedules()

            if index < 0 or index >= len(finished_schedules):
                logger.error(f"Invalid index {index} for finished schedules")
                return False

            # Remove the schedule at the specified index
            deleted_schedule = finished_schedules.pop(index)

            # Save back to file
            with open(self.finished_schedules_file, 'w', encoding='utf-8') as f:
                json.dump(finished_schedules, f, indent=2, ensure_ascii=False)

            logger.info(f"Deleted finished schedule at index {index}: {deleted_schedule.get('group_name', 'Unknown')}")
            return True

        except Exception as e:
            logger.error(f"Error deleting finished schedule: {str(e)}")
            return False

    def clear_all_finished_schedules(self) -> bool:
        """
        Clear all finished schedules

        Returns:
            bool: True if cleared successfully, False otherwise
        """
        try:
            with open(self.finished_schedules_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)

            logger.info("Cleared all finished schedules")
            return True

        except Exception as e:
            logger.error(f"Error clearing finished schedules: {str(e)}")
            return False

    def clear_all(self):
        """Clear all scheduled jobs and in-memory entries."""
        try:
            schedule.clear()
        except Exception:
            pass
        self.scheduled_messages = []

    def reset_with_entries(self, entries: List[Dict]):
        """Replace all scheduled entries with the provided list and reschedule."""
        self.clear_all()
        for data in entries:
            typ = data.get("type", "message")
            batch_id = data.get("batch_id")
            if typ == "image":
                self.schedule_image(
                    group_name=data.get("group_name"),
                    image_path=data.get("image_path"),
                    caption=data.get("caption"),
                    scheduled_time=data.get("time") or data.get("scheduled_time"),
                    repeat=data.get("repeat", "once"),
                    batch_id=batch_id
                )
            elif typ == "video":
                self.schedule_video(
                    group_name=data.get("group_name"),
                    video_path=data.get("video_path"),
                    caption=data.get("caption"),
                    scheduled_time=data.get("time") or data.get("scheduled_time"),
                    repeat=data.get("repeat", "once"),
                    batch_id=batch_id
                )
            elif typ == "poll":
                self.schedule_poll(
                    group_name=data.get("group_name"),
                    question=data.get("question"),
                    options=data.get("options", []),
                    allow_multiple=bool(data.get("allow_multiple", False)),
                    scheduled_time=data.get("time") or data.get("scheduled_time"),
                    repeat=data.get("repeat", "once"),
                    batch_id=batch_id
                )
            else:
                self.schedule_message(
                    group_name=data.get("group_name"),
                    message=data.get("message"),
                    scheduled_time=data.get("time") or data.get("scheduled_time"),
                    repeat=data.get("repeat", "once"),
                    batch_id=batch_id
                )

    def list_scheduled_messages(self):
        """List all scheduled messages"""
        if not self.scheduled_messages:
            logger.info("No scheduled messages")
            return

        logger.info(f"\n{'='*60}")
        logger.info(f"{'SCHEDULED MESSAGES':^60}")
        logger.info(f"{'='*60}")

        for i, msg in enumerate(self.scheduled_messages, 1):
            logger.info(f"\nMessage #{i}:")
            logger.info(f"  Group: {msg['group_name']}")
            logger.info(f"  Time: {msg['scheduled_time']}")
            logger.info(f"  Repeat: {msg['repeat']}")
            logger.info(f"  Message: {msg['message'][:50]}...")
            logger.info(f"  Created: {msg['created_at']}")

        logger.info(f"\n{'='*60}\n")

    def run(self):
        """Run the scheduler loop"""
        logger.info("Starting message scheduler...")
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")

    def start_background(self):
        """Start scheduler loop in a background thread."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()

        def loop():
            logger.info("Scheduler background thread started")
            while not self._stop_event.is_set():
                try:
                    schedule.run_pending()
                except Exception as e:
                    logger.error(f"Error running scheduled job: {str(e)}")
                    import traceback
                    traceback.print_exc()
                time.sleep(1)
            logger.info("Scheduler background thread stopped")

        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop_background(self):
        """Stop the background scheduler thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def is_running(self) -> bool:
        """Return True if the scheduler background thread is running."""
        return bool(self._thread and self._thread.is_alive() and not self._stop_event.is_set())

    def _has_upcoming_schedules(self, within_minutes: int = 10, batch_id: str = None) -> bool:
        """
        Check if there are any pending schedules within the next N minutes.

        Args:
            within_minutes (int): Look ahead this many minutes
            batch_id (str): If provided, only check schedules with this batch_id

        Returns:
            bool: True if there are upcoming schedules
        """
        now = datetime.now()
        cutoff = now + timedelta(minutes=within_minutes)

        for entry in self.scheduled_messages:
            # Skip if already done
            if entry.get("status") == "done":
                continue

            # If batch_id is provided, only check schedules with matching batch_id
            if batch_id and entry.get("batch_id") != batch_id:
                continue

            # Parse the scheduled time
            scheduled_time_str = entry.get("scheduled_time") or entry.get("time")
            if not scheduled_time_str:
                continue

            try:
                # Try parsing with different formats
                scheduled_time = None
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                    try:
                        scheduled_time = datetime.strptime(scheduled_time_str, fmt)
                        break
                    except ValueError:
                        continue

                if scheduled_time and now <= scheduled_time <= cutoff:
                    logger.info(f"Found upcoming schedule for {entry.get('group_name')} at {scheduled_time} (batch: {entry.get('batch_id', 'none')})")
                    return True
            except Exception as e:
                logger.warning(f"Error parsing schedule time {scheduled_time_str}: {e}")
                continue

        return False

    def _ensure_bot_ready(self, profile_name: str = None):
        """
        Start WhatsApp bot lazily if needed before executing a job.

        Args:
            profile_name (str): Chrome profile name to use (optional)
        """
        try:
            if self.bot is None:
                raise RuntimeError("Bot not initialized")
            needs_start = False
            if getattr(self.bot, 'driver', None) is None:
                needs_start = True
                logger.info("Browser not started yet, will start now...")
            else:
                try:
                    # Touch driver to ensure it's alive
                    _ = self.bot.driver.current_url  # may raise if closed
                    logger.info("Browser is already running and alive")
                except Exception as e:
                    needs_start = True
                    logger.info(f"Browser was closed or crashed, will restart: {e}")
            if needs_start:
                # Get the profile path from chrome_profiles module
                profile_path = None
                if profile_name:
                    try:
                        from chrome_profiles import list_chrome_profiles
                        profiles = list_chrome_profiles()
                        for profile in profiles:
                            if profile.get('name') == profile_name:
                                profile_path = profile.get('path')
                                logger.info(f"Using Chrome profile '{profile_name}' at: {profile_path}")
                                break
                        if not profile_path:
                            logger.warning(f"Chrome profile '{profile_name}' not found, using default")
                    except ImportError:
                        logger.info("chrome_profiles module not available, using default profile")

                logger.info("Starting WhatsApp bot for scheduled job...")
                self.bot.start(profile_path=profile_path)
                logger.info("Waiting for WhatsApp Web to load...")
                self.bot.wait_for_whatsapp_load(timeout=180)
                logger.info("WhatsApp Web loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to prepare WhatsApp bot: {e}")
            import traceback
            traceback.print_exc()
            raise  # Re-raise the exception so the job knows it failed


if __name__ == "__main__":
    # Test the scheduler
    bot = WhatsAppBot()

    try:
        bot.start()
        bot.wait_for_whatsapp_load()

        scheduler = MessageScheduler(bot)

        # Example: Schedule a message
        scheduler.schedule_message(
            group_name="Cairo",
            message="This is a scheduled test message!",
            scheduled_time="15:30",
            repeat="daily"
        )

        scheduler.list_scheduled_messages()
        scheduler.run()

    except KeyboardInterrupt:
        logger.info("Program stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        bot.close()
