from pathlib import Path
import sys
import __main__

try:
    main_file = Path(__main__.__file__).resolve()
except AttributeError:
    main_file = Path(sys.argv[0]).resolve()

PROJECT_ROOT = main_file.parent