import argparse
import time
from datetime import datetime
from appointment_checker import AppointmentChecker
from appointment_booker import AppointmentBooker
from appointment_canceller import AppointmentCanceller
from config import Config
from discord_webhook import DiscordWebhook


def parse_arguments():
    parser = argparse.ArgumentParser(description="HiKorea Appointment Checker")
    parser.add_argument("visa_name", help="Visa holder's name")
    parser.add_argument("visa_number", help="Visa number")
    parser.add_argument("visa_birth", help="Visa holder's birth date (YYYYMMDD)")
    parser.add_argument("office_numbers", help="Office numbers to check for appointments")
    parser.add_argument("max_inclusive_date", help="Maximum date to check for appointments (YYYYMMDD)")
    parser.add_argument("check_interval", type=int, help="Interval between checks (in seconds)")
    parser.add_argument("pin", help="PIN for the appointment")
    parser.add_argument("discord_webhook", help="Discord webhook URL")
    return parser.parse_args()


WEBHOOK_URL = None


def notify(message: str):
    webhook = DiscordWebhook(url=WEBHOOK_URL,
                             rate_limit_retry=True,
                             content=message)
    webhook.execute()


def main():
    args = parse_arguments()
    config = Config(
        visa_name=args.visa_name,
        visa_number=args.visa_number,
        visa_birth=int(args.visa_birth),
        office_numbers=args.office_numbers.split(","),
        max_inclusive_date=args.max_inclusive_date,
        pin=args.pin,
        check_interval=args.check_interval
    )
    global WEBHOOK_URL
    WEBHOOK_URL = args.discord_webhook

    print(f"Starting appointment checker with interval of {config.check_interval} seconds...")

    checker = AppointmentChecker(config)
    booker = AppointmentBooker(config)
    canceller = AppointmentCanceller(config)

    while True:
        print(f"Checking appointments at {datetime.now()}")
        current_appointments = canceller.get_current_appointments()
        for appointment in current_appointments:
            print(f"Found current appointment: {appointment}")
        new_appointments = checker.check_new_appointments()

        if new_appointments:
            for new_appointment in new_appointments:
                if not current_appointments or new_appointment['date'] < min(
                        app['date'] for app in current_appointments):
                    print(f"Found earlier appointment: {new_appointment}")
                    for current_appointment in current_appointments:
                        print(f"Cancelling appointment: {current_appointment['id']}")
                        canceller.cancel_appointment(current_appointment['id'])
                    result_msg = booker.book_appointment(new_appointment)
                    if result_msg != "Success":
                        print(f"Failed to book appointment: {result_msg}")
                        continue
                    print(f"Booked appointment: {new_appointment}")
                    notify(f"Booked appointment: {new_appointment}")
                    pin = "0000"
                    break

        print(f"Waiting for {config.check_interval} seconds before next check...")
        time.sleep(config.check_interval)


if __name__ == "__main__":
    main()
