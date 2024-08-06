from typing import Dict
from dotenv import load_dotenv
from src.utils.load_config import LoadConfig

load_dotenv()

CONFIG = LoadConfig()


class Neo4jChain:
    """This class maps extracted user's criteria to Neo4J graph database"""
    def __init__(self):
        self.graph = CONFIG.graph

    @staticmethod
    def get_question_attributes(values: Dict) -> Dict:
        """
        This function extracts all necessary dict values
        :param values: Dict with user's criteria
        :return: Correct dict to map the Neo4J DB
        """
        # Extract parameters directly from the input values
        min_price = values.get('min_price', None)
        max_price = values.get('max_price', None)
        if min_price and max_price and min_price == max_price:
            min_price = min_price - 100000
            max_price = max_price + 100000

        bedrooms = values.get('bedrooms', None)
        baths = values.get('baths', None)
        sqft_living = values.get('sqft_living', None)
        sqft_lot = values.get('sqft_lot', None)
        floors = values.get('floors', None)
        condition = values.get('condition', None)
        sqft_basement = values.get('sqft_basement', None)
        yr_built = values.get('yr_built', None)
        yr_renovated = values.get('yr_renovated', None)
        street = values.get('street', None)
        city = values.get('city', None)
        limit = values.get('limit') or 5

        match_dict = {
            "min_price": min_price,
            "max_price": max_price,
            "bedrooms": bedrooms,
            "baths": baths,
            "sqftLiving": sqft_living,
            "sqftLot": sqft_lot,
            "floors": floors,
            "condition": condition,
            "sqftBasement": sqft_basement,
            "yrBuilt": yr_built,
            "yrRenovated": yr_renovated,
            "street": street,
            "city": city,
            "limit": limit
        }
        # Log the actual parameters being used
        print(f"Parameters: {match_dict}")
        return match_dict

    def map_to_database(self, match_dict):
        """
       Maps the values to entities in the database and returns the mapping information.

       :param match_dict: A dict of values to map entities in database.
       :return: A string containing the mapping information of each value to entities in the database.
        """
        match_query = """
        MATCH (h:House)
            WHERE
            ($min_price IS NULL OR h.price >= $min_price) AND
            ($max_price IS NULL OR h.price <= $max_price) AND
            ($bedrooms IS NULL OR h.bedrooms = $bedrooms) AND
            ($baths IS NULL OR h.baths = $baths) AND
            ($sqftLiving IS NULL OR h.sqft_living >= $sqftLiving) AND
            ($sqftLot IS NULL OR h.sqft_lot >= $sqftLot) AND
            ($floors IS NULL OR h.floors = $floors) AND
            ($condition IS NULL OR h.condition = $condition) AND
            ($sqftBasement IS NULL OR h.sqft_basement = $sqftBasement) AND
            ($yrBuilt IS NULL OR h.yr_built >= $yrBuilt) AND
            ($yrRenovated IS NULL OR h.yr_renovated >= $yrRenovated)
            MATCH (h)-[:LOCATED_ON]->(s:Street)
            WHERE
            ($street IS NULL OR s.name = $street)
            MATCH (h)-[:LOCATED_IN]->(c:City)
            WHERE
            ($city IS NULL OR c.name = $city)
            RETURN h, s, c
            LIMIT $limit
        """

        # Query the database with parameters
        query_response = self.graph.query(match_query, match_dict)
        return query_response

    @staticmethod
    def process_query_response(cypher_response):
        """
        This function processes the query response and returns response that is more understandable by the final LLM.
        :param cypher_response: A string containing the mapping information of each value to entities in the database.
        :return: Result from the query response that is organised in easy to grasp string.
        """
        result = ""

        if cypher_response:
            for record in cypher_response:
                house = record.get('h', None)
                street_info = record.get('s', None)
                city_info = record.get('c', None)

                street_name = street_info['name'] if street_info else "N/A"
                city_name = city_info['name'] if city_info else "N/A"

                result += (
                    f"House found: Price of the house: {house['price']}, Number of bedrooms: {house['bedrooms']}, "
                    f"Number of bathrooms: {house['baths']}, Square footage of living space: {house['sqft_living']}, "
                    f"Total area of the land : {house['sqft_lot']} ft, Number of floors: {int(house['floors'])}, "
                    f"Condition: {house['condition']}, Area of the basement: {house['sqft_basement']} ft, "
                    f"Year Built: {house['yr_built']}, Year Renovated: {house['yr_renovated']}, "
                    f"Street: {street_name}, City: {city_name}\n"
                )
        else:
            result += "No matching house found in the database.\n"
        return result

    def home_app_response(self, user_criteria):
        """This function executes all functionality of the Neo4jChain class"""
        question_attributes = self.get_question_attributes(user_criteria)
        query_response = self.map_to_database(question_attributes)
        processed_query_response = self.process_query_response(query_response)

        return processed_query_response
