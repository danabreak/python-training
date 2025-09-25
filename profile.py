import sys


print("----------------------------------")
print("|      Name : " + sys.argv[1] + " " * (19 - len(sys.argv[1])) + "|")
print("|      Age  : " + sys.argv[2] + " " * (19 - len(sys.argv[2])) + "|")
print("|      City : " + sys.argv[3] + " " * (19 - len(sys.argv[3])) + "|")
print("|      Title: " + sys.argv[4] + " " * (19 - len(sys.argv[4])) + "|")
print("----------------------------------")
