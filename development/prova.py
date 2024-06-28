from vois.vuetify.utils.util import deprecated_init_alias, create_deprecated_alias, create_deprecated_alias_2


#
# from ipyvuetify import VuetifyTemplate
#
#
class Edo:

    deprecation_alias = dict(textcolor='text_color', iconcolor='icon_color')

    @deprecated_init_alias(**deprecation_alias)
    def __init__(self, text_color, icon_color, ciao):

        self.text_color = text_color
        self.icon_color = icon_color

        create_deprecated_alias_2(self, self.deprecation_alias)
        for alias, new in self.deprecation_alias.items():
            create_deprecated_alias(self, alias, new)
        # create_deprecated_alias(self, 'iconcolor', 'icon_color')
        print(self.text_color, self.textcolor)
        # print(dir(self))

        # print(dir(self))

    # @property
    # def mio(self):
    #     return self.MIO
    #
    # @mio.setter
    # def mio(self, val):
    #     self.MIO = val
#
#
# edo = Edo(textcolor=123, ciao=100, iconcolor='pink')
#
# print('Old {} - New {}'.format(edo.textcolor, edo.text_color))
# print('Old {} - New {}'.format(edo.iconcolor, edo.icon_color))
#
# edo.textcolor = 12
# edo.iconcolor = 'green'
#
# print('Old {} - New {}'.format(edo.textcolor, edo.text_color))
# print('Old {} - New {}'.format(edo.iconcolor, edo.icon_color))
#
# edo.text_color = 99
# edo.icon_color = 'red'
#
# print('Old {} - New {}'.format(edo.textcolor, edo.text_color))
# print('Old {} - New {}'.format(edo.iconcolor, edo.icon_color))

from vois.vuetify import button

btn = button.button(text='edoardo', iconcolor='red')

print('fuori', btn.iconcolor, btn.icon_color)
# print('id', id(btn))
