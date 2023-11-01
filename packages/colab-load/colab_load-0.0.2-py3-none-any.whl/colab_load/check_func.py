import os

class CheckValue:

    def _check_url(self, url):
        if not isinstance(url, str):
            raise TypeError('url is not str')
        elif not url.startswith("https://"):
            raise TypeError('the url does not start with - https://')

        return url

    def _check_count(self, c):
        if not isinstance(c, int):
            raise TypeError('count is not int')
        elif c <= 0:
            raise ValueError('count must be greater than 0')
        else:
            return c

    def _check_dir(self, save_dir):
        if not isinstance(save_dir, str):
            raise TypeError('save_dir is not str')
        else:
            try:
                os.mkdir(save_dir)
                return save_dir
            except:
                return save_dir