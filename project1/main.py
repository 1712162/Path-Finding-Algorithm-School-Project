from IOHandler import IOHandler

def main():
  IO = IOHandler()
  while True : 
    IO.display_menu(4)
    result = IO.handle_input()
    for path in result:
      IO.handle_output(path)
    wait = input("Press to continue")

if __name__ == "__main__":
  main()   

# /home/voquocthang/Study/CSTTNT/project1/test.txt

