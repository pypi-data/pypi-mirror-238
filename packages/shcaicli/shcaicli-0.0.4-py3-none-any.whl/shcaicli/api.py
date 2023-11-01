from shcaicli.shcai_exc import SHCAIException
import requests
import json


def _shc_infer_content_gen(json_str: str):
  cn_content = json.loads(json_str)
  yield cn_content


class SHCAi:
  def __init__(self,
               api_root: str = 'https://apim.ihealthgroup.tec.br/api',
               api_name: str = 'shc-mtask',
               api_version: str = 'v1',
               api_key: str = None
               ):
    self._api_root = api_root
    self._api_name = api_name[1:] if api_name.startswith('/') else api_name
    self.api_version = api_version
    self.api_key = api_key

  def infer(self, cn: str = None):
    if cn is None or cn.strip() == '':
      raise ValueError('invalid value for cn parameter')

    headers = {
      'Content-Type': 'application/json',
      'X-Gravitee-Api-Key': self.api_key,
    }
    url = f'{self._api_root}/{self._api_name}'
    data = {
      'text': cn
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
      return _shc_infer_content_gen(response.text)
    else:
      raise SHCAIException(f'Request failed with status code {response.status_code}. Response: {response.text}')
