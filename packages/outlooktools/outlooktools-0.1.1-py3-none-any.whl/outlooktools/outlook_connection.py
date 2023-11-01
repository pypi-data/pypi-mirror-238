
import win32com.client
import re
from pathlib import Path

class OutlookConnection:

    def __init__(self) -> None:
        # Initialize connection to the local Outlook instance
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        pass

    def getFolder(self, folder_name:str, parent_folder:str = None):
        folder = None
        if parent_folder is None:
            folder = self.outlook.Folders[folder_name]
        else:
            folder = parent_folder.Folders[folder_name]

        return folder
    
    def getInbox(self):
        return self.getFolder("Inbox")
    
    def traverseFolders(self, folder_path:str):
        """
        Will return the final Folder object
        Expects a folder_path like Inbox/Folder1/Subfolder1 or Inbox\\Folder1\\Subfolder 2
        Always start with 'Inbox' if that's where the folder is
        """
        #  Split the folder path
        path_list = re.split('[\\\/]', folder_path)
        folder = self.getFolder(path_list[0])
        for next_folder in path_list[1:]:
            folder = self.getFolder(folder_name=next_folder, parent_folder=folder)
        return folder
    
    def sendPlainEmail(self, to:str, subj:str, body:str, attachment:Path = None):
        # Cannot use the self.outlook because that is on the MAPI namespace
        oc = win32com.client.Dispatch("Outlook.Application")
        mail = oc.CreateItem(0)
        mail.To = to
        mail.Subject = subj
        mail.Body = body
        if attachment is not None:
            mail.Attachments.add(f"{attachment}")
        mail.Send()
        
        
        