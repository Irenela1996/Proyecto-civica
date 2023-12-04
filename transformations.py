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

    nuevo_list_products = []
    nueva_list_urls = []
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
            nuevo_list_products.append("nan")
            nueva_list_urls.append(crear_url(list_urls_to_compare[i], "nan"))
        elif order in list_orders:
            # We get the index of the order_id in the list_orders
            index = list_orders.index(order)
            nuevo_list_products.append(list_products[index])
            print(
                "The new values are: ",
                order + ":" + str(list_products[index]),
            )
            # We create a dictionary with the old and new values
            diccionario_old_new[product] = list_products[index]
            nueva_list_urls.append(
                crear_url(list_urls_to_compare[i], diccionario_old_new[product])
            )
        else:
            # We check if the product_id is in the dictionary
            if product in diccionario_old_new:
                print("It is in the list")
                # We get the new value
                nuevo_list_products.append(diccionario_old_new[product])
                print(
                    "The new value for PRODUCT is: " + str(diccionario_old_new[product])
                )
                nueva_list_urls.append(
                    crear_url(list_urls_to_compare[i], diccionario_old_new[product])
                )
            else:
                print("It isn't in the list")
                # We get a random product_id
                random_value = random.choice(list_products)
                nuevo_list_products.append(random_value)
                print("The new value for PRODUCT is: " + str(random_value))
                # We add the new value to the dictionary
                diccionario_old_new[product] = random_value
                nueva_list_urls.append(
                    crear_url(list_urls_to_compare[i], diccionario_old_new[product])
                )

    print(len(nuevo_list_products))
    # Delete the column PRODUCT_ID
    del data_to_change["PRODUCT_ID"]
    # Add the new column PRODUCT_ID
    data_to_change["PRODUCT_ID"] = nuevo_list_products

    # Delete the column PAGE_URL
    del data_to_change["PAGE_URL"]
    # Add the new column PAGE_URL
    data_to_change["PAGE_URL"] = nueva_list_urls

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


# Main function
if __name__ == "__main__":
    # change_field("order_items.csv", get_product_id())
    change_product_id_events("events.csv")
