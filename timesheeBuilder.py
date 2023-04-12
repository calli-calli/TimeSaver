# builds timesheet.csv from Calendar data
import csv
from datetime import timedelta
import userConfig


def _make_pretty(events: list) -> list:
    """expects list that contains dictionaries. Adds delta to all events."""
    total = timedelta()
    for count, event in enumerate(events):
        # add Start-Date & End-Date
        events[count]["s_date"] = events[count]["start"].strftime("%d.%m.%y")
        events[count]["e_date"] = events[count]["end"].strftime("%d.%m.%y")
        # reformat start & end to time in readable format
        events[count]["s_time"] = events[count]["start"].strftime("%H:%M:%S")
        events[count]["e_time"] = events[count]["end"].strftime("%H:%M:%S")
        # Add delta
        delta = abs(event["start"] - event["end"])
        hours = int(delta.total_seconds() / 3600)
        minutes = int((delta.total_seconds() % 3600) / 60)
        events[count]["delta"] = f"{hours}h {minutes}min"
        total += delta  # prep for calculating total
    # calc total time
    hours = int(total.total_seconds() / 3600)
    minutes = int((total.total_seconds() % 3600) / 60)
    events.append({"Total": f"{hours}h{minutes}min"})

    return events


def _write_to_file(events: list):
    # todo add arguments for flexibility. I.e. Show/don't show value
    # csv in this order. Structure: [[key for value: str, bool, column_name: str]]
    order = [["start", False, "Start"],
             ["end", False, "End"],
             ["s_date", True, "Start date"],
             ["e_date", True, "End date"],
             ["s_time", True, "Start Time"],
             ["e_time", True, "End Time"],
             ["delta", True, "Delta"],
             ["summary", True, "Summary"],
             ["description", True, "Details"],
             ["all_day", False, "All-Day"]]
    # header
    header = [["SEP=,"]]
    headings = []
    [headings.append(a[2]) for a in order if a[1]]
    header.append(headings)
    # body
    body = []
    for event in events:
        line = [event[o[i]] for i, o in enumerate(order) if order[i][1]]
        # [line.append() for i, o in enumerate(order) if order[i][1]]
        # for i, o in enumerate(order):
        #     if order[i][1] and o[0] in event.keys():
        #         line.append(event[o[0]])
        body.append(line[:])
    # footer
    footer = list(events[-1].items())
    # write to .csv file
    directory = userConfig.get_pref("output_path")['output_path']
    directory = directory.replace("/", "\\\\") + "\\\\"
    with open((directory + "timesheet.csv"), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(header + body + footer)


def build_assistant(events: list):
    """Makes the events pretty and writes them to a *.csv file"""
    mod_events = _make_pretty(events)
    _write_to_file(mod_events)


if __name__ == '__main__':
    pass
