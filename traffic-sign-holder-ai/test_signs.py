from src.slovak_signs_database import get_database

db = get_database()
print(f"Total signs in database: {len(db.signs)}")
print("\nSample signs (first 20):")
print("-" * 50)

for i, (code, sign) in enumerate(list(db.signs.items())[:20]):
    print(f"{code:>4}: {sign.name_sk:<30} ({sign.name_en})")
    
print("\nSearch examples:")
print("-" * 50)

# Test search functionality
print("\nSearching for 'stop':")
for code, sign in db.signs.items():
    if 'stop' in sign.name_en.lower() or 'stop' in sign.name_sk.lower():
        print(f"  {code}: {sign.name_sk} ({sign.name_en})")

print("\nSearching for 'zakaz' (prohibition):")
for code, sign in db.signs.items():
    if 'záka' in sign.name_sk.lower():
        print(f"  {code}: {sign.name_sk} ({sign.name_en})")
        if len([x for x in db.signs.items() if 'záka' in x[1].name_sk.lower()]) > 5:
            break