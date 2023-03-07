db = db.getSiblingDB("flask_task_db");
db.createCollection('resources_limits');
db.resources_limits.insertOne({category: "memory", value: 400});