from IPython.display import display


class Test_label:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import label, settings

            l1 = label.label(text='Label 1 test long long long long long label',
                             onclick=None,
                             argument=None,
                             disabled=False,
                             textweight=350,
                             height=20,
                             margins=0,
                             margintop=None,
                             icon=None,
                             iconlarge=False,
                             iconsmall=False,
                             iconleft=False,
                             iconcolor='black',
                             tooltip=None,
                             textcolor=None,
                             backcolor=None,
                             dark=settings.dark_mode)

            l2 = label.label(text='Label 2',
                             onclick=None,
                             argument=None,
                             disabled=False,
                             textweight=800,  # Tested
                             height=50,  # Tested
                             margins=10,  # Tested
                             margintop=None,
                             icon='mdi-car-light-high',  # Tested
                             iconlarge=False,
                             iconsmall=False,
                             iconleft=False,
                             iconcolor='red',  # Tested
                             tooltip=None,
                             textcolor='white',  # Tested
                             backcolor='black',  # Tested
                             dark=settings.dark_mode)

            display(l1.draw())
            display(l2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_label_1_locator = page_session.get_by_text("Label 1", exact=False).locator('..').locator('..')
        my_label_1_locator.wait_for()

        my_label_2_locator = page_session.get_by_text("Label 2", exact=False).locator('..').locator('..')
        my_label_2_locator.wait_for()

        assert_vois_compare_image(image=my_label_1_locator.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_label_2_locator.screenshot(animations='disabled'), postfix='2')

        # my_color_1_locator.click()
        #
        # canvas_1_locator = page_session.locator('canvas').locator('..').locator('..')
        #
        # assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'), postfix='1_canvas')
        #
        # # To remove overlay old canvas
        # page_session.mouse.click(0, 0)
        #
        # my_color_2_locator = page_session.get_by_role("button", name='Color2')
        # my_color_2_locator.wait_for()
        #
        # assert_vois_compare_image(image=my_color_2_locator.screenshot(animations='disabled'), postfix='2')
        #
        # my_color_2_locator.click()
        #
        # canvas_2_locator = page_session.locator("canvas").nth(1).locator('..').locator('..')

        # assert_vois_compare_image(image=canvas_2_locator.screenshot(animations='disabled'), postfix='2_canvas')

    def test_click(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import label, settings

            def on_click(value):
                l1.text = 'Label 1 After ' + value

            l1 = label.label(text='Label 1 Before',
                             onclick=on_click,  # Tested
                             argument='ciao',
                             icon='mdi-car-light-high',
                             iconlarge=True,  # Tested
                             iconleft=True, )  # Tested

            display(l1.draw())

        pass

        # TODO the onclick function require already to do the redraw

        # ipywidgets_vois_runner(kernel_code)
        #
        # my_label_1_locator = page_session.get_by_text("Label 1 Before", exact=False)
        # my_label_1_locator.wait_for()
        #
        # assert_vois_compare_image(image=my_label_1_locator.screenshot(animations='disabled'), postfix='before')
        #
        # my_label_1_locator.click()
        #
        # assert_vois_compare_image(image=my_label_1_locator.screenshot(animations='disabled'), postfix='after')

