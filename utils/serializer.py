def serializeDict(data) -> dict:
    allData = data.copy()
    ids = {key: str(allData.pop(key))for key in data.keys() if "_id" in key}
    return {
        **allData,
        **ids
    }

def serializeList(entity) -> list:
    return [serializeDict(item) for item in entity]