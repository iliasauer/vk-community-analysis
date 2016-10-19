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

### Vector
**Components:**
1) How many posts were created by the user? 
2) How many posts were liked by the user? 
3) How many posts were commented by the user? 
4) How many posts were reposted by the user? 
5) How many communities were subscribed by the user? 
6) How many followers have a user? 
7) The user's gender (?) 

### Next
Search for some similar papers about Facebook 
