from IPython.display import display


class Test_sliderFloat:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import sliderFloat, settings

            settings.color_first = 'green'

            my_slider_1 = sliderFloat.sliderFloat(value=1.8,
                                                  minvalue=1.0,
                                                  maxvalue=3.0,
                                                  text='Select',
                                                  showpercentage=False,
                                                  decimals=2,
                                                  maxint=None,
                                                  labelwidth=150,
                                                  sliderwidth=200,
                                                  resetbutton=False,
                                                  showtooltip=False,
                                                  onchange=None,
                                                  color=None,
                                                  editable=False,
                                                  editableWidth=90)

            my_slider_2 = sliderFloat.sliderFloat(value=3.8,
                                                  minvalue=0.0,  # Tested
                                                  maxvalue=5.0,  # Tested
                                                  text='Select Value',  # Tested
                                                  showpercentage=False,
                                                  decimals=3,  # Tested
                                                  maxint=None,
                                                  labelwidth=50,  # Tested
                                                  sliderwidth=100,  # Tested
                                                  resetbutton=True,  # Tested
                                                  showtooltip=True,  # Tested
                                                  onchange=None,
                                                  color='red',  # Tested
                                                  editable=False,
                                                  editableWidth=90)

            display(my_slider_1.draw())
            display(my_slider_2.draw())

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()

        my_switch_1_sel = sliders[1]
        my_slider_2_sel = sliders[4]

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_slider_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        # TODO
        pass
        # def kernel_code():
        #     import sys
        #     sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')
        #
        #     import warnings
        #     warnings.filterwarnings("ignore")
        #
        #     from vois.vuetify import sliderFloat
        #
        #     def on_change(value):
        #         my_slider_1.color = 'green'
        #         assert my_slider_1.value == value == 1
        #
        #     my_slider_1 = sliderFloat.sliderFloat(value=3.8,
        #                                           minvalue=0.0,  # Tested
        #                                           maxvalue=5.0,  # Tested
        #                                           text='Select Value',  # Tested
        #                                           showpercentage=False,
        #                                           decimals=3,  # Tested
        #                                           maxint=None,
        #                                           labelwidth=100,  # Tested
        #                                           sliderwidth=100,  # Tested
        #                                           resetbutton=True,  # Tested
        #                                           showtooltip=True,  # Tested
        #                                           onchange=on_change,
        #                                           color='red',  # Tested
        #                                           editable=False,
        #                                           editableWidth=90)
        #
        #     display(my_slider_1.draw())
        #
        # ipywidgets_vois_runner(kernel_code)
        #
        # switches = page_session.locator(".v-application--wrap").all()
        # my_switch_1_sel = switches[1]
        #
        # assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
        #
        # my_slider_1 = page_session.locator(".v-slider__thumb")
        # my_slider_1.wait_for()
        #
        # my_slider_1.click()
        #
        # assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='2')
        #
        # left = page_session.locator(".v-btn").first
        # left.wait_for()
        #
        # box = left.bounding_box()
        #
        # x_real = box['x'] + box['width'] / 2
        # y_real = box['y'] + box['height'] / 2
        #
        # # page_session.mouse.move(x_real, y_real)
        # page_session.mouse.click(x_real, y_real)
        # page_session.mouse.dblclick(x_real, y_real)
        # # page_session.mouse.up()
        #
        # assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='3')
        #
        #
        #
        # # right.wait_for()
        # reset = page_session.get_by_role("button").nth(2)
        # reset.wait_for()
        #
        # # left.click()
        #
        #
        #
        # reset.click()
        # assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='4')


class Test_SliderFloat:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import SliderFloat, settings

            settings.color_first = 'green'

            my_slider_1 = SliderFloat(value=1.8,
                                      min_value=1.0,
                                      max_value=3.0,
                                      text='Select',
                                      show_percentage=False,
                                      decimals=2,
                                      max_int=None,
                                      label_width=150,
                                      slider_width=200,
                                      reset_button=False,
                                      show_tooltip=False,
                                      on_change=None,
                                      color=None,
                                      editable=False,
                                      editable_width=90)

            my_slider_2 = SliderFloat(value=3.8,
                                      min_value=0.0,  # Tested
                                      max_value=5.0,  # Tested
                                      text='Select Value',  # Tested
                                      show_percentage=False,
                                      decimals=3,  # Tested
                                      max_int=None,
                                      label_width=50,  # Tested
                                      slider_width=100,  # Tested
                                      reset_button=True,  # Tested
                                      show_tooltip=True,  # Tested
                                      on_change=None,
                                      color='red',  # Tested
                                      editable=False,
                                      editable_width=90)

            display(my_slider_1)
            display(my_slider_2)

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()

        my_switch_1_sel = sliders[1]
        my_slider_2_sel = sliders[4]

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_slider_2_sel.screenshot(animations='disabled'), postfix='2')
