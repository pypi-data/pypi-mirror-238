
# Welcome to Sap Manager!

A library that facilitates the creation of a session in SAP, through the credentials provided and information from the environment, promoting the ease of logging in and working with SAP's native Scripting.

# Sap

A **Class** who starts SAP logged into the selected system with the credentials provided, facilitating Scripting.

## Attributes

| Attribute | Type |
| -------- | ------------------ |
| system | **str** |
| mandt | **str** |
| user | **str** |
| password | **str** |
| path | **str** or **None**|

- **system**: the system (by SID) you will use.

- **mandt**: the mandt you will use in the system.

- **user**: the user of the account you will use to login.

- **password**: the password of the account you will use to login.

- **path**: the path to saplogon.exe, If **None** the path used in the **default SAP installation will be used**.

- **language**: the language that will be used in SAP, by default is "EN".

- **timeout**: the timeout max value that will be used in SAP to connect into system, default is 10.

Example:
```
from sapmanager import Sap

session = Sap("PRD", "500", "Renks", "password")
```
>After success, it will be possible to use the SAP scripting with your account already logged in the selected system.


## Returns

Returns an object of type **win32com.client.CDispatch** ready to use an SAP session, by convention the variable is named "session".