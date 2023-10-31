import json
import cachetools
from botocore.client import Config
from s1crets.core import DictQuery
from s1crets.providers.base import BaseProvider, DefaultValue, args_cache_key
from s1crets.providers.aws.base import ServiceWrapper


@cachetools.cached(cache={}, key=args_cache_key)
class SecretProvider(BaseProvider):
    def __init__(self, sts_args={}, cache_args={}, retry=3, timeout=5, **kwargs):
        config = Config(connect_timeout=timeout, read_timeout=timeout,
                        retries={'total_max_attempts': retry})
        self.sm = ServiceWrapper('secretsmanager', boto_config=config, **sts_args)
        
        super().__init__(sts_args=sts_args, cache_args=cache_args)

    def _get_secret_value(self, secret, path, keypath=None, default=DefaultValue):
        if 'SecretBinary' in secret:
            return secret['SecretBinary']
        data = secret['SecretString']
        try:
            # secrets in Secret Manager are mostly a JSON, try to parse it
            data = json.loads(data)
        except Exception:
            pass
        else:
            if keypath:
                val = DictQuery(data).get(keypath, default)
                if val is DefaultValue:
                    raise KeyError(path, keypath)
                else:
                    return val
        return data

    def get(self, path, keypath=None, default=DefaultValue, cached=True, **kwargs):
        if cached:
            try:
                res = self.cache.get('keys', path)
            except KeyError:
                # not in cache
                pass
            else:
                return self._get_secret_value(res, path, keypath, default)

        try:
            res = self.sm.get_secret_value(SecretId=path)
            self.cache.set('keys', path, res)
        except self.sm.exceptions.ResourceNotFoundException:
            raise KeyError(path)

        return self._get_secret_value(res, path, keypath, default)

    def get_by_path(self, path, cached=True, **kwargs):
        secrets = {}
        kwargs = {}
        while True:
            r = self.sm.list_secrets(
                Filters=[{'Key': 'name', 'Values': [path]}],
                **kwargs
            )
            for s in r.get('SecretList', []):
                secrets[s['Name']] = None

            if 'NextToken' not in r or r['NextToken'] is None:
                # we've got all secrets
                break
            # set the next token
            kwargs['NextToken'] = r['NextToken']
        for k in secrets.keys():
            secrets[k] = self.get(k, cached=True, **kwargs)
        return secrets

    def update(self, path, value):
        # get the current secret in order to see its type
        secret = self.sm.get_secret_value(SecretId=path)
        if 'SecretBinary' in secret:
            kwargs = {'SecretBinary': value}
        else:
            kwargs = {'SecretString': value}

        self.sm.put_secret_value(SecretId=path, **kwargs)
        # remove path from the key_cache
        try:
            self.cache.delete('keys', path)
        except KeyError:
            pass

    def path_exists(self, path, keypath=None, cached=True, **kwargs):
        try:
            self.get(path, keypath)
            return True
        except KeyError:
            return False
