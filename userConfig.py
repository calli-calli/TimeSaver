# Displays previously used settings. Asks user to either change settings or proceed with previous settings.
# Writes a config-file to remember chosen settings.
# Configurable options are:
# last month, Start-Date, End-Date, Include events that have "All Day" set to true
# config.ini design: {last_month: True/False
#                     all_day: True/False
#                     start_date: UTC,
#                     end_date: UTC}
import configparser
import os
import os.path
import warnings
from datetime import datetime
from datetime import timedelta


settings_structure = {"last_month": [bool],
                      "all_day": [bool],
                      "start_date": [datetime],
                      "end_date": [datetime],
                      "cal_name": [str],
                      "output_path": [str]}

_factory_default_settings = {"last_month": True,
                             "all_day": False,
                             "start_date": "",
                             "end_date": "",
                             "cal_name": "primary",
                             "output_path": os.getcwd()}

_date_format = "%d%m%y"


def get_pref(option: str = None) -> dict:
    """Returns validated default config. If argument is specified returns only corresponding pref"""
    result = ""
    if not option:
        if not os.path.exists("config.ini"):
            save_pref(_factory_default_settings)
        config_parser = configparser.ConfigParser()
        config_parser.read("config.ini")
        result = _ini_to_dict(config_parser)
        result = validate(result, fill_missing_options=True)
    else:
        for opt, value in get_pref().items():
            if opt.lower() == option.lower():
                result = {option: value}
        if not result:
            warnings.warn(str(f"Requested option ('{option}') does not exist. Returning: ''."))
    return result


def save_pref(options: dict):
    """accepts dictionary. Ex: {last_mont: True}"""
    val_options = validate(options)
    config_ini = _dict_to_ini(val_options)
    with open("config.ini", "w") as f:
        config_ini.write(f)


def get_prev_month_dates(some_day: datetime = datetime.today()) -> dict:
    """Calculates first and last day of previous month. Return values as datetime-type (keys: start_date, end_date)"""
    some_day = some_day.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = some_day - timedelta(days=some_day.day)
    start_date = end_date.replace(day=1)
    return {"start_date": start_date, "end_date": end_date}


def validate(settings: dict, fill_missing_options=False):
    """Checks settings for validity. Raises Error if invalid"""
    error_msg = []
    valid_settings = settings.copy()
    # adds missing options to valid_settings and sets them to default value
    if fill_missing_options:
        for option in settings_structure:
            if option not in settings.keys():
                valid_settings[option] = _factory_default_settings[option]
    # Checks existing keys for validity. Alter values and type if necessary
    for option, pref in settings.items():
        if isinstance(pref, str) and (pref == "True" or pref == "False"):  # string "True" & "False" to bool type
            valid_settings[option] = eval(pref)
            pref = valid_settings[option]
        if option not in settings_structure:
            error_msg.append(f"This option is not supported: {option}, {pref}")
        if option == "output_path":
            if not os.path.dirname(pref):
                error_msg = f"Not a directory: {option}, {pref}"
        if option == "last_month":
            if isinstance(pref, str) and (pref == "True" or pref == "False"):
                pref = eval(pref)
            if not isinstance(pref, bool):
                error_msg.append(f"{option} must be bool, is: {type(pref)}, {pref}")
        if option == "all_day":
            if not isinstance(pref, bool):
                error_msg.append(f"{option} must be bool, is: {type(pref)}")
        if option == "start_date" or option == "end_date":
            if "last_month" in settings.keys() and settings["last_month"] is True:
                pref = get_prev_month_dates()[option]
            elif isinstance(pref, str) and len(pref) == 19:
                pref = datetime.fromisoformat(pref)
            elif isinstance(pref, str) and len(pref) == 6:
                pref = datetime.strptime(pref, _date_format)
            elif not isinstance(pref, datetime):
                error_msg.append(f"Type error. Type: {type(pref)} Option: {option}, Pref: {pref}")
        valid_settings[option] = pref
    if len(error_msg):
        raise Exception("\n".join(error_msg))
    return valid_settings


def _dict_to_ini(config_dict):
    config = configparser.ConfigParser()
    for key, value in config_dict.items():
        if isinstance(value, datetime):
            config["DEFAULT"][key] = str(value.isoformat())
        else:
            config["DEFAULT"][key] = str(config_dict[key])
    return config


def _ini_to_dict(config_ini):
    """Receives ini config, returns dict type"""
    config_dict = {}
    for section in config_ini:
        for option in config_ini[section]:
            config_dict[option] = config_ini.get(section, option)
    return config_dict


def _print_default_settings():
    """DEPRECATED."""
    config = get_pref()
    head = "----DEFAULT-SETTINGS----\n"
    body = ""
    foot = "------------------------\n"
    if config["last_month"] == "True":
        for key in config:
            if not (key == "start_date" or key == "end_date"):
                body += f"{key}:\t{str(config[key])}\n"
    else:
        for key in config:
            body += f"{key}:\t{str(config[key])}\n"
    print(head + body + foot)


if __name__ == '__main__':
    pass
