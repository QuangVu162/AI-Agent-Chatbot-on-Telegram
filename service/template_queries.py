# Provide clear descriptions so Gemini understands WHEN to use them
SQL_TEMPLATES = {
    "daily_revenue": {
        "description": "Calculates the daily total sales revenue trend over a specified date range. Trigger this when the user asks for daily sales, daily revenue, or earnings day-by-day.",
        "query": """SELECT o.Order_Date as order_date, SUM(Sales) as total_sales  FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s GROUP BY o.Order_Date ORDER BY o.Order_Date DESC"""
    },
    "current_month_revenue": {
        "description": "Calculates the total sales revenue aggregated by month over a specified date range. Trigger this when the user asks for monthly revenue trends, monthly sales, or performance month-by-month.",
        "query": """SELECT MONTH(o.Order_Date) as order_month, SUM(Sales) as total_sales FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s GROUP BY MONTH(o.Order_Date) ORDER BY MONTH(o.Order_Date) DESC"""
    },
    "top_category": {
        "description": "Identifies the highest revenue-generating product categories over a specific date range. Trigger this when the user asks which broad categories are selling the most or generating the highest revenue.",
        "query":"""SELECT p.Category as category, SUM(Sales) as total_sales FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID INNER JOIN products AS p ON p.Product_ID = d.Product_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s GROUP BY p.Category ORDER BY SUM(Sales) DESC"""
    },
    "top_subcategory": {
        "description": "Identifies the highest revenue-generating product sub-categories over a specific date range. Trigger this for a detailed breakdown of best-selling sub-categories or specific item groups.",
        "query": """SELECT p.Sub_Category as sub_category, SUM(Sales) as total_sales FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID INNER JOIN products AS p ON p.Product_ID = d.Product_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s GROUP BY p.Sub_Category ORDER BY SUM(Sales) DESC"""
    },
    "daily_profit": {
        "description": "Calculates the total net profit aggregated by day over a specific date range. Trigger this when the user asks about profitability, net earnings after costs, or the most profitable days.",
        "query": """SELECT o.Order_Date as order_date, SUM(Profit) as total_profit FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s GROUP BY o.Order_Date ORDER BY o.Order_Date DESC"""
    },
    "top_quantity_product": {
        "description": "Identifies the specific products with the highest volume of units sold over a specific date range. Trigger this when the user asks for best-selling items by physical quantity or inventory movement.",
        "query": """SELECT p.Product_Name as product_name, SUM(quantity) as total_quantity FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID INNER JOIN products AS p ON p.Product_ID = d.Product_ID WHERE o.Order_Date >= %s  AND o.Order_Date <= %s  GROUP BY p.Product_Name ORDER BY SUM(quantity) DESC"""
    },
    "top_discount": {
        "description": "Analyzes the frequency of different discount rates applied to orders over a specific date range. Trigger this when the user asks about promotional performance, marketing campaigns, or how often discounts are used.",
        "query": """SELECT d.discount as discount, COUNT(*) as number_of_discount FROM orders AS o INNER JOIN order_details AS d ON o.Order_ID = d.Order_ID WHERE o.Order_Date >= %s AND o.Order_Date <= %s AND d.discount <> 0 GROUP BY d.discount ORDER BY COUNT(*) DESC"""
    },
}