# Copyright 2021 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from scripts.config import Config
from scripts.deploy_contract import deploy
from scripts.score import Score
from tests import TestBase


class TestIRC31Metadata(TestBase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config = Config(*cls.getLocalEnvs())
        cls.owner = config.owner
        cls.tx_handler = config.tx_handler
        cls.score = Score(cls.tx_handler, deploy(config, 'multi_token'))

    def test_metadata(self):
        _id = self.getTokenId()
        _uri = f'http://nft.info/{_id}'
        params = {
            '_id': _id,
            '_supply': 100,
            '_uri': _uri
        }
        tx_hash = self.score.invoke(self.owner, 'mint', params)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # check tokenURI
        params2 = {
            '_id': _id
        }
        result = self.score.call('tokenURI', params2)
        self.assertEqual(_uri, result)

        # invoke setTokenURI
        _uri += '_updated'
        params3 = {
            '_id': _id,
            '_uri': _uri
        }
        tx_hash = self.score.invoke(self.owner, 'setTokenURI', params3)
        tx_result = self.tx_handler.ensure_tx_result(tx_hash)
        self.assertSuccess(tx_result['status'])

        # check updated URI
        result = self.score.call('tokenURI', params2)
        self.assertEqual(_uri, result)
