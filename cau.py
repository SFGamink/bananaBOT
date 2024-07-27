import os
import time
import requests
import json
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Definisikan headers global di sini
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-app-id": "carv",
    "Referer": "https://banana.carv.io/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_tginfo_from_file():
    try:
        with open("tgwebapp.txt", "r") as file:
            return file.read().strip().splitlines()
    except FileNotFoundError:
        print("Error: tgwebapp.txt not found")
        return []

def auth(tg_info):
    global headers  # Use global headers here
    url = "https://interface.carv.io/banana/login"
    
    body = {
        "tgInfo": tg_info,
    }
    
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Return full JSON response as Python dictionary
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error during authentication: {e}{Fore.RESET}")
        return None

def get_token(tg_info):
    auth_response = auth(tg_info)
    if auth_response:
        try:
            token = auth_response['data']['token']
            return token
        except KeyError:
            print(f"{Fore.RED}Error: 'token' key not found in authentication response{Fore.RESET}")
            return None
    else:
        print(f"{Fore.RED}Authentication failed.{Fore.RESET}")
        return None

def user_detail(tg_info):
    global headers  # Use global headers here
    token = get_token(tg_info)
    if token:
        url = "https://interface.carv.io/banana/get_user_info"
        headers['authorization'] = f"Bearer {token}"  # Update authorization header
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.json()  # Return JSON response as Python dictionary
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error fetching user details: {e}{Fore.RESET}")
            return None
    else:
        print(f"{Fore.RED}Failed to fetch user details because authentication failed.{Fore.RESET}")
        return None

def auto_click(tg_info):
    global headers  # Use global headers here
    
    user_info = user_detail(tg_info)
    if user_info:
        try:
            max_click_count = user_info['data']['max_click_count']
        except KeyError:
            print(f"{Fore.RED}Error: 'max_click_count' not found in user details{Fore.RESET}")
            return
        
        clickCount = max_click_count  # Ensure clickCount is not more than max_click_count
        
        url = "https://interface.carv.io/banana/do_click"
        headers['authorization'] = f"Bearer {get_token(tg_info)}"  # Update authorization header
        
        body = {
            "clickCount": clickCount,
        }
        
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Print success message in green
            print(f"{Fore.GREEN}Successfully clicked {clickCount} times for account.{Fore.RESET}")
            
            # Setelah selesai auto click, hapus token dari headers
            del headers['authorization']
            
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error during click action: {e}{Fore.RESET}")
    else:
        print(f"{Fore.RED}Failed to perform auto-click because failed to fetch user details.{Fore.RESET}")

def get_task(tg_info):
    global headers  # Use global headers here
    url = "https://interface.carv.io/banana/get_quest_list"
    token = get_token(tg_info)
    if token:
        headers['authorization'] = f"Bearer {token}"
    else:
        print(f"{Fore.RED}Failed to get task list because authentication failed.{Fore.RESET}")
        return None
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()  # Return JSON response as Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching task list: {e}{Fore.RESET}")
        return None

def clear_task(tg_info, quest_id):
    global headers  # Use global headers here
    url = "https://interface.carv.io/banana/achieve_quest"
    token = get_token(tg_info)
    if token:
        headers['authorization'] = f"Bearer {token}"
    else:
        print(f"{Fore.RED}Failed to clear task because authentication failed.{Fore.RESET}")
        return None
    
    # Body data as JSON string
    body = json.dumps({
        "quest_id": quest_id
    })

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()  # Return JSON response as Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error clearing task: {e}{Fore.RESET}")
        return None

def claim_task(tg_info, quest_id):
    global headers  # Use global headers here
    url = "https://interface.carv.io/banana/claim_quest"
    token = get_token(tg_info)
    if token:
        headers['authorization'] = f"Bearer {token}"
    else:
        print(f"{Fore.RED}Failed to claim task because authentication failed.{Fore.RESET}")
        return None
    
    # Body data as JSON string
    body = json.dumps({
        "quest_id": quest_id
    })

    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()  # Return JSON response as Python dictionary
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error claiming task: {e}{Fore.RESET}")
        return None

