# c513-data_cleaning
CS 513 Group Project, Data Cleaning NYPL-Menus

##  Getting Started
Ensure you have python3 and MySQL installed.

### Setting up MySQL
```bash
mysql -u root -p # root and password are the default mysql username and password
password
```

### Setup database
```sql
CREATE DATABASE cs513DB;
SHOW DATABASES;
USE cs513DB;
SELECT DATABASE(); # Verify the current database environment.

SOURCE /Users/wally/Databases/clean/Menu_clean.sql;
SOURCE /Users/wally/Databases/clean/MenuPage_clean.sql;
SOURCE /Users/wally/Databases/clean/MenuItem_clean.sql;
SOURCE /Users/wally/Databases/clean/Dish_clean.sql;

SOURCE /Users/wally/Databases/raw/Menu.sql;
SOURCE /Users/wally/Databases/raw/MenuPage.sql;
SOURCE /Users/wally/Databases/raw/MenuItem.sql;
SOURCE /Users/wally/Databases/raw/Dish.sql;

SHOW TABLES;
```
