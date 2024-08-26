from IPython.display import display


class Test_colorPicker:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import colorPicker, settings

            my_color_1 = colorPicker.colorPicker(color="#00FF00",  # Tested
                                                 dark=settings.dark_mode,
                                                 width=40,
                                                 height=30,
                                                 rounded=False,
                                                 canvas_height=100,
                                                 show_canvas=True,  # Tested
                                                 show_mode_switch=True,
                                                 show_inputs=False,  # Tested
                                                 show_swatches=False,  # Tested
                                                 swatches_max_height=164,
                                                 text='Color1',  # Tested
                                                 textweight=400,
                                                 onchange=None,
                                                 argument=None,
                                                 offset_x=False,
                                                 offset_y=True,
                                                 disabled=False)

            my_color_2 = colorPicker.colorPicker(color="#FF0000",  # tested
                                                 dark=settings.dark_mode,
                                                 width=200,  # tested
                                                 height=80,  # tested
                                                 rounded=True,  # Tested
                                                 canvas_height=300,  # Tested
                                                 show_canvas=True,
                                                 show_mode_switch=True,
                                                 show_inputs=True,
                                                 show_swatches=True,
                                                 swatches_max_height=200,  # Tested
                                                 text='Color2',  # Tested
                                                 textweight=900,  # Tested
                                                 onchange=None,
                                                 argument=None,
                                                 offset_x=False,
                                                 offset_y=True,
                                                 disabled=False)

            display(my_color_1.draw())
            display(my_color_2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_color_1_locator = page_session.get_by_role("button", name='Color1')
        my_color_1_locator.wait_for()

        assert_vois_compare_image(image=my_color_1_locator.screenshot(animations='disabled'), postfix='1')

        my_color_1_locator.click()

        canvas_1_locator = page_session.locator('canvas').locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'), postfix='1_canvas')

        # To remove overlay old canvas
        page_session.mouse.click(0, 0)

        my_color_2_locator = page_session.get_by_role("button", name='Color2')
        my_color_2_locator.wait_for()

        assert_vois_compare_image(image=my_color_2_locator.screenshot(animations='disabled'), postfix='2')

        my_color_2_locator.click()

        canvas_2_locator = page_session.locator("canvas").nth(1).locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        assert_vois_compare_image(image=canvas_2_locator.screenshot(animations='disabled'), postfix='2_canvas')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import colorPicker
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change(arg):
                with output:
                    print(my_color_1.color)

            my_color_1 = colorPicker.colorPicker(color="#00FF00",  # Tested
                                                 canvas_height=300,
                                                 argument='edo',
                                                 onchange=on_change,
                                                 text='Color3')

            display(my_color_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_color_1_locator = page_session.get_by_role("button", name='Color3')
        my_color_1_locator.wait_for()

        my_color_1_locator.click()

        canvas_1_locator = page_session.locator('canvas').locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        path_before = assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'),
                                                postfix='1_before')

        canvas_1_locator.click(position={'x': 50, 'y': 50})

        path_after = assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'),
                                               postfix='1_after')

        assert_vois_path_images(image1=path_before,
                                image2=path_after,
                                differ=True)

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='2')


class Test_ColorPicker:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import ColorPicker, settings

            my_color_1 = ColorPicker(color="#00FF00",  # Tested
                                     dark=settings.dark_mode,
                                     width=40,
                                     height=30,
                                     rounded=False,
                                     canvas_height=100,
                                     show_canvas=True,  # Tested
                                     show_mode_switch=True,
                                     show_inputs=False,  # Tested
                                     show_swatches=False,  # Tested
                                     swatches_max_height=164,
                                     text='Color1',  # Tested
                                     text_weight=400,
                                     on_change=None,
                                     argument=None,
                                     offset_x=False,
                                     offset_y=True,
                                     disabled=False)

            my_color_2 = ColorPicker(color="#FF0000",  # tested
                                     dark=settings.dark_mode,
                                     width=200,  # tested
                                     height=80,  # tested
                                     rounded=True,  # Tested
                                     canvas_height=300,  # Tested
                                     show_canvas=True,
                                     show_mode_switch=True,
                                     show_inputs=True,
                                     show_swatches=True,
                                     swatches_max_height=200,  # Tested
                                     text='Color2',  # Tested
                                     text_weight=900,  # Tested
                                     on_change=None,
                                     argument=None,
                                     offset_x=False,
                                     offset_y=True,
                                     disabled=False)

            display(my_color_1)
            display(my_color_2)

        ipywidgets_vois_runner(kernel_code)

        my_color_1_locator = page_session.get_by_role("button", name='Color1')
        my_color_1_locator.wait_for()

        assert_vois_compare_image(image=my_color_1_locator.screenshot(animations='disabled'), postfix='1')

        my_color_1_locator.click()

        canvas_1_locator = page_session.locator('canvas').locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'), postfix='1_canvas')

        # To remove overlay old canvas
        page_session.mouse.click(0, 0)

        my_color_2_locator = page_session.get_by_role("button", name='Color2')
        my_color_2_locator.wait_for()

        assert_vois_compare_image(image=my_color_2_locator.screenshot(animations='disabled'), postfix='2')

        my_color_2_locator.click()

        canvas_2_locator = page_session.locator("canvas").nth(1).locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        assert_vois_compare_image(image=canvas_2_locator.screenshot(animations='disabled'), postfix='2_canvas')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import ColorPicker
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change(arg):
                with output:
                    print(my_color_1.color)

            my_color_1 = ColorPicker(color="#00FF00",  # Tested
                                     canvas_height=300,
                                     argument='edo',
                                     on_change=on_change,
                                     text='Color3')

            display(my_color_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_color_1_locator = page_session.get_by_role("button", name='Color3')
        my_color_1_locator.wait_for()

        my_color_1_locator.click()

        canvas_1_locator = page_session.locator('canvas').locator('..').locator(
            '..')  # get_by_role("menu").locator("canvas")

        path_before = assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'),
                                                postfix='1_before')

        canvas_1_locator.click(position={'x': 50, 'y': 50})

        path_after = assert_vois_compare_image(image=canvas_1_locator.screenshot(animations='disabled'),
                                               postfix='1_after')

        assert_vois_path_images(image1=path_before,
                                image2=path_after,
                                differ=True)

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='2')
