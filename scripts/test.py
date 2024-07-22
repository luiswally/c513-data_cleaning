import mysql.connector
from mysql.connector import errorcode

# Database connection details
db_config = {
    'user': 'root',
    'password': 'password',  # replace with your actual password
    'host': '127.0.0.1',
    'database': 'testDB'
}

query = """
SELECT
  MenuPage.menu_id,
  MenuItem.menu_page_id,
  MenuItem.id as menu_item_id,
  MenuItem.dish_id,  
  Menu.name AS restaurant,
  Menu.currency,
  MenuItem.price
FROM
  MenuItem_csv as MenuItem
  JOIN MenuPage_csv as MenuPage ON MenuItem.menu_page_id = MenuPage.id
  LEFT JOIN Menu_csv as Menu ON MenuPage.menu_id = Menu.id
WHERE
  MenuItem.price > 0 AND
  MenuItem.price <= 15.00 AND
  Menu.id IS NULL
ORDER BY
  MenuItem.price;
"""

try:
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        menu_id, menu_page_id, menu_item_id, dish_id, restaurant, currency, price = row
        if price is not None:
            price_display = f"{currency} {price:.2f}"
        else:
            price_display = 'Price not available'
        print(f"Menu ID: {menu_id}, Menu Page ID: {menu_page_id}, Menu Item ID: {menu_item_id}, Dish ID: {dish_id}, Restaurant: {restaurant}, Price: {price_display}")

    print("This many matches: ", len(rows))

    # Close the cursor and connection
    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
except Exception as e:
    print(f"An error occurred: {e}")
