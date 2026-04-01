#!/usr/bin/env python3
import json
import os
import subprocess
import sys

LMS = os.path.expanduser("~/.lmstudio/bin/lms")


def run(cmd, timeout=6):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (r.stdout + r.stderr).strip()
    except Exception:
        return ""


def bytes_to_human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def server_status():
    out = run([LMS, "server", "status"])
    running = "not running" not in out.lower() and "running" in out.lower()
    return running, out


def loaded_models():
    out = run([LMS, "ps", "--json"])
    try:
        return json.loads(out)
    except Exception:
        return []


def loaded_model_keys():
    return {m["modelKey"] for m in loaded_models()}


def main_menu():
    running, status_text = server_status()
    loaded = loaded_models()
    items = []

    if running:
        items.append({
            "title": "Stop Server",
            "subtitle": status_text,
            "arg": "server:stop:",
            "valid": True,
            "icon": {"path": "icon.png"},
        })
    else:
        items.append({
            "title": "Start Server",
            "subtitle": f"{status_text}  ·  ⌘ CORS  ·  ⌥ LAN  ·  ⌃ CORS+LAN",
            "arg": "server:start:",
            "valid": True,
            "icon": {"path": "icon.png"},
            "mods": {
                "cmd": {
                    "subtitle": "Start with CORS enabled",
                    "arg": "server:start:cors",
                    "valid": True,
                },
                "alt": {
                    "subtitle": "Start on LAN (bind 0.0.0.0)",
                    "arg": "server:start:lan",
                    "valid": True,
                },
                "ctrl": {
                    "subtitle": "Start with CORS + LAN",
                    "arg": "server:start:cors,lan",
                    "valid": True,
                },
            },
        })

    items.append({
        "title": "Load a Model",
        "subtitle": "Tab to browse downloaded models  ·  ⌘ max GPU",
        "arg": "",
        "valid": False,
        "autocomplete": "load ",
        "icon": {"path": "icon.png"},
    })

    if loaded:
        items.append({
            "title": "Unload a Model",
            "subtitle": "Tab to browse loaded models",
            "arg": "",
            "valid": False,
            "autocomplete": "unload ",
            "icon": {"path": "icon.png"},
        })
        items.append({
            "title": f"Unload All Models  ({len(loaded)} loaded)",
            "subtitle": "  ".join(m.get("displayName", m.get("modelKey", "")) for m in loaded),
            "arg": "model:unload-all:",
            "valid": True,
            "icon": {"path": "icon.png"},
        })

    return {"items": items}


def load_menu(search):
    out = run([LMS, "ls", "--json", "--llm"])
    try:
        models = json.loads(out)
    except Exception:
        return {"items": [{"title": "Failed to list models", "subtitle": out, "valid": False}]}

    loaded = loaded_model_keys()
    items = []

    for m in models:
        key = m.get("modelKey", "")
        if key in loaded:
            continue

        name = m.get("displayName", key)
        if search and search.lower() not in name.lower() and search.lower() not in key.lower():
            continue

        size = bytes_to_human(m.get("sizeBytes", 0))
        quant = (m.get("quantization") or {}).get("name", "")
        params = m.get("paramsString", "")
        ctx = m.get("maxContextLength", 0)
        tags = ("  vision" if m.get("vision") else "") + ("  tools" if m.get("trainedForToolUse") else "")
        parts = [x for x in [size, params, quant, f"ctx {ctx:,}"] if x]
        subtitle = " · ".join(parts) + tags

        items.append({
            "title": name,
            "subtitle": subtitle + "  ·  ⌘ max GPU",
            "arg": f"model:load:{key}",
            "valid": True,
            "icon": {"path": "icon.png"},
            "mods": {
                "cmd": {
                    "subtitle": subtitle + "  (max GPU offload)",
                    "arg": f"model:loadgpu:{key}",
                    "valid": True,
                },
            },
        })

    if not items:
        msg = f"No models matching '{search}'" if search else "No unloaded models found"
        items.append({"title": msg, "valid": False})

    return {"items": items}


def unload_menu(search):
    models = loaded_models()

    if not models:
        return {"items": [{"title": "No models currently loaded", "valid": False}]}

    items = []
    for m in models:
        identifier = m.get("identifier") or m.get("modelKey", "")
        name = m.get("displayName", identifier)
        if search and search.lower() not in name.lower() and search.lower() not in identifier.lower():
            continue

        size = bytes_to_human(m.get("sizeBytes", 0))
        ctx = m.get("contextLength", 0)
        status = m.get("status", "")

        items.append({
            "title": name,
            "subtitle": " · ".join([size, f"ctx {ctx:,}", status]),
            "arg": f"model:unload:{identifier}",
            "valid": True,
            "icon": {"path": "icon.png"},
        })

    if not items:
        items.append({"title": f"No loaded models matching '{search}'", "valid": False})

    return {"items": items}


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    ql = query.lower()

    if ql.startswith("load"):
        result = load_menu(query[4:].strip())
    elif ql.startswith("unload"):
        result = unload_menu(query[6:].strip())
    else:
        result = main_menu()

    print(json.dumps(result))


if __name__ == "__main__":
    main()
