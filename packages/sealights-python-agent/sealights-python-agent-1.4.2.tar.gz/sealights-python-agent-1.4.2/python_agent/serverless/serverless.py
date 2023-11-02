import logging
import os
import shutil
from urllib.parse import urlparse

from python_agent.common.config_data import ConfigData
from python_agent.utils import disableable
from .lambda_config import LambdaConfig

log = logging.getLogger(__name__)

sealights_layer_path = os.path.join(os.path.dirname(__file__), 'sealights_layer')
sealights_layer_zip_filename = 'sealights_layer.zip'


class Serverless(object):
    def __init__(self, config_data: ConfigData, collectorurl: str, exportlayerpath: str,
                 slconfigpaths: list):
        self.collector_url = collectorurl
        self.config_data = config_data
        self.export_layer_path = exportlayerpath
        self.sl_config_paths = slconfigpaths

    @disableable()
    def execute(self):
        log.info("Starting Sealights lambda configuration setup")
        try:
            self.validate()
        except Exception as e:
            log.exception(str(e))
            return
        if self.export_layer_path is not None:
            self.export_sealights_layer_code()
        else:
            log.info("Skipping Sealights Layer export")

        try:
            self.save_sl_config()
        except Exception as e:
            log.exception(str(e))

        log.info("Sealights lambda configuration setup completed")

    def validate(self):
        if self.collector_url is not None:
            try:
                parsed_collector_url = urlparse(self.collector_url)
                if not parsed_collector_url.scheme or not parsed_collector_url.netloc:
                    raise Exception("Sealights Collector URL is invalid")
            except Exception as e:
                raise Exception(f"Sealgiths Collector URL is invalid, {e}")

    def export_sealights_layer_code(self):
        log.info(
            f"Exporting Sealights lambda layer to {os.path.join(self.export_layer_path, 'sealights_layer')}")
        try:
            if os.path.exists(os.path.join(self.export_layer_path, 'sealights_layer')):
                shutil.rmtree(os.path.join(self.export_layer_path, 'sealights_layer'))

            os.makedirs(self.export_layer_path, exist_ok=True)
            shutil.copytree(sealights_layer_path, os.path.join(self.export_layer_path, 'sealights_layer'))

            return True  # Copy operation successful
        except Exception as e:
            raise Exception(f"Failed to export Sealights Layer code, {e}")

    # def export_sealigths_layer_zip(self):
    #     log.info(f"Exporting Sealights Layer in {self.export_layer_type} format to {self.export_layer_path}")
    #     zip_path = None
    #     try:
    #         temp_dir = '/tmp'
    #         os.makedirs(temp_dir, exist_ok=True)
    #         zip_path = os.path.join(temp_dir, sealights_layer_zip_filename)
    #         with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #             for root, dirs, files in os.walk(sealights_layer_path):
    #                 for file in files:
    #                     file_path = os.path.join(root, file)
    #                     relative_path = os.path.relpath(file_path, sealights_layer_path)
    #                     zipf.write(file_path, arcname=relative_path)
    #
    #         os.makedirs(self.export_layer_path, exist_ok=True)
    #         shutil.copy(zip_path, os.path.join(self.export_layer_path, sealights_layer_zip_filename))
    #
    #         return True
    #     except Exception as e:
    #         raise Exception(f"Failed to export Sealights Layer zip, {e}")
    #     finally:
    #         if os.path.exists(zip_path):
    #             os.remove(zip_path)

    def save_sl_config(self):
        sl_config = LambdaConfig(self.config_data.appName, self.config_data.buildName, self.config_data.branchName,
                                 self.config_data.buildSessionId, self.collector_url)
        for sl_config_path in self.sl_config_paths:
            filepath = os.path.join(sl_config_path, 'sl_lambda_config.json')
            try:
                sl_config.save_to_file(filepath)
                log.info(f"Saving Sealights config file to {sl_config_path}")
            except Exception as e:
                log.exception(f"Failed to save Sealights config file to {sl_config_path}, {e}")
                continue
