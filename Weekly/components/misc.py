"MISC Methods"

def format_wk(wk_no_format):
    "Format the timetuple into a 2 digit string"
    wk_formatted = ""
    if len(str(wk_no_format)) == 2:
        wk_formatted = wk_no_format
    elif len(str(wk_no_format)) == 1:
        wk_formatted = f"0{wk_no_format}"
    return wk_formatted


def format_doy(doy_no_format):
    "Format the timetuple into a 3 digit string"
    if len(doy_no_format) == 3:
        doy_formatted = doy_no_format
    elif len(doy_no_format) == 2:
        doy_formatted = f"0{doy_no_format}"
    elif len(doy_no_format) == 1:
        doy_formatted = f"00{doy_no_format}"
    return doy_formatted
