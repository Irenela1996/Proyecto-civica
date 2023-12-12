import random
from pandas import read_csv
import string


def get_product_id():
    """Function to get product_id from CSV file"""
    product_id = []
    # reading CSV file
    data = read_csv("models_staging_data_base_peliculas.csv")
    # converting column data to list
    product_id = data["PRODUCT_ID"].tolist()
    return product_id


def change_field(csv, list_new_values):
    """Function to change product_id from CSV file"""
    # reading CSV file
    data = read_csv(csv)
    # converting column data to list
    list_values = data["PRODUCT_ID"].tolist()
    # Change the product_id_to_change by the product_id
    # randomly
    for i in range(len(list_values)):
        random_value = random.choice(list_new_values)
        list_values[i] = random_value
    # Delete the column PRODUCT_ID
    del data["PRODUCT_ID"]
    # Add the new column PRODUCT_ID
    data["PRODUCT_ID"] = list_values
    # Save the new CSV file
    data.to_csv(csv, index=False)
    print("The new list of values is: ", list_values)


def change_product_id_events(csv):
    """Function to change product_id from events CSV file"""
    # reading CSV file
    data = read_csv("order_items.csv")
    # converting column data to list
    list_orders = data["ORDER_ID"].tolist()
    list_products = data["PRODUCT_ID"].tolist()

    # reading CSV file
    data_to_change = read_csv(csv)
    # converting column data to list
    list_orders_to_compare = data_to_change["ORDER_ID"].tolist()
    list_products_to_compare = data_to_change["PRODUCT_ID"].tolist()
    list_urls_to_compare = data_to_change["PAGE_URL"].tolist()

    new_list_products = []
    new_list_urls = []
    # Create a dictionary to save the old and new values of product_id to allow to repeat
    # the same value in product_id
    diccionario_old_new = {}
    # If the order_id of order_items is in the list of list_orders_to_compare,
    # then we change the product_id for the same product_id as the order_items

    for i in range(len(list_orders_to_compare)):
        # We check if the order_id is nan
        order = str(list_orders_to_compare[i])
        product = str(list_products_to_compare[i])
        print("Order:" + order)
        print("Product:" + product)
        if order != "nan" and product == "nan":
            print("Product is nan")
            # We get a nan as product_id
            new_list_products.append("nan")
            new_list_urls.append(crear_url(list_urls_to_compare[i], "nan"))
        elif order in list_orders:
            # We get the index of the order_id in the list_orders
            index = list_orders.index(order)
            new_list_products.append(list_products[index])
            print(
                "The new values are: ",
                order + ":" + str(list_products[index]),
            )
            # We create a dictionary with the old and new values
            diccionario_old_new[product] = list_products[index]
            new_list_urls.append(
                crear_url(list_urls_to_compare[i], diccionario_old_new[product])
            )
        else:
            # We check if the product_id is in the dictionary
            if product in diccionario_old_new:
                print("It is in the list")
                # We get the new value
                new_list_products.append(diccionario_old_new[product])
                print(
                    "The new value for PRODUCT is: " + str(diccionario_old_new[product])
                )
                new_list_urls.append(
                    crear_url(list_urls_to_compare[i], diccionario_old_new[product])
                )
            else:
                print("It isn't in the list")
                # We get a random product_id
                random_value = random.choice(list_products)
                new_list_products.append(random_value)
                print("The new value for PRODUCT is: " + str(random_value))
                # We add the new value to the dictionary
                diccionario_old_new[product] = random_value
                new_list_urls.append(
                    crear_url(list_urls_to_compare[i], diccionario_old_new[product])
                )

    print(len(new_list_products))
    # Delete the column PRODUCT_ID
    del data_to_change["PRODUCT_ID"]
    # Add the new column PRODUCT_ID
    data_to_change["PRODUCT_ID"] = new_list_products

    # Delete the column PAGE_URL
    del data_to_change["PAGE_URL"]
    # Add the new column PAGE_URL
    data_to_change["PAGE_URL"] = new_list_urls

    # Save the new CSV file
    data_to_change.to_csv(csv, index=False)


def crear_url(url, valor):
    # Split the URL into parts
    url_parts = url.split("/")

    # Check if the URL has enough parts
    if len(url_parts) >= 4:
        # Construct the base URL using all parts until the 4th '/'
        base_url = "/".join(url_parts[:4]) + "/"

        # If valor is not "nan", use it as the second part
        if valor != "nan":
            second_part = valor
        else:
            # Create a random value with 3 elements, each with 1 to 5 characters and numbers, separated by "-"
            random_chars = "-".join(
                [
                    "".join(
                        random.choices(
                            string.ascii_letters + string.digits, k=random.randint(1, 5)
                        )
                    )
                    for _ in range(3)
                ]
            )
            second_part = random_chars

        # Create the complete URL
        url_complete = base_url + second_part

        # Return the URL
        return url_complete
    else:
        # Handle the case where the URL doesn't have enough parts
        return "Invalid URL structure"


