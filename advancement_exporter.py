import paramiko
import json
import getpass

HOST = "na2031.pebblehost.net"
PORT = 2222
USERNAME = "caedonr07@gmail.com.3489f2bb"

UUID_TO_NAME = {
    "4280396d-07dc-46b8-b277-f0ee6456e454": "Caedonnn",
    "76692783-7a5b-4375-ad03-93c6c84c6074": "aro__"
}

password = getpass.getpass("Enter SFTP password: ")

transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

players = []

for uuid, name in UUID_TO_NAME.items():
    try:
        path = path = f"world/advancements/{uuid}.json"

        with sftp.open(path, "r") as f:
            data = json.loads(f.read())

        completed = 0

        for advancement, info in data.items():
            if isinstance(info, dict) and info.get("done") is True:
                completed += 1

        players.append({
            "name": name,
            "advancements": completed
        })

        print(f"{name}: {completed}")

    except Exception as e:
        print(f"Failed for {name}: {e}")

output = {
    "players": players
}

with open("data/players.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print("\nCreated data/players.json")

sftp.close()
transport.close()