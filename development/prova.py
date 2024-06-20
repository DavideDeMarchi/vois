from vois.vuetify.utils.util import deprecated_init_alias

from ipyvuetify import VuetifyTemplate

from .VuetifyWidget import VuetifyWidget

class Edo:

    @deprecated_init_alias(mio='MIO')
    def __init__(self, MIO):
        self.MIO = MIO

    @property
    def mio(self):
        return self.MIO

    @mio.setter
    def mio(self, val):
        self.MIO = val

edo = Edo(mio=123)

print('Old {} - New {}'.format(edo.mio, edo.MIO))
# print(edo.mio)

edo.mio = 12

edo.mio = 24

print(edo.mio)

print('Old {} - New {}'.format(edo.mio, edo.MIO))

ele = Edo(mio=111)
print('Old {} - New {}'.format(ele.mio, ele.MIO))
ele.MIO = 990



print('Old {} - New {}'.format(ele.mio, ele.MIO))
print('Old {} - New {}'.format(edo.mio, edo.MIO))

# edo.edo = 90
# print(edo.ele)
