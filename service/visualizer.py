import matplotlib.pyplot as plt
import pandas as pd
import os
import logging
import datetime
from decimal import Decimal

class ChartGenerator:
    def __init__(self):
        self.output_dir = "output_images"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_chart(self, data, chart_type, x_col, y_col=None, filename="dynamic_chart.png"):

        # Standardize the data
        clean_data = []

        for row in data:
            clean_row = {}

            for key, value in row.items():
                # change the date data type
                if isinstance(value, (datetime.date, datetime.datetime)):
                    clean_row[key] = str(value)
                # change the decimal type to float type
                elif isinstance(value, Decimal):
                    clean_row[key] = float(value)
                else:
                    clean_row[key] = value

                clean_data.append(clean_row)

        logging.info(clean_data)

        # create dataframe
        df = pd.DataFrame(clean_data)

        if df.empty:
            logging.info("Pandas DataFrame is empty due to invalid input")
            return None

        plt.figure(figsize=(10, 6))

        try:
            if chart_type == "bar":
                plt.bar(df[x_col].astype(str), df[y_col], color='skyblue')
                plt.xticks(rotation=45)
            elif chart_type == "line":
                plt.plot(df[x_col].astype(str), df[y_col], marker='o', linestyle='-', color='green')
                plt.xticks(rotation=45)
            elif chart_type == "scatter":
                plt.scatter(df[x_col], df[y_col], color='red')
            elif chart_type == "hist":
                plt.hist(df[x_col], bins=10, color='purple', edgecolor='black')
            elif chart_type == "pie":
                plt.pie(df[y_col], labels=df[x_col], autopct='%1.1f%%', startangle=140)
            else:
                return None  # Fallback if unsupported type is passed

            plt.title(f"{chart_type.capitalize()} Chart")
            if chart_type != "pie":
                plt.xlabel(x_col)
                if y_col:
                    plt.ylabel(y_col)

            plt.tight_layout()
            filepath = os.path.join(self.output_dir, filename)
            logging.info(filepath)
            plt.savefig(filepath)
            plt.close()
            return filepath

        except Exception as e:
            print(f"Error generating chart: {e}")
            return None