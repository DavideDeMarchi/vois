from IPython.display import display


class Test_switch:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import switch, settings

            my_switch_1 = switch.switch(flag=0,
                                        label='Ciao',
                                        color='violet',
                                        inset=True,
                                        dense=False,
                                        onchange=None
                                        )

            settings.color_first = 'red'

            my_switch_2 = switch.switch(flag=1,
                                        label='Pippo',
                                        color=None,  # color_first
                                        inset=False,
                                        dense=True,
                                        onchange=None
                                        )

            display(my_switch_1.draw())
            display(my_switch_2.draw())

        ipywidgets_vois_runner(kernel_code)

        switches = page_session.locator(".v-application--wrap").all()

        my_switch_1_sel = switches[1]
        my_switch_2_sel = switches[2]

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_switch_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import switch

            def on_change(value):
                my_switch_1.color = 'green'
                assert my_switch_1.value == value == 1

            my_switch_1 = switch.switch(flag=0,
                                        label='Pippo',
                                        color=None,  # color_first
                                        inset=False,
                                        dense=True,
                                        onchange=on_change
                                        )

            display(my_switch_1.draw())

        ipywidgets_vois_runner(kernel_code)

        switches = page_session.locator(".v-application--wrap").all()
        my_switch_1_sel = switches[1]

        my_slider_1 = page_session.locator(".v-input--selection-controls__ripple")
        my_slider_1.wait_for()

        my_slider_1.click()

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')


class Test_Switch:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Switch, settings

            my_switch_1 = Switch(flag=0,
                                 label='Ciao',
                                 color='violet',
                                 inset=True,
                                 dense=False,
                                 on_change=None
                                 )

            settings.color_first = 'red'

            my_switch_2 = Switch(flag=1,
                                 label='Pippo',
                                 color=None,  # color_first
                                 inset=False,
                                 dense=True,
                                 on_change=None
                                 )

            display(my_switch_1)
            display(my_switch_2)

        ipywidgets_vois_runner(kernel_code)

        switches = page_session.locator(".v-application--wrap").all()

        my_switch_1_sel = switches[1]
        my_switch_2_sel = switches[2]

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_switch_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Switch

            def on_change(value):
                my_switch_1.color = 'green'
                assert my_switch_1.value == value == 1

            my_switch_1 = Switch(flag=0,
                                 label='Pippo',
                                 color=None,  # color_first
                                 inset=False,
                                 dense=True,
                                 on_change=on_change
                                 )

            display(my_switch_1)

        ipywidgets_vois_runner(kernel_code)

        switches = page_session.locator(".v-application--wrap").all()
        my_switch_1_sel = switches[1]

        my_slider_1 = page_session.locator(".v-input--selection-controls__ripple")
        my_slider_1.wait_for()

        my_slider_1.click()

        assert_vois_compare_image(image=my_switch_1_sel.screenshot(animations='disabled'), postfix='1')
