from IPython.display import display


class Test_toggle:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import toggle, settings

            my_toggle_1 = toggle.toggle(index=1,
                                        labels=['A', 'B', 'C'],
                                        tooltips=[],
                                        icons=[],
                                        onchange=None,
                                        row=True,
                                        width=150,
                                        height=36,
                                        justify='space-between',
                                        rounded=settings.button_rounded,
                                        outlined=False,
                                        colorselected=settings.color_first,
                                        colorunselected=settings.color_second,
                                        dark=settings.dark_mode,
                                        paddingrow=1,
                                        paddingcol=2,
                                        tile=False,
                                        small=False,
                                        xsmall=False,
                                        large=False,
                                        xlarge=False)

            my_toggle_2 = toggle.toggle(index=2,  # Tested
                                        labels=['A2', 'B2', 'C2'],
                                        tooltips=[],
                                        icons=[],
                                        onchange=None,
                                        row=False,  # Tested
                                        width=100,  # Tested
                                        height=50,  # Tested
                                        justify='space-between',
                                        rounded=False,  # Tested
                                        outlined=True,  # Tested
                                        colorselected='red',
                                        colorunselected='blue',
                                        dark=settings.dark_mode,
                                        paddingrow=1,
                                        paddingcol=4,  # Tested
                                        tile=False,
                                        small=False,
                                        xsmall=False,
                                        large=False,
                                        xlarge=False)

            my_toggle_3 = toggle.toggle(index=1,  # Tested
                                        labels=['A3', 'B3', 'C3'],
                                        tooltips=['Tooltip A'],
                                        icons=['mdi-file-word-box-outline', 'mdi-file-word-box', 'mdi-auto-fix'],
                                        # Tested
                                        onchange=None,
                                        row=False,
                                        width=100,
                                        height=50,
                                        justify='start',  # Tested
                                        rounded=False,
                                        outlined=True,
                                        colorselected='red',
                                        colorunselected='blue',
                                        dark=settings.dark_mode,
                                        paddingrow=1,
                                        paddingcol=2,
                                        tile=False,
                                        small=False,
                                        xsmall=False,
                                        large=True,  # Tested
                                        xlarge=False)

            display(my_toggle_1.draw())
            display(my_toggle_2.draw())
            display(my_toggle_3.draw())

        ipywidgets_vois_runner(kernel_code)

        my_toggle_1_sel = page_session.get_by_text('ABC')
        my_toggle_2_sel = page_session.get_by_text('A2B2C2')
        my_toggle_3_sel = page_session.get_by_text('A3B3C3')

        tooltip_sel = page_session.get_by_text('A3')

        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_toggle_2_sel.screenshot(animations='disabled'), postfix='2')
        assert_vois_compare_image(image=my_toggle_3_sel.screenshot(animations='disabled'), postfix='3')

        tooltip_sel.hover()

        assert_vois_compare_image(image=my_toggle_3_sel.screenshot(animations='disabled'), postfix='4')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import toggle, settings

            def onchange(index):
                my_toggle_1.buttons[index].disabled = True
                my_toggle_1.colorunselected = '#00ffdd'

            my_toggle_1 = toggle.toggle(index=1,
                                        labels=['A', 'B', 'C'],
                                        tooltips=[],
                                        icons=[],
                                        onchange=onchange,
                                        row=False,
                                        width=50,
                                        height=50,
                                        justify='space-between',
                                        rounded=settings.button_rounded,
                                        outlined=True,
                                        colorselected=settings.color_first,
                                        colorunselected=settings.color_second,
                                        dark=settings.dark_mode,
                                        paddingrow=1,
                                        paddingcol=2,
                                        tile=False,
                                        small=False,
                                        xsmall=False,
                                        large=False,
                                        xlarge=False)

            display(my_toggle_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_toggle_1_sel = page_session.get_by_text('ABC')
        button_1 = page_session.get_by_text('A')

        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='before')
        button_1.click()
        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='after')


