import os
import requests
import json
import zipfile

# Base URL of the server (ensure there is no trailing slash)
BASE_URL = "http://new.serveminecraft.net:5060".rstrip("/") + "/"

# Global variables to store session credentials (used for upload, create_account, etc.)
USER_EMAIL = None
USER_PASSWORD = None
CREDENTIALS_FILE = "credentials.txt"

def load_credentials():
    """Load credentials from 'credentials.txt'"""
    global USER_EMAIL, USER_PASSWORD
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = f.read().strip().split('\n')
            if len(credentials) == 2:
                USER_EMAIL = credentials[0]
                USER_PASSWORD = credentials[1]
                print("Credentials loaded successfully!")

def save_credentials():
    """Save credentials to 'credentials.txt'"""
    global USER_EMAIL, USER_PASSWORD
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f"{USER_EMAIL}\n{USER_PASSWORD}")
    print("Credentials saved successfully!")

def create_account():
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}create_account", json=data)
    if response.status_code == 201:
        print("Account created!")
        global USER_EMAIL, USER_PASSWORD
        USER_EMAIL = email
        USER_PASSWORD = password
        save_credentials()
    else:
        print("Error creating account:", response.json().get('error'))

def login():
    global USER_EMAIL, USER_PASSWORD
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}login", json=data)
    if response.status_code == 200:
        USER_EMAIL = email
        USER_PASSWORD = password
        print("Login successful!")
        save_credentials()
    else:
        print("Login error:", response.json().get('error'))

def get_folder_structure(folder_path):
    """Recursively gets the structure of a folder, including subfolders and files."""
    structure = {}
    for root, dirs, files in os.walk(folder_path):
        relative_path = os.path.relpath(root, folder_path)
        if relative_path == ".":
            relative_path = ""
        structure[relative_path] = {
            "files": {},
            "subfolders": []
        }
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            structure[relative_path]["files"][file] = content
        for dir in dirs:
            structure[relative_path]["subfolders"].append(dir)
    return structure

def upload_library():
    if not USER_EMAIL or not USER_PASSWORD:
        print("You must be logged in to upload!")
        return

    folder_path = input("Enter the path of the folder you want to upload: ").strip()
    if not os.path.exists(folder_path):
        print("Folder not found!")
        return

    # Obtém o nome original da pasta
    folder_name = os.path.basename(folder_path)

    # Obtém a estrutura da pasta
    folder_structure = get_folder_structure(folder_path)

    # Envia a estrutura para o servidor
    data = {
        "email": USER_EMAIL,
        "password": USER_PASSWORD,
        "folder_name": folder_name,  # Envia o nome original da pasta
        "folder_structure": folder_structure
    }
    try:
        response = requests.post(f"{BASE_URL}upload", json=data, timeout=30)
        if response.status_code == 200:
            print("Library uploaded successfully!")
        else:
            print("Error during upload:", response.json().get('error'))
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)
    except requests.exceptions.Timeout as e:
        print("Upload timed out:", e)
    except Exception as e:
        print("An error occurred:", e)

def download_library():
    library_name = input("Enter the name of the library to be downloaded: ").strip().strip("/")
    url = f"{BASE_URL}download/{library_name}"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Verifica se o conteúdo é um arquivo ZIP
            if "application/zip" in response.headers.get("Content-Type", ""):
                zip_file_path = os.path.join(os.getcwd(), f"{library_name}.zip")
                with open(zip_file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                # Extrai o arquivo ZIP
                extract_folder = os.path.join(os.getcwd(), library_name)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)
                os.remove(zip_file_path)
                print(f"Library folder '{library_name}' downloaded and extracted successfully to {extract_folder}!")
            else:
                # Caso seja um único arquivo
                save_path = os.path.join(os.getcwd(), library_name)
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Library '{library_name}' downloaded successfully to {save_path}!")
        else:
            try:
                error = response.json().get('error')
            except Exception:
                error = response.text
            print("Download error:", error)
    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)

def search_library():
    query = input("Enter the search term: ").strip()
    url = f"{BASE_URL.rstrip('/')}/search"
    response = requests.get(url, params={"q": query})
    if response.status_code == 200:
        results = response.json()
        if results:
            print("Libraries found:")
            for folder, files in results.items():
                print(f" - {folder}")
                for file in files:
                    print(f"     - {file}")
        else:
            print("Nothing found.")
    else:
        try:
            error = response.json().get('error')
        except Exception:
            error = response.text
        print("Search error:", error)

def main():
    load_credentials()  # Load credentials on startup
    print("Client C/C++ Packages/Libraries")
    while True:
        command = input("Enter the command (create_account, login, upload, download, search, exit): ").strip().lower()
        if command == "create_account":
            create_account()
        elif command == "login":
            login()
        elif command == "upload":
            upload_library()
        elif command == "download":
            download_library()
        elif command == "search":
            search_library()
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print("Command not found, try again later.")

if __name__ == "__main__":
    main()