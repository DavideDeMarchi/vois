from IPython.display import display


class Test_dayCalendar:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import dayCalendar, settings

            my_date_1 = dayCalendar.dayCalendar(start='1996-09-01',
                                                end='1996-09-30',
                                                color=settings.color_first,  # Color used to highlight the events
                                                dark=settings.dark_mode,
                                                days=[],
                                                show_count=False,
                                                width=340,  # Width on pixels
                                                height=None,  # Height in pixels
                                                on_click=None,
                                                on_click_event=None)

            my_date_2 = dayCalendar.dayCalendar(start='1996-11-01',
                                                end='1996-11-30',
                                                color='pink',  # Tested
                                                dark=True,  # Tested
                                                days=['1996-11-11'],  # Tested
                                                show_count=True,  # Tested
                                                width=400,  # Tested
                                                height=None,  # Tested
                                                on_click=None,
                                                on_click_event=None)

            display(my_date_1.draw())
            display(my_date_2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_role("button", name="Sep").locator('..').locator('..').locator(
            '..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1')

        my_date_2_locator = page_session.get_by_role("button", name="Nov").locator('..').locator('..').locator(
            '..').locator('..')
        my_date_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_2_locator.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import dayCalendar, settings
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change(day):
                my_date_1.color = 'green'

            def on_change_event(day):
                my_date_1.color = 'blue'

            my_date_1 = dayCalendar.dayCalendar(start='1996-09-01',
                                                end='1996-09-30',
                                                color=settings.color_first,  # Color used to highlight the events
                                                dark=settings.dark_mode,
                                                days=['1996-09-19'],
                                                show_count=True,
                                                width=340,  # Width on pixels
                                                height=None,  # Height in pixels
                                                on_click=on_change,
                                                on_click_event=on_change_event)

            display(my_date_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_text("˚")
        calendar_locator = my_date_1_locator.locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='start')

        my_date_1_locator.click()
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='middle')

        my_date_2_locator = page_session.get_by_role("button", name="11")
        my_date_2_locator.dblclick()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='end')


class Test_DayCalendar:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import DayCalendar, settings

            my_date_1 = DayCalendar(start='1996-09-01',
                                    end='1996-09-30',
                                    color=settings.color_first,  # Color used to highlight the events
                                    dark=settings.dark_mode,
                                    days=[],
                                    show_count=False,
                                    width=340,  # Width on pixels
                                    height=None,  # Height in pixels
                                    on_click=None,
                                    on_click_event=None)

            my_date_2 = DayCalendar(start='1996-11-01',
                                    end='1996-11-30',
                                    color='pink',  # Tested
                                    dark=True,  # Tested
                                    days=['1996-11-11'],  # Tested
                                    show_count=True,  # Tested
                                    width=400,  # Tested
                                    height=None,  # Tested
                                    on_click=None,
                                    on_click_event=None)

            display(my_date_1)
            display(my_date_2)

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_role("button", name="Sep").locator('..').locator('..').locator(
            '..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=my_date_1_locator.screenshot(animations='disabled'), postfix='1')

        my_date_2_locator = page_session.get_by_role("button", name="Nov").locator('..').locator('..').locator(
            '..').locator('..')
        my_date_2_locator.wait_for()

        assert_vois_compare_image(image=my_date_2_locator.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image, assert_vois_path_images):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import DayCalendar, settings
            import ipywidgets as widgets

            output = widgets.Output()

            display(output)

            def on_change(day):
                my_date_1.color = 'green'

            def on_change_event(day):
                my_date_1.color = 'blue'

            my_date_1 = DayCalendar(start='1996-09-01',
                                    end='1996-09-30',
                                    color=settings.color_first,  # Color used to highlight the events
                                    dark=settings.dark_mode,
                                    days=['1996-09-19'],
                                    show_count=True,
                                    width=340,  # Width on pixels
                                    height=None,  # Height in pixels
                                    on_click=on_change,
                                    on_click_event=on_change_event)

            display(my_date_1)

        ipywidgets_vois_runner(kernel_code)

        my_date_1_locator = page_session.get_by_text("˚")
        calendar_locator = my_date_1_locator.locator('..').locator('..').locator('..').locator('..')
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='start')

        my_date_1_locator.click()
        my_date_1_locator.wait_for()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='middle')

        my_date_2_locator = page_session.get_by_role("button", name="11")
        my_date_2_locator.dblclick()

        assert_vois_compare_image(image=calendar_locator.screenshot(animations='disabled'), postfix='end')
