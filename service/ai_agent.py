import os
import json
import logging
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from service.db_manager import DatabaseManager
from service.visualizer import ChartGenerator
from service.ai_base import PromptManager
from service.template_queries import SQL_TEMPLATES


# Setup security logging for Ad-Hoc queries
logging.basicConfig(filename='sql_security_audit.log', level=logging.INFO,
                    format='%(asctime)s - SECURITY AUDIT - Generated SQL: %(message)s')


class AIAgent:
    def __init__(self):
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.0,
            # request_options={"timeout":120.0},
            timeout=120.0,
            max_retries=1,
            convert_system_message_to_human=True
        )
        # self.llama = Ollama(model="llama3", base_url="http://ollama:11434")
        # self.sql_expert = Ollama(model="sqlcoder", base_url="http://ollama:11434", temperature = 0.0)
        # AI model to generate SQL
        self.sql_expert = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.0,
            # request_options={"timeout":120.0},
            timeout=120.0,
            max_retries=1,
            convert_system_message_to_human=True
        )
        self.db = DatabaseManager()
        self.visualizer = ChartGenerator()
        self.prompts = PromptManager()

    def process_query(self, user_question):

        # The hidden detailed instructions stored safely on your server
        button_questions = {
            "daily_revenue": "I want to know what is the daily revenue of today and is it going good or bad?",
            "top_category": "I want to know which categories have the best sales performance today.",
            "current_month_revenue": "I want to know what is the current month's sales.",
            "top_quantity_product": "I want to know top products in term of sales quantity today."
        }

        # 1. ROUTING: Ask Gemini if this is a known template
        action_code = SQL_TEMPLATES.get(user_question)

        if action_code:
            current_date = datetime.now().strftime("%Y-%m-%d")
            first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            route_data = {
                            "route": "template",
                            "template_name": user_question,
                            "start_date": first_day,
                            "end_date": current_date
                        }

            user_question = button_questions.get(user_question)
        else:
            route_response = self.gemini.invoke(self.prompts.get_routing_prompt(user_question)).content
            logging.info(route_response)

            # Check the output format
            if isinstance(route_response, list):
                route_string = route_response[0].get("text")
            else:
                route_string = route_response

            logging.info(route_string)

            route_data = json.loads(route_string.replace("\n    ", "").replace("`", "").strip())


        logging.info(route_data)

        raw_data = None
        sql_query = None

        # 2. EXECUTION: Template vs Ad-Hoc
        if route_data.get("route") == "template":
            template_name = route_data.get("template_name")
            start_date = route_data.get("start_date")
            end_date = route_data.get("end_date")
            extra_filters = route_data.get("extra_filters")
            extra_tables = route_data.get("extra_tables")
            limit = route_data.get("limit")
            print(f"Executing secure template: {template_name}")

            # Using execute_dynamic_template instead of execute_template since extra_filters are present
            if extra_filters:
                raw_data = self.db.execute_dynamic_template(template_name=template_name, date_params=[start_date, end_date], extra_tables=extra_tables, extra_filters=extra_filters, limit=limit)
            else:
                raw_data = self.db.execute_template(template_name, limit, [start_date, end_date])

        else:
            print("Fallback to Ad-Hoc Text-to-SQL...")
            # Use sql_expert for SQL generation
            sql_prompt = self.prompts.generate_sql_prompt(user_question, route_data)
            sql_output = self.sql_expert.invoke(sql_prompt).content


            if isinstance(sql_output, list):
                sql_query = sql_output[0].get("text")
            else:
                sql_query = sql_output

            sql_query = sql_query.replace("\n", " ").strip()
            logging.info(sql_query)
            # LOG THE QUERY FOR SECURITY AUDIT


            raw_data = self.db.execute_raw_sql(sql_query)

        logging.info(raw_data)

        if not raw_data:
            return "No data found for this request.", None

        # 3. VISUALIZATION & INSIGHTS
        chart_data = self.gemini.invoke(self.prompts.get_dynamic_sql_and_chart_prompt(raw_data)).content
        logging.info(chart_data)

        # check the chart_data format
        if isinstance(chart_data, list):
            chart_string = chart_data[0].get("text")
        else:
            chart_string = chart_data


        chart_select = json.loads(chart_string.replace("\n    ", "").replace("`", "").strip())

        logging.info(chart_select)

        #Get information of chart
        chart_type = chart_select.get("chart_type")
        x_col = chart_select.get("x_col")
        y_col = chart_select.get("y_col")

        # Check the log
        logging.info(chart_type)
        logging.info(x_col)
        logging.info(y_col)


        chart_path = self.visualizer.generate_chart(raw_data, chart_type, x_col, y_col)  # Let visualizer handle logic
        logging.info(chart_path)

        #Generate insight
        insight_prompt = self.prompts.get_insight_prompt(raw_data, user_question)
        insight = self.gemini.invoke(insight_prompt).content

        logging.info(insight_prompt)
        logging.info(insight)

        return insight, chart_path
