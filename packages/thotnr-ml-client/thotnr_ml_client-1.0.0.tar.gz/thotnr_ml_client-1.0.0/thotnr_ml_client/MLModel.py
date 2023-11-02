from thotnr_ml_client.GraphQlWebClient import GraphQlWebClient
from thotnr_ml_client.ConfigurationManager import ConfigurationManager


class MLModel:
    def __init__(self):
        self._config_manager = ConfigurationManager()
        self._graphql_web_client = GraphQlWebClient(self._config_manager)
        self._graphql_web_client.refresh_token()

    def register_model(self, s3_path, model_metadata, is_active):
        is_active_string = "true" if is_active else "false"
        ml_code = self._config_manager.get_ml_code()
        group_id = self._config_manager.get_current_group_id()

        input_string = (
            f's3Path:"{s3_path}",'
            f'groupId:"{group_id}",'
            f'modelMetadata:"{model_metadata}",'
            f'isActive:{is_active_string},'
            f'mlCode:"{ml_code}"'
        )

        agi_id = self._config_manager.get_current_agi_id()
        query = (
            f'mutation {{ createMlModel{agi_id}_api (input: {{MlModel{agi_id}_api: {{ {input_string} }} }}) {{ '
            f'MlModel{agi_id}_api {{ s3Path, groupId, modelMetadata, isActive, mlCode, created_on }} }} }}'
        )
        return self._graphql_web_client.query(query, "mutation")

    def get_current_active_model(self):
        ml_code = self._config_manager.get_ml_code()
        group_id = self._config_manager.get_current_group_id()
        agi_id = self._config_manager.get_current_agi_id()

        query = f"""
                query MyQuery {{
                    MlModel{agi_id}_api (
                        filter: {{
                            groupId: {{equalTo: "{group_id}"}},
                            and: {{
                                mlCode: {{equalTo: "{ml_code}"}},
                                and: {{isActive: {{equalTo: true}}}}
                            }}
                        }},
                        first: 1
                    ) {{
                        nodes {{
                            s3Path, groupId, modelMetadata, isActive, mlCode, created_on
                        }}
                    }}
                }}
            """

        return self._graphql_web_client.query(query, "query")


if __name__ == '__main__':
    ml_model = MLModel()
    print(ml_model.get_current_active_model())
    # ml_model.register_model(s3_path="abc", model_metadata="cde", is_active=False)
