from database import Mongo
from dotenv import load_dotenv
from pydantic import BaseModel
from scraper import Main
import os

load_dotenv()


class BlacklistedContract(BaseModel):
    ContractAddress: str
    UserAddress: str
    reason: str
    Signature: str


class WhiteListedContract(BaseModel):
    ContractAddress: str
    CreatorAddress: str
    AuditorsSignature: str


mongo_uri = os.getenv("MONGO_URI")
mongo = Mongo(mongo_uri)
mongo.connect()


def get_blacklisted_contracts():
    cursor = mongo.find("blacklisted_contracts")
    blacklisted_contracts = [doc for doc in cursor]
    return {"blacklisted_contracts": blacklisted_contracts}


def blacklist_contract(contract: BlacklistedContract):
    # Insert the contract into the blacklisted_contracts collection
    mongo.insert(where="blacklisted_contracts", data=contract.dict())

    # Check if the user has submitted more than 3 contracts with the same signature
    user = contract.UserAddress
    count = mongo.count_collection(
        {"Signature": contract.Signature, "UserAddress": user}
    )

    if count > 3:
        # Add the user to the blacklisted_users collection
        mongo.insert(where="blacklisted_users", data={"user": user})
        return {"message": "User blacklisted"}

    return {"message": "Contract blacklisted"}


def whitelist_contract(contract: WhiteListedContract):
    mongo.insert(where="whitelisted_contracts", data=contract.dict())
    return {"message": "Contract Whitelisted"}


def get_whitelisted_contracts():
    cursor = mongo.find("whitelisted_contracts")
    whitelisted_contracts = [doc for doc in cursor]
    return {"whitelisted_contracts": whitelisted_contracts}


def is_contract_blacklisted(address: str):
    documents = mongo.find("blacklisted_contracts")

    for document in documents:
        if document.get("ContractAddress") == address:
            tags = ["exploit", "heist"]
            return {"message": tags}

    getscrapeddata = Main(address)
    if getscrapeddata:
        data = {"address": address, "reason": getscrapeddata}
        mongo.insert(where="blacklisted_contracts", data=data)

        return {"message": getscrapeddata}

    # If the address is not found, return False
    return {"message": False}
