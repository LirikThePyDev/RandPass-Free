# RandPass
RandPass is a lightweight Windows password generator. Create strong, random passwords offline using letters, numbers, and symbols. Easy-to-use, fully local, and no passwords are stored.

License: Personal use only; redistribution prohibited unless explicitly permitted.

Requirements:

- Python 3.x installed on Windows
- Basic knowledge of running Python scripts
- PyInstaller installed: pip install pyinstaller

How to Run:
- Clone or download the repository: git clone https://github.com/LirikThePyDev/RandPass.git
- Navigate to the folder: cd RandPass
- Build a standalone Windows .exe: pyinstaller --onefile --name RandPass randpass.py

  or

  py -m pyinstaller --onefile --name RandPass randpass.py

Notes:
- Passwords are generated locally; no passwords are stored
- Minimum password length is enforced for security
- Use this software for personal, non-commercial purposes only
