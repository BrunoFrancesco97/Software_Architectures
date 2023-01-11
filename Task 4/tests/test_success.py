import sys 

def func(number):
    if int(number) % 2 == 0:
        print("1") 
    else:
        print("0") 

if __name__ == '__main__':
    number = sys.argv[1]
    func(number)


