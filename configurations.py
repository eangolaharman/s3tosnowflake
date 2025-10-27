import os
from datetime import datetime

import pandas as pd


class Config:
    """Load configurations as per the environment variable.
    The Configurations can be further modified at granular level by moving the required variable
    to it's respective environment block.
    """

    def __init__(self):

        start_time = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

        parent_directory = os.path.join(os.path.dirname(__file__), '..')

        # Mapping of lowercase region names to IBP-standard region names
        self.bucket_name = 'channeldataforecastingprod'
        self.aws_region = 'us-east-2'
        self.params = {
            'account': "harman.eu-central-1",
            'user': 'SVC_DEVELOPER_LS_DIBT',
            'private_key': None,
            'warehouse': "DISPLAY_WAREHOUSE",
            'role': "DEVELOPER_LS_DIBT_ROLE",
        }
        self.start_time = start_time
        self.SECRET_NAME = 'prod/Snowflake/DIBT_key'


