from pathlib import Path
import sys

# 1. Point Python to look inside the 'app' directory for your imports
APP_DIR = Path(__file__).resolve().parent / "app"
sys.path.insert(0, str(APP_DIR))

# 2. Import the main function from your menu app inside the folder
from main import main as launch_grc_menu

if __name__ == "__main__":
    # 3. Fire up the complete interactive menu
    launch_grc_menu()