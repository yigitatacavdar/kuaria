from pathlib import Path
from kuaria.utils import customEncryption
import hashlib

def get_data_path(filename: str) -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / filename

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def loadCommonCreds(filename="commonCreds.txt"):
    file_path = get_data_path(filename)
    creds = []

    if not file_path.exists() or file_path.stat().st_size == 0:
        return creds

    with file_path.open("rb") as f:
        encrypted_data = f.read()
    try:
        plaintext = customEncryption.decrypt(encrypted_data, "internal_program_key")
    except Exception:
        raise ValueError("Failed to decrypt credentials file.")

    for line in plaintext.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",", 2)]
        while len(parts) < 3:
            parts.append("")
        username, password, secret = parts
        creds.append((username, password, secret))
    return creds


def saveCommonCreds():
    cred_file = get_data_path("commonCreds.txt")
    pass_file = get_data_path("credPass.txt")

    print("Credentials Menu. Choose (1,2,3):")
    print("1 - List device credentials.")
    print("2 - Add device credentials.")
    print("3 - Set new credential access password")

    choice = input("> ").strip()

    if choice == "1":
        access = input("Enter access password: ").strip()
        if not pass_file.exists():
            print("No access password set. Please set one first.")
            return
        with pass_file.open() as f:
            saved_hash = f.read().strip()
        if hash_password(access) != saved_hash:
            print("Access denied.")
            return
        creds = loadCommonCreds()
        if not creds:
            print("No credentials saved.")
            return
        for i, (u, p, s) in enumerate(creds, 1):
            print(f"Device {i}: username={u}, password={p}, secret={s}")

    elif choice == "2":
        access = input("Enter access password: ").strip()
        if not pass_file.exists():
            print("No access password set. Please set one first.")
            return
        with pass_file.open() as f:
            saved_hash = f.read().strip()
        if hash_password(access) != saved_hash:
            print("Access denied.")
            return

        creds_list = loadCommonCreds()
        while True:
            line = input("Enter credential (username,password,enablepassword) or 'exit' to finish: ").strip()
            if line.lower() == "exit":
                break
            if "," not in line:
                print("Invalid format. Use username,password,enablepassword")
                continue
            creds_list.append(tuple([p.strip() for p in line.split(",", 2)]))
            print("Credential saved successfully.")

        plaintext = "\n".join([",".join(c) for c in creds_list])
        encrypted = customEncryption.encrypt(plaintext, "internal_program_key")
        with cred_file.open("wb") as f:
            f.write(encrypted)

    elif choice == "3":
        new_pass = input("Enter new access password: ").strip()
        with pass_file.open("w") as f:
            f.write(hash_password(new_pass) + "\n")
        with cred_file.open("wb") as f:
            pass
        print("New access password set. All previous credentials cleared.")

    else:
        print("Invalid choice.")
