from typing import List, Text, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import pandas as pd

class ActionShowProducts(Action):
    def name(self) -> Text:
        return "action_show_products"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            products = fetch_products(tracker)  # Fetch top 5 products based on user input
            if products:
                dispatcher.utter_message(text="Here are the top 5 products:")
                for product in products:
                    dispatcher.utter_message(product)
            else:
                dispatcher.utter_message(text="I couldn't find any products matching your criteria.")
            return []
        except Exception as e:
            dispatcher.utter_message(text="An error occurred while showing products: {}".format(str(e)))
            return []

def fetch_products(tracker: Tracker) -> List[str]:
    try:
        user_input = tracker.latest_message.get('text')

        product_data = pd.read_csv('sample_data_10k.csv')

        filtered_products = product_data[product_data['Product Description'].str.contains(user_input, case=False, na=False)]

        if not filtered_products.empty:
            ranked_products = filtered_products.sort_values(by='Popularity', ascending=False).head(5)
            top_products = ranked_products['Product Name'].tolist()
            return top_products
        else:
            return []
    except Exception as e:
        raise e
