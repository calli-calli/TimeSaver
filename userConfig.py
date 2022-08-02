# Displays previously used settings. Asks user to either change settings or proceed with previous settings.
# Writes a config-file to remember chosen settings.
# Configurable options are:
# last month, Start-Date, End-Date, Include entries that have "All Day" ticked
# config.ini design: {last_month: [bool]
#                     all_day: [bool]
#                     start_date: "yyyymmdd",
#                     end_date: "yyyymmdd"}
import configparser
import os
import os.path
from datetime import datetime
from datetime import timedelta

_user_options = {"last_month": "Timesheet of last month (y/n)? ",
                 "all_day": "include 'All-Day' entries (y/n)? ",
                 "start_date": "enter custom start-date (yymmdd): ",
                 "end_date": "enter custom end-date (yymmdd): "}


def get_default_config():
    """Returns current default config as dict. The default config is always the config that has been used during the
    last run. If this is the first run, a factory default is used. """
    if os.path.exists("config.ini"):
        config = load_config()
    else:
        _config_factory_default = {"last_month": True, "all_day": False, "start_date": "", "end_date": ""}
        save_config(_config_factory_default)
        config = _config_factory_default
    return config


def load_config():
    """Returns config from disk as dict"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    config_dict = _ini_to_dict(config)
    return config_dict


def save_config(config):
    print(f"save_config: {config}")
    """Saves configuration as ini-file. Accepts dict type or Str in ini format"""
    if isinstance(config, dict):
        config_ini = _dict_to_ini(config)
    else:
        config_ini = config
    with open("config.ini", "w") as f:
        config_ini.write(f)


def _write_ini_to_disk(config_ini):
    with open("config.ini" "w") as f:
        config_ini.write(f)


def _dict_to_ini(config_dict):
    config = configparser.ConfigParser()
    for key in config_dict:
        config["DEFAULT"][key] = str(config_dict[key])
    return config


def _ini_to_dict(config_ini):
    """Receives ini config, returns dict type"""
    config_dict = {}
    for section in config_ini:
        for option in config_ini[section]:
            config_dict[option] = config_ini.get(section, option)
    return config_dict


def _prev_month(any_day: datetime):
    """Replaces month with previous one"""
    month = any_day.month
    year = any_day.year
    if month < 12:
        month -= 1
        year -= 1
    else:
        month = 1
    return any_day.replace(year=year, month=month)


def _last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)


def _validate_config(config: dict):
    """Validates settings. Sets start_date and end_date"""
    start_date = config["start_date"]
    end_date = config["end_date"]
    if config["last_month"]:
        # determines correct dates for last month's start and end date
        start_date = _prev_month(datetime.today())
        start_date = start_date.replace(day=1)
        end_date = _last_day_of_month(start_date)
    else:
        # check validity of start_date and end_date
        valid_start = len(start_date) == 6 and start_date.isdigit()
        valid_end = len(end_date) == 6 and end_date.isdigit()
        valid_start_end = bool(int(end_date) - int(start_date))
        if valid_start and valid_end and valid_start_end:
            start_date = datetime.strptime(start_date, "%y%m%d")
            end_date = datetime.strptime(end_date, "%y%m%d")
        else:
            if not valid_start:
                raise Exception("Invalid start date")
            if not valid_end:
                raise Exception("Invalid end date")
            if not valid_start_end:
                raise Exception("Start date must be before end date")
    config["start_date"] = start_date
    config["end_date"] = end_date
    return config


def _print_default_config():
    config = get_default_config()
    head = "----DEFAULT-SETTINGS----\n"
    body = ""
    foot = "------------------------"
    if config["last_month"]:
        for key in config:
            if not (key == "start_date" or key == "end_date"):
                body += f"{key}:\t{str(config[key])}\n"
    else:
        for key in config:
            body += f"{key}:\t{str(config[key])}\n"
    print(head + body + foot)


def get_user_config():
    """Ask user for config preferences, returns dict"""
    print("DEFAULT CONFIG:")
    _print_default_config()
    default = True if input("Use default config (y/n)? ") == "y" else False
    user_config = {}
    if default:
        user_config = get_default_config()
    else:
        user_config["last_month"] = True if input(_user_options["last_month"]) == "y" else False
        user_config["all_day"] = True if input(_user_options["all_day"]) == "y" else False
        if not user_config["last_month"]:
            user_config["start_date"] = input(_user_options["start_date"])
            user_config["end_date"] = input(_user_options["end_date"])
    user_config = _validate_config(user_config)
    return user_config


if __name__ == '__main__':
    get_user_config()
