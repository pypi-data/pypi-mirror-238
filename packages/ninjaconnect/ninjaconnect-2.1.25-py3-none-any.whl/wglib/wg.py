import os
import time
import subprocess
import sys
import requests
from wglib.auth import GitlabOuth
from wglib.storesess import Store
import json
import keyring
import sys
import random
from time import sleep
from rich import print
from rich.progress import Progress
from rich.panel import Panel
from rich.console import Console
import tempfile
from rich.prompt import Prompt
from wglib.wizard import Cliwiz
from wglib.wizard import wizarding
from wgexpection.wireguardexpections import *
console = Console()

ob = Store()
SERVICENAME = "SNALABS"
USERNAME = "SNALABS"

# def load_env(file_path=None):
#     if file_path is None:
#         # Get the directory of the script where this function is called
#         script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
#         # Construct the path to the .env file relative to the script's directory
#         file_path = os.path.join(script_dir, "../wg0.env")

#     try:
#         with open(file_path, "r") as file:
#             lines = file.readlines()
#             for line in lines:
#                 parts = line.strip().split("=")
#                 if len(parts) == 2:
#                     key, value = parts
#                     os.environ[key] = value
#     except FileNotFoundError:
#         print(f"The .env file ({file_path}) was not found.")


# load_env()

INSTALLWG = "sudo apt install wireguard -y"
INSTALLWGGET = "sudo apt-get install wireguard -y"
WIREGUARD_UP = "wg-quick up wg0"
WIREGUARD_DOWN = "wg-quick down wg0"
WIREGUARD_STATUS = "sudo wg show wg0"
OPENCONF = "nano /etc/wireguard/wg0.conf"
WGPRIVATEKEYGEN = "wg genkey | sudo tee /etc/wireguard/private.key"
WGPRIVATEKEYOPEN = "sudo cat /etc/wireguard/private.key"
WGPUBLICKEYGEN = "cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key"
WGPUBLICKEYOPEN = "sudo cat /etc/wireguard/public.key"
# def isloggedin():
#     if keyring.get_password(SERVICENAME,USERNAME):
#         return True
#     else:
#         return False

