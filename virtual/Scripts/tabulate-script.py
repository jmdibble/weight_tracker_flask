#!"c:\users\josh\onedrive\all documents\coding\python\mega\weight_tracker_flask\virtual\scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'tabulate==0.8.3','console_scripts','tabulate'
__requires__ = 'tabulate==0.8.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('tabulate==0.8.3', 'console_scripts', 'tabulate')()
    )
