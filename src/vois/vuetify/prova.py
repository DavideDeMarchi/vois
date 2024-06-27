
import sys
print(dir(sys.modules[__name__]))
print(globals())
print(sys.path)

from vois.vuetify.Button import button

b = button()



