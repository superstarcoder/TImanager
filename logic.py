#input start of event
#input end of event
#sleep
#school
def thing(a, st, et, ls):
	ls.append([a, st, et])
	ls.sort(key=lambda x: x[1])
	print(ls)
	schedule = ""
	for x in ls:
		schedule += str(x[0]).center(22)+"|"+str(x[1]).center(14)+"|"+str(x[2]).center(12)+"|"+"\n"
	print("""
      event name      |  start time  |  end time  |:
"""+schedule)

ls = []
while True:
	a = input("what event would you like to add? (type done if done): ")
	if a == "done":
		break
	st = input("start time [00:00]: ")
	et = input("end time  [00:00]:")
	thing(a,st,et,ls)