content = """
[Interface]
PrivateKey = {private_key}
Address = 172.20.9.100/32

[Peer]
PublicKey = cm9KJKYKSfXynAgznrH8+8JzYwxdk1Sn62/YWV/amW4=
AllowedIPs = 172.20.0.0/16
Endpoint = vpn.selfmade.ninja:44556
PersistentKeepalive = 30
"""
class Wireguard:
    """A Python class designed for WireGuard VPN management, providing key functionalities.
    It allows users to check if WireGuard is installed, start and stop WireGuard connections, 
    retrieve status information and keys, and uniquely, generate public and private keys along with a 'wg0'
    configuration file, streamlining the setup process for WireGuard connections."""
    global wgstatus

    def wgcheck(self):
        try:
            path = "/usr/bin/wg-quick"
            if os.path.exists(path):
                # print("WireGuard already installed")
                return True
            else:
                wgcmd1 = subprocess.run(
                    INSTALLWG, shell=True, text=True, check=True, capture_output=True
                )
                if "is already the newest version" in wgcmd1.stdout:
                    print("WireGuard is already installed")
                    return True
            return False  # Return False if neither condition is met
        except subprocess.CalledProcessError as e:
            print("Error occurred with apt. Trying apt-get instead...")
            try:
                subprocess.run(
                    INSTALLWGGET,
                    shell=True,
                    text=True,
                    check=True,
                    capture_output=False,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error occurred. Check .env: {e.stderr.strip()}")
            return False  # Return False if an error occurs

    # def openwg0(self):
    #     try:
    #         subprocess.run(OPENCONF, shell=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error :{e.output.decode('utf-8').strip()}")

    # def configexit(self):
    #     if os.path.exists("/etc/wireguard/wg0.conf"):
    #         return True
    #     else:
    #         return False

    # def allowed_ips(self):
    #     with open("labs.json", "r") as k:
    #         data = json.load(k)
    #         peer_info = data.get("peer_info", {})
    #         allowed_ips = peer_info.get("allowed ips", "")
    #     try:
    #         filepath = os.path.join("/etc/wireguard/wg0.conf")
    #         with open(filepath, "r") as w:
    #             filecontent = w.read()
    #             finalconf = filecontent.replace("{Address}", "{}".format(allowed_ips))
    #         with open(filepath, "w") as f:
    #             f.write(finalconf)
    #     except:
    #         print("After Configure run this sudo ./wireguard --action openwg0")

    def wgconnect(self):
        if ob.getkey() is not None:
            try:
                output = subprocess.check_output(['sudo','wg','show'],stderr=subprocess.STDOUT,text=True)
                if 'interface' in output:
                    connectedmessage = [
                        "[green1]:small_blue_diamond: Device already [purple]connected[/purple] :link:[/green1]"
                    ]
                    paneconn = Panel("\n".join(connectedmessage),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
                    console.print(paneconn)
                elif os.path.exists("/usr/bin/wg-quick"):
                    subprocess.run('sudo wg-quick up wg0', shell=True, capture_output=True)
                    messages = [
                            "[green1]:small_blue_diamond: Device Connected Successfully to Labs :link:[/green1]",
                            "[green1]:small_blue_diamond: Now Connect labs with SSH :rocket:[/green1]",
                            "[green1]:small_blue_diamond: Example: ssh yourusername@your_lab_ip :globe_with_meridians:[/green1]",]
                    panel = Panel("\n".join(messages),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
                    console.print(panel)
                else:
                    wgissuemessage = [
                            ":small_blue_diamond:[bold red1] ⚠️  WireGuard Configuration Issue[/bold red1]\n",
                            ":small_blue_diamond:[bold red1] ⚠️  Configure the Wireguard again [/bold red1]:wrench: \n",
                            "[italic]  apt-get remove --purge -y wireguard wireguard-tools[/italic]",
                            "[italic]  sudo rm -rf /etc/wireguard[/italic]",]
                    panelissue = Panel("\n".join(wgissuemessage),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
                    console.print(panelissue)
            except subprocess.CalledProcessError as e:
                print(f"Error:{e.output.decode('utf-8').strip()}")

        else:
            unabletolog = [
                "[bold green1]:small_blue_diamond: [red1]Unable to Connect [/red1]Login with Gitlab :Dog_Face:[/bold green1]",
            ]
            uabletoconnect = Panel("\n".join(unabletolog),title='SELF-MADE-NINJA-ACADEMY-CLI-VPN',style='bold orchid')
            console.print(uabletoconnect)

    def wgdisconnect(self):
        try:
            subprocess.run('sudo wg-quick down wg0', shell=True, capture_output=True)
            disconnect_message = [
                "[bold green1]:small_blue_diamond: Device [red1]disconnect[/red1] from labs :Electric_Plug:[/bold green1]",
            ]
            disconnet_pannel = Panel("\n".join(disconnect_message),title='SELF-MADE-NINJA-ACADEMY-CLI-VPN',style='bold orchid')
            console.print(disconnet_pannel)
        except subprocess.CalledProcessError as e:
            print(f"Error:{e.output.decode.strip()}")

    def getstatus(self):
        try:
            while True:
                output = subprocess.check_output(["sudo", "wg", "show", "wg0"]).decode(
                    "utf-8"
                )
                lines = output.split("\n")
                for line in lines:
                    if "transfer" in line:
                        parts = line.split()
                        received_data = float(parts[1])
                        recevid_unit = parts[2]
                        if received_data is not None:
                            print(
                                f"\rReceived data: {received_data:.2f} {recevid_unit}",
                                end="",
                            )
                        else:
                            print(
                                "\rFailed to retrieve data. Retrying in 60 seconds...",
                                end="",
                            )
                            self.wgconnect()
                time.sleep(2)
        except KeyboardInterrupt:
            print("\r")

    def getprivatekey(self):
        try:
            result = subprocess.run(WGPRIVATEKEYOPEN, shell=True, capture_output=True)
            privatekey = result.stdout.strip().decode()
            return str(privatekey)
        except subprocess.CalledProcessError as e:
            print(f"Unable to fetch the key :{e.output.strip()}")
    def myprivatekey(self):
        try:
            result = subprocess.run(WGPRIVATEKEYOPEN, shell=True, capture_output=True)
            privatekey = result.stdout.strip().decode()
            console.print("[red1]Note : Don't Share Your Privatekey[/red1]")
            console.print("[green1]We do not save your private key in our servers.[/green1]")
            console.print(f"[green1]Your Private Key :key: [/green1]{privatekey}")
        except subprocess.CalledProcessError as e:
            print(f"Unable to fetch the key :{e.output.strip()}")

    def getpublickey(self):
        try:
            result = subprocess.run(WGPUBLICKEYOPEN, shell=True, capture_output=True)
            publickey = result.stdout.strip().decode()
            # print("Your Public Key : " + str(publickey))
            return publickey
        except subprocess.CalledProcessError as e:
            print(f"Unable to fetch the key :{e.output.strip()}")
    def mypublickey(self):
        try:
            result = subprocess.run(WGPUBLICKEYOPEN, shell=True, capture_output=True)
            publickey = result.stdout.strip().decode()
            console.print(f"[green1]Your Public Key :key: [/green1]{publickey}")
        except subprocess.CalledProcessError as e:
            print(f"Unable to fetch the key :{e.output.strip()}")
    def isinstalled(self):
        if os.path.exists("/usr/bin/wg"):
            return True
        else:
            return False
    def newconfigure(self):
        try:
                subprocess.run(["sudo","apt-get", "remove", "--purge", "-y", "wireguard", "wireguard-tools"], check=True,capture_output=True)
                subprocess.run(["sudo","rm", "-rf", "/etc/wireguard/*"], check=True,capture_output=True)
                if self.isinstalled():
                    print("[bold green1]:small_Blue_Diamond:Old Configrations removed[bold green1]")
                else:
                    pass
                time.sleep(3)
                print("[bold green1]:small_Blue_Diamond: Initiating the process[bold green1]")
                wireguard_installed = subprocess.run(
                    ["sudo", "apt", "install", "-y", "wireguard-tools"],
                    capture_output=True,
                )
                with Progress() as progress:
                    task = progress.add_task(
                        "[bold green1]:small_Blue_Diamond: Installing WireGuard", total=10.348
                    )

                    while not progress.finished:
                        progress.update(task, advance=1)
                        sleep(1)
                print(
                    "[bold green1]:small_Blue_Diamond: WireGuard Succesfully Installed [/bold green1]:Thumbs_Up:"
                )
                if wireguard_installed.returncode == 0:
                    subprocess.run(
                        "wg genkey | sudo tee /etc/wireguard/private.key",
                        shell=True,
                        capture_output=True,
                    )
                    time.sleep(3)
                    output = subprocess.run(
                        "sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key",
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    if output.returncode == 0:
                        print(
                            "[bold green1]:small_Blue_Diamond: Keys Generated [/bold green1]:Thumbs_Up:"
                        )
                    output2 = subprocess.run(
                        "sudo cat /etc/wireguard/private.key",
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    private_key = output2.stdout.decode()
                    config_content = content.replace(
                            "{private_key}", "{}".format(private_key)
                        )
                command = f'echo "{config_content}" | sudo tee /etc/wireguard/wg0.conf'
                process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout ,stderr = process.communicate()
                print(
                    "[bold green1]:small_Blue_Diamond: WireGuard configuration has been created [/bold green1]:Thumbs_Up:"
                )
        except subprocess.CalledProcessError:
                print(
                    "[bold green1]:small_Blue_Diamond: Failed to install WireGuard. Please install it manually :No_Entry:"
                )
                return
    def configure(self):
        try:
            if self.isinstalled():
                print(
                    "[bold green1]:small_Blue_Diamond: WireGuard is already installed [/bold green1]:Thumbs_Up:"
                )
                print("[bold red1]:No_entry: Please be aware: Reconfiguring will result in the deletion of existing configurations[/bold red1]")
                reconf = Prompt.ask("[bold green1]:small_Blue_Diamond: Do you wish to proceed with the reconfiguration? (Y/N) [/bold green1]")
                if reconf.lower() == "y" or reconf == "yes" or reconf == "YES":
                    self.newconfigure()
                elif reconf.lower() == "n" or reconf == "no" or reconf == "NO":
                    print("[bold green1]:small_Blue_Diamond: OK login and connect to labs[bold green1]")
                else:
                    print("[bold green1]:small_Blue_Diamond: Option not valid[bold green1]")
            else:
                self.newconfigure()
        except KeyboardInterrupt as e:
            print(f"\n[bold orchid]Keyboard interrupted{e}[/bold orchid]")

    # def privatekeychange(self, privatek):
    #     try:
    #         filepath = os.path.join("/etc/wireguard/wg0.conf")
    #         with open(filepath, "r") as w:
    #             filecontent = w.read()
    #             finalconf = filecontent.replace("{private_key}", "{}".format(privatek))
    #         with open(filepath, "w") as f:
    #             f.write(finalconf)
    #     except:
    #         print("After Configure run this sudo ./wireguard --action openwg0")

    def showinfo(self):
        devices = len(self.listdevices())
        print(":small_blue_diamond:[green1 bold] NAME : NINJA CONNECT[/green1 bold]")
        print(":small_blue_diamond:[green1 bold] Version : 2.0.12[/green1 bold]")
        console.print(f":small_blue_diamond:[red1 bold] Number of connected devices in  labs {devices}[/red1 bold]")
        print(":small_blue_diamond: [green1 bold]Developed By SNA TEAM[/green1 bold] :wrench:")
        print(":small_blue_diamond: [green1 bold]Purpose : Educational VPN[/green1 bold] :mortar_board:")
        print(":small_blue_diamond: [green1 bold]Upto 5 device can connect to labs[/green1 bold] :link:")
        print(":small_blue_diamond: [green1 bold]Supported Platforms : Linux[/green1 bold] :penguin:")
        print(":small_blue_diamond: [green1 bold]PIP url : https://pypi.org/project/ninjaconnect/")

    def login(self):
            auth = GitlabOuth()
            auth.gitlablogin()
    def listdevices(self):
        try:
            session = ob.getsess()
            if session is not None:
                alllsitdeviceurl = "https://labs.selfmade.ninja/api/device/v2/all"
                headers = {"Cookie": f"PHPSESSID={session}"}
                deviceresponse = requests.get(alllsitdeviceurl, headers=headers)
                devicedata = deviceresponse.json()
                return devicedata
            else:
                print(":small_blue_diamond: [bold red1]Your are not login[bold red1]")
                return []
        except:
            print("[bold red]:small_blue_diamond: No Such Password found[/bold red]")

    def logout(self):
        session = ob.getsess()
        if session is not None:
            ob.deletekey()
            gitloboutmessages = [
                "[bold green1]:small_blue_diamond: [red1]Logged[/red1] out from Gitlabs :door:[/bold green1]",
            ]
            gitlout = Panel("\n".join(gitloboutmessages),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
            console.print(gitlout)
        else:
            notinlabs = [
                "[bold green1]:small_blue_diamond: You are not [red1]Logged[/red1] in gitlabs :Prohibited:[/bold green1]",
            ]
            notlogedin = Panel("\n".join(notinlabs),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
            console.print(notlogedin)

    def add_device(self):
        deivie_name = Prompt.ask("[bold green1]:small_blue_diamond: Enter the device name :Desktop_Computer:  [/bold green1]")
        device_url = "https://labs.selfmade.ninja/api/device/add"
        payload = {
            "device_name": str(deivie_name),
            "device_type": "Laptop",
            "device_key": self.getpublickey(),
        }
        session = ob.getsess()
        headers = {"Cookie": f"PHPSESSID={session}"}
        try:
            response = requests.post(device_url, headers=headers, data=payload)
            data = response.json()
            json_string = json.dumps(data,indent=4)
            with open("labs.json", "w") as j:
                j.write(json_string)
                connected_device =  len(self.listdevices())
                print(f"[bold red1]:small_blue_diamond: No of Added devices in labs {connected_device}[/bold red1]")
            if response.status_code == 200:
                print("[bold green1]:small_blue_diamond: Device added successfully![/bold green1]")
                self.addip()
            elif "Already" in response.text:
                print("[bold green1]:small_blue_diamond:This Device Already Registered :No_Entry:[/bold green1]")
            elif "You reached a rate limit" in response.text:
                print("[bold red1]:small_blue_diamond:You have reached the limit of devices. You cannot add more. You can delete an existing device and add one.:No_Entry:[/bold red1]")
            else:
                # print(f"[bold green1]:small_blue_diamond: Failed to add device | Login and try[/bold green1]")
                if response.status_code == 409:
                    raise AlreadyregisterExpection(102,'This Device Already Registerd')
        except requests.exceptions.ConnectionError as con:
            print(f"An Error Occured {con}")
        except AlreadyregisterExpection as a:
            print(a.args[0])
    def addip(self):
        # Load JSON data from 'labs.json'
        with open('labs.json', "r") as l:
            content = json.load(l)
            preer = content.get("peer_info", {})
            allowed_ips = preer.get('allowed ips')

        # Use subprocess to create a temporary file with the updated 'wg0.conf' using awk
        try:
            # Create a temporary directory for the temporary file
            temp_dir = tempfile.mkdtemp()
            temp_file = f"{temp_dir}/wg0_temp.conf"

            # Construct the awk command
            awk_command = [
                'awk',
                '-v',
                f'new_address={allowed_ips}',
                '$1 == "Address" { sub(/=.*/, "= " new_address) } 1',
                '/etc/wireguard/wg0.conf'
            ]

            # Use sudo to run the awk command with privileges and save the output to the temporary file
            with open(temp_file, 'w') as temp:
                subprocess.run(['sudo'] + awk_command, stdout=temp, check=True)

            # Replace the original file with the temporary file
            subprocess.run(['sudo', 'mv', temp_file, '/etc/wireguard/wg0.conf'], check=True)

            ipmoify = [
                "[bold green1]:small_blue_diamond: Device IP Added :link:[/bold green1]",
            ]
            ippanel = Panel("\n".join(ipmoify), title='SELF-MADE-NINJA-ACADEMY-CLI-VPN', style='bold orchid')
            console = Console()
            console.print(ippanel)
        except subprocess.CalledProcessError:
            print("Error: Failed to modify 'wg0.conf'")
    def removedevice(self):
        deleteapiurl  = "https://labs.selfmade.ninja/api/device/delete"
        payload = {
            'id': self.getpublickey(),
        }
        session = ob.getsess()
        headers = {"Cookie": f"PHPSESSID={session}"}
        try:
            response = requests.request("POST",url=deleteapiurl,headers=headers,data=payload)
            if "true" in response.text:
                print("[bold green1] Device Removed Succesfully[/bold green1]")
            else:
                raise UnabletoDeleteExpection(103,"Unable to Remove Device")
        except UnabletoDeleteExpection as d:
            print(d.args[0])
    def wizmode(self): 
        wizarding()