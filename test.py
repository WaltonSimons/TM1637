import tm1637

disp = tm1637.TM1637(3, 2)

disp.set_values(['A', 'B', 'b', 'C'])
r = raw_input()

disp.set_values(['c', 'D', 'd', 'E'])
r = raw_input()

disp.set_values(['F', 'G', 'H', 'h'])
r = raw_input()

disp.set_values(['I', 'J', 'K', 'L'])
r = raw_input()

disp.set_values(['l', 'n', 'O', 'o'])
r = raw_input()

disp.set_values(['P', 'r', 'S', 'U'])
r = raw_input()

disp.set_values(['Y', 'Z', ' ', ' '])
r = raw_input()

disp.set_values(['T1', 'T2', 'T1', 'T2'])
r = raw_input()

disp.set_values(range(4))
r = raw_input()

disp.set_values(range(4, 8))
r = raw_input()

disp.set_values(range(6, 10))
r = raw_input()

disp.clear()
