dic = {
    'a':1, 
    'b':2,
    'c':3,
    'e':5,
    'd':4
}

sorted_list = sorted(dic.items())
final_list = [x[0] for x in sorted_list]
print(final_list)