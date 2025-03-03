import os
import subprocess
import urllib.request

# Define the base URL and version
BASE_URL = "https://cdn.openbsd.org/pub/OpenBSD/snapshots/arm64"
VERSION = "76"

# List of files to download
FILES = [
    f"base{VERSION}.tgz",
    f"comp{VERSION}.tgz",
    f"xbase{VERSION}.tgz",
    f"xfont{VERSION}.tgz",
    f"xserv{VERSION}.tgz",
    f"xshare{VERSION}.tgz",
]

# Download each file
def download_files():
    for file in FILES:
        url = f"{BASE_URL}/{file}"
        print(f"Downloading {file}...")
        urllib.request.urlretrieve(url, file)
        print(f"Downloaded {file}")

# Extract tar files
def extract_files():
    os.makedirs("root", exist_ok=True)
    for file in FILES:
        filepath = f"./{file}"
        print(f"Extracting {filepath} into ./root...")
        subprocess.run(["tar", "xzphf", filepath, "-C", "root"], check=True)

    # Extract specific files with sudo
    os.chdir("root")
    subprocess.run(["sudo", "tar", "xvzf", "root/var/sysmerge/xetc.tgz"], check=True)
    subprocess.run(["sudo", "tar", "xvzf", "root/var/sysmerge/etc.tgz"], check=True)

def main():
    download_files()
    extract_files()

if __name__ == "__main__":
    main()
