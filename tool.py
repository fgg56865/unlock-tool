
import os
import time
import subprocess

# Terminal Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_main_menu():
    clear_screen()
    print(f"{CYAN}==================================================")
    print("       SMART XIAOMI TERMUX TOOLKIT (PRO MAX)      ")
    print(f"=================================================={RESET}")
    print(f" {GREEN}[1]{RESET} Unlock Bootloader (MIUI)")
    print(f" {GREEN}[2]{RESET} Unlock Bootloader (HyperOS)")
    print(f" {GREEN}[3]{RESET} Flash ROM (Auto-Detect & Smart)")
    print(f" {GREEN}[4]{RESET} Mi Assistant (Advanced)")
    print(f" {RED}[5]{RESET} Exit")
    print(f"{CYAN}=================================================={RESET}")

def show_sub_menu(title, options):
    clear_screen()
    print(f"{CYAN}==================================================")
    print(f"       {title.upper()}                       ")
    print(f"=================================================={RESET}")
    for idx, opt in enumerate(options, 1):
        print(f" {GREEN}[{idx}]{RESET} {opt}")
    print(f"{CYAN}=================================================={RESET}")

def smart_unlock_device():
    """Smart function with fixed stdout checking for oem unlock"""
    print(f"\n{YELLOW}[*] Testing 'fastboot flashing unlock' support...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'flashing', 'unlock'], capture_output=True, text=True, timeout=15)
        output = (res.stdout + res.stderr).lower()
        
        if res.returncode == 0 or "already" in output:
            print(f"{GREEN}[+] 'flashing unlock' command executed successfully!{RESET}")
            return True
        
        print(f"{YELLOW}[!] 'flashing unlock' not accepted. Trying 'oem unlock'...{RESET}")
        res_oem = subprocess.run(['fastboot', 'oem', 'unlock'], capture_output=True, text=True, timeout=15)
        oem_output = (res_oem.stdout + res_oem.stderr).lower() # Bug Fixed: separate oem output variable
        
        if res_oem.returncode == 0 or "already" in oem_output:
            print(f"{GREEN}[+] 'oem unlock' command executed successfully!{RESET}")
            return True
            
        print(f"{RED}[-] Both methods returned error. Check device screen for manual prompt.{RESET}")
        print(f"{YELLOW}Response: {res_oem.stderr.strip() or res_oem.stdout.strip()}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[-] Error during smart unlock execution: {e}{RESET}")
        return False

def run_unlock(is_hyperos=False):
    clear_screen()
    print(f"{YELLOW}==================================================")
    print("     SMART BOOTLOADER UNLOCK AUTOMATION           ")
    print(f"=================================================={RESET}")
    print(f"{RED}[!] Warning: Data will be wiped completely!{RESET}")
    
    action = input(f"\n{CYAN}Press Enter to start or 'q' to cancel: {RESET}").strip()
    if action.lower() == 'q':
        return

    print(f"\n{YELLOW}[*] Checking fastboot device connection...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True, timeout=10)
        if not res.stdout or not res.stdout.strip():
            print(f"{RED}[-] No fastboot device found! Connect via OTG properly.{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")
            return
        print(f"{GREEN}[+] Device found:\n{res.stdout.strip()}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Fastboot tool error: {e}{RESET}")
        input(f"\n{CYAN}Press Enter to return...{RESET}")
        return

    print(f"\n{YELLOW}[*] Running Smart Unlock Sequence ({'HyperOS' if is_hyperos else 'MIUI'})...{RESET}")
    smart_unlock_device()
        
    input(f"\n{CYAN}Press Enter to return...{RESET}")

def handle_unlock(name, is_hyperos=False):
    while True:
        options = ["Open Login Portal & Unlock", "Back"]
        show_sub_menu(name, options)
        choice = input(f"{CYAN}Select (1-2): {RESET}").strip()
        
        if choice == '1':
            clear_screen()
            print(f"{YELLOW}Opening Xiaomi Portal...{RESET}")
            try:
                subprocess.run(['termux-open-url', 'https://account.xiaomi.com'])
            except Exception:
                try:
                    subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', 'https://account.xiaomi.com'])
                except Exception:
                    print(f"{RED}[-] Open https://account.xiaomi.com manually in browser.{RESET}")
            
            print(f"\n{CYAN}Instructions:{RESET}")
            print("1. Login & Bind account in browser.")
            print("2. Come back here.")
            
            while True:
                ans = input(f"\n{CYAN}Type {GREEN}'done'{CYAN} when finished (or {RED}'back'{CYAN}): {RESET}").strip().lower()
                if ans == 'done' or ans == '':
                    print(f"\n{GREEN}[+] Proceeding to smart unlock...{RESET}")
                    time.sleep(1)
                    run_unlock(is_hyperos)
                    break
                elif ans == 'back':
                    break
                else:
                    print(f"{RED}Invalid input. Type 'done' or 'back'.{RESET}")
            break
        elif choice == '2':
            break

def handle_rom():
    while True:
        options = ["Check Fastboot Devices", "Flash Fastboot ROM (Smart Auto)", "Back"]
        show_sub_menu("Flash ROM", options)
        choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        
        if choice == '1':
            clear_screen()
            try:
                res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True, timeout=5)
                print(f"{GREEN}{res.stdout.strip() if res.stdout and res.stdout.strip() else 'No device found.'}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
            
        elif choice == '2':
            clear_screen()
            print(f"{YELLOW}[i] Note: Ensure ROM folder is accessible or pushed to phone storage via adb.{RESET}")
            path = input(f"{CYAN}Enter extracted ROM folder path: {RESET}").strip()
            if os.path.isdir(path):
                flash_script = os.path.join(path, 'flash_all.sh')
                windows_script = os.path.join(path, 'flash_all.bat')
                
                if os.path.exists(flash_script):
                    print(f"{YELLOW}[*] Executing flash_all.sh script...{RESET}")
                    subprocess.run(['sh', flash_script])
                elif os.path.exists(windows_script):
                    print(f"{YELLOW}[!] Found flash_all.bat. Parsing fastboot commands...{RESET}")
                    try:
                        with open(windows_script, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                if line.strip().startswith('fastboot'):
                                    cmd_line = line.strip().replace('%~dp0', '').replace('images/', '')
                                    print(f"Running: {cmd_line}")
                                    subprocess.run(cmd_line, shell=True)
                    except Exception as ex:
                        print(f"{RED}[-] Error parsing bat script: {ex}{RESET}")
                else:
                    print(f"{YELLOW}[*] No script found, auto-flashing all .img files in folder...{RESET}")
                    try:
                        imgs = [f for f in os.listdir(path) if f.endswith('.img')]
                        for img in imgs:
                            img_path = os.path.join(path, img)
                            img_name = os.path.splitext(img)[0]
                            print(f"Flashing partition -> {img_name}...")
                            subprocess.run(['fastboot', 'flash', img_name, img_path])
                    except Exception as e:
                        print(f"{RED}[-] Error during image flashing: {e}{RESET}")
                print(f"{GREEN}[+] ROM Flashing process finished!{RESET}")
            else:
                print(f"{RED}[-] Invalid directory path provided!{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
            
        elif choice == '3':
            break

def handle_mi_assistant():
    while True:
        options = [
            "ADB Sideload (Flash Zip)", 
            "Reboot System", 
            "Reboot to Fastboot", 
            "Wipe Data (Fastboot -w)", 
            "Check ADB Device", 
            "Back"
        ]
        show_sub_menu("Mi Assistant (Advanced)", options)
        choice = input(f"{CYAN}Select (1-6): {RESET}").strip()
        
        if choice == '1':
            clear_screen()
            zpath = input(f"{CYAN}Enter Recovery Zip file path: {RESET}").strip()
            if os.path.exists(zpath) and zpath.endswith('.zip'):
                print(f"{YELLOW}[*] Starting ADB Sideload...{RESET}")
                res = subprocess.run(['adb', 'sideload', zpath])
                if res.returncode == 0:
                    print(f"{GREEN}[+] Sideload Done Successfully!{RESET}")
                else:
                    print(f"{RED}[-] Sideload failed. Check recovery sideload mode status.{RESET}")
            else:
                print(f"{RED}[-] Invalid zip file path!{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
            
        elif choice == '2':
            print(f"{YELLOW}[*] Rebooting device to system...{RESET}")
            subprocess.run(['adb', 'reboot'])
            input(f"{CYAN}Press Enter...{RESET}")
            
        elif choice == '3':
            print(f"{YELLOW}[*] Forcing device to Fastboot mode...{RESET}")
            subprocess.run(['adb', 'reboot', 'bootloader'])
            input(f"{CYAN}Press Enter...{RESET}")
            
        elif choice == '4':
            print(f"{RED}[!] WARNING: This will wipe user data completely via fastboot!{RESET}")
            confirm = input(f"{CYAN}Type 'yes' to proceed: {RESET}").strip().lower()
            if confirm == 'yes':
                # Bug Fixed: Replaced incorrect adb shell wipe data with fastboot -w
                print(f"{YELLOW}[*] Executing 'fastboot -w' (Wiping data/cache)...{RESET}")
                res = subprocess.run(['fastboot', '-w'])
                if res.returncode == 0:
                    print(f"{GREEN}[+] Data wipe successful!{RESET}")
                else:
                    print(f"{RED}[-] Wipe failed. Ensure device is connected in fastboot mode.{RESET}")
            input(f"{CYAN}Press Enter...{RESET}")
            
        elif choice == '5':
            clear_screen()
            try:
                res = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
                print(f"{GREEN}{res.stdout.strip() if res.stdout and res.stdout.strip() else 'No ADB device found.'}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error checking ADB: {e}{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
            
        elif choice == '6':
            break

def main():
    while True:
        show_main_menu()
        choice = input(f"{CYAN}Select (1-5): {RESET}").strip()
        if choice == '1':
            handle_unlock("Unlock Bootloader (MIUI)", False)
        elif choice == '2':
            handle_unlock("Unlock Bootloader (HyperOS)", True)
        elif choice == '3':
            handle_rom()
        elif choice == '4':
            handle_mi_assistant()
        elif choice == '5':
            print(f"{GREEN}Goodbye!{RESET}")
            break

if __name__ == "__main__":
    main()
