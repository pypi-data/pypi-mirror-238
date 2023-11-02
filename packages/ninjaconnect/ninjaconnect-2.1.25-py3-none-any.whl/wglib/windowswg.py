import subprocess
import os
import requests
import rich
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from wglib.storesess import Store
from wgexpection.wireguardexpections import *
import json
import urllib.parse
from wglib.auth import GitlabOuth
import shutil
console = Console()
ob = Store()
SERVICENAME = "SNALABS"
USERNAME = "SNALABS"
msi_url = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
class windowswireguard:
    def wireguardcheck(self):
        if os.path.exists("C:\Program Files\WireGuard\Data"):
            return True
        else:
            return False
    def configure(self):
        if self.wireguardcheck() == False:
            wireguardmsi = requests.get(msi_url)
            open(r"C:\Users\wireguard-installer.exe","wb").write(wireguardmsi.content)
            subprocess.run([r"C:\Users\wireguard-installer.exe","/S"],shell=True)
            print(":small_blue_diamond:[bold green1] WireGuard Installed Successfully[/bold green1]")
            self.generatekeys()
        else:
            print(":small_blue_diamond:[bold green1] WireGuard Already Installed[/bold green1]")
            reconfig = Prompt.ask("[bold green1]Do you want to configure again[/bold green1]")
            if reconfig.lower() == "y" or reconfig == "yes" or reconfig == "YES":
                self.newconfigure()
            elif reconfig.lower() == "n" or reconfig == "no" or reconfig == "NO":
                print("[bold green1]:small_blue_diamond: OK login and connect to labs[bold green1]")
            else:
                print("[bold green1]:small_blue_diamond: Option not valid[bold green1]")
    def generatekeys(self):
        privatekey = subprocess.run('"C:\Program Files\WireGuard\wg.exe" genkey', shell=True, capture_output=True, text=True)
        if privatekey.returncode == 0:
            private_key_str = privatekey.stdout
            public_key_gen = f'"C:\Program Files\WireGuard\wg.exe" pubkey'
            publickey = subprocess.run(public_key_gen, shell=True,input=private_key_str, capture_output=True, text=True)
            public_key_str = publickey.stdout
            private_file_path = "C:\Program Files\WireGuard\private.key"
            public_file_path = "C:\Program Files\WireGuard\public.key"

            with open(private_file_path, "w") as private_file:
                private_file.write(private_key_str)

            with open(public_file_path, "w") as public_file:
                public_file.write(public_key_str)
    def getwinpublickey(self):
        with open("C:\Program Files\WireGuard\public.key","r") as public:
            return public.read()
    def getwinprivatekey(self):
        with open("C:\Program Files\WireGuard\private.key","r") as private:
            return private.read()
    def winlistdevices(self):
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
    def add_device(self):
        deivie_name = Prompt.ask("[bold green1]:small_blue_diamond: Enter the device name :Desktop_Computer:  [/bold green1]")
        device_url = "https://labs.selfmade.ninja/api/device/add"
        payload = {
            "device_name": str(deivie_name),
            "device_type": "Laptop",
            "device_key": self.getwinpublickey(),
        }
        session = ob.getsess()
        headers = {"Cookie": f"PHPSESSID={session}"}
        try:
            response = requests.post(device_url, headers=headers, data=payload)
            data = response.json()
            json_string = json.dumps(data,indent=4)
            with open("labs.json", "w") as j:
                j.write(json_string)
                connected_device =  len(self.winlistdevices())
                print(f"[bold red1]:small_blue_diamond: No of Added devices in labs {connected_device}[/bold red1]")
            if response.status_code == 200:
                self.configfilecreate()
                print("[bold green1]:small_blue_diamond: Device added successfully![/bold green1]")
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

    def configfilecreate(self):
        deviceiplabconf = "https://labs.selfmade.ninja/api/device/wgconfig?id="
        publickey = self.getwinpublickey()
        encodepublickey = urllib.parse.quote(publickey)
        session = ob.getsess()
        headers = {"Cookie": f"PHPSESSID={session}"}
        configresponse = requests.get(deviceiplabconf+encodepublickey,headers=headers)
        tunnelconf = configresponse.text.replace("{private_key}",self.getwinprivatekey())
        with open("C:\Program Files\WireGuard\Win.conf","w") as w:
            w.write(tunnelconf)

    def wgconnect(self):
        if ob.getkey() is not None:
            try:
                subprocess.run('wireguard /installtunnelservice "C:\Program Files\WireGuard\Win.conf',shell=True,capture_output=True)
                messages = [
                            "[bold green1]:small_blue_diamond: Device Connected Successfully to Labs [/bold green1]",
                            "[bold green1]:small_blue_diamond: Now Connect labs with SSH [/bold green1]",
                            "[bold green1]:small_blue_diamond: Example: ssh yourusername@your_lab_ip[/bold green1]",]
                panel = Panel("\n".join(messages),title="SELF-MADE-NINJA-ACADEMY-CLI-VPN",style="bold orchid")
                console.print(panel)
            except subprocess.CalledProcessError as e:
                print(f"Error {e}")
        else:
            unabletolog = [
                "[bold green1]:small_blue_diamond: [red1]Unable to Connect [/red1]Login with Gitlab :Dog_Face:[/bold green1]",
            ]
            uabletoconnect = Panel("\n".join(unabletolog),title='SELF-MADE-NINJA-ACADEMY-CLI-VPN',style='bold orchid')
            console.print(uabletoconnect)
    def wgdisconnect(self):
        if ob.getkey() is not None:
            try:
                subprocess.run('wireguard /uninstalltunnelservice Win')
                disconnect_message = [
                    "[bold green1]:small_blue_diamond: Device [red1]disconnect[/red1] from labs[/bold green1]",
                ]
                disconnet_pannel = Panel("\n".join(disconnect_message),title='SELF-MADE-NINJA-ACADEMY-CLI-VPN',style='bold orchid')
                console.print(disconnet_pannel)
            except subprocess.CalledProcessError as e:
                print(f"Error{e}")
            except Exception as s:
                print("An error occurred",str(e))
        else:
            unabletolog = [
                "[bold green1]:small_blue_diamond: [red1]Unable to Connect [/red1]Login with Gitlab :Dog_Face:[/bold green1]",
            ]
            uabletoconnect = Panel("\n".join(unabletolog),title='SELF-MADE-NINJA-ACADEMY-CLI-VPN',style='bold orchid')
            console.print(uabletoconnect)            
                
    def login(self):
        auth = GitlabOuth()
        auth.gitlablogin()
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
    def newconfigure(self):
        try:
            subprocess.run('wmic product where name="WireGuard" call uninstall',capture_output=True,shell=True)
            folder_path = r'C:\Program Files\WireGuard'
            try:
                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"An error occurred : {str(e)}")
            wireguardmsi = requests.get(msi_url)
            open(r"C:\Users\wireguard-installer.exe","wb").write(wireguardmsi.content)
            subprocess.run([r"C:\Users\wireguard-installer.exe","/S"],shell=True)
            print(":small_blue_diamond:[bold green1] WireGuard Installed Successfully[/bold green1]")
            self.generatekeys()
        except subprocess.CalledProcessError as e:
            print(f"Error{e}")
    def showinfo(self):
        devices = len(self.winlistdevices())
        print(":small_blue_diamond:[green1 bold] NAME : NINJA CONNECT[/green1 bold]")
        print(":small_blue_diamond:[green1 bold] Version : 2.0.12[/green1 bold]")
        console.print(f":small_blue_diamond:[red1 bold] Number of connected devices in  labs {devices}[/red1 bold]")
        print(":small_blue_diamond: [green1 bold]Developed By SNA TEAM[/green1 bold] :wrench:")
        print(":small_blue_diamond: [green1 bold]Purpose : Educational VPN[/green1 bold] :mortar_board:")
        print(":small_blue_diamond: [green1 bold]Upto 5 device can connect to labs[/green1 bold] :link:")
        print(":small_blue_diamond: [green1 bold]Supported Platforms : Linux[/green1 bold] :penguin:")
        print(":small_blue_diamond: [green1 bold]PIP url : https://pypi.org/project/ninjaconnect/")
    def removedevice(self):
        deleteapiurl  = "https://labs.selfmade.ninja/api/device/delete"
        payload = {
            'id': self.getwinpublickey(),
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