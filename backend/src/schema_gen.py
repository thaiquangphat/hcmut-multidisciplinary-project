from pymongo import MongoClient

def create_schema():
    client = MongoClient("mongodb://localhost:27017")
    db = client["QQ"] 

    device_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["ID", "Humidity", "Light", "Temperature", "placeID"],
            "properties": {
                "ID": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "Humidity": {
                    "bsonType": "number",
                    "description": "must be a number and is required"
                },
                "Light": {
                    "bsonType": "number",
                    "description": "must be a number and is required"
                },
                "Temperature": {
                    "bsonType": "object",
                    "required": ["time", "value"],
                    "properties": {
                        "time": {
                            "bsonType": "date",
                            "description": "must be a date and is required"
                        },
                        "value": {
                            "bsonType": "number",
                            "description": "must be a number and is required"
                        }
                    },
                    "description": "temperature object containing time and value"
                },
                "placeID": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

    # Pass the schema directly to the validator parameter
    db.create_collection(
        "record_device",
        validator=device_schema
    )
    print("Collection with schema created successfully")


create_schema()
