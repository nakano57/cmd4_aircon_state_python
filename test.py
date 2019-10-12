import sys

f = open('./test.txt', "a")

for i in sys.argv:
    text = i + ' '
    f.write(text)

f.write('\n')
sys.exit()
