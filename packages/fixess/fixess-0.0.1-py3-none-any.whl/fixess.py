import time
import requests

class Fixess():
  def __init__(self, api_key):
    self._api_key = api_key

  def keys(self):
    return self._post(cmd='keys')

  def values(self):
    return self._post(cmd='values')

  def items(self):
    return list(zip(*(self.keys(), self.values())))

  def __delitem__(self, key):
    return self._post(cmd='__delitem__',
                      key=key)

  def __len__(self):
    return self._post(cmd='__len__')

  def __str__(self):
    return str(self._post(cmd='__str__'))

  def __getitem__(self, key):
    return self.get(key)

  def __setitem__(self, key, value):
    self.set(key, value)

  def __contains__(self, key):
    return self._post(cmd='__contains__',
                      key=key)

  def get(self, key, default=None, temperature=1.0, batch=False):
    return self._post(
        cmd='get',
        key=key,
        default=default,
        temperature=temperature,
        batch=batch)

  def get_training_status(self):
    return self._post(cmd='get_training_status')

  def clear(self, fit=True):
    if fit:
      remaining_training_time = 1
      while remaining_training_time > 0:
        training_status = self.get_training_status()
        print(training_status)
        remaining_training_time = training_status.get('time_left', 0)
        exception = training_status.get('exception', None)
        if exception:
          print(exception)
          assert False, exception
        time.sleep(remaining_training_time)
    result = self._post(cmd='clear',
                        fit=False)
    print(self._post(cmd='__str__'))
    assert isinstance(len(self), int), len(self)
    assert len(self) == 0, self.keys()
    return result

  def set(self, key, value, batch=False):
    return self._post(cmd='set',
                      key=key,
                      value=value,
                      batch=batch)

  def _getitem(self, key):
    return self.get(key)

  def _setitem(self, key, value):
    return self.set(key, value)

  def _post(self, cmd, **kwargs):
    assert isinstance(cmd, str), cmd
    args = {
      'cmd': cmd
    }
    headers = {
        'x-rapidapi-host': "fixess.p.rapidapi.com",
        'x-rapidapi-key': self._api_key
    }
    for key, value in kwargs.items():
      args[key] = value
    response = requests.post('https://fixess.p.rapidapi.com',
                             json=args,
                             headers=headers)
    response.raise_for_status()
    return response.json()
