#!/usr/bin/env python3
"""
Test script to send a poll to Cairo group
Use this for testing the bot's poll creation functionality
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
    """Test sending a poll to a group"""

    # Get group name, question and options from command line arguments
    if len(sys.argv) < 4:
        logger.error("Usage: python test_send_poll.py <group_name> <question> <option1> <option2> [option3...] [--multiple]")
        logger.error("Example: python test_send_poll.py Cairo 'What's your favorite food?' Pizza Burger Pasta --multiple")
        sys.exit(1)

    group_name = sys.argv[1]
    question = sys.argv[2]

    # Check if --multiple flag is present
    allow_multiple = '--multiple' in sys.argv

    # Get options (everything between question and --multiple flag if present)
    if allow_multiple:
        options = sys.argv[3:sys.argv.index('--multiple')]
    else:
        options = sys.argv[3:]

    if len(options) < 2:
        logger.error("Poll must have at least 2 options")
        sys.exit(1)

    if len(options) > 12:
        logger.error("Poll can have maximum 12 options")
        sys.exit(1)

    logger.info(f"Question: {question}")
    logger.info(f"Options: {options}")
    logger.info(f"Allow multiple answers: {allow_multiple}")

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

        # Send poll to specified group
        logger.info(f"Attempting to send poll to '{group_name}' group...")

        success = bot.send_poll_to_group(group_name, question, options, allow_multiple)

        if success:
            logger.info("✓ Poll sent successfully!")
        else:
            logger.error("✗ Failed to send poll")

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
