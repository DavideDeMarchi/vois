from IPython.display import display


class Test_radio:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import radio
            from ipywidgets import widgets, Layout

            output = widgets.Output(layout=Layout(width='250px', height='150px'))
            display(output)

            my_radio_1 = radio.radio(index=0,
                                     labels=['A', 'B', 'C'],
                                     tooltips=['AA', 'BB', 'CC'],
                                     color='violet',  # Tested
                                     onchange=None,
                                     row=True)  # Tested

            my_radio_2 = radio.radio(index=0,
                                     labels=['D', 'E', 'F'],
                                     tooltips=[],
                                     color='red',  # Tested
                                     onchange=None,
                                     row=False)  # Tested

            display(my_radio_1.draw())
            display(my_radio_2.draw())

        ipywidgets_vois_runner(kernel_code)

        radio_1_locator = page_session.locator('.v-input__control').first

        radio_1_locator.wait_for()

        assert_vois_compare_image(image=radio_1_locator.screenshot(animations='disabled'), postfix='1')

        radio_A = page_session.get_by_label('A').locator('..')
        radio_A.wait_for()

        parent = page_session.locator("#rendered_cells")

        radio_A.hover()

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='1_tooltip')

        radio_2_locator = page_session.locator('.v-input__control').nth(1)

        radio_2_locator.wait_for()

        assert_vois_compare_image(image=radio_2_locator.screenshot(animations='disabled'), postfix='2')






    def test_change(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import radio
            from ipywidgets import widgets, Layout

            output = widgets.Output(layout=Layout(width='250px', height='150px'))
            display(output)

            my_radio_1 = radio.radio(index=0,
                                     labels=['A', 'B', 'C'],
                                     tooltips=[],
                                     color='violet',  # Tested
                                     onchange=None,
                                     row=True)  # Tested

            display(my_radio_1.draw())

        ipywidgets_vois_runner(kernel_code)

        radio_1_locator = page_session.locator('.v-input__control')

        radio_1_locator.wait_for()

        assert_vois_compare_image(image=radio_1_locator.screenshot(animations='disabled'), postfix='1')
