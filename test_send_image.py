#!/usr/bin/env python3
"""
Test script to send an image to Cairo group
Use this for testing the bot's image sending functionality
"""

from whatsapp_bot import WhatsAppBot
import logging
import sys

# Configure logging to show on console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Test sending an image to a group"""

    # Get group name, image path, and optional caption from command line arguments
    if len(sys.argv) < 3:
        logger.error("Usage: python test_send_image.py <group_name> <image_path> [caption]")
        logger.error("Example: python test_send_image.py Cairo /path/to/image.jpg 'hey ya regalaa am omar'")
        sys.exit(1)

    group_name = sys.argv[1]
    image_path = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else "hey ya regalaa am omar"

    # Create bot instance
    bot = WhatsAppBot(headless=False)

    try:
        # Start the bot and open WhatsApp Web
        logger.info("Starting WhatsApp bot...")
        bot.start()

        # Wait for WhatsApp to load (scan QR code if first time)
        logger.info("Waiting for WhatsApp to load...")
        logger.info("Please scan QR code if this is your first time!")
        bot.wait_for_whatsapp_load(timeout=120)  # 2 minutes timeout

        # Send image to specified group
        logger.info(f"Attempting to send image to '{group_name}' group...")
        logger.info(f"Image: {image_path}")
        logger.info(f"Caption: {caption}")

        success = bot.send_image_to_group(group_name, image_path, caption)

        if success:
            logger.info("✓ Image sent successfully!")
        else:
            logger.error("✗ Failed to send image")

        # Keep browser open for 10 seconds so you can see the result
        logger.info("Keeping browser open for 10 seconds...")
        import time
        time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Test stopped by user")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Close the browser
        bot.close()
        logger.info("Test completed!")


if __name__ == "__main__":
    main()
