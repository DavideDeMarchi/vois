from IPython.display import display


class Test_rangeSlider:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import rangeSlider, settings

            my_slider_1 = rangeSlider.rangeSlider(selectedminvalue=40,
                                                  selectedmaxvalue=55,
                                                  minvalue=10,
                                                  maxvalue=70,
                                                  color=settings.color_first,
                                                  onchange=None,
                                                  height=150,
                                                  vertical=True)

            my_slider_2 = rangeSlider.rangeSlider(selectedminvalue=1,
                                                  selectedmaxvalue=60,
                                                  minvalue=0,
                                                  maxvalue=70,
                                                  color='red',
                                                  onchange=None,
                                                  height=50,
                                                  vertical=False)

            display(my_slider_1.draw())
            display(my_slider_2.draw())

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()

        my_slider_1_sel = page_session.locator(".v-input__slot").all()[0]
        my_slider_2_sel = sliders[2]

        parent = page_session.locator("#rendered_cells")

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_slider_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import rangeSlider, settings

            def on_change(value):
                my_slider_1.slider.color = 'red'

            my_slider_1 = rangeSlider.rangeSlider(selectedminvalue=1,
                                                  selectedmaxvalue=60,
                                                  minvalue=0,
                                                  maxvalue=70,
                                                  color='blue',
                                                  onchange=on_change,
                                                  height=50,
                                                  vertical=False)

            display(my_slider_1.draw())

        ipywidgets_vois_runner(kernel_code)
        parent = page_session.locator("#rendered_cells")
        sliders = page_session.locator(".v-application--wrap").all()
        my_slider_1_sel = sliders[1]

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='pre')

        my_slider_1 = page_session.locator(".v-slider__thumb-label").all()[0]
        my_slider_1.wait_for()
        box = my_slider_1.bounding_box()

        x_real = box['x'] + box['width'] / 2
        y_real = box['y'] + box['height'] / 2

        page_session.mouse.move(x_real, y_real)
        page_session.mouse.down()
        page_session.mouse.move(x_real + 100, y_real)
        page_session.mouse.up()

        assert_vois_compare_image(image=my_slider_1_sel.screenshot(animations='disabled'), postfix='post')


class Test_RangeSlider:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import RangeSlider, settings

            my_slider_1 = RangeSlider(selected_min_value=40,
                                      selected_max_value=55,
                                      min_value=10,
                                      max_value=70,
                                      color=settings.color_first,
                                      on_change=None,
                                      height=150,
                                      vertical=True)

            my_slider_2 = RangeSlider(selected_min_value=1,
                                      selected_max_value=60,
                                      min_value=0,
                                      max_value=70,
                                      color='red',
                                      on_change=None,
                                      height=50,
                                      vertical=False)

            display(my_slider_1)
            display(my_slider_2)

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()

        my_slider_1_sel = page_session.locator(".v-input__slot").all()[0]
        my_slider_2_sel = sliders[2]

        parent = page_session.locator("#rendered_cells")

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_slider_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import RangeSlider

            def on_change(value):
                my_slider_1.slider.color = 'red'

            my_slider_1 = RangeSlider(selected_min_value=1,
                                      selected_max_value=60,
                                      min_value=0,
                                      max_value=70,
                                      color='blue',
                                      on_change=on_change,
                                      height=50,
                                      vertical=False)

            display(my_slider_1.draw())

        ipywidgets_vois_runner(kernel_code)
        parent = page_session.locator("#rendered_cells")
        sliders = page_session.locator(".v-application--wrap").all()
        my_slider_1_sel = sliders[1]

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='pre')

        my_slider_1 = page_session.locator(".v-slider__thumb-label").all()[0]
        my_slider_1.wait_for()
        box = my_slider_1.bounding_box()

        x_real = box['x'] + box['width'] / 2
        y_real = box['y'] + box['height'] / 2

        page_session.mouse.move(x_real, y_real)
        page_session.mouse.down()
        page_session.mouse.move(x_real + 100, y_real)
        page_session.mouse.up()

        assert_vois_compare_image(image=my_slider_1_sel.screenshot(animations='disabled'), postfix='post')
