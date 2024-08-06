import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
from langchain_community.graphs import Neo4jGraph
from openai import OpenAI

print("Environment variables are loaded:", load_dotenv())


class LoadConfig:
    """
    This class is used to load config files.
    """
    def __init__(self) -> None:
        with open(here("configs/app_config.yml")) as cfg:
            self.app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_llm_configs()
        self.load_graph_db()
        self.load_openai()

    def load_llm_configs(self):
        self.model_name = self.app_config["llm_config"]["model_name"]
        self.temperature = self.app_config["llm_config"]["temperature"]
        self.system_message_extract = self.app_config["llm_config"]["system_message_extract"]
        self.final_system_message = self.app_config["llm_config"]["final_system_message"]
        self.default_message = [(None, "Welcome to the HomeApp! How can I assist you today?")]

    def load_graph_db(self):
        NEO4J_URL = os.environ["NEO4J_URL"]
        NEO4J_USERNAME = os.environ["NEO4J_USERNAME"]
        NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]
        NEO4J_DATABASE = os.environ["NEO4J_DATABASE"]
        self.graph = Neo4jGraph(url=NEO4J_URL, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE)

    def load_openai(self):
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.client = OpenAI(api_key=self.openai_api_key)
