from pathlib import Path

def loadCommonCreds(filename="commonCreds.txt"):
    base_dir = Path(__file__).resolve().parent.parent   # utils/ -> kuaria/
    file_path = base_dir / "data" / filename

    creds = []
    with file_path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",", 2)]
            while len(parts) < 3:
                parts.append("")
            username, password, secret = parts
            creds.append((username, password, secret))
    return creds