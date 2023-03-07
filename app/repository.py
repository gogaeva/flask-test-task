DB_NAME = 'flask_task_db'
COLLECTION_NAME = 'resources_limits'

class ResourceLimit:
    def __init__(self, category, value):
        self.category = category
        self.value = value

class LimitsRepository:
    def __init__(self, client):
        self.collection = client[DB_NAME][COLLECTION_NAME]

    def get_by_category(self, category):
        return self.collection.find_one({'category': category})

    def add(self, limit):
        return self.collection.insert_one(limit)

    def modify(self, new_limit):
        category = new_limit['category']
        new_value = new_limit['value']
        return self.collection.update_one({'category': category}, {'$set': {'value': new_value}})
