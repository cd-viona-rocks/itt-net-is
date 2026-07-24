# built-in converter aren't permitted here
#
# assumed your input is right. you should care about it
# no input verification is done here.

HEX = "ABCDEF"
PREFIX = {2: "0b_", 8: "0o_", 16: "0x_",}

def conv_to_dec(base: int):
    if base not in PREFIX.keys():
        raise ValueError(f"wrong wrapper definition. base must be one of {",".join([str(b) for b in PREFIX.keys()])}")

    def wrapped(n: str):
        """e.g. 10 -> 2*2^1 + 0 = 2"""
        len_n = len(n)
        result = 0
        for x in range(len_n):
            idx = len_n - x
            try:
                c = int(n[idx-1])
            except:
                # for this implementation, should run only for 0x
                c = 10

            try:
                if base == 16 and n in HEX:
                    c += HEX.find(n[idx-1])
            except:
                raise ValueError("i think, a digit from base 16 isn't between A-Z. check and try again.")

            if c >= base:
                raise ValueError("a digit from input is greater than base. check and try again.")
            
            result += c * pow(base,x)
        return result

    return wrapped


def conv_from_dec(base: int):
    if base not in PREFIX.keys():
        raise ValueError(f"wrong wrapper definition. base must be one of {",".join([str(b) for b in PREFIX.keys()])}")

    def wrapper(n: str):
        """e.g. 2 10 -> 0b_110"""
        if n == "0": return PREFIX[base]

        # find first bit
        rest = int(n)
        p = 0
        while pow(base,p) <= rest:
            last_p = p
            p += 1

        # then loop it back
        result = PREFIX[base]
        p = last_p
        while p >= 0:
            if pow(base,p) <= rest:
                c = rest - pow(base,p) + 1
                if base == 16 and c > 9:
                    c = HEX[c-10]
                result += str(c)
                rest -= pow(base,p) 
            else:
                result += "0"
            p -= 1
        return result

    return wrapper

bin_to_dec = conv_to_dec(2)
dec_to_bin = conv_from_dec(2)

octal_to_dec = conv_to_dec(8)
dec_to_octal = conv_from_dec(8)

hex_to_dec = conv_to_dec(16)
dec_to_hex = conv_from_dec(16)


if __name__ == "__main__":
    # your code here
    
    options = {
        0: "to cancel execution enter '0 0'",
        "M" : "print the menu enter 'M 0'",
        1: "binary to decimal",
        2: "decimal to binary",
        3: "octal to decimal",
        4: "decimal to octal",
        5: "hexadecimal to decimal",
        6: "decimal to hexadecimal",
    }
    menu = "\n\n" + " "*4 + "choose an option"
    menu += "\n" + " -"*20
    for k,v in options.items():
        menu += "\n" + " "*4 + f"{k}: {v}"
    print(menu + "\n\n") 

    o = -1
    while o != 0:
        try:
            input_number = input("enter an option and a number e.g. '1 110': ").upper()
            o,n = input_number.strip().split(" ")

            err = False
            if o == "0":
                print(f"execution terminated\n\n")
                break
            if o == "M":
                print(menu + "\n\n") 
                err = True
            elif o == "1":
                inp = "0b_"+n
                out = bin_to_dec(n)
            elif o == "2":
                inp = "dec "+n
                out = dec_to_bin(n)
            elif o == "3":
                inp = "0o_"+n
                out = octal_to_dec(n)
            elif o == "4":
                inp = "dec "+n
                out = dec_to_octal(n)
            elif o == "5":
                inp = "0x_"+n
                out = hex_to_dec(n)
            elif o == "6":
                inp = "dec "+n
                out = dec_to_hex(n)
            else:
                err = True
                print(f"invalid option. try again.")   

            if not err:
                print(f"{inp} -> {out}")
                
        except ValueError as e:
            print(str(e))
            continue
        except:
            print("invalid input. try gain.")
            continue
