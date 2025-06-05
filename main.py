import asyncio, random, os, time
from colorama import Fore, Style
from rich.console import Console
from rich.panel import Panel
from aiohttp import ClientResponseError, ClientSession, ClientTimeout


def user():
    """user input menu
    
    return -> input_mode, input_timer_minute, input_delay_msg, input_channel_id"""

    menu = ["Basic Mode",
            "Timer Mode",
            "Exit"]
    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Main Menu :" + Style.RESET_ALL)
    for i, option in enumerate(menu, start=1):
        print(f"{Fore.GREEN + Style.BRIGHT}{i:>6}.{Style.RESET_ALL} {option}")

    while True:
        try:
            input_mode = int(input(f"Select an option {Fore.GREEN + Style.BRIGHT}[1 to {len(menu)}]{Style.RESET_ALL}: "))
            if 1 <= input_mode <= len(menu):
                if input_mode == len(menu):
                    raise SystemExit(Fore.YELLOW + "Exiting the program..." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + f"Please enter a number [1 to {len(menu)}]" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + f"Invalid input. Please enter a number [1 to {len(menu)}]" + Style.RESET_ALL)
    
    if input_mode == 2:
        while True:
            try:
                input_timer_minute = int(input(f"Please input the {Fore.YELLOW}timer in minutes{Style.RESET_ALL} : "))
                if input_timer_minute < 1:
                    print(Fore.RED + f"Please enter a positive number" + Style.RESET_ALL)
                    continue
                break
            except ValueError:
                print(Fore.RED + f"Invalid input. Please enter a valid number" + Style.RESET_ALL)
    else:
        input_timer_minute = None

    while True:
        try:
            input_delay_msg = int(input(f"Please input the delay messages in {Fore.CYAN + Style.BRIGHT}seconds{Style.RESET_ALL}: "))
            if input_delay_msg < 0:
                print(Fore.RED + f"Please enter a positive number" + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + f"Invalid input. Please enter a valid number" + Style.RESET_ALL)

    while True:
        input_channel_id = input(f"Please input the Channel ID: ")
        if input_channel_id:
            break
        else:
            print(Fore.RED + f"Channel ID empty" + Style.RESET_ALL)
        
    return input_mode, input_timer_minute, input_delay_msg, input_channel_id
    

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    console = Console()
    banner = """                                                         
        ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██████╗  ██████╗ ████████╗
        ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
        ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██████╔╝██║   ██║   ██║   
        ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██╔══██╗██║   ██║   ██║   
        ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██████╔╝╚██████╔╝   ██║   
        ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═════╝  ╚═════╝    ╚═╝   
"""
    console.print(Panel(banner, title="[bold yellow]Multiple Accounts Sending Messages[/bold yellow]",
                        title_align="center",
                        subtitle="By Meowstronot (Khisan)", subtitle_align="center", 
                        border_style="cyan", width=100, style="rgb(0,200,0)"))


