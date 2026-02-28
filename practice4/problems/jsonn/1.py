import json

with open("sample-data.json", "r") as file:
    d = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<51} {'Description':<22} {'Speed':<9} MTU")
print("-" * 51,'-' * 22, '-'*9, '-'*6 )

for x in d["imdata"]:
    abc = x["l1PhysIf"]["attributes"]

    dn =abc["dn"]
    descr = abc["descr"]
    speed = abc["speed"]
    mtu = abc["mtu"]

    print(f"{dn:<51} {descr:<22} {speed:<9} {mtu:<6}")