# SPDX-FileCopyrightText: 2023-present richmr <richmr@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
from pathlib import Path

import typer

from outlooktools.__about__ import __version__
from outlooktools.outlook_connection import OutlookConnection

app = typer.Typer(name="OutlookTools")

def printSubfolders(folder_com_obj):
    """
    Prints all the folders inside the supplied folder path
    """
    # make a list of them
    folder_list = [f.name for f in folder_com_obj.Folders]
    # sort it for ease of reading
    folder_list.sort(key=str.lower)
    for folder_name in folder_list:
        print(f"\t{folder_name}")

@app.command()
def count_items(folder_path:str):
    """
    Returns a count of items in the designated folder
    Expects a folder_path like Inbox/Folder1/Subfolder1 or Inbox\\Folder1\\Subfolder 2
    """
    oc = OutlookConnection()
    folder = oc.traverseFolders(folder_path)
    messages = list(folder.Items)
    print(f"There are {len(messages)} messages in {folder_path}")
    
@app.command()
def list_mailboxes():
    """
    Prints a list of all available mailboxes for this Outlook instance
    """
    oc = OutlookConnection()
    print("Available mailboxes:")
    printSubfolders(oc.outlook)
    print("")
    print("Prepend this to your folder path to delve into correct mailbox")

@app.command()
def list_folders(folder_path:str):
    """
    Lists all folders for a given folder path
    """
    oc = OutlookConnection()
    folder = oc.traverseFolders(folder_path)
    print(f"Subfolders in this {folder_path}")
    printSubfolders(folder)

@app.command()
def export_attachments(email_folder_path:str, save_location:Path):
    """
    Saves all attachments found in the designated email folder.
    """
    if not save_location.is_dir():
        print(f"The provided path {save_location} is not a valid folder.  Please check and create it if necessary.")
        raise typer.Exit(code=3)
    
    # If you use a relative path, it will save the attachments relative to the file location of the exchange mailbox!
    save_location = save_location.absolute()
    
    oc = OutlookConnection()
    folder = oc.traverseFolders(email_folder_path)
    # Store filenames to deal with duplicates
    filenames = []
    # Adapted from: https://hridai.medium.com/automate-your-outlook-e-mail-with-python-f4eddce975
    for msg in folder.Items:
        for atmt in msg.Attachments:
            filename = atmt.FileName
            count_of_file = filenames.count(filename)
            if count_of_file > 0:
                # split from suffixes
                parts = filename.split(".")
                filename = f"{parts[0]}_{count_of_file}"
                # watch out for filenames with no suffixes
                if len(parts) > 0:
                    filename = filename + "." + ".".join(parts[1:])
            filename = f"{save_location}\\{filename}"
            try:
                atmt.SaveAsFile(filename)
                filenames.append(atmt.Filename)
            except Exception as badnews:
                print(f"Unable to save {filename} because {badnews}")

            

    print(f"Exported {len(filenames)} files to {save_location}")
    print("Please note there may be a lot of 'filler' images labeled like image001.jpg or image002.png.  These are generally from signatures and other design elements in the email.\nHowever, screenshots are labeled the same way, so these are exported as well.")

@app.command()
def send_plain_email():
    """
    Allows sending a plain text email with a single attachment
    """
    oc = OutlookConnection()
    to = typer.prompt("To")
    subj = typer.prompt("Subject")
    body = typer.prompt("Message")
    attachment_path = typer.prompt("Path to attachment", default="None", show_default=True)
    if attachment_path != "None":
        attachment_path = Path(attachment_path)
    else:
        attachment_path = None
    send_it = typer.confirm("Send this email?")
    if send_it:
        oc.sendPlainEmail(to, subj, body, attachment_path)
    else:
        print("Email was not sent")

def outlooktools():
    try:
        app()
    except Exception as badnews:
        if -2147352567 in badnews.args:
            print("The supplied mailbox or folder does not exist.  Please use list-mailboxes and list-folders to see valid entries.")
            raise typer.Exit(code=3)
        else:
            raise badnews