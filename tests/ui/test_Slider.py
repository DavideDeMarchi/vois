from IPython.display import display


class Test_slider:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import slider, settings

            my_slider_1 = slider.slider(selectedvalue=51,
                                        minvalue=0,
                                        maxvalue=100,
                                        vertical=False,
                                        color=settings.color_first,
                                        onchange=None,
                                        height=150,
                                        width=None,
                                        step=1.0
                                        )

            my_slider_2 = slider.slider(selectedvalue=99.5,  #Tested
                                        minvalue=0,
                                        maxvalue=100,
                                        vertical=True, #Tested
                                        color=settings.color_first,
                                        onchange=None,
                                        height=350, #Tested
                                        width=None,
                                        step=0.5 # Tested
                                        )


            display(my_slider_1.draw())
            display(my_slider_2.draw())

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()

        my_slider_1_sel = sliders[1]
        my_slider_2_sel = sliders[2]

        assert_vois_compare_image(image=my_slider_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_slider_2_sel.screenshot(animations='disabled'), postfix='2')


    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():

            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import slider, settings

            def on_change(value):
                my_slider_1.slider.color = 'red'

            my_slider_1 = slider.slider(selectedvalue=0,
                                        minvalue=-50,
                                        maxvalue=50,
                                        vertical=False,
                                        color=settings.color_first, # Tested
                                        onchange=on_change,
                                        height=150,
                                        width=None,
                                        step=1.5
                                        )

            display(my_slider_1.draw())

        ipywidgets_vois_runner(kernel_code)

        sliders = page_session.locator(".v-application--wrap").all()
        my_slider_1_sel = sliders[1]

        my_slider_1 = page_session.locator(".v-slider__thumb-label")
        my_slider_1.wait_for()
        box = my_slider_1.bounding_box()

        x_real = box['x'] + box['width'] / 2
        y_real = box['y'] + box['height'] / 2

        page_session.mouse.move(x_real, y_real)
        page_session.mouse.down()
        page_session.mouse.move(x_real - 100, y_real)
        page_session.mouse.up()

        assert_vois_compare_image(image=my_slider_1_sel.screenshot(animations='disabled'), postfix='1')

