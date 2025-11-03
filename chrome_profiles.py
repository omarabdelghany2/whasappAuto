#!/usr/bin/env python3
"""
Script to list and get information about Google Chrome profiles
"""

import os
import json
import platform
from pathlib import Path


def get_chrome_profile_path():
    """Get the Chrome user data directory path based on OS"""
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library/Application Support/Google/Chrome"
    elif system == "Windows":
        return Path.home() / "AppData/Local/Google/Chrome/User Data"
    elif system == "Linux":
        return Path.home() / ".config/google-chrome"
    else:
        raise OSError(f"Unsupported operating system: {system}")


def get_local_state_profiles(chrome_path):
    """Get profile names from Local State file"""
    local_state_file = chrome_path / "Local State"

    if not local_state_file.exists():
        return {}

    try:
        with open(local_state_file, 'r', encoding='utf-8') as f:
            local_state = json.load(f)

        profiles_cache = local_state.get('profile', {}).get('info_cache', {})
        profile_names = {}

        for profile_dir, info in profiles_cache.items():
            profile_names[profile_dir] = info.get('name', 'Unknown')

        return profile_names
    except Exception as e:
        return {}


def get_profile_info(profile_path, profile_name=None):
    """Extract profile information from Preferences file"""
    preferences_file = profile_path / "Preferences"

    if not preferences_file.exists():
        return None

    try:
        with open(preferences_file, 'r', encoding='utf-8') as f:
            prefs = json.load(f)

        profile_info = {
            'name': profile_name if profile_name else prefs.get('profile', {}).get('name', 'Unknown'),
            'email': prefs.get('account_info', [{}])[0].get('email', 'Not signed in'),
            'path': str(profile_path)
        }
        return profile_info
    except Exception as e:
        return {
            'name': profile_name if profile_name else 'Error reading profile',
            'email': str(e),
            'path': str(profile_path)
        }


def list_chrome_profiles():
    """List all Chrome profiles"""
    try:
        chrome_path = get_chrome_profile_path()

        if not chrome_path.exists():
            print(f"Chrome profile directory not found at: {chrome_path}")
            return []

        # Get profile names from Local State
        profile_names = get_local_state_profiles(chrome_path)

        profiles = []

        # Check for Default profile
        default_profile = chrome_path / "Default"
        if default_profile.exists() and default_profile.is_dir():
            profile_name = profile_names.get('Default')
            info = get_profile_info(default_profile, profile_name)
            if info:
                profiles.append({
                    'profile_dir': 'Default',
                    **info
                })

        # Check for numbered profiles (Profile 1, Profile 2, etc.)
        for item in chrome_path.iterdir():
            if item.is_dir() and item.name.startswith("Profile "):
                profile_name = profile_names.get(item.name)
                info = get_profile_info(item, profile_name)
                if info:
                    profiles.append({
                        'profile_dir': item.name,
                        **info
                    })

        return profiles

    except Exception as e:
        print(f"Error listing Chrome profiles: {e}")
        return []


def main():
    """Main function"""
    print("=" * 60)
    print("Google Chrome Profiles")
    print("=" * 60)

    profiles = list_chrome_profiles()

    if not profiles:
        print("\nNo Chrome profiles found.")
        return

    print(f"\nFound {len(profiles)} profile(s):\n")

    for i, profile in enumerate(profiles, 1):
        print(f"Profile {i}:")
        print(f"  Directory: {profile['profile_dir']}")
        print(f"  Name: {profile['name']}")
        print(f"  Email: {profile['email']}")
        print(f"  Path: {profile['path']}")
        print()

    # Also print the base Chrome directory
    chrome_path = get_chrome_profile_path()
    print(f"Chrome User Data Directory: {chrome_path}")


if __name__ == "__main__":
    main()
