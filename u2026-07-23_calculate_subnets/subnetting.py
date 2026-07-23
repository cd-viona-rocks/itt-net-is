import sys

from typing import Union, Sequence

class NetID:
    def __init__(self, addr: Union[str, Sequence[Union[int, str]]], sn: Union[str, int]) -> None:
        # ---- normalize addr -> list[int] of length 4 ----
        if isinstance(addr, str):
            parts = addr.split(".")
        else:
            parts = list(addr)

        if len(parts) != 4:
            raise ValueError("A valid address must represent 4 octets (X.X.X.X).")

        addr_list: list[int] = []
        for p in parts:
            try:
                o = int(p)
            except (TypeError, ValueError):
                raise ValueError("All octets must be integers (or strings of integers).")

            if o < 0 or o > 255:
                raise ValueError("All octets are limited to 0 and 255.")
            addr_list.append(o)

        # ---- normalize sn -> int ----
        try:
            sn_int = int(sn)
        except (TypeError, ValueError):
            raise ValueError("Subnet mask must be an integer (or string of integer).")

        if sn_int < 0 or sn_int > 32:
            raise ValueError("Subnet mask must be an integer between 0 and 32.")

        self.addr = addr_list
        self.sn = sn_int

        self.ip_first = self.sum_to_addr(1)
        self.valid_ips = pow(2,32-self.sn)-2
        self.ip_last  = self.sum_to_addr(self.valid_ips)
        self.broadcast = self.sum_to_addr(self.valid_ips+1)

    def sum_to_addr(self, value: int, o: int = 4) -> None:
        """sum a value to an ip addr, by octect.

        Args:
            value: int - value to be summed
            o: int - octect where the sum must start, default = 4
        """
        ipv4 = self.addr[:]
        to_sum = value
        for idx in range(o):
            x = 3-idx
            v = ipv4[x] + to_sum
            if v < 256:
                ipv4[x] = v
                break
            else:
                ipv4[x] = v % 256
                to_sum = 1
        return ipv4

    def get_str_id(self):
        return ".".join([str(o) for o in self.addr])

    def get_net(self):
        return {
            "net_id": self.__str__(),
            "valid_ips": str(self.valid_ips),
            "ip_first": ".".join([str(o) for o in self.ip_first]),
            "ip_last":".".join([str(o) for o in self.ip_last]), 
            "broadcast": ".".join([str(o) for o in self.broadcast])
        }

    def __str__(self):
        addr_str = ".".join([str(o) for o in self.addr])
        return f"IPv4 {addr_str} /{self.sn}"


msg = "\n\n" + " -"*40
msg += "\n" + " "*4 + "Hallo! Ich bin Ihre Subnetting Assistent.\n"
msg += "\n" + " "*4 + "Bitte geben Sie eine günstige Netz-ID mit SN: X.X.X.X/SN"
msg += "\n" + " "*4 + "die Anzahl der gewünschten Subnetz innerhalb des ursprunglichen Netzes"
msg += "\n" + " "*4 + " -"*30
msg += "\n" + " "*4 + "Bitte folgen Sie das Eingabemodell: X.X.X.X/SN 20"
msg += "\n" + " "*4 + " -"*30 + "\n\n"
print(msg)

# param = input("Geben Sie die Parameter ein: ")
param = "10.0.0.0/24 4"

if "," in param:
    print("invalid input, space separated values. exit application.")
    sys.exit(0)

param = param.split(" ")
# print(param)

if len(param) !=2:
    print("invalid input, length must be 2 values. exit application.")
    sys.exit(0)

net_id,sn = param[0].strip().split("/")
net = NetID(net_id, sn)
n = int(param[1])


p = 1
while True:
    valid_n = pow(2,p)
    if n > valid_n:
        p += 1
    elif n == valid_n:
        n = valid_n
        print(" "*4 + f"{n} subnets is a valid division")
        break
    else:
        print(" "*4 + f"{n} subnets isn't a valid division. you must use {valid_n} subnets for this problem.")
        n = valid_n
        break

sn2 = net.sn + p
free_bits = 32 - sn2
n_addr = pow(2,free_bits)

# TODO: check if entry net_id is a valid id

# from here is assumed, net_id is valid
print(f"\n\noriginal net: \n{net.get_net()}\n")

network_table = [NetID(net.addr, sn2)]
for x in range(n-1):
    prev_net = network_table[len(network_table)-1]
    next_id_addr = prev_net.sum_to_addr(n_addr)
    next_net = NetID(next_id_addr, sn2)
    network_table.append(next_net)

for n in network_table:
    print(n.get_net())

print("\n\n"+" "*4+"Enjoy the code ! ! !  :)"+"\n")
    






