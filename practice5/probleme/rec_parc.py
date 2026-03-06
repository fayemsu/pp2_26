import re

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

priceNname = r'\d\d?[.]\n(.+)\n(.{5})\s[x]\s(.+)'
x = re.findall(priceNname, text)

print("Products&Prices&Amount")
for i in range(len(x)):
    print(f"{i+1}. {x[i][0]}: {x[i][2]} tg x {x[i][1]} pc")

total = re.search(r'ИТОГО[:]\n(.+)', text)

print(f"TOTAL: {total.group(1)}")

time = re.search(r"Время:\s(.+)", text)
print(f'TIME&DATE: {time.group(1)}')

paymeth = re.search(r'Банковская карта|Наличные', text)
print(f'PAYMENT METHOD: {paymeth.group()}')