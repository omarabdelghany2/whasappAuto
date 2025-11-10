import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WhatsAppBot:
    """WhatsApp Web automation bot for sending messages to groups"""

    def __init__(self, headless=False):
        """
        Initialize the WhatsApp bot

        Args:
            headless (bool): Run browser in headless mode (not recommended for first run)
        """
        self.driver = None
        self.headless = headless
        self.wait_time = 10  # Reduced from 30 for faster operations

    def start(self, profile_path: str = None):
        """
        Start the browser and open WhatsApp Web

        Args:
            profile_path (str): Path to Chrome profile directory (optional)
        """
        logger.info("Starting WhatsApp bot...")

        options = webdriver.ChromeOptions()

        # Use custom profile if provided, otherwise use default ./chrome_data
        import os
        if profile_path:
            user_data_dir = os.path.abspath(profile_path)
        else:
            user_data_dir = os.path.abspath("./chrome_data")

        # Create directory if it doesn't exist
        os.makedirs(user_data_dir, exist_ok=True)

        options.add_argument(f"--user-data-dir={user_data_dir}")
        logger.info(f"Using Chrome profile: {user_data_dir}")

        # Fix for "DevTools remote debugging requires a non-default data directory"
        options.add_argument("--remote-debugging-port=9222")

        # Disable automation detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Additional options to prevent errors
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--disable-popup-blocking")

        # Performance optimizations (especially for Windows)
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")  # Helps on Windows
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--no-sandbox")  # Can help with startup speed
        options.add_argument("--disable-web-security")  # Faster startup
        options.add_argument("--disable-features=VizDisplayCompositor")
        options.add_argument("--disable-logging")
        options.add_argument("--disable-permissions-api")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        options.add_argument("--metrics-recording-only")
        options.add_argument("--mute-audio")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-prompt-on-repost")
        options.add_argument("--disable-domain-reliability")
        options.add_argument("--disable-component-update")

        # Set page load strategy to eager for faster startup
        options.page_load_strategy = 'eager'

        # Disable images and CSS for even faster loading (optional - uncomment if needed)
        # prefs = {
        #     "profile.managed_default_content_settings.images": 2,
        #     "profile.managed_default_content_settings.stylesheets": 2
        # }
        # options.add_experimental_option("prefs", prefs)

        if self.headless:
            options.add_argument("--headless")

        # Initialize the driver
        try:
            # Try to get the chromedriver path and fix if needed
            import os
            driver_path = ChromeDriverManager().install()

            # Check if path points to wrong file and fix it
            if not os.access(driver_path, os.X_OK) or 'THIRD_PARTY' in driver_path:
                # Find the actual chromedriver executable
                driver_dir = os.path.dirname(driver_path)
                for root, _, files in os.walk(driver_dir):
                    for file in files:
                        if file == 'chromedriver' or file == 'chromedriver.exe':
                            driver_path = os.path.join(root, file)
                            break
                    if os.path.basename(driver_path).startswith('chromedriver'):
                        break

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            logger.warning(f"ChromeDriverManager failed: {str(e)}")
            logger.info("Trying to use system Chrome without explicit driver path...")
            # Fallback: let Selenium find the driver automatically
            self.driver = webdriver.Chrome(options=options)

        self.driver.maximize_window()

        # Open WhatsApp Web
        logger.info("Opening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")

        logger.info("Please scan the QR code if this is your first time...")

    def wait_for_whatsapp_load(self, timeout=60):
        """
        Wait for WhatsApp to load completely

        Args:
            timeout (int): Maximum time to wait in seconds
        """
        logger.info("Waiting for WhatsApp to load...")
        try:
            # Wait for the search box to appear (indicates WhatsApp has loaded)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            logger.info("WhatsApp loaded successfully!")
            return True
        except TimeoutException:
            logger.error("Timeout waiting for WhatsApp to load")
            return False

    def search_group(self, group_name):
        """
        Search for a group by name

        Args:
            group_name (str): Name of the group to search for
        """
        # Strip whitespace to handle trailing/leading spaces
        group_name = group_name.strip()
        logger.info(f"Searching for group: {group_name}")

        try:
            # Find the search box
            search_box = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )

            # Click and clear the search box
            search_box.click()
            time.sleep(0.3)  # Reduced from 1s
            search_box.clear()

            # Type the group name
            search_box.send_keys(group_name)

            # Wait for search results to appear (smarter than fixed sleep)
            time.sleep(0.5)  # Reduced from 2s

            # Click on the first result - Try exact match first
            logger.info(f"Clicking on group: {group_name}")
            group_element = None

            try:
                # Method 1: Exact match (fastest)
                group_element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, f'//span[@title="{group_name}"]'))
                )
                logger.info("Found group with exact match")
            except TimeoutException:
                # Method 2: Case-insensitive match (fallback)
                try:
                    group_element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, f'//span[contains(translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{group_name.lower()}")]'))
                    )
                    logger.info("Found group with case-insensitive match")
                except TimeoutException:
                    # Method 3: Partial match (last resort)
                    group_element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, f'//span[contains(@title, "{group_name}")]'))
                    )
                    logger.info("Found group with partial match")

            group_element.click()
            time.sleep(0.5)  # Reduced from 2s

            logger.info(f"Successfully opened group: {group_name}")
            return True

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to find group '{group_name}': {str(e)}")
            return False

    def send_message(self, message, group_name=None):
        """
        Send a message to the currently open chat

        Args:
            message (str): Message to send
        """
        logger.info(f"Sending message: {message[:50]}...")
        if group_name:
            group_name = group_name.strip()
            logger.info(f"Navigating to group for message: {group_name}")
            if not self.search_group(group_name):
                logger.error(f"Cannot open group '{group_name}' to send message")
                return False

        try:
            # Find the message input box
            message_box = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )

            # Click on the message box
            message_box.click()
            time.sleep(0.3)  # Reduced from 1s

            # Type the message (handle multi-line messages)
            lines = message.split('\n')
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    # Send Shift+Enter for new line
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)

            time.sleep(0.3)  # Reduced from 1s

            # Send the message - Try multiple methods
            try:
                # Method 1: Press Enter key
                message_box.send_keys(Keys.ENTER)
                time.sleep(0.5)  # Reduced from 1s
            except:
                pass

            # Method 2: Click the send button (backup)
            try:
                send_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Send"]')
                send_button.click()
                logger.info("Message sent using send button!")
            except:
                try:
                    # Alternative send button xpath
                    send_button = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                    send_button.click()
                    logger.info("Message sent using send icon!")
                except:
                    logger.info("Message sent using Enter key!")

            # Wait 5 seconds to verify message was sent
            logger.info("Waiting 5 seconds to verify message was sent...")
            time.sleep(5)
            return True

        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to send message: {str(e)}")
            return False

    def send_image(self, image_path, caption=None, group_name=None):
        """
        Send an image to the currently open chat

        Args:
            image_path (str): Path to the image file
            caption (str): Optional caption for the image
        """
        import os

        logger.info(f"Sending image: {image_path}")
        if group_name:
            group_name = group_name.strip()
            logger.info(f"Navigating to group for image: {group_name}")
            if not self.search_group(group_name):
                logger.error(f"Cannot open group '{group_name}' to send image")
                return False

        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            return False

        try:
            absolute_path = os.path.abspath(image_path)
            logger.info(f"Absolute path: {absolute_path}")

            # IMPORTANT: Click the attachment button first to open the menu
            # This ensures the preview window appears
            logger.info("Clicking attachment button to open menu...")

            attach_selectors = [
                '//div[@title="Attach"]',
                '//span[@data-icon="plus"]',
                '//span[@data-icon="clip"]',
                '//button[@aria-label="Attach"]',
                '//div[@aria-label="Attach"]'
            ]

            attach_clicked = False
            for selector in attach_selectors:
                try:
                    attach_button = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    attach_button.click()
                    logger.info(f"Clicked attach button with selector: {selector}")
                    attach_clicked = True
                    time.sleep(0.8)  # Reduced from 2s
                    break
                except Exception as e:
                    logger.debug(f"Attach selector {selector} failed: {str(e)}")
                    continue

            if not attach_clicked:
                logger.error("Could not find or click attachment button")
                return False

            # Now find and use the file input (should open preview window)
            logger.info("Looking for file input element...")
            input_selectors = [
                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]',
                '//input[@type="file"][@accept*="image"]',
                '//input[@type="file"]'
            ]

            file_uploaded = False
            for selector in input_selectors:
                try:
                    file_input = WebDriverWait(self.driver, 5).until(  # Reduced from 10s
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logger.info(f"Found file input with selector: {selector}")

                    # Send the file path - this should open the preview window
                    file_input.send_keys(absolute_path)
                    logger.info(f"Image file path sent: {absolute_path}")
                    file_uploaded = True

                    # Wait for preview window to appear
                    logger.info("Waiting for preview window to appear...")
                    time.sleep(1)  # Reduced from 5s -> 2s -> 1s
                    break
                except Exception as e:
                    logger.debug(f"File input selector {selector} failed: {str(e)}")
                    continue

            if not file_uploaded:
                logger.error("Could not upload file")
                return False

            # If there's a caption, add it to the preview window
            if caption:
                try:
                    logger.info("Adding caption to image preview...")

                    # The caption box should be visible in the preview window now
                    caption_selectors = [
                        # Caption box in the image preview (most common)
                        '//div[@contenteditable="true"][@role="textbox"]',
                        '//div[@contenteditable="true" and @data-tab="10"]',
                        # Alternative selectors
                        '//div[contains(@class, "lexical")]//div[@contenteditable="true"]',
                        '//div[@contenteditable="true" and contains(@aria-placeholder, "caption")]',
                    ]

                    caption_added = False
                    for selector in caption_selectors:
                        try:
                            # Wait for the caption box to be visible
                            caption_box = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                                EC.visibility_of_element_located((By.XPATH, selector))
                            )

                            # Make sure it's not the search box by checking data-tab attribute
                            data_tab = caption_box.get_attribute('data-tab')
                            if data_tab == '3':  # Skip search box
                                logger.debug(f"Skipping search box (data-tab=3)")
                                continue

                            # Click and add caption
                            caption_box.click()
                            time.sleep(0.3)  # Reduced from 0.5s
                            caption_box.send_keys(caption)
                            logger.info(f"✓ Caption added successfully: {caption}")
                            caption_added = True
                            time.sleep(0.3)  # Reduced from 1s
                            break

                        except Exception as e:
                            logger.debug(f"Caption selector {selector} failed: {str(e)}")
                            continue

                    if not caption_added:
                        logger.warning("⚠ Could not add caption to preview window")

                except Exception as e:
                    logger.warning(f"Error adding caption: {str(e)}")

            # Click the send button
            time.sleep(0.5)  # Reduced from 2s
            send_selectors = [
                '//span[@data-icon="send"]',
                '//button[@aria-label="Send"]',
                '//div[@role="button"][@aria-label="Send"]',
                '//span[@data-icon="send"]/parent::button',
                '//span[@data-testid="send"]'
            ]

            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    send_button.click()
                    logger.info(f"Image send button clicked using selector: {selector}!")

                    # Wait for image to upload completely (important for high-quality images!)
                    logger.info("Waiting for image to upload and send...")
                    # Wait up to 30 seconds for upload to complete
                    # High-quality images may take longer to upload
                    max_wait = 30
                    wait_interval = 1
                    elapsed = 0

                    while elapsed < max_wait:
                        time.sleep(wait_interval)
                        elapsed += wait_interval

                        # Check if there's an upload progress indicator or if send is complete
                        # WhatsApp shows a clock icon or progress while uploading
                        try:
                            # Look for upload progress indicator (clock icon or progress bar)
                            uploading = self.driver.find_elements(By.XPATH, '//span[@data-icon="msg-time" or @data-icon="msg-check" or @data-icon="status-time"]')
                            if uploading:
                                logger.info(f"Upload in progress... ({elapsed}s)")
                                continue
                            else:
                                # No upload indicator found, likely sent
                                break
                        except:
                            pass

                    logger.info(f"Image upload completed after {elapsed} seconds!")
                    # Extra buffer to ensure message is fully sent
                    time.sleep(2)
                    return True
                except:
                    continue

            logger.error("Could not find send button for image")
            return False

        except Exception as e:
            logger.error(f"Failed to send image: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def send_video(self, video_path, caption=None, group_name=None):
        """
        Send a video to the currently open chat

        Args:
            video_path (str): Path to the video file
            caption (str): Optional caption for the video
            group_name (str): Optional group name to send to
        """
        import os

        logger.info(f"Sending video: {video_path}")
        if group_name:
            group_name = group_name.strip()
            logger.info(f"Navigating to group for video: {group_name}")
            if not self.search_group(group_name):
                logger.error(f"Cannot open group '{group_name}' to send video")
                return False

        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            return False

        try:
            absolute_path = os.path.abspath(video_path)
            logger.info(f"Absolute path: {absolute_path}")

            # Click the attachment button first to open the menu
            logger.info("Clicking attachment button to open menu...")

            attach_selectors = [
                '//div[@title="Attach"]',
                '//span[@data-icon="plus"]',
                '//span[@data-icon="clip"]',
                '//button[@aria-label="Attach"]',
                '//div[@aria-label="Attach"]'
            ]

            attach_clicked = False
            for selector in attach_selectors:
                try:
                    attach_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    attach_button.click()
                    logger.info(f"Clicked attach button with selector: {selector}")
                    attach_clicked = True
                    time.sleep(0.8)
                    break
                except Exception as e:
                    logger.debug(f"Attach selector {selector} failed: {str(e)}")
                    continue

            if not attach_clicked:
                logger.error("Could not find or click attachment button")
                return False

            # Find and use the file input (should open preview window)
            logger.info("Looking for file input element...")
            input_selectors = [
                '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]',
                '//input[@type="file"][@accept*="video"]',
                '//input[@type="file"]'
            ]

            file_uploaded = False
            for selector in input_selectors:
                try:
                    file_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logger.info(f"Found file input with selector: {selector}")

                    # Send the file path - this should open the preview window
                    file_input.send_keys(absolute_path)
                    logger.info(f"Video file path sent: {absolute_path}")
                    file_uploaded = True

                    # Wait for preview window to appear
                    logger.info("Waiting for video preview window to appear...")
                    time.sleep(2)  # Give time for video to load in preview
                    break
                except Exception as e:
                    logger.debug(f"File input selector {selector} failed: {str(e)}")
                    continue

            if not file_uploaded:
                logger.error("Could not upload video file")
                return False

            # If there's a caption, add it to the preview window
            if caption:
                try:
                    logger.info("Adding caption to video preview...")

                    caption_selectors = [
                        '//div[@contenteditable="true"][@role="textbox"]',
                        '//div[@contenteditable="true" and @data-tab="10"]',
                        '//div[contains(@class, "lexical")]//div[@contenteditable="true"]',
                        '//div[@contenteditable="true" and contains(@aria-placeholder, "caption")]',
                    ]

                    caption_added = False
                    for selector in caption_selectors:
                        try:
                            caption_box = WebDriverWait(self.driver, 2).until(
                                EC.visibility_of_element_located((By.XPATH, selector))
                            )

                            # Make sure it's not the search box by checking data-tab attribute
                            data_tab = caption_box.get_attribute('data-tab')
                            if data_tab == '3':  # Skip search box
                                logger.debug(f"Skipping search box (data-tab=3)")
                                continue

                            # Click and add caption
                            caption_box.click()
                            time.sleep(0.3)
                            caption_box.send_keys(caption)
                            logger.info(f"✓ Caption added successfully: {caption}")
                            caption_added = True
                            time.sleep(0.3)
                            break

                        except Exception as e:
                            logger.debug(f"Caption selector {selector} failed: {str(e)}")
                            continue

                    if not caption_added:
                        logger.warning("⚠ Could not add caption to preview window")

                except Exception as e:
                    logger.warning(f"Error adding caption: {str(e)}")

            # Click the send button
            time.sleep(0.5)
            send_selectors = [
                '//span[@data-icon="send"]',
                '//button[@aria-label="Send"]',
                '//div[@role="button"][@aria-label="Send"]',
                '//span[@data-icon="send"]/parent::button',
                '//span[@data-testid="send"]'
            ]

            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    send_button.click()
                    logger.info(f"Video send button clicked using selector: {selector}!")

                    # Wait for video to upload completely - videos take much longer than images!
                    logger.info("Waiting for video to upload and send...")
                    # Videos can take a while to upload depending on size
                    # We'll wait up to 2 minutes (120 seconds) for videos
                    max_wait = 120
                    wait_interval = 2
                    elapsed = 0

                    while elapsed < max_wait:
                        time.sleep(wait_interval)
                        elapsed += wait_interval

                        # Check if there's an upload progress indicator
                        # WhatsApp shows a progress bar or clock icon while uploading
                        try:
                            # Look for upload progress indicators
                            uploading_indicators = self.driver.find_elements(
                                By.XPATH,
                                '//span[@data-icon="msg-time" or @data-icon="msg-check" or @data-icon="status-time" or contains(@class, "progress")]'
                            )

                            # Also check for progress bar or percentage
                            progress_bars = self.driver.find_elements(
                                By.XPATH,
                                '//*[contains(@class, "progress") or contains(@role, "progressbar")]'
                            )

                            if uploading_indicators or progress_bars:
                                logger.info(f"Video upload in progress... ({elapsed}s / {max_wait}s)")
                                continue
                            else:
                                # No upload indicator found, video likely sent
                                logger.info("No upload indicators found - video appears to be sent")
                                break
                        except Exception as e:
                            logger.debug(f"Error checking upload status: {e}")
                            pass

                    logger.info(f"Video upload completed after {elapsed} seconds!")
                    # Extra buffer to ensure video is fully sent and processed
                    logger.info("Waiting additional 10 seconds to ensure video is fully sent...")
                    time.sleep(10)
                    return True
                except:
                    continue

            logger.error("Could not find send button for video")
            return False

        except Exception as e:
            logger.error(f"Failed to send video: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def send_poll(self, question, options, allow_multiple_answers=False, group_name=None):
        """
        Create and send a poll to the currently open chat

        Args:
            question (str): The poll question
            options (list): List of option strings (max 12 options)
            allow_multiple_answers (bool): Allow users to select multiple answers
        """
        logger.info(f"Creating poll with question: {question}")
        logger.info(f"Options: {options}")
        logger.info(f"Allow multiple answers: {allow_multiple_answers}")
        if group_name:
            group_name = group_name.strip()
            logger.info(f"Navigating to group for poll: {group_name}")
            if not self.search_group(group_name):
                logger.error(f"Cannot open group '{group_name}' to send poll")
                return False

        if len(options) < 2:
            logger.error("Poll must have at least 2 options")
            return False

        if len(options) > 12:
            logger.error("Poll can have maximum 12 options")
            return False

        try:
            # Click the attachment button to open menu
            logger.info("Clicking attachment button...")
            attach_selectors = [
                '//div[@title="Attach"]',
                '//span[@data-icon="plus"]',
                '//span[@data-icon="clip"]',
                '//button[@aria-label="Attach"]',
                '//div[@aria-label="Attach"]'
            ]

            attach_clicked = False
            for selector in attach_selectors:
                try:
                    attach_button = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    attach_button.click()
                    logger.info(f"Clicked attach button with selector: {selector}")
                    attach_clicked = True
                    time.sleep(0.8)  # Reduced from 2s
                    break
                except Exception as e:
                    logger.debug(f"Attach selector {selector} failed: {str(e)}")
                    continue

            if not attach_clicked:
                logger.error("Could not find or click attachment button")
                return False

            # Click the poll option
            logger.info("Looking for poll option...")
            poll_selectors = [
                '//span[@data-icon="poll-create"]',
                '//li[@aria-label="Poll"]',
                '//div[@aria-label="Poll"]',
                '//span[contains(text(), "Poll")]/..',
                '//div[@title="Poll"]'
            ]

            poll_clicked = False
            for selector in poll_selectors:
                try:
                    poll_button = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    poll_button.click()
                    logger.info(f"Clicked poll button with selector: {selector}")
                    poll_clicked = True
                    time.sleep(0.8)  # Reduced from 2s
                    break
                except Exception as e:
                    logger.debug(f"Poll selector {selector} failed: {str(e)}")
                    continue

            if not poll_clicked:
                logger.error("Could not find or click poll option")
                return False

            # Enter the question
            logger.info("Entering poll question...")
            question_selectors = [
                '//div[@contenteditable="true"][@data-tab="1"]',
                '//input[@placeholder="Question"]',
                '//div[@contenteditable="true" and contains(@aria-placeholder, "question")]',
                '//div[@contenteditable="true"][@role="textbox"]'
            ]

            question_entered = False
            for selector in question_selectors:
                try:
                    question_box = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    question_box.click()
                    time.sleep(0.3)  # Reduced from 0.5s
                    question_box.send_keys(question)
                    logger.info(f"Question entered: {question}")
                    question_entered = True
                    time.sleep(0.3)  # Reduced from 1s
                    break
                except Exception as e:
                    logger.debug(f"Question selector {selector} failed: {str(e)}")
                    continue

            if not question_entered:
                logger.error("Could not enter poll question")
                return False

            # Wait for poll form to fully load
            time.sleep(0.5)  # Reduced from 2s -> 1s -> 0.5s

            # Enter the options
            logger.info("Entering poll options...")

            # First, try to find all input fields in the poll form
            try:
                # Look for all text inputs in the poll creation dialog
                all_text_inputs = self.driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]//div[@contenteditable="true"]')
                logger.info(f"Found {len(all_text_inputs)} contenteditable fields total")

                # Alternative: look for input elements
                all_inputs = self.driver.find_elements(By.XPATH, '//input[@type="text"]')
                logger.info(f"Found {len(all_inputs)} text input fields")
            except Exception as e:
                logger.debug(f"Error counting input fields: {str(e)}")

            for i, option in enumerate(options):
                logger.info(f"Entering option {i+1}: {option}")
                option_entered = False

                # Method 1: Try data-tab="2" for option fields (tab index after question)
                if not option_entered:
                    try:
                        option_boxes = self.driver.find_elements(By.XPATH, '//div[@contenteditable="true"][@data-tab="2"]')
                        logger.info(f"Method 1: Found {len(option_boxes)} option fields with data-tab=2")
                        if i < len(option_boxes):
                            option_boxes[i].click()
                            time.sleep(0.3)
                            option_boxes[i].send_keys(option)
                            logger.info(f"✓ Option {i+1} entered successfully (method 1)")
                            option_entered = True
                            time.sleep(0.3)
                    except Exception as e:
                        logger.debug(f"Method 1 failed for option {i+1}: {str(e)}")

                # Method 2: Find all contenteditable textboxes and skip the first (question)
                if not option_entered:
                    try:
                        all_textboxes = self.driver.find_elements(By.XPATH, '//div[@contenteditable="true"][@role="textbox"]')
                        logger.info(f"Method 2: Found {len(all_textboxes)} total textboxes")
                        # First one is question, rest are options
                        if i + 1 < len(all_textboxes):
                            all_textboxes[i + 1].click()
                            time.sleep(0.3)
                            all_textboxes[i + 1].send_keys(option)
                            logger.info(f"✓ Option {i+1} entered successfully (method 2)")
                            option_entered = True
                            time.sleep(0.3)
                    except Exception as e:
                        logger.debug(f"Method 2 failed for option {i+1}: {str(e)}")

                # Method 3: Look for copyable-text divs with contenteditable
                if not option_entered:
                    try:
                        copyable_fields = self.driver.find_elements(By.XPATH, '//div[contains(@class, "copyable-text")]//div[@contenteditable="true"]')
                        logger.info(f"Method 3: Found {len(copyable_fields)} copyable-text fields")
                        # First is question, rest are options
                        if i + 1 < len(copyable_fields):
                            copyable_fields[i + 1].click()
                            time.sleep(0.3)
                            copyable_fields[i + 1].send_keys(option)
                            logger.info(f"✓ Option {i+1} entered successfully (method 3)")
                            option_entered = True
                            time.sleep(0.3)
                    except Exception as e:
                        logger.debug(f"Method 3 failed for option {i+1}: {str(e)}")

                if not option_entered:
                    logger.warning(f"⚠ Could not enter option {i+1}: {option}")

            # Ensure the multiple-answers toggle matches desired state
            try:
                logger.info(f"Setting multiple answers to: {allow_multiple_answers}")
                toggle_candidates = [
                    # Native checkbox near the label
                    '//label[contains(., "Allow multiple answers")]//input[@type="checkbox"]',
                    '//span[contains(text(), "Allow multiple answers")]/ancestor::label//input[@type="checkbox"]',
                    # Any checkbox within the poll dialog
                    '//div[contains(@role, "dialog")]//input[@type="checkbox"]',
                    # Switch-style control with aria-checked
                    '//*[(@role="switch" or @aria-checked) and (contains(., "Allow multiple") or contains(@aria-label, "multiple"))]',
                    # Fallback: element next to the text
                    '//span[contains(text(), "Allow multiple answers")]/following::*[1]'
                ]

                def get_toggle_state(el):
                    try:
                        tag = el.tag_name.lower()
                        if tag == 'input':
                            # For input checkbox, rely on selected/checked
                            checked_attr = el.get_attribute('checked')
                            return el.is_selected() or (checked_attr is not None)
                        aria = el.get_attribute('aria-checked')
                        if aria in ('true', 'false'):
                            return aria == 'true'
                        # Some custom toggles encode state in aria-pressed
                        aria_pressed = el.get_attribute('aria-pressed')
                        if aria_pressed in ('true', 'false'):
                            return aria_pressed == 'true'
                    except Exception:
                        pass
                    return None

                toggle_set = False
                for selector in toggle_candidates:
                    try:
                        el = WebDriverWait(self.driver, 2).until(  # Reduced from 3s
                            EC.presence_of_element_located((By.XPATH, selector))
                        )

                        # If the element is not clickable, try its parent label/button
                        candidate_click = None
                        try:
                            candidate_click = WebDriverWait(self.driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                        except Exception:
                            # try a nearby clickable ancestor
                            try:
                                candidate_click = el.find_element(By.XPATH, './ancestor::*[@role="switch" or self::label or self::button][1]')
                            except Exception:
                                candidate_click = el

                        state = get_toggle_state(el)
                        if state is None:
                            # Try reading state from clickable wrapper
                            state = get_toggle_state(candidate_click)

                        # If we still don't know state, click only when enabling to be safe
                        if state is None:
                            if allow_multiple_answers:
                                candidate_click.click()
                                logger.info("Multiple answers toggle clicked (state unknown, enabling)")
                            else:
                                logger.info("Multiple answers toggle state unknown; assuming default is single-answer")
                            toggle_set = True
                            time.sleep(0.5)
                            break

                        if state != allow_multiple_answers:
                            candidate_click.click()
                            logger.info("Multiple answers toggled to desired state")
                            time.sleep(0.5)
                        else:
                            logger.info("Multiple answers already in desired state")
                        toggle_set = True
                        break
                    except Exception as e:
                        logger.debug(f"Multiple answers toggle selector {selector} failed: {str(e)}")
                        continue

                if not toggle_set:
                    logger.warning("Could not locate multiple answers toggle; proceeding with default")
            except Exception as e:
                logger.warning(f"Error while setting multiple answers: {str(e)}")

            # Click send button
            logger.info("Sending poll...")
            time.sleep(0.5)  # Reduced from 2s
            send_selectors = [
                '//span[@data-icon="send"]',
                '//button[@aria-label="Send"]',
                '//div[@role="button"][@aria-label="Send"]',
                '//span[@data-icon="send"]/parent::button'
            ]

            for selector in send_selectors:
                try:
                    send_button = WebDriverWait(self.driver, 2).until(  # Reduced from 5s
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    send_button.click()
                    logger.info(f"Poll sent successfully using selector: {selector}!")
                    # Wait 4 seconds to verify poll was sent
                    logger.info("Waiting 4 seconds to verify poll was sent...")
                    time.sleep(4)
                    return True
                except Exception as e:
                    logger.debug(f"Send selector {selector} failed: {str(e)}")
                    continue

            logger.error("Could not find send button for poll")
            return False

        except Exception as e:
            logger.error(f"Failed to send poll: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def send_message_to_group(self, group_name, message):
        """
        Send a message to a specific group

        Args:
            group_name (str): Name of the group
            message (str): Message to send
        """
        group_name = group_name.strip()
        logger.info(f"Sending message to group '{group_name}'")

        if self.search_group(group_name):
            return self.send_message(message)
        else:
            logger.error(f"Failed to send message to group '{group_name}'")
            return False

    def send_image_to_group(self, group_name, image_path, caption=None):
        """
        Send an image to a specific group

        Args:
            group_name (str): Name of the group
            image_path (str): Path to the image file
            caption (str): Optional caption for the image
        """
        group_name = group_name.strip()
        logger.info(f"Sending image to group '{group_name}'")

        if self.search_group(group_name):
            return self.send_image(image_path, caption)
        else:
            logger.error(f"Failed to send image to group '{group_name}'")
            return False

    def send_video_to_group(self, group_name, video_path, caption=None):
        """
        Send a video to a specific group

        Args:
            group_name (str): Name of the group
            video_path (str): Path to the video file
            caption (str): Optional caption for the video
        """
        group_name = group_name.strip()
        logger.info(f"Sending video to group '{group_name}'")

        if self.search_group(group_name):
            return self.send_video(video_path, caption)
        else:
            logger.error(f"Failed to send video to group '{group_name}'")
            return False

    def send_poll_to_group(self, group_name, question, options, allow_multiple_answers=False):
        """
        Send a poll to a specific group

        Args:
            group_name (str): Name of the group
            question (str): The poll question
            options (list): List of option strings
            allow_multiple_answers (bool): Allow users to select multiple answers
        """
        group_name = group_name.strip()
        logger.info(f"Sending poll to group '{group_name}'")

        if self.search_group(group_name):
            return self.send_poll(question, options, allow_multiple_answers)
        else:
            logger.error(f"Failed to send poll to group '{group_name}'")
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            logger.info("Closing browser...")
            self.driver.quit()
            logger.info("Browser closed successfully")


if __name__ == "__main__":
    # Simple test
    bot = WhatsAppBot()

    try:
        bot.start()
        bot.wait_for_whatsapp_load()

        # Test sending a message to Cairo group
        bot.send_message_to_group("Cairo", "Hello from WhatsApp Bot!")

        logger.info("Test completed. Press Ctrl+C to exit...")
        time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
    finally:
        bot.close()