class Test_Toggle:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Toggle, settings

            my_toggle_1 = Toggle(index=1,
                                 labels=['A', 'B', 'C'],
                                 tooltips=[],
                                 icons=[],
                                 on_change=None,
                                 row=True,
                                 width=150,
                                 height=36,
                                 justify='space-between',
                                 rounded=settings.button_rounded,
                                 outlined=False,
                                 color_selected=settings.color_first,
                                 color_unselected=settings.color_second,
                                 dark=settings.dark_mode,
                                 padding_row=1,
                                 padding_col=2,
                                 tile=False,
                                 small=False,
                                 x_small=False,
                                 large=False,
                                 x_large=False)

            my_toggle_2 = Toggle(index=2,  # Tested
                                 labels=['A2', 'B2', 'C2'],
                                 tooltips=[],
                                 icons=[],
                                 on_change=None,
                                 row=False,  # Tested
                                 width=100,  # Tested
                                 height=50,  # Tested
                                 justify='space-between',
                                 rounded=False,  # Tested
                                 outlined=True,  # Tested
                                 color_selected='red',
                                 color_unselected='blue',
                                 dark=settings.dark_mode,
                                 padding_row=1,
                                 padding_col=4,  # Tested
                                 tile=False,
                                 small=False,
                                 x_small=False,
                                 large=False,
                                 x_large=False)

            my_toggle_3 = Toggle(index=1,  # Tested
                                 labels=['A3', 'B3', 'C3'],
                                 tooltips=['Tooltip A'],
                                 icons=['mdi-file-word-box-outline', 'mdi-file-word-box', 'mdi-auto-fix'],
                                 # Tested
                                 on_change=None,
                                 row=False,
                                 width=100,
                                 height=50,
                                 justify='start',  # Tested
                                 rounded=False,
                                 outlined=True,
                                 color_selected='red',
                                 color_unselected='blue',
                                 dark=settings.dark_mode,
                                 padding_row=1,
                                 padding_col=2,
                                 tile=False,
                                 small=False,
                                 x_small=False,
                                 large=True,  # Tested
                                 x_large=False)

            display(my_toggle_1)
            display(my_toggle_2)
            display(my_toggle_3)

        ipywidgets_vois_runner(kernel_code)

        my_toggle_1_sel = page_session.get_by_text('ABC')
        my_toggle_2_sel = page_session.get_by_text('A2B2C2')
        my_toggle_3_sel = page_session.get_by_text('A3B3C3')

        tooltip_sel = page_session.get_by_text('A3')

        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_toggle_2_sel.screenshot(animations='disabled'), postfix='2')
        assert_vois_compare_image(image=my_toggle_3_sel.screenshot(animations='disabled'), postfix='3')

        tooltip_sel.hover()

        assert_vois_compare_image(image=my_toggle_3_sel.screenshot(animations='disabled'), postfix='4')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Toggle, settings

            def onchange(index):
                my_toggle_1.buttons[index].disabled = True
                my_toggle_1.color_unselected = '#00ffdd'

            my_toggle_1 = Toggle(index=1,
                                 labels=['A', 'B', 'C'],
                                 tooltips=[],
                                 icons=[],
                                 on_change=onchange,
                                 row=False,
                                 width=50,
                                 height=50,
                                 justify='space-between',
                                 rounded=settings.button_rounded,
                                 outlined=True,
                                 color_selected=settings.color_first,
                                 color_unselected=settings.color_second,
                                 dark=settings.dark_mode,
                                 padding_row=1,
                                 padding_col=2,
                                 tile=False,
                                 small=False,
                                 x_small=False,
                                 large=False,
                                 x_large=False)

            display(my_toggle_1)

        ipywidgets_vois_runner(kernel_code)

        my_toggle_1_sel = page_session.get_by_text('ABC')
        button_1 = page_session.get_by_text('A')

        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='before')
        button_1.click()
        assert_vois_compare_image(image=my_toggle_1_sel.screenshot(animations='disabled'), postfix='after')
