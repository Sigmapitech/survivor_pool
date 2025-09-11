#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.requests

import json
import random
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000/api"
FRONT_BASE_URL = "http://localhost:5173/"
PROJECTS_FILE = Path("projects.json")

EMAIL = "sg@a.b"


def login():
    password = input("Enter admin password: ")
    resp = requests.post(
        f"{BASE_URL}/auth/login", json={"email": EMAIL, "password": password}
    )
    if not resp.ok:
        print("Login failed:", resp.text)
        exit(1)
    data = resp.json()
    token = data.get("token")
    if not token:
        print("Login failed: no token received")
        exit(1)
    return {"Authorization": f"Bearer {token}"}


def download_logo(logo_path):
    resp = requests.get(FRONT_BASE_URL + logo_path)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download image: {FRONT_BASE_URL + logo_path}")
    return ("logo.png", resp.content, "image/png")


def create_project(headers, project, startup_id):
    worth = random.randint(10_000_000, 50_000_000)
    files = {
        "name": (None, project["name"]),
        "description": (None, project["description"]),
        "worth": (None, str(worth)),
        "logo": download_logo(project.get("logo", "")),
    }
    resp = requests.post(
        f"{BASE_URL}/projects/{startup_id}", headers=headers, files=files
    )
    print(f"Created project '{project['name']}' (Response: {resp.text})")


def main():
    headers = login()

    if not PROJECTS_FILE.exists():
        print(f"File {PROJECTS_FILE} not found")
        exit(1)

    with PROJECTS_FILE.open("r", encoding="utf-8") as f:
        projects = json.load(f)

    for i, project in enumerate(projects, start=1):
        # choose a random startup_id (1–32 as in your previous script)
        startup_id = random.randint(1, 32)
        try:
            create_project(headers, project, startup_id)
        except Exception as e:
            print(f"Failed to create project '{project['name']}': {e}")


if __name__ == "__main__":
    main()
