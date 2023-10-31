import argparse
import shutil
import sys
import os
import subprocess
from colorama import Fore, init ,Back, Style  # For colored version display

init(autoreset=True) 

def path():
  # Get the full path of the current working file
  current_file_path = os.path.abspath(__file__)
  
  # Get the directory path without the file
  current_directory = os.path.dirname(current_file_path)
  return current_directory

class Command:
  def ask(self,question,default=None):
    try:
      qe = input(f"{question} ? \t")
      
      if len(str(qe.strip())) == 0 and default == None:
        self.Print(f"Expected a value","error")
        self.ask(question,default)
        
      if not len(str(qe.strip())) == 0:
        return qe
      else:
        return default
          
    except(EOFError , KeyboardInterrupt):
      self.Print("\nTerimnated by User","warning")
      sys.exit()
  def Print(self,msg,typeMSG):
    terminal_width, _ = shutil.get_terminal_size((80, 20))
    padding_length = max(0, (terminal_width - len(msg)) // 2)
    padding = " " * padding_length
    if typeMSG == "error":
      print(Back.RED + padding + Fore.BLACK + f"[ERROR] {msg}" + padding + Style.RESET_ALL)
    if typeMSG == "warning":
      print(Back.YELLOW + Fore.BLACK + f"[WARNING] {msg}" + Style.RESET_ALL)
    if typeMSG == "success":
      print(Back.GREEN + Fore.WHITE + f"[OK] {msg}" + Style.RESET_ALL)
    if typeMSG == "info":
      print(Back.LIGHTBLACK_EX + Fore.WHITE + f"[Info] {msg}" + Style.RESET_ALL)
  def run_cmd(self,cmd):
    command = cmd
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout
    
class Setup(Command):
  def __init__(self,dest):
    self.dest = dest
    if self.dest == None:
      answer = self.ask("In wich destination must be the celer-server installed","./celer-server")
      self.dest = answer
      
    self.Print("Setuping the server...","info")
    result = self.run_cmd(f"{path()}/bin/setup {self.dest}")
    if "Success" in result:
        self.Print("Setting up the server was successful", "success")
    else:
        self.Print(f"Setup failed: {result}", "error")
        sys.exit(1)

    
class Install(Command):
    def __init__(self,args):
      self.args = args
      ignoreSetup = args.ignoreSetup if args.ignoreSetup is not None else False
      
    def install(self):
      if self.args.dest == None:
        answer = self.ask("In wich destination must be the celer-server installed [default:./celer-server]","./celer-server")
        self.args.dest = answer
      if self.args.type == None:
        print(f"[{Fore.GREEN}0{Style.RESET_ALL}] Celer Server")
        print(f"[{Fore.GREEN}1{Style.RESET_ALL}] Celer Server | SQlite3")
        answer = self.ask("Select wich celer-server you want to install [default:0] " , "0")
        if answer == '0':
          self.args.type = "normal"
        else:
          self.args.type = "sqlite"
        
        if self.args.type == "normal":
          url = "https://github.com/celer-redis/celer-server-python"
        else:
          url = "https://github.com/celer-redis/celer-server-python"
          
        self.Print("Installation in process","info")
        self.run_cmd(f"git clone {url} {self.args.dest}")
        self.Print("Installation was successful","success")
        
        if self.args.ignoreSetup == None:
          Setup(self.args.dest)
        else:
          self.Print("Setupping was terminated by the user","warning")
          

class Diagnose(Command):
    def __init__(self,args):
      self.args = args
      if self.args.dest == None:
        answer = self.ask("In wich destination must be the celer-server installed")
        self.args.dest = answer
      self.Print("Diagnose in process...","info")
      result = self.run_cmd(f"{path()}/bin/diagnose {self.args.dest}")
      if "Success" in result:
          self.Print("The server was setupped successfully", "success")
      else:
          self.Print(f"Error Found: {result}", "error")
          sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Celer Installer Tool v1.20.3', add_help=False)
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install a package')
    install_parser.add_argument('--ignoreSetup', action='store_true', help='Boolean option to ignore setup')
    install_parser.add_argument('--dest', type=str, help='Destination path')
    install_parser.add_argument('--type', type=str, help='celer server type')

    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Configure the application')
    setup_parser.add_argument('--dest', type=str, help='Destination path')

    # Diagnose command
    diagnose_parser = subparsers.add_parser('diagnose', help='Diagnose issues')
    diagnose_parser.add_argument('--dest', type=str, help='Destination path')

    parser.add_argument('-V', '--version', action='store_true', help='Show version and exit')

    args = parser.parse_args()

    if args.version:
        print(Fore.GREEN + 'Celer Installer v1.1.0' + Style.RESET_ALL)
    elif not args.command:
        parser.print_help()
    elif args.command == 'install':
        Install(args).install()
    elif args.command == 'setup':
        Setup(args.dest)
    elif args.command == 'diagnose':
        Diagnose(args)
    else:
        # If -h [cmd] is used, show help for that specific command
        if args.command == '-h':
            subparsers.choices[args.command_args[0]].print_help()
        else:
            print("Invalid command. Use 'install', 'setup', or 'diagnose'.")
            parser.print_help()

if __name__ == '__main__':
    main()
