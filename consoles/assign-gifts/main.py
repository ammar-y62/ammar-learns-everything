import csv
import random

def gift_exchange():
  with open('people.csv', newline='') as csvfile:
    next(csvfile, None)
    emails = []
    file_content = csv.reader(csvfile)
    for row in file_content:
        if not row or len(row) < 2:
            continue
        emails.append(row[1])
    if len(emails) < 2:
        raise ValueError("Need 2 participants")
    res = random_assign(emails)
    for i, n in enumerate(res):
      print(emails[i]," -> ", n)
def random_assign(emails):
  emails_set = set(emails)
  assigned = [""] * len(emails)
  for i, email in enumerate(emails):
    assigned[i] = random.choice(tuple(emails_set))
    while assigned[i] == email:
        if i == len(emails) - 1 and len(emails_set) == 1 and list(emails_set)[0] == email:
            # swap recipients between last and previous
            assigned[i], assigned[i-1] = assigned[i-1], email
            break
        assigned[i] = random.choice(tuple(emails_set))
    emails_set.discard(assigned[i])


  return assigned

if __name__ == "__main__":
    gift_exchange()
