# randpass.py
import secrets
import string
import os
import json
import time

# -----------------------------
# File handling (Windows-safe)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_FILE = os.path.join(BASE_DIR, "password_history.json")

MIN_LENGTH = 8
DEFAULT_LENGTH = 12
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/|"
AMBIGUOUS = "O0l1I"

# -----------------------------
# Password utilities
# -----------------------------
def generate_password(
    length=DEFAULT_LENGTH,
    use_upper=True,
    use_lower=True,
    use_numbers=True,
    use_symbols=True,
    avoid_ambiguous=True
):
    length = max(MIN_LENGTH, length)
    chars = ""

    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += SYMBOLS

    if avoid_ambiguous:
        for c in AMBIGUOUS:
            chars = chars.replace(c, "")

    if not chars:
        chars = string.ascii_letters + string.digits

    return "".join(secrets.choice(chars) for _ in range(length))

def password_strength(password):
    score = 0.0

    if len(password) >= 12:
        score += 0.25
    if any(c.islower() for c in password):
        score += 0.2
    if any(c.isupper() for c in password):
        score += 0.2
    if any(c.isdigit() for c in password):
        score += 0.2
    if any(c in SYMBOLS for c in password):
        score += 0.15

    return min(score, 1.0)

# -----------------------------
# History (NO plaintext storage)
# -----------------------------
def load_history():
    if not os.path.exists(STORAGE_FILE):
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(length, strength):
    history = load_history()
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "length": length,
        "strength_percent": round(strength * 100, 1)
    }
    history.append(entry)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# -----------------------------
# Main program
# -----------------------------
def main():
    print("==============================")
    print("           RandPass        ")
    print("==============================\n")

    while True:
        print("Options:")
        print("1. Generate password")
        print("2. View password history")
        print("0. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            try:
                length = int(input("Password length (default 12): ") or DEFAULT_LENGTH)
            except ValueError:
                length = DEFAULT_LENGTH

            print("\nComplexity levels:")
            print("1. Basic  (letters + numbers)")
            print("2. Strong (letters + numbers + symbols)")
            print("3. Max    (strong + avoid ambiguous)")
            level = input("Select level (1-3, default 2): ").strip() or "2"

            if level == "1":
                pw = generate_password(
                    length,
                    use_upper=True,
                    use_lower=True,
                    use_numbers=True,
                    use_symbols=False,
                    avoid_ambiguous=False
                )
            elif level == "3":
                pw = generate_password(
                    length,
                    use_upper=True,
                    use_lower=True,
                    use_numbers=True,
                    use_symbols=True,
                    avoid_ambiguous=True
                )
            else:
                pw = generate_password(
                    length,
                    use_upper=True,
                    use_lower=True,
                    use_numbers=True,
                    use_symbols=True,
                    avoid_ambiguous=False
                )

            strength = password_strength(pw)

            print(f"\nGenerated password:\n{pw}")
            print(f"Strength: {strength * 100:.1f}%\n")

            save_history(len(pw), strength)

        elif choice == "2":
            history = load_history()
            if not history:
                print("\nNo password history found.\n")
            else:
                print("\nPassword History:")
                for h in history:
                    print(
                        f"{h['timestamp']} | "
                        f"Length: {h['length']} | "
                        f"Strength: {h['strength_percent']}%"
                    )
                print()

        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
