# Kilm – Kilmainham Gaol Tour Slot Checker

This Python script checks for available tour slots at Kilmainham Gaol and sends an email notification if slots are found.

## Features

- Scrapes the Kilmainham Gaol booking website for available tour slots on a specified date
- Sends an email notification with available slot details
- Command-line interface for easy usage

Note: The CLI is only useful when being periodically executed by cron.

## Installation

You can install this package directly from GitHub using pip:

```bash
pip install git+https://github.com/RobbyRed98/kilm.git
```

Alternatively, you can clone the repository and install it locally:
1. Clone this repository:
   ```bash
   git clone https://github.com/RobbyRed98/kilm.git
   cd kilmainham-slot-checker
   ```

2. Install the required dependencies:
   ```bash
   pip install -e .
   ```

## Usage

Run the script from the command line:

```bash
kilm YYYYMMDD recipient@email.com
```

Replace `YYYYMMDD` with the date you want to check (e.g., 20250701 for July 1, 2025) and `recipient@email.com` with the email address where you want to receive notifications.

## Environment Variables

The script requires two environment variables to be set:

- `EMAIL`: The email address used to send notifications
- `PWD`: The password for the email account

## Dependencies

- requests
- beautifulsoup4

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
