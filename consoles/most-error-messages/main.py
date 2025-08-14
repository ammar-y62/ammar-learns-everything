def main():
    file_name = "log.txt"
    res = most_errors(file_name)
    print(res)
def most_errors(file_name):
    with open(file_name, 'r', encoding='UTF-8') as file:
        error_count = {}
        for line in file:
            error = line.split("] ")[1].split()[0]
            print(error)
            if error.upper() != error:
                continue
            error_count[error] = 1 + error_count.get(error,0)
        return sorted(error_count, key=lambda r: error_count[r], reverse=True)

if __name__ == "__main__":
    main()