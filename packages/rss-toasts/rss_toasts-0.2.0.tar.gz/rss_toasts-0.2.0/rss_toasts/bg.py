import subprocess
import sys
from textwrap import dedent


def run_in_background():
    """Runs rss-toasts in the background with pythonw"""
    script = dedent(
        """
        import subprocess
        subprocess.Popen(
            'start "" /B rss-toasts run',
            shell=True,
        )
        """
    )
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    subprocess.Popen([pythonw, "-c", script])


if __name__ == "__main__":
    run_in_background()
