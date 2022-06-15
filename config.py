from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = 2344247
API_HASH = "853cae451f8091db916cd9ad395bbf12"
BOT_TOKEN = "5386390739:AAFY8Lak8tz1CrMQb9kbZJfCJlBduaDTXhw"

MONGO_DB_URI = getenv("MONGO_DB_URI","mongodb+srv://techz:wall@techzwallbotdb.katsq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")