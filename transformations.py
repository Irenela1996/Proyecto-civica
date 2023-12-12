# Main function
import tools_transformations as tt

if __name__ == "__main__":
    tt.change_field("order_items.csv", tt.get_product_id())
    tt.change_product_id_events("events.csv")
    tt.orders_purchase_rent("orders.csv")
    tt.delete_quantity()
    tt.change_user()
    tt.create_col_empty()
    tt.change_place_column()
    # pass
