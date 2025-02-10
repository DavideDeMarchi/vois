from IPython.display import display


class Test_multiSwitch:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import multiSwitch, settings

            m1 = multiSwitch.multiSwitch(values=[True, False, True],
                                         labels=['A1', 'B1', 'C1'],
                                         tooltips=[],
                                         onchange=None,
                                         dark=settings.dark_mode,
                                         row=True,
                                         width=150,
                                         height=36,
                                         justify='space-between',
                                         rounded=False,
                                         outlined=False,
                                         colorselected=settings.color_first,
                                         colorunselected=settings.color_second,
                                         managedblclick=False,
                                         paddingrow=1,
                                         paddingcol=2,
                                         tile=False,
                                         small=False,
                                         xsmall=False,
                                         large=False,
                                         xlarge=False)

            m2 = multiSwitch.multiSwitch(values=[True, False, False, True],
                                         labels=['A2', 'B2', 'C2', 'D2'],
                                         tooltips=['A2', 'B2', 'C2', 'D2'],
                                         onchange=None,
                                         dark=settings.dark_mode,
                                         row=True,
                                         width=250,
                                         height=50,
                                         justify='space-between',
                                         rounded=False,
                                         outlined=True,
                                         colorselected='blue',
                                         colorunselected='green',
                                         managedblclick=False,
                                         paddingrow=1,
                                         paddingcol=2,
                                         tile=False,
                                         small=True,
                                         xsmall=False,
                                         large=False,
                                         xlarge=False)

            display(m1.draw())
            display(m2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_switch_1_locator = page_session.get_by_role("button", name="A1").locator('..').locator('..').locator('..')
        my_switch_1_locator.wait_for()

        my_multi_2_locator = page_session.get_by_role("button", name="A2")
        my_multi_2_container = my_multi_2_locator.locator('..').locator('..').locator('..')
        my_multi_2_locator.wait_for()

        assert_vois_compare_image(image=my_switch_1_locator.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_multi_2_container.screenshot(animations='disabled'), postfix='2')

        my_multi_2_locator.hover()

        parent = page_session.locator("#rendered_cells")

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='3')




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

            from vois.vuetify import multiSwitch, settings

            from ipywidgets import widgets
            output = widgets.Output()

            display(output)

            def onchange(value):
                with output:
                    print(value)

            m1 = multiSwitch.multiSwitch(values=[True, False, True],
                                         labels=['A1', 'B1', 'C1'],
                                         tooltips=[],
                                         onchange=onchange,
                                         dark=settings.dark_mode,
                                         row=True,
                                         width=150,
                                         height=36,
                                         justify='space-between',
                                         rounded=False,
                                         outlined=False,
                                         colorselected=settings.color_first,
                                         colorunselected=settings.color_second,
                                         managedblclick=False,
                                         paddingrow=1,
                                         paddingcol=2,
                                         tile=False,
                                         small=False,
                                         xsmall=False,
                                         large=False,
                                         xlarge=False)

            display(m1.draw())

        ipywidgets_vois_runner(kernel_code)

        parent = page_session.locator("#rendered_cells")
        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='pre')
        my_multi_2_locator = page_session.get_by_role("button", name="B1")
        my_multi_2_locator.wait_for()

        my_multi_2_locator.click()

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='post')

