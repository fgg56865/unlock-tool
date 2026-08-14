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
    print(" SMART XIAOMI TERMUX TOOLKIT (PRO MAX v1.1) ")
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
    print(f" {title.upper()} ")
    print(f"=================================================={RESET}")
    for idx, opt in enumerate(options, 1):
        print(f" {GREEN}[{idx}]{RESET} {opt}")
    print(f"{CYAN}=================================================={RESET}")

def smart_unlock_device():
    """Smart function with proper output checking"""
    print(f"\n{YELLOW}[*] Testing 'fastboot flashing unlock' support...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'flashing', 'unlock'], capture_output=True, text=True, timeout=15)
        output = (res.stdout + res.stderr).lower()

        if res.returncode == 0 or "okay" in output:
            print(f"{GREEN}[+] 'flashing unlock' command accepted! Check phone screen and confirm.{RESET}")
            return True

        print(f"{YELLOW}[!] 'flashing unlock' not accepted. Trying 'oem unlock'...{RESET}")
        res_oem = subprocess.run(['fastboot', 'oem', 'unlock'], capture_output=True, text=True, timeout=15)
        oem_output = (res_oem.stdout + res_oem.stderr).lower()

        if res_oem.returncode == 0 or "okay" in oem_output:
            print(f"{GREEN}[+] 'oem unlock' command accepted! Check phone screen and confirm.{RESET}")
            return True

        print(f"{RED}[-] Both methods failed. Device may require official Mi Unlock Tool on PC.{RESET}")
        print(f"{YELLOW}Server Response: {res_oem.stderr.strip() or res_oem.stdout.strip()}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}[-] Error during smart unlock: {e}{RESET}")
        return False

def run_unlock(is_hyperos=False):
    clear_screen()
    print(f"{YELLOW}==================================================")
    print(" SMART BOOTLOADER UNLOCK AUTOMATION ")
    print(f"=================================================={RESET}")

    if is_hyperos:
        print(f"{RED}[!] WARNING: HyperOS requires 168h wait + PC + Mi Unlock Tool!{RESET}")
        print(f"{RED}[!] Fastboot command alone might not bypass security on HyperOS 1.0+{RESET}\n")
        cont = input(f"{CYAN}Still want to try fastboot command? (y/n): {RESET}").strip().lower()
        if cont != 'y': 
            return
    else:
        print(f"{RED}[!] WARNING: All data will be wiped completely!{RESET}")

    action = input(f"\n{CYAN}Press Enter to start or 'q' to cancel: {RESET}").strip()
    if action.lower() == 'q': 
        return

    print(f"\n{YELLOW}[*] Checking fastboot device...{RESET}")
    try:
        res = subprocess.run(['fastboot', 'devices'], capture_output=True, text=True, timeout=10)
        if not res.stdout.strip():
            print(f"{RED}[-] No fastboot device found! Check your OTG cable connection.{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")
            return
        print(f"{GREEN}[+] Device found:\n{res.stdout.strip()}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Fastboot error: {e}{RESET}")
        input(f"\n{CYAN}Press Enter to return...{RESET}")
        return

    print(f"\n{YELLOW}[*] Checking unlock status...{RESET}")
    subprocess.run(['fastboot', 'oem', 'device-info'])

    print(f"\n{YELLOW}[*] Running Smart Unlock Sequence...{RESET}")
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
                    print(f"{RED}[-] Please open https://account.xiaomi.com manually in your browser.{RESET}")

            print(f"\n{CYAN}Instructions:{RESET}")
            print("1. Login & Bind account in browser")
            print("2. Wait required hours if first time binding")
            print("3. Come back and type 'done'")

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
                print(f"{GREEN}{res.stdout.strip() if res.stdout.strip() else 'No device found.'}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '2':
            clear_screen()
            print(f"{YELLOW}[i] ROM folder-টি /sdcard এ রাখুন অথবা সঠিক পাথ (path) দিন{RESET}")
            path = input(f"{CYAN}Enter extracted ROM folder path: {RESET}").strip()
            if os.path.isdir(path):
                flash_script = os.path.join(path, 'flash_all.sh')
                windows_script = os.path.join(path, 'flash_all.bat')

                if os.path.exists(flash_script):
                    print(f"{YELLOW}[*] Executing flash_all.sh...{RESET}")
                    subprocess.run(['sh', flash_script])
                elif os.path.exists(windows_script):
                    print(f"{YELLOW}[!] Parsing flash_all.bat...{RESET}")
                    try:
                        with open(windows_script, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith('fastboot'):
                                    parts = line.split()
                                    if len(parts) >= 4:
                                        partition = parts[2]
                                        img_file = parts[3].replace('%~dp0', '').replace('images\\', '').replace('images/', '')
                                        img_path = os.path.join(path, img_file)
                                        print(f"Flashing {partition}...")
                                        subprocess.run(['fastboot', 'flash', partition, img_path])
                    except Exception as ex:
                        print(f"{RED}[-] Error parsing bat: {ex}{RESET}")
                else:
                    print(f"{YELLOW}[*] No script found. Flashing .img files directly...{RESET}")
                    try:
                        imgs = [f for f in os.listdir(path) if f.endswith('.img')]
                        for img in imgs:
                            img_path = os.path.join(path, img)
                            img_name = os.path.splitext(img)[0]
                            print(f"Flashing {img_name}...")
                            subprocess.run(['fastboot', 'flash', img_name, img_path])
                    except Exception as e:
                        print(f"{RED}[-] Error flashing: {e}{RESET}")
                print(f"{GREEN}[+] ROM Flashing finished!{RESET}")
                print(f"{YELLOW}[*] Run 'fastboot reboot' to restart{RESET}")
            else:
                print(f"{RED}[-] Invalid directory path!{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

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
            print(f"{YELLOW}[*] Reboots to recovery first...{RESET}")
            subprocess.run(['adb', 'reboot', 'recovery'])
            print(f"{CYAN}Recovery-তে গিয়ে 'Apply update from ADB' সিলেক্ট করুন{RESET}")
            input("করার পর Enter চাপুন...")
            zpath = input(f"{CYAN}Enter Recovery Zip file path: {RESET}").strip()
            if os.path.exists(zpath) and zpath.endswith('.zip'):
                print(f"{YELLOW}[*] Starting ADB Sideload...{RESET}")
                res = subprocess.run(['adb', 'sideload', zpath], capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"{GREEN}[+] Sideload Done!{RESET}")
                else:
                    print(f"{RED}[-] Sideload failed: {res.stderr}{RESET}")
            else:
                print(f"{RED}[-] Invalid zip file path!{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

        elif choice == '2':
            print(f"{YELLOW}[*] Rebooting to system...{RESET}")
            subprocess.run(['adb', 'reboot'])
            input(f"{CYAN}Press Enter to return...{RESET}")

        elif choice == '3':
            print(f"{YELLOW}[*] Rebooting to Fastboot...{RESET}")
            subprocess.run(['adb', 'reboot', 'bootloader'])
            input(f"{CYAN}Press Enter to return...{RESET}")

        elif choice == '4':
            print(f"{RED}[!] WARNING: This will wipe all data!{RESET}")
            confirm = input(f"{CYAN}Type 'yes' to proceed: {RESET}").strip().lower()
            if confirm == 'yes':
                print(f"{YELLOW}[*] Executing 'fastboot -w'...{RESET}")
                res = subprocess.run(['fastboot', '-w'], capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"{GREEN}[+] Wipe successful!{RESET}")
                else:
                    print(f"{RED}[-] Wipe failed: {res.stderr}{RESET}")
            input(f"{CYAN}Press Enter to return...{RESET}")

        elif choice == '5':
            clear_screen()
            try:
                res = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
                print(f"{GREEN}{res.stdout.strip() if res.stdout.strip() else 'No ADB device found.'}{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")
            input(f"\n{CYAN}Press Enter to return...{RESET}")

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
        else:
            print(f"{RED}Invalid choice!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