def orders_purchase_rent(csv):
    """Function to change SHIPPING from orders CSV file"""
    # reading CSV file
    data = read_csv("models_staging_data_base_peliculas.csv")
    # converting column data to list
    list_products = data["PRODUCT_ID"].tolist()
    list_purchase_rent = data["COMPRA_O_ALQUILER"].tolist()

    data_orders = read_csv("order_items.csv")
    # converting column data to list
    list_orders = data_orders["ORDER_ID"].tolist()
    list_products_order_items = data_orders["PRODUCT_ID"].tolist()

    # reading CSV file
    data_to_change = read_csv(csv)
    # converting column data to list
    list_orders_to_compare = data_to_change["ORDER_ID"].tolist()

    new_list_purchase_rent = []

    for i in range(len(list_orders_to_compare)):
        # We check if the order_id is list_orders
        order = str(list_orders_to_compare[i])
        print("Order:" + order)
        if order in list_orders:
            # We get the index of the order_id in the list_orders
            index = list_orders.index(order)
            # We get the product_id of the order_id
            product = list_products_order_items[index]
            # We get the index of the product_id in the list_products
            index = list_products.index(product)
            print("Product:" + product)
            print("The value is: " + str(list_purchase_rent[index]))
            if list_purchase_rent[index] == "Comprar o alquilar":
                # We choose a random value between "Comprar" and "Alquilar"
                random_value = random.choice(["Purchase", "Rent"])
                new_list_purchase_rent.append(random_value)
                print(
                    "The new values are: ",
                    order + ":" + str(random_value),
                )
            else:
                new_list_purchase_rent.append("Purchase")
                print(
                    "The new values are: ",
                    order + ":" + str("Purchase"),
                )
        else:
            print("Error")

    # Delete the column SHIPPING
    del data_to_change["SERVICE"]
    # Add the new column SHIPPING
    data_to_change["SERVICE"] = new_list_purchase_rent
    # Save the new CSV file
    data_to_change.to_csv("orders.csv", index=False)


def delete_quantity():
    """Function to delete the column QUANTITY from order_items CSV file"""
    # reading CSV file
    data = read_csv("order_items.csv")
    # Delete the column QUANTITY
    del data["QUANTITY"]
    # Save the new CSV file
    data.to_csv("order_items.csv", index=False)


def change_user():
    """Function to change the column USER_ID from orders CSV file"""
    # reading CSV file to have all users
    data_users = read_csv("users.csv")
    # converting column data to list
    list_users_table_users = data_users["USER_ID"].tolist()
    # reading CSV file
    data = read_csv("orders.csv")
    # converting column data to list
    list_users = data["USER_ID"].tolist()
    listado_repetidos = []
    # Change the user_id by the user_id randomly
    for i in range(len(list_users)):
        random_value = random.choice(list_users_table_users)
        list_users[i] = random_value
        # if random_value in listado_repetidos more than 5 times, we change the value
        # by another random value
        if listado_repetidos.count(random_value) > 5:
            random_value = random.choice(list_users_table_users)
            list_users[i] = random_value
    # Delete the column USER_ID
    del data["USER_ID"]
    # Add the new column USER_ID
    data["USER_ID"] = list_users
    # Save the new CSV file
    data.to_csv("orders.csv", index=False)
    print("The new list of values is: ", list_users)


def create_col_empty():
    """Function to create a column empty"""
    # reading CSV file
    data = read_csv("orders.csv")
    # converting column data to list
    list_orders = data["ORDER_ID"].tolist()
    list_empty = []
    # get number of elements in list
    length = len(list_orders)
    for i in range(length):
        list_orders[i] = ","
    # Add the new column USER_ID
    data["_FIVETRAN_DELETED"] = list_orders
    # Save the new CSV file
    data.to_csv("orders.csv", index=False)
    print("The new list of values is: ", list_empty)


def change_place_column():
    """Function to change the place of a column"""
    # reading CSV file
    data = read_csv("orders.csv")
    # converting column data to list
    list__FIVETRAN_SYNCED = data["_FIVETRAN_SYNCED"].tolist()
    # Delete the column USER_ID
    del data["_FIVETRAN_SYNCED"]
    # add the new column USER_ID
    data["_FIVETRAN_SYNCED"] = list__FIVETRAN_SYNCED
    # Save the new CSV file
    data.to_csv("orders.csv", index=False)
