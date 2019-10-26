from IOHandler import IOHandler

def main():
  IO = IOHandler()
  while True : 
    IO.display_menu(4)
    result = IO.handle_input()
    if(result == 0):
      break
    if(result) : 
      for path in result:
        IO.handle_output(path)
    wait = input("Press to continue")

if __name__ == "__main__":
  main()   

