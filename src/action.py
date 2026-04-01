#!/usr/bin/env python3
import os
import subprocess
import sys

LMS = os.path.expanduser("~/.lmstudio/bin/lms")


def spawn(cmd):
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    parts = arg.split(":", 2)
    kind   = parts[0] if len(parts) > 0 else ""
    action = parts[1] if len(parts) > 1 else ""
    target = parts[2] if len(parts) > 2 else ""

    if kind == "server":
        if action == "start":
            opts = [o for o in target.split(",") if o]
            cmd = [LMS, "server", "start"]
            if "cors" in opts:
                cmd.append("--cors")
            if "lan" in opts:
                cmd.extend(["--bind", "0.0.0.0"])
            spawn(cmd)
            label = "Starting server"
            if opts:
                label += f" ({', '.join(o.upper() for o in opts)})"
            print(label + "…")

        elif action == "stop":
            spawn([LMS, "server", "stop"])
            print("Stopping server…")

    elif kind == "model":
        if action == "load":
            spawn([LMS, "load", target, "-y"])
            print(f"Loading: {target}")

        elif action == "loadgpu":
            spawn([LMS, "load", target, "-y", "--gpu", "max"])
            print(f"Loading (max GPU): {target}")

        elif action == "unload":
            spawn([LMS, "unload", target])
            print(f"Unloading: {target}")

        elif action == "unload-all":
            spawn([LMS, "unload", "--all"])
            print("Unloading all models…")

    else:
        print(f"Unknown action: {arg}")


if __name__ == "__main__":
    main()
