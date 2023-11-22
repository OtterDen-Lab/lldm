import CharGen

charGen = CharGen()
people = []

def creation():
    people.append(charGen.user_character())

def main():
    counter = 0
    while counter < 3:
        creation()
        counter += 1

    for person in people:
        print(person)
    print("done")

if __name__ == "__main__":
    main()