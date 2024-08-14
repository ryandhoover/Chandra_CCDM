"SSR Rollover Detection"

from cxotime import CxoTime
from components.data_requests import maude_data_request as maude_data

def ssr_rollover_detection(user_vars):
    "ssr rollover detection"
    ssr_rollover_data = get_ssr_rollover_data(user_vars)
    return_string = add_ssr_rollovers(user_vars.ssr_prime[0],ssr_rollover_data)
    return return_string


def get_ssr_rollover_data(user_vars):
    "Parse data for SSR rollovers"
    print("SSR Rollover Detection...")
    rollover_data_full, rollover_data = {}, {}
    active_ssr = user_vars.ssr_prime[0]
    data_a = maude_data(user_vars.ts,user_vars.tp,"COSARCEN")
    data_b = maude_data(user_vars.ts,user_vars.tp,"COSBRCEN")

    for time_a, value_a in zip(data_a["data-fmt-1"]["times"],data_a["data-fmt-1"]["values"]):
        if active_ssr == "A":
            if value_a == "0":
                rollover_data_full.setdefault("A",[]).append({f"{time_a}": f"{value_a}"})
        elif active_ssr == "B":
            if value_a == "1":
                rollover_data_full.setdefault("A",[]).append({f"{time_a}": f"{value_a}"})

    for time_b, value_b in zip(data_b["data-fmt-1"]["times"],data_b["data-fmt-1"]["values"]):
        if active_ssr == "A":
            if value_b == "1":
                rollover_data_full.setdefault("B",[]).append({f"{time_b}": f"{value_b}"})
        elif active_ssr == "B":
            if value_b == "0":
                rollover_data_full.setdefault("B",[]).append({f"{time_b}": f"{value_b}"})

    for ssr, data_lists in rollover_data_full.items():
        for index, (data) in enumerate(data_lists):
            for time, value in data.items():
                if index in (0, (len(data_lists) - 1)):
                    rollover_data.setdefault(ssr,[]).append({f"{time}":f"{value}"})

    del rollover_data_full
    return rollover_data


def add_ssr_rollovers(active_ssr, rollover_data):
    "Add SSR rollover data to config_section string"
    return_string = ""
    if rollover_data:
        if active_ssr == "A":
            for date in rollover_data["A"][0].keys():
                date = CxoTime(date,format="maude")
                return_string += (
                    f"<li>SSR Rollover from SSR-A to SSR-B on {date.yday}z</li>")
                print(f"   - SSR Rollover from SSR-A to SSR-B detected on {date.yday}.")
            for date in rollover_data["A"][1].keys():
                date = CxoTime(date,format="maude")
                return_string += (
                    f"<li>SSR Recovery from SSR-B to SSR-A on {date.yday}z</li>")
                print(f"   - SSR Recovery from SSR-B to SSR-A detected on {date.yday}.")
        else:
            for date in rollover_data["B"][0].keys():
                date = CxoTime(date,format="maude")
                return_string += (
                    f"<li>SSR Rollover from SSR-B to SSR-A on {date.yday}z</li>")
                print(f"   - SSR Rollover from SSR-B to SSR-A detected on {date.yday}.")
            for date in rollover_data["B"][1].keys():
                date = CxoTime(date,format="maude")
                return_string += (
                    f"<li>SSR Recovery from SSR-A to SSR-B on {date.yday}z</li>")
                print(f"   - SSR Recovery from SSR-A to SSR-B detected on {date.yday}.")
    else:
        print(" - No SSR rollover detected.")

    return_string += "</li></ul></div></div>"
    return return_string
