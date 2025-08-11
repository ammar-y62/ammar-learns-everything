def main():
    fileName = "products.txt"
    process_file(fileName)

def process_file(filename):
    with open(filename) as f:
        res = "id,name,price\n"
        nameSet = set()
        for i in f.readlines()[1:]:
            x = i.split(",")
            id = x[0].strip()
            name = x[1].strip()
            price = x[2].strip()
            if name.lower() not in nameSet:
                res+=id+","+name+","+price+"\n"
                nameSet.add(name.lower())
        with open("res.txt", "w") as o:
            f.write(res)

if __name__ == "__main__":
    main()
