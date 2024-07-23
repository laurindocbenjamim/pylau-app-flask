
import os

def _catch_sys_except_information(sys, traceback, location="model", custom_message="error"):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

    error_info = f"Error occured on method[{location}] \
        \nFile name: {fname}\
        \nException-instance: {fname}\
        \nException-classe: {exc_type}\
        \nException-object: {exc_obj}\
        \nCustomized-message: {custom_message}\
        \nLine of error: {exc_tb.tb_lineno}\
        \n ____ ERROR DETAILS_____: \n{str(sys.exc_info())}\
        \nTB object: {exc_tb}\
        \nTraceback object: {str(traceback.format_exc())}\
        "
    return error_info