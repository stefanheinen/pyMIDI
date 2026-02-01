import os
import subprocess
from logging import info
from pathlib import Path

from launchd_plist import Plist

from globals import PROJECT_ROOT

label = "com.stefanchaim.pyConduktor"
plistPath = Path(f"~/Library/LaunchAgents/{label}.plist").expanduser().resolve()
stdout_log = Path("/tmp/pyConduktor.log")
stderr_log = Path("/tmp/pyConduktor.log")


class MyAgentPlist(Plist):
    # The agent’s label (unique identifier)
    Label = label

    # Ensures the job runs at load (login)
    RunAtLoad = True

    # ProgramArguments must include the full interpreter + script
    ProgramArguments = [
        str(PROJECT_ROOT / "pyConduktor.sh"),
        "--statusbar"
    ]

    # Define your PATH so launchd runs tools in that PATH
    EnvironmentVariables = {
        "PATH": os.environ.get("PATH"),
        "DYLD_LIBRARY_PATH": os.environ.get("DYLD_LIBRARY_PATH")
    }

    # Standard output and error logs (optional but helpful)
    @property
    def StandardOutPath(self):
        return str(Path("/tmp/pyConduktor.log"))

    @property
    def StandardErrorPath(self):
        return str(Path("/tmp/pyConduktor.log"))



def activate():
    # Write out the plist file
    agent = MyAgentPlist()
    info(f"Writing launchAgent plist to {plistPath}")
    agent.create(str(plistPath))

    # this might display an error (Bootstrap failed: 5: Input/output error) if the deactivate() function
    # was used, as it only removes the plist file so as not to kill the running application.
    # that means it is still bootstrapped in launchctl, but the plist file doesn't exist anymore.
    info("Bootstrapping launchAgent...")
    cmd = ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(plistPath)]
    print(f"\t{" ".join(cmd)}")
    result = subprocess.run(cmd)

def deactivate():
    if plistPath.exists():
        info("Deactivating launchAgent plist...")
        plistPath.unlink(missing_ok=True)

def deactivate_and_kill():
    info("Booting out launchAgent...")
    cmd = ["launchctl", "bootout", f"gui/{os.getuid()}", str(plistPath)]
    print(f"\t{" ".join(cmd)}")
    result = subprocess.run(cmd)
    deactivate()

def remove():
    info(f"Deleting launchAgent plist: {plistPath}")
    plistPath.unlink(missing_ok=True)
    info(f"Deleting launchAgent plist: {plistPath}.deactivated")
    plistPath.with_suffix(".deactivated").unlink(missing_ok=True)

def get_activated_status():
    # check if plist exists
    if not plistPath.exists():
        return False
    return True