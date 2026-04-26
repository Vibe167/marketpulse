import pymongo
import bcrypt

client = pymongo.MongoClient("mongodb://localhost:27017/")
db     = client["marketpulse"]

# Drop old users collection if exists
db["users"].drop()

# Create unique index
db["users"].create_index("username", unique=True)

# Add default admin user
hashed = bcrypt.hashpw("market123".encode("utf-8"), bcrypt.gensalt())
db["users"].insert_one({
    "username": "admin",
    "password": hashed,
    "role":     "admin"
})

print("Database created: marketpulse")
print("Collection created: users")
print("Admin user created: admin / market123")
print(f"Total users: {db['users'].count_documents({})}")
client.close()