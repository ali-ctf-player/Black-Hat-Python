

from builtins import WindowsError
import os
import subprocess
import winreg
import ctypes
import sys
from datetime import datetime

def is_admin():
    """Check if running as admin"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_windows_updates():
    """Check for missing security updates"""
    try:
        result = subprocess.check_output(
            'wmic qfe list full /format:list', 
            stderr=subprocess.STDOUT,
            shell=True
        ).decode('utf-8', errors='ignore')
        return result
    except Exception as e:
        return f"Update check failed: {str(e)}"

def check_always_install_elevated():
    """Check for AlwaysInstallElevated vulnerability"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
            r"SOFTWARE\Policies\Microsoft\Windows\Installer") as key:
            always_install_elevated = winreg.QueryValueEx(key, "AlwaysInstallElevated")[0]
        return always_install_elevated == 1
    except WindowsError:
        return False

def check_unquoted_service_paths():
    """Find services with unquoted paths"""
    try:
        output = subprocess.check_output(
            'wmic service get name,pathname,startmode | findstr /i "auto"',
            shell=True
        ).decode('utf-8', errors='ignore')
        vulnerable_services = []
        for line in output.split('\n'):
            if line.strip() and ' ' in line:
                parts = line.strip().split()
                path = ' '.join(parts[1:-1])
                if ' ' in path and not path.startswith('"'):
                    vulnerable_services.append((parts[0], path))
        return vulnerable_services
    except Exception as e:
        return f"Error checking services: {str(e)}"

def check_writable_directories():
    """Check for writable system directories"""
    dangerous_dirs = [
        os.environ.get('SystemRoot') + '\\Temp',
        os.environ.get('SystemRoot') + '\\Tasks',
        os.environ.get('SystemRoot') + '\\System32\\Spool\\Drivers',
    ]
    writable_dirs = []
    for directory in dangerous_dirs:
        try:
            test_file = os.path.join(directory, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            writable_dirs.append(directory)
        except Exception:
            pass
    return writable_dirs

def main():
    print(f"\nWindows Privilege Escalation Check - {datetime.now()}\n")
    
    if not is_admin():
        print("[!] Warning: Not running as administrator (some checks may fail)")
    
    print("\n[1] Checking Windows updates...")
    print(check_windows_updates())
    
    print("\n[2] Checking AlwaysInstallElevated...")
    print("Vulnerable!" if check_always_install_elevated() else "Not vulnerable")
    
    print("\n[3] Checking for unquoted service paths...")
    services = check_unquoted_service_paths()
    if services:
        for service, path in services:
            print(f"Found: {service} -> {path}")
    else:
        print("No vulnerable services found")
    
    print("\n[4] Checking writable system directories...")
    writable = check_writable_directories()
    if writable:
        print("Writable directories found:")
        for directory in writable:
            print(f" - {directory}")
    else:
        print("No writable system directories found")
    
    print("\n[+] Checks completed")

if __name__ == "__main__":
    main()