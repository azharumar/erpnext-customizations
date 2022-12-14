def disable_inactive_items():
    for items in frappe.db.get_list("Item",{"is_stock_item":1,"is_fixed_asset":0,"disabled":0},["item_code"]):
        stock_qty = erpnext.stock.utils.get_latest_stock_qty(items.item_code, warehouse=None)
        if stock_qty == 0:
            stock_value = get_stock_value_on(warehouse=None, posting_date=None, item_code=items.item_code)
            if stock_value == 0:
                if not frappe.db.get_list("Stock Ledger Entry",{"item_code":items.item_code, "posting_date":["between",[add_to_date(today(), days=-90, as_string=True),today()]], "voucher_type":["!=","Stock Reconciliation"]}):
                    frappe.db.set_value("Item",{"name":items.item_code},{"disabled":1})
                    print(items.item_code)