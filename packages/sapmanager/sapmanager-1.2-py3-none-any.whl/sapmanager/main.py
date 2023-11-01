from sapmanager.exceptions import SapLoginError, SapConnectionError
from win32com.client import CDispatch, GetObject
from win32gui import FindWindowEx
from subprocess import Popen
from typing import Union
import time
import os


class Sap(object):
    """Starts SAP logged into the selected system with the credentials provided, facilitating Scripting.

    Attributes
    ----------
    - system(`str`): the system you will use
    - mandt(`str`): the mandt you will use in the system
    - user(`str`): the user of the account you will use to login
    - password(`str`): the password of the account you will use to login
    - path(`str`): the path to saplogon.exe, If `None` the path used in the default SAP installation will be used
    - language(`str`) the language that will be used in SAP, by default is "EN"
    """

    def __new__(cls, system: str,
                mandt: str,
                user: str,
                password: str,
                path: str = None,
                language="EN",
                timeout=10) -> Union[CDispatch, None]:

        system = cls.__check_arg_type(system, str, "system")
        mandt = cls.__check_arg_type(mandt, str, "mandt")
        user = cls.__check_arg_type(user, str, "user")
        password = cls.__check_arg_type(password, str, "password")
        language = cls.__check_arg_type(language, str, "language")
        path = cls.__check_path(path)
        timeout = cls.__check_arg_type(timeout, int, "timoeut")

        process = Popen(f"{path} -system={system} -client={mandt} -user={user} -pw={password} -language={language}")

        start_time = time.time()
        while time.time() < start_time + timeout:
            if FindWindowEx(None, None, None, "SAP") != 0:
                break

            if time.time() >= start_time + timeout:

                raise ConnectionError("timeout for connect into system has been reached")

        application = GetObject('SAPGUI').GetScriptingEngine
        session = application.Children(0).Children(0)

        if session.Info.user:
            if session.ActiveWindow.Text == "Copyright":
                session.findById("wnd[1]").sendVKey(0)
            return session
        else:
            error = session.findById("wnd[0]/sbar").text
            raise SapLoginError(error)

    @classmethod
    def __check_arg_type(cls, arg, valid_type, arg_name):
        if not isinstance(arg, valid_type):
            raise ValueError(f"{arg_name} must be str")
        return arg

    @classmethod
    def __check_path(cls, path):
        if path is None:
            if not os.path.exists("C:\\Program Files\\SAP\\FrontEnd\\SAPGUI\\sapshcut.exe"):
                OSError("sapshcut.exe not found")

            return "C:\\Program Files\\SAP\\FrontEnd\\SAPGUI\\sapshcut.exe"

        if not isinstance(path, str):
            raise ValueError("the path must be str")
        if not os.path.exists(path):
            raise OSError("sapshcut.exe not found")
        return path
