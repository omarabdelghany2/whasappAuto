#!/usr/bin/env python3
"""
WhatsApp Message Scheduler
Main entry point for scheduling and sending WhatsApp messages
"""

import argparse
import logging
import sys
from whatsapp_bot import WhatsAppBot
from scheduler import MessageScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_immediate_message(args):
    """Send an immediate message to a group"""
    bot = WhatsAppBot(headless=args.headless)

    try:
        bot.start()
        bot.wait_for_whatsapp_load(timeout=args.timeout)

        logger.info(f"Sending message to group: {args.group}")
        success = bot.send_message_to_group(args.group, args.message)

        if success:
            logger.info("Message sent successfully!")
        else:
            logger.error("Failed to send message")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if not args.keep_open:
            bot.close()


def send_immediate_image(args):
    """Send an image to a group"""
    bot = WhatsAppBot(headless=args.headless)

    try:
        bot.start()
        bot.wait_for_whatsapp_load(timeout=args.timeout)

        logger.info(f"Sending image to group: {args.group}")
        logger.info(f"Image path: {args.image}")

        caption = args.caption if args.caption else None
        success = bot.send_image_to_group(args.group, args.image, caption)

        if success:
            logger.info("Image sent successfully!")
        else:
            logger.error("Failed to send image")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if not args.keep_open:
            bot.close()


def send_immediate_poll(args):
    """Send a poll to a group"""
    bot = WhatsAppBot(headless=args.headless)

    try:
        bot.start()
        bot.wait_for_whatsapp_load(timeout=args.timeout)

        logger.info(f"Sending poll to group: {args.group}")
        logger.info(f"Question: {args.question}")
        logger.info(f"Options: {args.options}")
        logger.info(f"Allow multiple answers: {args.multiple}")

        success = bot.send_poll_to_group(args.group, args.question, args.options, args.multiple)

        if success:
            logger.info("Poll sent successfully!")
        else:
            logger.error("Failed to send poll")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if not args.keep_open:
            bot.close()


def schedule_messages(args):
    """Schedule messages from a configuration file"""
    bot = WhatsAppBot(headless=args.headless)

    try:
        bot.start()
        bot.wait_for_whatsapp_load(timeout=args.timeout)

        scheduler = MessageScheduler(bot)

        if args.file:
            # Load schedules from file
            logger.info(f"Loading schedules from: {args.file}")
            scheduler.load_schedules_from_file(args.file)
        else:
            # Add a single scheduled message
            scheduler.schedule_message(
                group_name=args.group,
                message=args.message,
                scheduled_time=args.time,
                repeat=args.repeat
            )

        # List all scheduled messages
        scheduler.list_scheduled_messages()

        # Run the scheduler
        scheduler.run()

    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        bot.close()


def interactive_mode():
    """Run in interactive mode"""
    bot = WhatsAppBot(headless=False)

    try:
        bot.start()
        bot.wait_for_whatsapp_load()

        scheduler = MessageScheduler(bot)

        print("\n" + "="*60)
        print("WhatsApp Message Scheduler - Interactive Mode")
        print("="*60)
        print("\nCommands:")
        print("  1. Send immediate message")
        print("  2. Schedule a message")
        print("  3. Load schedules from file")
        print("  4. List scheduled messages")
        print("  5. Start scheduler")
        print("  6. Exit")
        print("="*60)

        while True:
            choice = input("\nEnter command number: ").strip()

            if choice == "1":
                group = input("Enter group name: ").strip()
                message = input("Enter message: ").strip()
                scheduler.add_immediate_message(group, message)

            elif choice == "2":
                group = input("Enter group name: ").strip()
                message = input("Enter message: ").strip()
                time_str = input("Enter time (HH:MM): ").strip()
                repeat = input("Enter repeat (once/daily/hourly/monday/etc): ").strip() or "once"
                scheduler.schedule_message(group, message, time_str, repeat)

            elif choice == "3":
                file_path = input("Enter file path: ").strip()
                scheduler.load_schedules_from_file(file_path)

            elif choice == "4":
                scheduler.list_scheduled_messages()

            elif choice == "5":
                print("\nStarting scheduler... Press Ctrl+C to stop")
                scheduler.run()

            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        logger.info("\nInteractive mode stopped by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        bot.close()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="WhatsApp Message Scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send immediate message
  python main.py send --group "Cairo" --message "Hello World!"

  # Send image with caption
  python main.py send-image --group "Cairo" --image "/path/to/image.jpg" --caption "hey ya regalaa am omar"

  # Send poll
  python main.py send-poll --group "Cairo" --question "What's your favorite?" --options Pizza Burger Pasta

  # Send poll with multiple answers allowed
  python main.py send-poll --group "Cairo" --question "Select all you like" --options Coffee Tea Juice --multiple

  # Schedule a daily message
  python main.py schedule --group "Cairo" --message "Daily update" --time "09:00" --repeat daily

  # Load schedules from file
  python main.py schedule --file schedules.json

  # Interactive mode
  python main.py interactive
        """
    )

    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--timeout', type=int, default=60, help='Timeout for WhatsApp to load (seconds)')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Send command
    send_parser = subparsers.add_parser('send', help='Send immediate message')
    send_parser.add_argument('--group', required=True, help='Group name')
    send_parser.add_argument('--message', required=True, help='Message to send')
    send_parser.add_argument('--keep-open', action='store_true', help='Keep browser open after sending')

    # Send image command
    send_image_parser = subparsers.add_parser('send-image', help='Send image to group')
    send_image_parser.add_argument('--group', required=True, help='Group name')
    send_image_parser.add_argument('--image', required=True, help='Path to image file')
    send_image_parser.add_argument('--caption', help='Optional caption for the image')
    send_image_parser.add_argument('--keep-open', action='store_true', help='Keep browser open after sending')

    # Send poll command
    send_poll_parser = subparsers.add_parser('send-poll', help='Send poll to group')
    send_poll_parser.add_argument('--group', required=True, help='Group name')
    send_poll_parser.add_argument('--question', required=True, help='Poll question')
    send_poll_parser.add_argument('--options', nargs='+', required=True, help='Poll options (space-separated)')
    send_poll_parser.add_argument('--multiple', action='store_true', help='Allow multiple answers')
    send_poll_parser.add_argument('--keep-open', action='store_true', help='Keep browser open after sending')

    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Schedule messages')
    schedule_parser.add_argument('--group', help='Group name')
    schedule_parser.add_argument('--message', help='Message to send')
    schedule_parser.add_argument('--time', help='Time to send (HH:MM)')
    schedule_parser.add_argument('--repeat', default='once', help='Repeat frequency (once/daily/hourly/monday/etc)')
    schedule_parser.add_argument('--file', help='Load schedules from JSON file')

    # Interactive command
    subparsers.add_parser('interactive', help='Run in interactive mode')

    args = parser.parse_args()

    if args.command == 'send':
        send_immediate_message(args)
    elif args.command == 'send-image':
        send_immediate_image(args)
    elif args.command == 'send-poll':
        send_immediate_poll(args)
    elif args.command == 'schedule':
        schedule_messages(args)
    elif args.command == 'interactive':
        interactive_mode()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
