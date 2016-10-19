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
1) Сколько пользователь создал постов?
2) Сколько пользователь лайкнул постов?
3) Сколько пользователь откомментировал постов?
4) Сколько пользователь репостов сделал пользователь?
5) Пол пользователя (?)
6) Количество фолловеров
7) Количество групп, на которые он подписан