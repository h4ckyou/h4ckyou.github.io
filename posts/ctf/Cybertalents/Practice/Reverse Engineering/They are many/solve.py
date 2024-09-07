import gdb

ge = gdb.execute
parse = gdb.parse_and_eval

ge('break *main')

output = []

with open('func.txt', 'r') as f:
    for line in f.readlines():
        addr = line.strip()

        ge('run')
        ge(f"break *0x8048330")
        ge(f'jump *{addr}')

        eax = parse("$eax")
        reg_ptr = eax.cast(gdb.lookup_type('char').pointer())
        result = reg_ptr.string()
        if "flag" in result:
            print(result)
            break
        
        output.append(result)
    
print(output)
