# from components.scenes import lobby
#
# lobby.main(2)

from components import logger


@logger.logged_class
class MyClass(object):
    def __init__(self):
        self.logger.debug('hello logger')
        print('adios')


mc = MyClass()

