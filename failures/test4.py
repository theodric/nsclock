from os import system
import curses

def get_param(prompt_string):
     screen.clear()
     screen.border(0)
     screen.addstr(2, 2, prompt_string)
     screen.refresh()
     input = screen.getstr(10, 10, 60)
     return input

def execute_cmd(cmd_string):
     system("clear")
     a = system(cmd_string)
     print("")
     if a == 0:
          print("Command executed correctly")
     else:
          print("Command terminated with error")
     input("Press enter")
     print("")


stdscr = curses.initscr()
curses.start_color()

x = 0
while x != ord('4'):
        screen = curses.initscr()
        screen.clear()
        screen.border(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1))
        screen.addstr(2, 2, "Please enter a number...")
        screen.addstr(4, 4, "1 - Add a user")
        screen.addstr(5, 4, "2 - Restart Apache")
        screen.addstr(6, 4, "3 - Show disk space")
        screen.addstr(7, 4, "4 - Exit")
        screen.refresh()

        x = screen.getch()




curses.endwin()

