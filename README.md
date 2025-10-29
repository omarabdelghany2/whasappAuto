# WhatsApp Message Scheduler

Automate sending messages to WhatsApp Web groups with scheduling capabilities. Features both a modern web UI and CLI interface.

## Features

### Core Features
- 📱 Send messages, images, and polls to WhatsApp groups
- ⏰ Schedule messages for specific times with various repeat options
- 🔄 Recurring messages (daily, hourly, specific days)
- 🌐 **Web UI with React frontend** for easy management
- 🔌 **REST API with FastAPI backend** for programmatic access
- 📁 File upload system for images
- 📊 Track completed schedules history
- 🗑️ Delete finished schedules (individual or bulk)
- 🔒 Browser automation with QR code authentication
- 🚀 Auto-close browser after scheduled jobs complete
- 💾 Persistent schedule storage in JSON files

## Architecture

The project consists of three main components:

1. **Backend API** (`server.py`) - FastAPI REST API server
2. **Scheduler** (`scheduler.py`) - Background job scheduler
3. **WhatsApp Bot** (`whatsapp_bot.py`) - Selenium-based WhatsApp Web automation
4. **Frontend UI** (`Frontend/`) - React-based web interface

## Installation

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
# or using pipenv
pipenv install
```

2. Make sure you have Chrome browser installed

### Frontend Setup

1. Navigate to the Frontend directory:
```bash
cd Frontend
npm install
```

2. Build the frontend:
```bash
npm run build
```

## Usage

### Option 1: Web UI (Recommended)

1. **Start the backend server:**
```bash
pipenv run uvicorn server:app --reload
# Server runs on http://localhost:8000
```

2. **Start the frontend (in another terminal):**
```bash
cd Frontend
npm run dev
# Frontend runs on http://localhost:5173
```

3. **Open your browser** and navigate to `http://localhost:5173`

4. **Using the Web UI:**
   - Click "Start" to start the scheduler
   - Add schedules using the form (messages, images, or polls)
   - View all pending schedules in the main view
   - Edit or delete schedules with the action buttons
   - View completed schedules by clicking "Finished"
   - Delete individual or all finished schedules

### Option 2: CLI (Command Line)

### First Time Setup

On first run, you'll need to scan the WhatsApp Web QR code. The session will be saved for future use.

### Send Immediate Message

```bash
python main.py send --group "Cairo" --message "Hello from the bot!"
```

### Send Image with Caption

Send an image with optional caption:
```bash
python main.py send-image --group "Cairo" --image "/path/to/image.jpg" --caption "hey ya regalaa am omar"
```

Send image without caption:
```bash
python main.py send-image --group "Cairo" --image "/path/to/photo.png"
```

Or use the test script:
```bash
pipenv run python test_send_image.py "/path/to/image.jpg" "hey ya regalaa am omar"
```

### Send Poll

Send a poll with multiple choice options:
```bash
python main.py send-poll --group "Cairo" --question "What's your favorite food?" --options Pizza Burger Pasta
```

Allow multiple answers:
```bash
python main.py send-poll --group "Cairo" --question "Select all you like" --options Coffee Tea Juice --multiple
```

Or use the test script:
```bash
pipenv run python test_send_poll.py "What's your favorite?" Pizza Burger Pasta

# With multiple answers
pipenv run python test_send_poll.py "Select all you like" Coffee Tea Juice --multiple
```

**Poll Requirements:**
- Minimum 2 options required
- Maximum 12 options allowed
- Question is required
- Use --multiple flag to allow selecting multiple answers

### Schedule a Message

Schedule a one-time message:
```bash
python main.py schedule --group "Cairo" --message "Meeting reminder" --time "14:30" --repeat once
```

Schedule a daily message:
```bash
python main.py schedule --group "Cairo" --message "Good morning!" --time "09:00" --repeat daily
```

Schedule for specific day:
```bash
python main.py schedule --group "Cairo" --message "Weekly update" --time "10:00" --repeat monday
```

### Load Schedules from File

Create a `schedules.json` file (see example) and run:
```bash
python main.py schedule --file schedules.json
```

### Interactive Mode

For easier use:
```bash
python main.py interactive
```

## API Endpoints

The FastAPI backend provides the following endpoints:

### Schedules
- `GET /schedules` - Get all pending schedules
- `POST /schedules/load` - Load/update schedules (with entries list)
- `POST /schedules/save` - Save schedules to file