class discord_bot:

    def __init__(self) -> None:
        self.channel_id = None
        self.delay_msg = random.randint(2, 7)  # Random Delay 2-7 Detik
        self.timer_minute = None

    @property 
    def api_url(self):
        return f"https://discord.com/api/v9/channels/{self.channel_id}/messages"
    
    def logger(self, header:str, header_color, message: str, end="\n"):
        print(f"{header_color}[{header.center(8)}]{Style.RESET_ALL} | {message}", end=end)

    def read_file_lines(self, file_path, method= "r"):
        """Membaca file dan mengembalikan list baris non-kosong."""
        try:
            with open(file_path, method, encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.logger(header="Failed", header_color=Fore.RED, message=f"File not found: {file_path}")
            return []
    
    async def send_msg(self, token:str=None, msg:str=None, attempt:int=3):

        header = {"authorization" : token}
        payload = {"content" : msg}

        for i in range(attempt):
            try:
                async with ClientSession(timeout=ClientTimeout(total=120)) as session:
                    async with session.post(url=self.api_url, headers=header, data=payload) as response:
                        response.raise_for_status()
                        result = await response.json()
                        return result
                    
            except ClientResponseError as e:
                self.logger(header="Failed", header_color=Fore.RED, message=f"[{token[:4]}***{token[-4:]}] Attempt {i+1}/{attempt} - HTTP Error: {e.status} {e.message}")
            except Exception as e:
                self.logger(header="Failed", header_color=Fore.RED, message=f"[{token[:4]}***{token[-4:]}] Attempt {i+1}/{attempt} - Error: {e}")
            if i < attempt - 1:
                await asyncio.sleep(random.randint(2, 5))  # Delay Retry antara 2-5 detik
                
        return None

    async def main(self, mode:int):
        token_list = self.read_file_lines("token.txt")
        msg_list = self.read_file_lines("msg.txt")

        if not token_list:
            self.logger(header="Failed", header_color=Fore.RED, message="The token.txt file is empty")
            return

        if not msg_list:
            self.logger(header="Failed", header_color=Fore.RED, message="The msg.txt file is empty")
            return

        if mode ==1:
            # basic mode
            for i, msg in enumerate(msg_list, start=1):

                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"\n{"="*10} Sending the Message ({i}) {"="*10}" + Style.RESET_ALL)
                tasks = [self.send_msg(token, msg) for token in token_list]
                responses = await asyncio.gather(*tasks)

                for token, response in zip(token_list, responses):
                    if response:
                        username = response.get("author", {}).get("username", token[:5]+"**")
                        content = response.get("content", "")
                        self.logger(header="Success", header_color=Fore.GREEN + Style.BRIGHT, message=f"[{username}] : {content}")
                    else:
                        self.logger(header="Failed", header_color=Fore.RED, message=f"[{token[:4]}***{token[-4:]}] Failed to send message {i}")

                for delay in range(self.delay_msg, 0, -1):
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Delay: {delay}", end="            \r" + Style.RESET_ALL)
                    print("", end="")
                    await asyncio.sleep(1)
                print_banner()

        elif mode == 2:
            # timer mode
            max_duration = self.timer_minute * 60   # convert durasi maksimal ke detik
            start_time = time.time()

            i = 0
            while True:
                if time.time() - start_time > max_duration:
                    print(Fore.YELLOW + f"The execution time reaches {max_duration/60} minutes, the program stops." + Style.RESET_ALL)
                    break
                
                # looping index melingkar 
                # msg = msg_list[i % len(msg_list)] # tiap akun pesan sama
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"\n{"="*10} Sending the Message ({(i% len(msg_list))+1}) {"="*10}" + Style.RESET_ALL)

                # tasks = [self.send_msg(token, msg) for token in token_list] # tiap akun pesan sama
                tasks = [self.send_msg(token, msg_list[(i + idx) % len(msg_list)]) for idx, token in enumerate(token_list)] # tiap akun pesan beda
                responses = await asyncio.gather(*tasks)

                for token, response in zip(token_list, responses):
                    if response:
                        username = response.get("author", {}).get("username", token[:5]+"**")
                        content = response.get("content", "")
                        self.logger(header="Success", header_color=Fore.GREEN + Style.BRIGHT, message=f"[{username}] : {content}")
                    else:
                        self.logger(header="Failed", header_color=Fore.RED, message=f"[{token[:4]}***{token[-4:]}] Failed to send message {(i% len(msg_list))+1}")

                for delay in range(self.delay_msg, 0, -1):
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"Delay: {delay}", end="            \r" + Style.RESET_ALL)
                    print("", end="")
                    await asyncio.sleep(1)
                i += 1
                print_banner()

        self.logger(header="Status", header_color=Fore.CYAN + Style.BRIGHT, 
                    message=f"{Fore.GREEN + Style.BRIGHT}All messages have been sent to all accounts {Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        print_banner()
        input_mode, input_timer_minute, input_delay_msg, input_channel_id = user()
        bot = discord_bot()

        bot.delay_msg = input_delay_msg
        bot.timer_minute = input_timer_minute
        bot.channel_id = input_channel_id

        print_banner()
        asyncio.run(bot.main(mode=input_mode))

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nINTERRUPTED! The program was stopped by the user." + Style.RESET_ALL)








# __/\\\________/\\\__/\\\________/\\\__/\\\\\\\\\\\_____/\\\\\\\\\\\_______/\\\\\\\\\_____/\\\\\_____/\\\_        
#  _\/\\\_____/\\\//__\/\\\_______\/\\\_\/////\\\///____/\\\/////////\\\___/\\\\\\\\\\\\\__\/\\\\\\___\/\\\_       
#   _\/\\\__/\\\//_____\/\\\_______\/\\\_____\/\\\______\//\\\______\///___/\\\/////////\\\_\/\\\/\\\__\/\\\_      
#    _\/\\\\\\//\\\_____\/\\\\\\\\\\\\\\\_____\/\\\_______\////\\\_________\/\\\_______\/\\\_\/\\\//\\\_\/\\\_     
#     _\/\\\//_\//\\\____\/\\\/////////\\\_____\/\\\__________\////\\\______\/\\\\\\\\\\\\\\\_\/\\\\//\\\\/\\\_    
#      _\/\\\____\//\\\___\/\\\_______\/\\\_____\/\\\_____________\////\\\___\/\\\/////////\\\_\/\\\_\//\\\/\\\_   
#       _\/\\\_____\//\\\__\/\\\_______\/\\\_____\/\\\______/\\\______\//\\\__\/\\\_______\/\\\_\/\\\__\//\\\\\\_  
#        _\/\\\______\//\\\_\/\\\_______\/\\\__/\\\\\\\\\\\_\///\\\\\\\\\\\/___\/\\\_______\/\\\_\/\\\___\//\\\\\_ 
#         _\///________\///__\///________\///__\///////////____\///////////_____\///________\///__\///_____\/////__
