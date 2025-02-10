from IPython.display import display


class Test_tabs:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import tabs, settings

            my_tab_1 = tabs.tabs(index=0,
                                 labels=['TAB_11', 'TAB_12', 'TAB_13'],
                                 contents=['A1', 'A2', 'A3'],
                                 tooltips=None,
                                 color='red',
                                 dark=settings.dark_mode,
                                 onchange=None,
                                 row=True)

            my_tab_2 = tabs.tabs(index=0,
                                 labels=['TAB_21', 'TAB_22', 'TAB_23', 'TAB_24'],
                                 contents=['A1', 'A2', 'A3', 'A4'],
                                 tooltips=['A1', 'A2', 'A3', 'A4'],
                                 color='blue',
                                 dark=settings.dark_mode,
                                 onchange=None,
                                 row=False)

            display(my_tab_1.draw())
            display(my_tab_2.draw())

        ipywidgets_vois_runner(kernel_code)

        tabs1_locator = page_session.get_by_text('TAB_11').locator('..').locator('..').locator('..').locator('..')

        tab_locator = page_session.get_by_text('TAB_22')
        tabs2_locator = tab_locator.locator('..').locator('..').locator('..').locator('..')
        tab_locator.wait_for()
        tab_locator.hover()

        assert_vois_compare_image(image=tabs1_locator.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=tabs2_locator.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import tabs, settings

            def on_change(value):
                if value == 1:
                    my_tab_1.value = 0
                if value == 2:
                    my_tab_1.disabled = True

            my_tab_1 = tabs.tabs(index=0,
                                 labels=['TAB_11', 'TAB_12', 'TAB_13'],
                                 contents=['A1', 'A2', 'A3'],
                                 tooltips=None,
                                 color='red',
                                 dark=True,
                                 onchange=on_change,
                                 row=True)

            display(my_tab_1.draw())

        ipywidgets_vois_runner(kernel_code)

        tab1_locator = page_session.get_by_text('TAB_12')

        tab2_locator = page_session.get_by_text('TAB_13')

        tabs_locator = tab1_locator.locator('..').locator('..').locator('..').locator('..')

        assert_vois_compare_image(image=tabs_locator.screenshot(animations='disabled'), postfix='pre')

        tab1_locator.wait_for()
        tab1_locator.click()

        assert_vois_compare_image(image=tabs_locator.screenshot(animations='disabled'), postfix='middle')

        tab2_locator.wait_for()
        tab2_locator.click()

        assert_vois_compare_image(image=tabs_locator.screenshot(animations='disabled'), postfix='post')