def lotre(tg_info):
    global headers  # Use global headers here
    url = "https://interface.carv.io/banana/do_lottery"
    token = get_token(tg_info)
    if token:
        headers['authorization'] = f"Bearer {token}"
    else:
        print(f"{Fore.RED}Failed to perform lotre action because authentication failed.{Fore.RESET}")
        return None

    # Verifikasi remain_lottery_count sebelum melakukan lotre
    user_info = user_detail(tg_info)
    if user_info:
        remain_lottery_count = user_info['data']['lottery_info']['remain_lottery_count']
        if remain_lottery_count < 1:
            print(f"{Fore.RED}Not enough lottery attempts remaining ({remain_lottery_count}).{Fore.RESET}")
            return

    body = {}

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Mendapatkan data dari respons
        data = response.json().get('data', {})
        name = data.get('name', 'Unknown')
        rarity = data.get('rarity', 'Unknown')
        sell_exchange_peel = data.get('sell_exchange_peel', 0)
        sell_exchange_usdt = data.get('sell_exchange_usdt', 0)

        # Print success message dengan detail
        print(f"{Fore.GREEN}Selamat! Anda mendapatkan {name} dengan rarity {rarity}.")
        print(f"{Fore.GREEN}Sell Exchange Peel: {sell_exchange_peel}")
        print(f"{Fore.GREEN}Sell Exchange USDT: {sell_exchange_usdt}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error during lottery action: {e}{Fore.RESET}")

