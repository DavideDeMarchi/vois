from vois.vuetify import DatePicker
from vois.vuetify.utils.util import deprecation_class_warning


class datePicker(DatePicker):

    def __init_subclass__(cls, **kwargs):
        deprecation_class_warning(cls.__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        deprecation_class_warning(self.__class__.__name__)
