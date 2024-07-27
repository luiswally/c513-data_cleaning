import mysql.connector
from mysql.connector import errorcode

# Database connection details
db_config = {
    'user': 'root',             # 'root' is the default user, verify and change if needed
    'password': 'password',     # 'password' is the default password, verify and change if needed
    'host': '127.0.0.1',
    'database': 'cs513DB'
}

# Queries for existing database
query0 = """
DROP TABLE IF EXISTS lowCostRestaurants_clean;
"""

query1 = """
CREATE TABLE lowCostRestaurants_clean AS
SELECT
    Menu.restaurant_name AS restaurant,
    Dish.name as dish,
    Menu.currency_symbol,
    MenuItem.price,
    MenuPage.menu_id,
    MenuItem.menu_page_id,
    MenuItem.id as menu_item_id,
    MenuItem.dish_id
FROM
    MenuItem_clean as MenuItem
    JOIN MenuPage_clean as MenuPage ON MenuItem.menu_page_id = MenuPage.id
    JOIN Menu_clean as Menu ON MenuPage.menu_id = Menu.id # ensures that a restaurant can be identified
    LEFT JOIN Dish_clean as Dish ON MenuItem.dish_id = Dish.id
WHERE
    MenuItem.price > 5 AND
    MenuItem.price <= 15.00
ORDER BY
    restaurant,
    MenuItem.price;
"""

query2 = """
SELECT
    *
FROM
  lowCostRestaurants_clean
ORDER BY
    restaurant,
    price;
"""

query3 = """
SELECT
    restaurant,
    COUNT(DISTINCT(dish_id)) AS cheap_meal_count,
    COUNT(DISTINCT(menu_id)),
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM
    lowCostRestaurants_clean
GROUP BY
    restaurant
ORDER BY
    restaurant;
"""

# Helper functions
def price_display(price, currency_symbol):
    if price is not None:
        return f"{currency_symbol} {price:.2f}"
    else:
        return 'Price not available'

# Main body wrapped in Try...Except blocks
try:
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Creating DB tables with use case query
    cursor.execute(query0)
    cursor.execute(query1)
    
    # Query: Get all low cost meals between $5-$15
    cursor.execute(query2)
    rows = cursor.fetchall()

    # Print the query results
    for row in rows:
        restaurant, dish, currency_symbol, price, menu_id, menu_page_id, menu_item_id, dish_id = row
        priceDisplay = price_display(price, currency_symbol)
        print(f"Restaurant: {restaurant}, Dish: {dish}, Price: {priceDisplay}")

    print("# of low cost meals: ", len(rows))

    # Query: Get all restaurants with low cost meals between $5-$15
    cursor.execute(query3)
    rows = cursor.fetchall()
    
    # Print the query results
    for row in rows:
        restaurant, mealCount, menuCount, avg_price, min_price, max_price  = row
        print(f"Restaurant: {restaurant}, Value Meals: {mealCount}, Avg Price: {avg_price:.2f}")

    print("# of affordable restaurants: ", len(rows))
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

# Except blocks for debugging
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
except Exception as e:
    print(f"An error occurred: {e}")