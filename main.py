import argparse
import time
from datetime import datetime
from appointment_checker import AppointmentChecker
from appointment_booker import AppointmentBooker
from appointment_canceller import AppointmentCanceller
from config import Config


def parse_arguments():
    parser = argparse.ArgumentParser(description="HiKorea Appointment Checker")
    parser.add_argument("visa_name", help="Visa holder's name")
    parser.add_argument("visa_number", help="Visa number")
    parser.add_argument("visa_birth", help="Visa holder's birth date (YYYYMMDD)")
    parser.add_argument("office_numbers", help="Office numbers to check for appointments")
    parser.add_argument("max_inclusive_date", help="Maximum date to check for appointments (YYYYMMDD)")
    parser.add_argument("check_interval", type=int, help="Interval between checks (in seconds)")
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = Config(
        visa_name=args.visa_name,
        visa_number=args.visa_number,
        visa_birth=int(args.visa_birth),
        office_numbers=args.office_numbers.split(","),
        max_inclusive_date=args.max_inclusive_date,
        check_interval=args.check_interval
    )

    print(f"Starting appointment checker with interval of {config.check_interval} seconds...")

    checker = AppointmentChecker(config)
    booker = AppointmentBooker(config)
    canceller = AppointmentCanceller(config)

    while True:
        print(f"Checking appointments at {datetime.now()}")
        current_appointments = canceller.get_current_appointments()
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
                    # here you can implement some kind of notification system, perhaps a webhook or email
                    break

        print(f"Waiting for {config.check_interval} seconds before next check...")
        time.sleep(config.check_interval)


if __name__ == "__main__":
    main()
