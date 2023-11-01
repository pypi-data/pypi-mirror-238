from useless_test_package.hulu import easy

def main():
    value: str = input('gimme bites: ')
    num: int = int(value)
    print(f"result: {easy(num)}")

if __name__=="__main__":
    main()