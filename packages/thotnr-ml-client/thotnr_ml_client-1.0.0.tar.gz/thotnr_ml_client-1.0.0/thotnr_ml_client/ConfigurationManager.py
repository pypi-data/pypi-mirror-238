import os
import base64
import json


class ConfigurationManager:
    AUTHORIZATION = "Authorization"
    QUERY_PARAM_FOR_APP_INSTANCE_ID = "appInstanceId"
    QUERY_PARAM_BITEMPORAL_PROPS = "biTemporalProps"
    QUERY_PARAM_TIME_LABEL_PROP = "timeLabel"
    QUERY_PARAM_CURRENTLY_EXECUTING_JOB_ID = "currentJobId"
    ML_CODE_PROP = "mlCode"
    GROUP_ID = "groupId"
    AGI_ID = "agiId"
    EP_ID = "epId"

    def __init__(self):
        self._auth_token = ""
        self._json_config = json.loads(os.environ["CONFIG"])
        token_obj = json.loads(base64.b64decode(self._json_config["TOKEN"]).decode("utf-8"))
        self._host_name = token_obj["hostName"]
        self._session_code = self._json_config["sessionCode"]
        self._agiId = str(self._json_config[
                              self.AGI_ID]) if self.AGI_ID in self._json_config else None
        self._token = token_obj["refreshToken"]
        self._bitemporal_props = (
            '"' + str(self._json_config[
                          self.QUERY_PARAM_BITEMPORAL_PROPS]) + '"' if self.QUERY_PARAM_BITEMPORAL_PROPS in self._json_config else None)
        self._time_label = self._json_config[
            self.QUERY_PARAM_TIME_LABEL_PROP] if self.QUERY_PARAM_TIME_LABEL_PROP in self._json_config else None
        self._app_instance_id = str(self._json_config[
                                        self.QUERY_PARAM_FOR_APP_INSTANCE_ID]) if self.QUERY_PARAM_FOR_APP_INSTANCE_ID in self._json_config else None
        self._currently_executing_job_id = str(self._json_config[
                                                   self.QUERY_PARAM_CURRENTLY_EXECUTING_JOB_ID]) if self.QUERY_PARAM_CURRENTLY_EXECUTING_JOB_ID in self._json_config else None
        self._pipeline_conf = self._json_config["cittaAgent"]["launcher"]["pipelineConf"] \
            if "cittaAgent" in self._json_config and "launcher" in self._json_config["cittaAgent"] and "pipelineConf" in \
               self._json_config["cittaAgent"]["launcher"] else None
        self._ml_code = self._pipeline_conf[
            self.ML_CODE_PROP] if self._pipeline_conf is not None and self.ML_CODE_PROP in self._pipeline_conf else None
        self._group_id = str(
            self._pipeline_conf["group"][
                self.GROUP_ID]) if self._pipeline_conf is not None and "group" in self._pipeline_conf and self.GROUP_ID in \
                                   self._pipeline_conf["group"] else None
        self._ep_id = str(
            self._pipeline_conf["execution_profile"][
                self.EP_ID]) if self._pipeline_conf is not None and "execution_profile" in self._pipeline_conf and self.EP_ID in \
                                self._pipeline_conf["execution_profile"] else None

    def get_object_from_app_config(self, key):
        return self._pipeline_conf[key]

    def does_app_config_contain_key(self, key):
        return key in self._pipeline_conf

    def get_object_from_base_config(self, key):
        return self._json_config[key]

    def does_base_config_contain_key(self, key):
        return key in self._json_config

    def get_current_execution_profile_id(self):
        return self._ep_id

    def get_ml_code(self):
        return self._ml_code

    def get_current_time_label(self):
        return self._time_label

    def get_current_bi_temporal_props(self):
        return self._bitemporal_props

    def get_currently_executing_job_id(self):
        return self._currently_executing_job_id

    def get_app_instance(self):
        return self._app_instance_id

    def get_current_group_id(self):
        return self._group_id

    def get_current_agi_id(self):
        return self._agiId

    def get_host_name(self):
        return self._host_name

    def get_session_code(self):
        return self._session_code

    def get_refresh_token(self):
        return self._token

    def get_current_app_instance_id(self):
        return self._app_instance_id