def claim_token_lottery(tg_info):
    url = "https://interface.carv.io/banana/claim_lottery"
    token = get_token(tg_info)
    if not token:
        print(f"{Fore.RED}Failed to get token. Cannot claim lottery.{Fore.RESET}")
        return None
    
    headers['authorization'] = f"Bearer {token}"
    body = {
        "claimLotteryType": 1
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error claiming lottery token: {e}{Fore.RESET}")
        return None

def print_welcome_message():
    """Function to print a welcome message."""
    print(r"""      

▒█▀▀▀█ █▀▀█ ░█▀█░ ▒█▄░▒█ 
░▀▀▀▄▄ ░░▀▄ █▄▄█▄ ▒█▒█▒█ 
▒█▄▄▄█ █▄▄█ ░░░█░ ▒█░░▀█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Banana BOT")
    print(Fore.RED + Style.BRIGHT + "Jangan di edit la bang :)\n\n")                

def main():
    tg_info_list = read_tginfo_from_file()
    if not tg_info_list:
        print(f"{Fore.RED}No TG info found in the file.{Fore.RESET}")
        return

    # Dictionary to store account details
    account_details = {}

    for index, tg_info in enumerate(tg_info_list, start=1):
        clear_screen()
        print_welcome_message()
        
        # 1. Konfirmasi Clear Task
        confirm_clear = input(Fore.WHITE + f"Apakah Anda ingin melakukan clear task otomatis untuk akun nomor {index}? (y/n): ")
        if confirm_clear.lower() == 'y':
            auth_response = auth(tg_info)
            if auth_response:
                token = auth_response['data']['token']
                headers['authorization'] = f"Bearer {token}"

                task_list = get_task(tg_info)
                if task_list:
                    print("Task list:")
                    for quest in task_list['data']['quest_list']:
                        clear_result = clear_task(tg_info, quest['quest_id'])
                        if clear_result:
                            print(f"{Fore.GREEN}Task with ID {quest['quest_id']} cleared successfully.{Fore.RESET}")
                            claim_result = claim_task(tg_info, quest['quest_id'])
                            if claim_result:
                                print(f"{Fore.GREEN}Task with ID {quest['quest_id']} claimed successfully.{Fore.RESET}")
                            else:
                                print(f"{Fore.RED}Failed to claim task with ID {quest['quest_id']}.{Fore.RESET}")
                        else:
                            print(f"{Fore.RED}Failed to clear task with ID {quest['quest_id']}.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Failed to fetch task list for account number {index}.{Fore.RESET}")
            else:
                print(f"{Fore.RED}Authentication failed for account number {index}.{Fore.RESET}")

         # 2. Auto Claim Token Lottery
        print(f"\nMengklaim token lotre untuk akun nomor {index}...")
        result = claim_token_lottery(tg_info)
        if result:
            status_code = result.get('code')
            if status_code == 200:
                print(f"{Fore.GREEN}Claim successful{Fore.RESET}")
            elif status_code == 0:
                print(f"{Fore.RED}Claim failed{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}Unexpected response code: {status_code}{Fore.RESET}")
        else:
            print(f"{Fore.RED}Failed to claim token lottery.{Fore.RESET}")

        # 3. Tampilkan Detail Akun
        print(Fore.WHITE + f"\n=============== Detail akun nomor {index} : ===============\n")
        auth_response = auth(tg_info)
        if auth_response:
            user_info = user_detail(tg_info)
            if user_info:
                try:
                    # Save account details in dictionary
                    account_details[index] = {
                        "username": user_info['data']['username'],
                        "peel": user_info['data']['peel'],
                        "banana_name": user_info['data']['equip_banana']['name'],
                        "daily_limit": user_info['data']['equip_banana']['daily_peel_limit'],
                        "lotre": user_info['data']['lottery_info']['remain_lottery_count'],
                    }
                except KeyError as e:
                    print(f"{Fore.RED}Error: Key '{e}' not found in user details.{Fore.RESET}")
            else:
                print(f"{Fore.RED}Failed to fetch user details for account number {index}.{Fore.RESET}")
        else:
            print(f"{Fore.RED}Authentication failed for account number {index}.{Fore.RESET}")

        if index in account_details:
            details = account_details[index]
            print(Fore.WHITE + f"Username    : {details['username']}")
            print(Fore.WHITE + f"Peel        : {details['peel']}")
            print(Fore.WHITE + f"Banana Name : {details['banana_name']}")
            print(Fore.WHITE + f"Daily Limit : {details['daily_limit']}")
            print(Fore.WHITE + f"Lotre       : {details['lotre']}")
            print(Fore.WHITE + f"\n=============== Auto Click ===============\n")
        else:
            print(Fore.RED + f"No account details to display for account number {index}.{Fore.RESET}")

        # 4. Konfirmasi Auto Click
        confirm_auto_click = input(Fore.WHITE + f"Apakah Anda ingin menggunakan auto click otomatis untuk akun nomor {index}? (y/n): ")
        if confirm_auto_click.lower() == 'y':
            auto_click(tg_info)
            if 'authorization' in headers:
                del headers['authorization']

          # 5. Konfirmasi Lotre
        user_info = user_detail(tg_info)
        if user_info:
            remain_lottery_count = user_info['data']['lottery_info']['remain_lottery_count']
            if remain_lottery_count > 0:
                confirm_lotre = input(Fore.WHITE + f"Apakah Anda ingin melakukan lotre untuk akun nomor {index}? (y/n): ")
                if confirm_lotre.lower() == 'y':
                    print(f"{Fore.WHITE}Melakukan lotre untuk akun nomor {index}...\n")
                    lotre(tg_info)
                else:
                    print(f"{Fore.YELLOW}Lotre dibatalkan untuk akun nomor {index}.{Fore.RESET}")
            else:
                print(f"{Fore.RED}Not enough lottery attempts remaining ({remain_lottery_count}) for account number {index}.{Fore.RESET}")
        else:
            print(f"{Fore.RED}Failed to fetch user details for account number {index}.{Fore.RESET}")

        # Wait 5 seconds before proceeding to the next account
        print(Fore.WHITE + f"Menunggu 5 detik sebelum melanjutkan ke akun nomor {index} berikutnya...\n")
        time.sleep(5)

if __name__ == "__main__":
    main()
