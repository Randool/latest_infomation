def load_eaddr(filename="emails.txt") -> list:
    emails = []
    with open(filename) as f:
        for line in f.readlines():
            print(line.strip())
            emails.append(line.strip())
    return emails


if __name__ == '__main__':
    e = load_eaddr()
    print(e)
