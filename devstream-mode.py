import json
import subprocess


def set_audio_output(audio_output_device_name):
    subprocess.run(["SwitchAudioSource", "-s", audio_output_device_name])


def clear_all_apps_from_dock():
    subprocess.run(["dockutil", "--remove", "all"])


def add_apps_to_dock(app_paths):
    for i, app_path in enumerate(app_paths):
        # app_path e.g. "/Applications/Visual Studio Code.app/"
        app_path = app_path.replace("%20", " ")

        if i < len(app_paths) - 1:
            # Use dockutil's --no-restart param to prevent dock flicker
            # (refresh) everytime we add an app
            params = ["dockutil", "--add", app_path, "--no-restart"]
        else:
            # When adding the last app, we need the dock to refresh so that
            # all apps we've added before (with the no-restart) will show up.
            # To force refresh, run WITHOUT the '--no-restart' param
            params = ["dockutil", "--add", app_path]

        subprocess.run(params, stdout=subprocess.PIPE).stdout.decode("utf-8")


def enable_stream_mode(config):
    """
    1. Replace the entire dock with only the devstream apps in config
    2. Set audio output to the custom multi-channel output for streams
    """
    # 1. Gather a list of the current apps in the dock
    current_apps_in_dock = []
    output = subprocess.run(
        ["dockutil", "--list"], stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    for i in output.split("\n")[:-1]:
        # file:///Applications/Bear.app -> /Applications/Bear.app
        app_path = i.split("\t")[1].replace("file://", "")
        current_apps_in_dock.append(app_path)

    # and store that list for later
    config["dockAppsToRestore"] = current_apps_in_dock

    # Then clear the dock
    clear_all_apps_from_dock()

    # and add only devstream apps
    add_apps_to_dock(config["devstreamApps"])

    # 2. Set audio output
    set_audio_output("DevStream")

    # Lastly, update config switches
    config["enabled"] = True
    config["shouldOpenDevStreamApps"] = True
    return "openDevStreamApps"


def disable_stream_mode(config):
    """
    1. Remove devstream apps that have been added previously (clear the dock)
    2. Restore previously removed apps from the dock
    3. Set audio output to the default
    """
    # 1. Clear apps from the dock
    clear_all_apps_from_dock()

    # 2. Restore previously removed apps from the dock
    add_apps_to_dock(config["dockAppsToRestore"])

    # 3. Set audio output to default
    set_audio_output("MacBook Pro Speakers")

    # Lastly, update config switches
    config["dockAppsToRestore"] = []
    config["enabled"] = False
    config["shouldOpenDevStreamApps"] = False
    return ""


CONFIG_FILE = "./devstream-mode-config.json"


# Load config from file
with open(CONFIG_FILE, "r") as rstream:
    config = json.load(rstream)

    # Run the appropriate action based on the "enabled" key in config
    if config["enabled"]:
        outcome_string = disable_stream_mode(config)
    else:
        outcome_string = enable_stream_mode(config)

    # For the next step in the overall Alfred Workflow:
    # Pass data (using print), to determine whether to open the apps
    # "openDevStreamApps" = open all devstream apps, "" = don't open anything
    print(outcome_string)

# Save the updated config file so that state is persisted
with open(CONFIG_FILE, "w") as wstream:
    json.dump(config, wstream)
