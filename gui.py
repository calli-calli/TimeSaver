import PySimpleGUI as sg

import apiInteractions
import timesheeBuilder
import userConfig

# todo block focus on sg.Combo elements
sg.theme("DarkGray2")
config = userConfig.get_pref()
def_cal_name = config["cal_name"]
def_cal_name_list = apiInteractions.get_calendar_names()
def_all_day = config["all_day"]
def_last_month_bool = config["last_month"]
def_last_month = "Previous month" if def_last_month_bool else "Custom"
def_start_date = config["start_date"].strftime("%d.%m.%y")
def_end_date = config["end_date"].strftime("%d.%m.%y")
def_output_path = config["output_path"]

# build layout
left_column = [
    [
        sg.Text("Calendar Name:"),
        sg.Combo(def_cal_name_list, default_value=def_cal_name, readonly=True, disabled=True, key="cal_name")
    ],
    [sg.Text("Output:"), sg.Input(def_output_path, enable_events=True, key="directory"), sg.FolderBrowse()],
    [sg.Checkbox("Default Settings", default=True, enable_events=True, key="default")],
    [sg.Button("Start", size=(5, 1), key="start")]
]
right_column = [
    [sg.Combo(["Previous month", "Custom"], default_value=def_last_month, enable_events=True, disabled=True,
              readonly=True, key="last_month")],
    [sg.Checkbox("Full day entries", default=def_all_day, disabled=True, key="all_day")],
    [sg.Text("Start"), sg.Input(def_start_date, size=(8, 1), disabled=True, enable_events=True, key="start_date")],
    [sg.Text("End "), sg.Input(def_end_date, size=(8, 1), disabled=True, enable_events=True, key="end_date")]
]
layout = [
    [
        sg.Column(left_column),
        sg.VSeperator(),
        sg.Column(right_column)
    ]
]
# build window
window = sg.Window(title="Timesheet from calendar", layout=layout)


def set_def_values(keys: list):
    """sets window elements to default values"""
    for k in keys:
        window[k].update(eval("def_" + k))


def set_option(keys: list, option: str, value: bool):
    """Sets window option to passed value"""
    for k in keys:
        window[k].update(**{option: value})


def validate_format(test_date: str, rollback_date: str = "01.01.23") -> str:
    """validates and formats date (xx.xx.xx)"""
    test_date = test_date.replace(".", "")
    if test_date.isdigit() or test_date == "":
        n = 2
        segments = [test_date[i:i + n] for i in range(0, len(test_date), n)]
        result = ".".join(segments)
    else:
        result = rollback_date
    return result


def start_gui():
    """Opens window, shows GUI, runs UI logic"""
    while True:
        event, values = window.read()
        if event == "default":  # sets relevant options to read only, update all preferences
            dependent_keys = ["all_day", "last_month", "cal_name", "all_day"]
            if not window["last_month"].get() == "Previous month":
                dependent_keys.extend(["start_date", "end_date"])
            deactivate_dependencies = True if window["default"].get() else False
            set_option(keys=dependent_keys, option="disabled", value=deactivate_dependencies)
        if event == "directory":
            config["output_path"] = window["directory"].get()
        if event == "last_month":  # sets "start_date" & "end_date" to read only, update their values
            if window["last_month"].get() == "Previous month":
                set_def_values(["start_date", "end_date"])
                deactivate_dependencies = True
            else:
                deactivate_dependencies = False
            set_option(["start_date", "end_date"], "disabled", deactivate_dependencies)
            window["end_date"].update(disabled=deactivate_dependencies)
        if event == "all_day":
            config["all_day"] = False
        if event == "start_date":
            rollback = ""
            if "rollback_date" not in locals():
                rollback = eval("def_" + event)
            window[event].update(validate_format(test_date=window[event].get(), rollback_date=rollback))
            rollback = window[event].get()  # save input for later
        if event == "end_date":
            rollback = ""
            if "rollback_date" not in locals():
                rollback = eval("def_" + event)
            window[event].update(validate_format(test_date=window[event].get(), rollback_date=rollback))
            rollback = window[event].get()  # save input for later
        if event == "start":  # download events, create timesheet, save current settings
            # get values from interface
            for key in window.key_dict:
                if key in userConfig.settings_structure.keys():
                    config[key] = window[key].get()
                    if key == "last_month":
                        config[key] = True if window[key].get().lower() == "previous month" else False
                    if key == "start_date" or key == "end_date":
                        config[key] = window[key].get()[0:2] + window[key].get()[3:5] + window[key].get()[6:8]
            # save values as config file
            userConfig.save_pref(config)
            appointments = apiInteractions.download_appointments()
            timesheeBuilder.build_assistant(appointments)
        if event == sg.WIN_CLOSED:
            break
    window.close()


if __name__ == "__main__":
    start_gui()
