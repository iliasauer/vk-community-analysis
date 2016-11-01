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
1. How many posts were created by the user?  
    1.1. Взять id пользователя из базы участников  
    1.2. Перебирая все посты в таблицах сообществ, увеличивать счётчик, если id создателя поста совпадает со взятым id  
    1.3. Добавить результаты в список и вернуться к 1  
2. How many posts were liked by the user?  
    2.1. Взять id пользователя из базы участников  
    2.2. Перебирать все посты в таблицах сообществ. В каждом из постов:  
        2.2.1. Перебирая всех пользователей, которые поставили лайк посту, увеличивать счётчик, если id данного пользователя совпадает со взятым id  
    2.3. Добавить результаты в список и вернуться к 1  
3. How many posts were commented by the user?  
    3.1. Взять id пользователя из базы участников  
    3.2. Перебирать все посты в таблицах сообществ. В каждом из постов:  
        3.2.1. Перебирая все комментарии к посту, увеличивать счётчик, если id создателя комментария совпадает со взятым id  
    3.3. Добавить результаты в список и вернуться к 1  
4. How many posts were reposted by the user?  
    4.1. Взять id пользователя из базы участников  
    4.2. Перебирать все посты в таблицах сообществ. В каждом из постов:  
        4.2.1. Перебирая всех пользователей, которые сделали репост, увеличивать счётчик, если id данного пользователя совпадает со взятым id  
    4.3. Добавить результаты в список и вернуться к 1  
5. How many communities were subscribed by the user? (Возможно, стоит брать только футбольные сообщества)  
    5.1. Взять id пользователя из базы участников  
    5.2. Взять количество сообществ из той же коллекции  
    5.3. Добавить результаты в список и вернуться к 1  
6. How many followers have a user? (Возможно, стоит брать только участников сообществ, хотя спорно)  
    6.1. Взять id пользователя из базы участников  
    6.2. Взять количество фолловеров из той же коллекции  
    6.3. Добавить результаты в список и вернуться к 1  

__**Note**: практически одинаковыми являются следующие алгоритмы:__
- 2 и 4
- 5 и 6

### Next
Search for some similar papers about Facebook 
