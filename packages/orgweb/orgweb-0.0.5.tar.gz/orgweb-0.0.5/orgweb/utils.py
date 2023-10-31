# [[file:../org/orgweb/utils.org::*Imports][Imports:1]]
import os
from gitignore_parser import parse_gitignore
# Imports:1 ends here

# [[file:../org/orgweb/utils.org::*=.orgwebignore=][=.orgwebignore=:1]]
def orgweb_ignored(file: str, folder: str) -> bool:
    """Check for a .orgwebignore file in `folder`. Check if `file` needs to be
    ignored accordingt to the .orgwebignore file. True if it is ignored, False
    otherwise."""

    # make sure `folder` ends with a '/'
    folder = folder.rstrip('/') + '/'

    # if there is no .gitignore file, then nothing is ignored
    if not os.path.isfile(f"{folder}.orgwebignore"):
        return False

    matches = parse_gitignore(f"{folder}.orgwebignore")
    return matches(f"{folder}{file}")
# =.orgwebignore=:1 ends here
