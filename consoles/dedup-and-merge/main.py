import json


def main():
    res = {}
    with open("customers.json") as json_file:
        json_data = json.load(json_file)
        res = deduplicates(json_data)
    print(json.dumps(res, indent=2))

def deduplicates(json_data):
    unique_emails = {}
    processed = kept = duplicates = skippedEmptyEmails = 0
    for i in json_data:
        if not isinstance(i, dict):
            continue
        processed+=1
        id = i.get("id")
        name = (i.get("name") or "").strip()
        email = (i.get("email") or "").strip().lower()
        phone = (i.get("phone") or "").strip()
        if not email:
                skippedEmptyEmails+=1
                continue
        elif email in unique_emails:
            details = unique_emails[email]
            if len(name) > len(details["name"]):
                unique_emails[email]["name"] = name
            if not details["phone"] and phone :
                details["phone"] = phone
            duplicates+=1
        else:
            unique_emails[email] = {
                "id": id,
                "name": name,
                "phone": phone,
                "email": email,
                }
            kept+=1
    print("Processed:", processed, "Kept:", kept, "Duplicates:", duplicates, "SkippedEmptyEmails:", skippedEmptyEmails)
    return sorted(unique_emails.values(),key=lambda r:r["id"])



if __name__ == "__main__":
    main()
