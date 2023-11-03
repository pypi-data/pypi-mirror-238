from agentive.utils.evaluation.distance import cosine_similarity

import pandas as pd


class LocalVectorTools:
    def __init__(self, llm):
        self.llm = llm
        self.tools = pd.DataFrame(columns=['name', 'description', 'parameters', 'embeddings'])

    def add_tool(self, name, description, parameters):
        tool = {
            'name': name,
            'description': description,
            'parameters': parameters,
            'embeddings': self.llm.embed(f'{name} {description} {parameters}')
        }

        self.tools = pd.concat([self.tools, pd.DataFrame([tool])], ignore_index=True)

    def get_tools(self):
        """Returns all tools in the toolkit as a list of dictionaries"""
        return self._format_tools(self.tools.to_dict(orient='records'))

    def get_tool(self, name):
        tool = self.tools[self.tools['name'] == name].to_dict(orient='records')
        return self._format_tools(tool)[0]

    @staticmethod
    def _format_tools(tools):
        return [
            {
                'name': tool['name'],
                'description': tool['description'],
                'parameters': tool['parameters']
            }
            for tool in tools
        ]

    def search_tools(self, query, n=5):
        if self.tools.empty:
            return []

        similarities = self.tools['embeddings'].apply(lambda x: cosine_similarity(x, self.llm.embed(query)))
        tools = self.tools.iloc[similarities.nlargest(n).index].to_dict(orient='records')
        return self._format_tools(tools)

