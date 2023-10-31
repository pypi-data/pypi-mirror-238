# [[file:../org/orgweb/org.org::*Imports][Imports:1]]
import os
import re
from typing import Optional
from orgweb.container import create_container, delete_container
from orgweb.utils import orgweb_ignored
# Imports:1 ends here

# [[file:../org/orgweb/org.org::*Folder Referencing][Folder Referencing:1]]
def folder_ref(folder: str) -> str:
    return os.path.abspath(os.path.expanduser(folder))
# Folder Referencing:1 ends here

# [[file:../org/orgweb/org.org::*Get relative directory][Get relative directory:1]]
def relative_dir(root: str, folder: str) -> str:
    """Return the relative `dir` for a file's `root` path according to
    `folder`. The returned relative path ends with `/`. If `root` is the same
    as `folder`, then an empty string is returned

    """
    dir = root.removeprefix(folder).strip('/')
    if len(dir) == 0:
        return ''
    else:
        return dir + '/'
# Get relative directory:1 ends here

# [[file:../org/orgweb/org.org::*Tangle][Tangle:1]]
def tangle(folder: str, files: Optional[list]=None):
   """Tangle all the files of `folder` recursively. If `files` contains any
   file, the tangling will be restricted to those listed files only."""

   folder = folder_ref(folder)

   try:
       volume = {f"{folder}": {'bind': '/mnt/org',
                                'mode': 'rw'}}

       container = create_container(volume)

       if not files:
           print(f"Tangling {folder}...")
       else:
           print(f"Tangling {files}...")

       # for each org file in the folder, recursively, tangle them
       for root, dirs, dir_files in os.walk(folder):
           for file in dir_files:
              if file.endswith(".org") and (not files or file in files):
                 dir = relative_dir(root, folder)

                 # ignore file if it is igored by a .gitignore file
                 if orgweb_ignored(root + "/" + file, folder):
                    continue

                 print("Tangling:", file)
                 response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (find-file \\\"/mnt/org/{dir}{file}\\\") (org-babel-tangle))\"")
                 print(response.output.decode('utf-8'))
   except Exception as e:
       print("Tangling canceled:", str(e))
   finally:
       delete_container()
# Tangle:1 ends here

# [[file:../org/orgweb/org.org::*Detangle][Detangle:1]]
def detangle(folder: str, files: Optional[list]=None):
    """Syhnchronize the source files there have been tangled back to their
    original Org code blocks. Code blocks needs to have the header 
    `:comments link` or `:comments both` to be detangled. If you use
    `:noweb yes` references, then the noweb references won't be detangled,
    and the original Org file will be missing the noweb references. So,
    don't use detangle until detangling with noweb is fixed in Org-mode.
    If `files` has a reference to one or more files, only
    tangle the files, in the `folder`, that are in the `files` 
    list."""

    folder = folder_ref(folder)

    try:
        volume = {f"{folder}": {'bind': '/mnt/org',
                                'mode': 'rw'}}

        container = create_container(volume)

        if not files:
            print(f"Detangling {folder}...")
        else:
            print(f"Detangling {files}...")

        # for each source file in the folder, detangle it
        for root, dirs, dir_files in os.walk(folder):

            # ignore folder if it is igored by a .gitignore file
            if orgweb_ignored(root, folder):
                continue

            for file in dir_files:
                if not file.endswith(".org") and (not files or file in files):
                    dir = relative_dir(root, folder)

                    # ignore file if it is igored by a .gitignore file
                    if orgweb_ignored(root + "/" + file, folder):
                        continue

                    org_file = ""

                    with open(f"{dir}{file}", "r") as tangled_file:
                        content = tangled_file.read()
                        try:
                            org_file = list(set(re.findall(r"file:(.*)::",content)))[-1]
                        except Exception as e:
                            continue

                        if(len(org_file) > 0):
                            org_file = org_file.split("/")[-1]
                            print(f"Detangling: {file} into {org_file}")
                            response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (org-babel-detangle \\\"/mnt/org/{dir}{file}\\\") (switch-to-buffer \\\"{org_file}\\\") (save-buffer))\"")
                            print(response.output.decode('utf-8'))
    except Exception as e:
        print("Detangling canceled:", str(e))
    finally:
        delete_container()
# Detangle:1 ends here

# [[file:../org/orgweb/org.org::*Execute][Execute:1]]
def execute(folder: str, files: Optional[list]=None):
    """Execute all the code blocks in the Org files in the folder.
    When you use this operation, it will execute all the code blocks
    of the file(s)."""

    folder = folder_ref(folder)

    try:
        volume = {f"{folder}": {'bind': '/mnt/org',
                                'mode': 'rw'}}
        container = create_container(volume)

        if not files:
            print(f"Execute {folder}...")
        else:
            print(f"Execute {files}...")

        # for each org file in the folder, tangle it
        for root, dirs, dir_files in os.walk(folder):
            for file in dir_files:
                if file.endswith(".org") and (not files or file in files):
                    dir = relative_dir(root, folder)

                    # ignore file if it is igored by a .gitignore file
                    if orgweb_ignored(root + "/" + file, folder):
                        continue

                    print("Execute:", file)
                    response = container.exec_run(f"emacs --load /root/.emacs.d/site-start.el --batch --eval \"(progn (find-file \\\"/mnt/org/{dir}{file}\\\") (setq org-confirm-babel-evaluate nil) (org-babel-execute-buffer))\"")
                    print(response.output.decode('utf-8'))
    except Exception as e:
        print("Execute canceled:", str(e))
    finally:
        delete_container()
# Execute:1 ends here
