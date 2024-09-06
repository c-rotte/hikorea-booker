# HiKorea Appointment Checker

## Overview

The HiKorea Appointment Checker is a tool designed for D2 visa holders (international students) coming to Korea who need
to register for their Alien Registration Card (ARC). This tool automatically checks for cancelled appointments at
specified immigration offices, allowing users to potentially secure earlier appointment slots.

## Features

- Continuously checks for available appointments at multiple immigration offices
- Automatically books an earlier appointment if found
- Cancels previous appointments when a better slot is secured
- Configurable check interval and date range

## Installation

1. Clone this repository or download the source code.
2. Navigate to the project directory.
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line with the following arguments:

```
python main.py "VISA_NAME" VISA_NUMBER VISA_BIRTH_DATE OFFICE_NUMBERS MAX_DATE CHECK_INTERVAL_SECONDS URL
```

Example:

```
# check for appointments 
# for SMITH JOHN DOE ,
# at office 800 and 801,
# up until December 31, 2024,
# with checks every 15 seconds
# starting with pin 0000
# notifying discord at <url>
python main.py "SMITH JOHN DOE" GE2400001337 20010625 800,801 20241231 15 0000 <url>
```

### Arguments

- `VISA_NAME`: Your full name as it appears on your visa (in quotes)
- `VISA_NUMBER`: Your visa number
- `VISA_BIRTH_DATE`: Your birth date in YYYYMMDD format
- `OFFICE_NUMBERS`: One or more office numbers to check for appointments (comma-separated), see `OFFICES.txt`
- `MAX_DATE`: The latest date you want to check for appointments (YYYYMMDD)
- `CHECK_INTERVAL`: Time in seconds between each check
- `PIN`: The password to use when booking appointments
- `URL`: The URL of the discord webhook to send notifications to

## Important Notes

- This tool is for educational purposes only. Use it responsibly and in accordance with HiKorea's terms of service.
- Excessive use may result in your IP being blocked by HiKorea.
- Always verify any appointments booked through this tool on the official HiKorea website.

## Disclaimer

This tool is not officially associated with HiKorea or any Korean government agency. Use it at your own risk.
