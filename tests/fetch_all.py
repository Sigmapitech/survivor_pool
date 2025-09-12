#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3Packages.requests
import requests

BASE = "http://localhost:8000/api"
ENDPOINTS = ["events", "investors", "news", "partners", "projects", "startups", "users"]

# endpoints that have a /{id}/image sub-endpoint
IMAGE_ENDPOINTS = {"events", "investors", "news", "users"}

for ep in ENDPOINTS:
    url = f"{BASE}/{ep}/"
    res = requests.get(url).json()
    print(f"\n=== {ep.upper()} ({len(res)} items) ===")

    for i, item in enumerate(res):
        print(f"[{i}] {item}")

        # special case: call /{id}/image
        if ep in IMAGE_ENDPOINTS:
            # assume primary key is always `id`
            item_id = item.get("id")
            if item_id is not None:
                image_url = f"{BASE}/{ep}/{item_id}/image"
                img_res = requests.get(image_url)
                print(f"    Image status: {img_res.status_code}")