### Scheduler Control
- `GET /scheduler/status` - Get scheduler status (running/stopped)
- `POST /scheduler/start` - Start the scheduler
- `POST /scheduler/stop` - Stop the scheduler

### File Upload
- `POST /upload` - Upload image file (returns absolute path)

### Finished Schedules
- `GET /finished-schedules` - Get all completed schedules
- `DELETE /finished-schedules/{index}` - Delete a specific finished schedule
- `DELETE /finished-schedules` - Clear all finished schedules

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Configuration

### Schedule File Format (schedules.json)

```json
[
  {
    "type": "message",
    "group_name": "Cairo",
    "message": "Your message here",
    "time": "2025-10-30 09:00",
    "repeat": "once"
  },
  {
    "type": "image",
    "group_name": "Cairo",
    "image_path": "/absolute/path/to/image.jpg",
    "caption": "Optional caption",
    "time": "2025-10-30 10:00",
    "repeat": "once"
  },
  {
    "type": "poll",
    "group_name": "Cairo",
    "question": "What's your favorite food?",
    "options": ["Pizza", "Burger", "Pasta"],
    "allow_multiple": false,
    "time": "2025-10-30 12:00",
    "repeat": "once"
  }
]
```

**Schedule Types:**
- `message` - Text message
- `image` - Image with optional caption
- `poll` - Poll with multiple options

**Time Format:**
- Absolute: `"2025-10-30 15:30"` (YYYY-MM-DD HH:MM)
- Time only: `"15:30"` (for daily recurring)

**Repeat options:**
- `once` - Send once at specified time
- `daily` - Send every day at specified time
- `hourly` - Send every hour
- `monday`, `tuesday`, etc. - Send on specific day at specified time

### Finished Schedules (finishedSchedules.json)

Completed schedules are automatically saved to `finishedSchedules.json` with completion timestamps:
```json
[
  {
    "type": "message",
    "group_name": "Cairo",
    "message": "Good morning",
    "time": "2025-10-30 09:00",
    "status": "done",
    "created_at": "2025-10-29 15:00:00",
    "completed_at": "2025-10-30 09:00:05",
    "repeat": "once"
  }
]
```

### File Uploads

Images uploaded through the web UI are stored in the `uploads/` directory with absolute paths

## How It Works

### Scheduling Flow

1. **Add Schedule** - Create a schedule through Web UI or API
2. **Start Scheduler** - Click "Start" button or call `/scheduler/start`
3. **Background Execution** - Scheduler runs in a background thread checking every second
4. **Lazy Browser Start** - When a job is due, browser opens automatically
5. **Send Message** - Bot logs into WhatsApp Web and sends the message/image/poll
6. **Auto Close** - Browser closes automatically after successful send
7. **Track Completion** - Schedule saved to `finishedSchedules.json` with timestamp
8. **Repeat or Remove** - Recurring jobs reschedule, one-time jobs are removed

### Browser Management

- **First Run**: Scan QR code (session saved in `chrome_data/`)
- **Subsequent Runs**: Auto-login using saved session
- **Auto-Close**: Browser closes after each scheduled job completes
- **On Failure**: Browser stays open for debugging
- **Manual Use**: CLI mode keeps browser open during interactive use

## Important Notes

1. **First Run**: You must scan the QR code on first run (saved for future use)
2. **Session**: Browser session is saved in `chrome_data` folder
3. **Group Names**: Use exact group name as shown in WhatsApp (case-sensitive)
4. **Time Format**:
   - Absolute: `"2025-10-30 15:30"` (YYYY-MM-DD HH:MM)
   - Time only: `"15:30"` (24-hour format)
5. **Image Uploads**: Use the web UI to upload images - gets real absolute path
6. **Auto-Close**: Browser automatically closes after scheduled jobs (saves resources)
7. **Finished Schedules**: View history and delete unwanted entries via "Finished" page
8. **File Paths**: Web UI uploads files to `uploads/` directory automatically

## Project Structure

```
whasappAuto/
├── server.py                 # FastAPI backend server
├── scheduler.py              # Job scheduler with background thread
├── whatsapp_bot.py          # Selenium WhatsApp Web automation
├── main.py                   # CLI interface
├── schedules.json            # Pending schedules storage
├── finishedSchedules.json    # Completed schedules history
├── uploads/                  # Uploaded images directory
├── chrome_data/              # WhatsApp session data
├── Frontend/                 # React web UI
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Index.tsx              # Main dashboard
│   │   │   └── FinishedSchedules.tsx  # History page
│   │   ├── components/
│   │   │   ├── SchedulerHeader.tsx    # Header with controls
│   │   │   ├── AddScheduleForm.tsx    # Schedule creation form
│   │   │   ├── ScheduleCard.tsx       # Schedule display card
│   │   │   └── EditScheduleDialog.tsx # Edit dialog
│   │   └── App.tsx           # Main app with routing
│   └── package.json
└── requirements.txt          # Python dependencies
```

