import sys;import os; from json import dumps
def Error(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fnamez = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error_equals = {
        "Error Type": f"{exc_type}",
        "File Name": f"{fnamez}",
        "Line number": f"{exc_tb.tb_lineno}",
        "Error": f"{e}"
    }
    print(dumps(error_equals, indent=4))