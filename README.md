# vk-community-analysis
First steps to learn machines with vk communities data ;)

## Current notes
### Mongo
A dump of MongoDB is a simple folder containing .bson and .metadata files.
To import the folder to the database you should use the next command:
```bash
    mongorestore -d db_name path_to_folder
```
**Note:** Mongo server must be running at the time