## Features in Detail

### Web UI Features
- ✅ Start/Stop scheduler with one click
- ✅ Add messages, images, and polls via forms
- ✅ Upload images directly (auto-saved to uploads/)
- ✅ Edit existing schedules
- ✅ Delete pending schedules
- ✅ View finished schedules history
- ✅ Delete individual or all finished schedules
- ✅ Real-time scheduler status
- ✅ Save/Load schedules from file
- ✅ Responsive design with modern UI

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Background scheduler thread
- ✅ Lazy browser initialization (starts only when needed)
- ✅ Auto-close browser after jobs (saves resources)
- ✅ File upload handling
- ✅ Persistent storage (JSON files)
- ✅ Finished schedules tracking
- ✅ Error handling and logging

## Troubleshooting

### Common Issues

**QR Code Issues:**
- If QR code doesn't appear, delete `chrome_data` folder and try again
- Make sure Chrome browser is up to date

**Group Not Found:**
- Make sure group name matches exactly (case-sensitive)
- Try searching for the group in WhatsApp Web manually first

**Image Upload Failed:**
- Check that the image file exists at the specified path
- Use the web UI upload feature instead of manual paths
- Ensure `uploads/` directory has write permissions

**Browser Won't Close:**
- This is intentional if the message failed to send (for debugging)
- Check logs for errors
- Manually close browser and fix the issue

**Scheduler Not Running:**
- Click "Start" button in web UI
- Check scheduler status indicator (should show "Running")
- Check backend logs for errors

### Logs

Check these files for debugging:
- `whatsapp_bot.log` - Browser automation logs
- Backend console output - API and scheduler logs

### Reset Everything

```bash
# Stop the server (Ctrl+C)
# Delete session and schedules
rm -rf chrome_data/
rm schedules.json finishedSchedules.json
# Restart server
pipenv run uvicorn server:app --reload
```

## Examples

### Web UI Example Workflow

1. **Start the servers:**
```bash
# Terminal 1 - Backend
pipenv run uvicorn server:app --reload

# Terminal 2 - Frontend
cd Frontend && npm run dev
```

2. **Open browser** to `http://localhost:5173`

3. **Add a schedule:**
   - Select "Text" tab
   - Enter group name: "Cairo"
   - Enter message: "Good morning team!"
   - Select date/time
   - Click "Add Schedule"

4. **Start scheduler:** Click "Start" button in header

5. **View completion:** Click "Finished" to see completed schedules

### API Example

```python
import requests

# Add a schedule
schedule = {
    "type": "message",
    "group_name": "Cairo",
    "message": "Hello from API!",
    "time": "2025-10-30 15:00",
    "repeat": "once"
}

response = requests.post(
    "http://localhost:8000/schedules/load",
    json={"entries": [schedule]}
)

# Start scheduler
requests.post("http://localhost:8000/scheduler/start")

# Get finished schedules
finished = requests.get("http://localhost:8000/finished-schedules")
print(finished.json())
```

### CLI Examples

Send message to Cairo group:
```bash
python main.py send --group "Cairo" --message "Test message"
```

Send image with caption:
```bash
python main.py send-image --group "Cairo" --image "/path/to/image.jpg" --caption "Check this out!"
```

Send poll:
```bash
python main.py send-poll --group "Cairo" --question "What's your favorite food?" --options Pizza Burger Pasta
```

Daily reminder at 9 AM:
```bash
python main.py schedule --group "Cairo" --message "Daily standup in 30 mins" --time "09:00" --repeat daily
```

## Development

### Running in Development Mode

**Backend with auto-reload:**
```bash
pipenv run uvicorn server:app --reload
```

**Frontend with hot reload:**
```bash
cd Frontend
npm run dev
```

### Making Changes

1. **Backend changes** - Modify Python files, uvicorn auto-reloads
2. **Frontend changes** - Modify React files, Vite hot-reloads instantly
3. **Test changes** - Use the web UI or API to test functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.
