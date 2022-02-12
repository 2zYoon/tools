import sys
import clipboard

while 1:
    a = input("> ")
    name = a[:a.find("(")].strip()
    score = a.count("★")
    comment = a[a.find(")")+1:].strip()
 
    to_print = "/eat {} {} {} {} {} {}".format(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        name,
        score,
        comment
    )

    print(to_print)
    clipboard.copy(to_print)