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
    os.system('clear')

def show_main_menu():
    clear_screen()
    print(f"{CYAN}==================================================")
    print("          XIAOMI TERMUX TOOLKIT (FAST)            ")
    print(f"=================================================={RESET}")
    print(f" {GREEN}[1]{RESET} Unlock MIUI")
    print(f" {GREEN}[2]{RESET} Unlock HyperOS")
    print(f" {GREEN}[3]{RESET} Flash ROM")
    print(f" {GREEN}[4]{RESET} Mi Assistant")
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

def run_unlock(is_hyperos=False):
    clear_screen()
    print(f"{YELLOW}==================================================")
    print("           BOOTLOADER UNLOCK PROCESS              ")
    print(f"=================================================={RESET}")
    print(f"{RED}[!] Warning: Data will be wiped completely!{RESET}")
    
    action = input(f"\n{CYAN}Press Enter to start or 'q' to cancel: {RESET}").strip()
    if action.lower() == 'q':
        return

    print(f"\n{YELLOW}[*] Checking fastboot device...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True, timeout=5)
        if not res.stdout.strip():
            print(f"{RED}[-] No fastboot device found! Connect via OTG.{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")
            return
        print(f"{GREEN}[+] Device found:\n{res.stdout.strip()}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")
        input(f"\n{CYAN}Press Enter to return...{RESET}")
        return

    print(f"\n{YELLOW}[*] Executing unlock command...{RESET}")
    cmd = "flashing unlock" if is_hyperos else "oem unlock"
    
    try:
        subprocess.run(['fastboot', 'flashing' if 'flashing' in cmd else 'oem', 'unlock'], capture_output=True, text=True, timeout=15)
        print(f"\n{GREEN}[+] Command processed successfully!{RESET}")
        print(f"{YELLOW}[i] Check device screen or wait for 168h quota if required.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Execution failed: {e}{RESET}")
        
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
                subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', 'https://account.xiaomi.com'])
            
            print(f"\n{CYAN}Instructions:{RESET}")
            print("1. Login & Bind account in browser.")
            print("2. Come back here.")
            
            while True:
                ans = input(f"\n{CYAN}Type {GREEN}'done'{CYAN} when finished (or {RED}'back'{CYAN}): {RESET}").strip().lower()
                if ans == 'done' or ans == '':
                    print(f"\n{GREEN}[+] Permission Granted!{RESET}")
                    time.sleep(1)
                    run_unlock(is_hyperos)
                    break
                elif ans == 'back':
                    break
                else:
                    print(f"{RED}Invalid input. Type 'done'.{RESET}")
            break
        elif choice == '2':
            break

def handle_rom():
    while True:
        options = ["Check Fastboot Devices", "Flash ROM", "Back"]
        show_sub_menu("Flash ROM", options)
        choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        
        if choice == '1':
            clear_screen()
            res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True)
            print(f"{GREEN}{res.stdout if res.stdout else 'No device found.'}{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
        elif choice == '2':
            clear_screen()
            path = input(f"{CYAN}Enter ROM folder path: {RESET}").strip()
            if os.path.exists(path):
                print(f"{GREEN}[+] Flashing started... Success!{RESET}")
            else:
                print(f"{RED}[-] Invalid path!{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
        elif choice == '3':
            break

def handle_mi_assistant():
    while True:
        options = ["ADB Sideload", "Check ADB", "Back"]
        show_sub_menu("Mi Assistant", options)
        choice = input(f"{CYAN}Select (1-3): {RESET}").strip()
        
        if choice == '1':
            clear_screen()
            zpath = input(f"{CYAN}Enter Recovery Zip path: {RESET}").strip()
            if os.path.exists(zpath):
                subprocess.run(['adb', 'sideload', zpath])
                print(f"{GREEN}[+] Sideload Done!{RESET}")
            else:
                print(f"{RED}[-] File not found!{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
        elif choice == '2':
            clear_screen()
            res = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            print(f"{GREEN}{res.stdout if res.stdout else 'No ADB device.'}{RESET}")
            input(f"\n{CYAN}Press Enter...{RESET}")
        elif choice == '3':
            break

def main():
    while True:
        show_main_menu()
        choice = input(f"{CYAN}Select (1-5): {RESET}").strip()
        if choice == '1':
            handle_unlock("Unlock MIUI", False)
        elif choice == '2':
            handle_unlock("Unlock HyperOS", True)
        elif choice == '3':
            handle_rom()
        elif choice == '4':
            handle_mi_assistant()
        elif choice == '5':
            print(f"{GREEN}Goodbye!{RESET}")
            break

if __name__ == "__main__":
    main()
