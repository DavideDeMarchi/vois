from IPython.display import display


class Test_datePicker:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import datePicker, settings

            my_date_1 = datePicker.datePicker(date='1996-09-19',
                                              label='Date1',
                                              dark=settings.dark_mode,
                                              width=88,
                                              color=settings.color_first,
                                              show_week=False,
                                              onchange=None,
                                              offset_x=False,
                                              offset_y=True,
                                              disabled=False,
                                              mindate=None,
                                              maxdate=None)

            my_date_2 = datePicker.datePicker(date='1996-09-19',
                                              label='Date2',
                                              dark=settings.dark_mode,
                                              width=150,  # Tested
                                              color='red',  # Tested
                                              show_week=True,  # Tested
                                              onchange=None,
                                              offset_x=False,
                                              offset_y=True,
                                              disabled=False,
                                              mindate='1996-09-01',  # Tested
                                              maxdate='1996-09-30')  # Tested

            display(my_date_1.draw())
            display(my_date_2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_label('Date1').locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1')

        my_date_1_locator.click()

        my_date_card_1_locator = page_session.get_by_role('menu')
        my_date_card_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_card_1_locator.screenshot(animations='disabled'), postfix='1_card')

        page_session.mouse.click(0, 0)

        my_date_2_locator = page_session.get_by_label('Date2').locator('..').locator('..').locator('..').locator('..')
        my_date_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_2_locator.screenshot(animations='disabled'), postfix='2')

        my_date_2_locator.click()

        my_date_card_2_locator = page_session.get_by_role('menu')
        my_date_card_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_card_2_locator.screenshot(animations='disabled'), postfix='2_card')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import datePicker
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change():
                with output:
                    print(my_date_1.date)

            my_date_1 = datePicker.datePicker(date='1996-09-19',
                                              label='Ciao',
                                              width=150,
                                              onchange=on_change)

            display(my_date_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_label('Ciao').locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1_before')

        my_date_1_locator.click()

        my_date_card_1_locator = page_session.get_by_role('menu')
        my_date_card_1_locator.wait_for()

        page_session.get_by_role("button", name="26").click()

        page_session.mouse.click(0, 0)

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1_after')

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='2')


class Test_DatePicker:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import DatePicker, settings

            my_date_1 = DatePicker(date='1996-09-19',
                                   label='Date1',
                                   dark=settings.dark_mode,
                                   width=88,
                                   color=settings.color_first,
                                   show_week=False,
                                   onchange=None,
                                   offset_x=False,
                                   offset_y=True,
                                   disabled=False,
                                   mindate=None,
                                   maxdate=None)

            my_date_2 = DatePicker(date='1996-09-19',
                                   label='Date2',
                                   dark=settings.dark_mode,
                                   width=150,  # Tested
                                   color='red',  # Tested
                                   show_week=True,  # Tested
                                   onchange=None,
                                   offset_x=False,
                                   offset_y=True,
                                   disabled=False,
                                   mindate='1996-09-01',  # Tested
                                   maxdate='1996-09-30')  # Tested

            display(my_date_1.draw())
            display(my_date_2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_label('Date1').locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1')

        my_date_1_locator.click()

        my_date_card_1_locator = page_session.get_by_role('menu')
        my_date_card_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_card_1_locator.screenshot(animations='disabled'), postfix='1_card')

        page_session.mouse.click(0, 0)

        my_date_2_locator = page_session.get_by_label('Date2').locator('..').locator('..').locator('..').locator('..')
        my_date_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_2_locator.screenshot(animations='disabled'), postfix='2')

        my_date_2_locator.click()

        my_date_card_2_locator = page_session.get_by_role('menu')
        my_date_card_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_card_2_locator.screenshot(animations='disabled'), postfix='2_card')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import DatePicker
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change():
                with output:
                    print(my_date_1.date)

            my_date_1 = DatePicker(date='1996-09-19',
                                   label='Ciao',
                                   width=150,
                                   onchange=on_change)

            display(my_date_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_label('Ciao').locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1_before')

        my_date_1_locator.click()

        my_date_card_1_locator = page_session.get_by_role('menu')
        my_date_card_1_locator.wait_for()

        page_session.get_by_role("button", name="26").click()

        page_session.mouse.click(0, 0)

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1_after')

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='2')
