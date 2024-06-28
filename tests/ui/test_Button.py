from IPython.display import display


class Test_button:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import button, settings

            my_button_1 = button.button(text='Edoardo1',
                                        onclick=None,
                                        argument=None,
                                        width=150,  # TEST
                                        height=50,  # TEST
                                        selected=False,
                                        disabled=False,
                                        tooltip='',
                                        large=True,  # TEST
                                        xlarge=False,
                                        small=False,
                                        xsmall=False,
                                        outlined=True,  # TEST
                                        textweight=700,  # TEST
                                        href=None,
                                        target=None,
                                        onlytext=False,
                                        textcolor='green',  # TEST
                                        class_="pa-0 ma-0 btn1",
                                        icon=None,
                                        iconlarge=False,
                                        iconsmall=False,
                                        iconleft=False,
                                        iconcolor='black',
                                        autoselect=False,
                                        dark=settings.dark_mode,
                                        rounded=settings.button_rounded,
                                        tile=False,
                                        colorselected=settings.color_first,
                                        colorunselected=settings.color_second,
                                        ondblclick=None
                                        )

            my_button_2 = button.button(text='Edoardo2',
                                        onclick=None,
                                        argument=None,
                                        width=100,
                                        height=36,
                                        selected=False,
                                        disabled=False,
                                        tooltip='',
                                        large=False,
                                        xlarge=False,
                                        small=False,
                                        xsmall=False,  # TEST
                                        outlined=False,
                                        textweight=500,
                                        href=None,
                                        target=None,
                                        onlytext=False,
                                        textcolor=None,
                                        class_="pa-0 ma-0 btn2",
                                        icon=None,
                                        iconlarge=False,
                                        iconsmall=False,
                                        iconleft=False,
                                        iconcolor='black',
                                        autoselect=False,
                                        dark=True,  # TEST
                                        rounded=False,  # TEST
                                        tile=False,
                                        colorselected=settings.color_first,
                                        colorunselected=settings.color_second,
                                        ondblclick=None
                                        )

            my_button_3 = button.button(text='Edoardo',
                                        class_="btn3",
                                        xlarge=True)
            my_button_4 = button.button(text='Edoardo',
                                        class_="btn4",
                                        xlarge=False)

            display(my_button_1.draw())
            display(my_button_2.draw())
            display(my_button_3.draw())
            display(my_button_4.draw())

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo1")
        my_button_1_sel.wait_for()

        my_button_2_sel = page_session.get_by_role("button", name="Edoardo2")
        my_button_2_sel.wait_for()

        my_button_3_sel = page_session.locator(".btn3").locator('.v-btn')
        my_button_3_sel.wait_for()

        my_button_4_sel = page_session.locator(".btn4").locator('.v-btn')
        my_button_4_sel.wait_for()

        assert_vois_bytes_image(image1=my_button_3_sel.screenshot(animations='disabled'),
                                image2=my_button_4_sel.screenshot(animations='disabled'),
                                differ=True)

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_button_2_sel.screenshot(animations='disabled'), postfix='2')
        # assert_vois_compare_image(image=page_session.locator(".v-btn").screenshot(animations='disabled'),
        #                           postfix=1)

    def test_icon(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                  assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import button

            def click():
                my_button_1.iconlarge = False
                my_button_1.iconsmall = True
                my_button_1.iconcolor = 'red'
                my_button_1.setIcon('mdi-menu')

            my_button_1 = button.button(text='Edoardo',
                                        icon='mdi-alpha-e-circle-outline',
                                        class_='pa-0 ma-0 btn1',
                                        iconlarge=True,
                                        iconsmall=False,
                                        onclick=click,
                                        iconcolor='black')

            my_button_2 = button.button(text='Edoardo',
                                        class_='pa-0 ma-0 btn2',
                                        icon='mdi-alpha-e-circle-outline',
                                        iconlarge=False,
                                        iconsmall=True,
                                        onclick=click,
                                        iconcolor='black')

            my_button_3 = button.button(text='Edoardo',
                                        class_='pa-0 ma-0 btn3',
                                        icon='mdi-alpha-e-circle-outline',
                                        iconlarge=False,
                                        iconsmall=False,
                                        onclick=click,
                                        iconcolor='black')

            display(my_button_1.draw())
            display(my_button_2.draw())
            display(my_button_3.draw())

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.locator(".btn1").locator('.v-btn')
        my_button_2_sel = page_session.locator(".btn2").locator('.v-btn')
        my_button_3_sel = page_session.locator(".btn3").locator('.v-btn')
        my_button_1_sel.wait_for()
        my_button_2_sel.wait_for()
        my_button_3_sel.wait_for()

        assert_vois_bytes_image(image1=my_button_1_sel.screenshot(animations='disabled'),
                                image2=my_button_2_sel.screenshot(animations='disabled'),
                                differ=True)
        assert_vois_bytes_image(image1=my_button_2_sel.screenshot(animations='disabled'),
                                image2=my_button_3_sel.screenshot(animations='disabled'),
                                differ=True)

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.click()
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import button

            def on_single_click(text):
                my_button_1.setText(text)

            def on_double_click(*args):
                my_button_1.selected = not my_button_1.selected

            my_button_1 = button.button(text='Edoardo',
                                        argument='Arianna',
                                        onclick=on_single_click,
                                        ondblclick=on_double_click,
                                        colorselected='pink',
                                        colorunselected='blue')

            display(my_button_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo")
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.click()

        my_button_1_sel = page_session.get_by_role("button", name="Arianna")
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='2')

        my_button_1_sel.dblclick()
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='3')

    def test_tooltip(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import button

            my_button_1 = button.button(text='Edoardo',
                                        tooltip='this is a tooltip')

            display(my_button_1.draw())

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo")
        my_button_1_sel.wait_for()

        parent = page_session.locator("#rendered_cells")

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.hover()

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='2')


class Test_Button:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Button, settings

            my_button_1 = Button(text='Edoardo1',
                                 on_click=None,
                                 argument=None,
                                 width=150,  # TEST
                                 height=50,  # TEST
                                 selected=False,
                                 disabled=False,
                                 tooltip='',
                                 large=True,  # TEST
                                 x_large=False,
                                 small=False,
                                 x_small=False,
                                 outlined=True,  # TEST
                                 text_weight=700,  # TEST
                                 href=None,
                                 target=None,
                                 only_text=False,
                                 text_color='green',  # TEST
                                 class_="pa-0 ma-0 btn1",
                                 icon=None,
                                 icon_large=False,
                                 icon_small=False,
                                 icon_left=False,
                                 icon_color='black',
                                 auto_select=False,
                                 dark=settings.dark_mode,
                                 rounded=settings.button_rounded,
                                 tile=False,
                                 color_selected=settings.color_first,
                                 color_unselected=settings.color_second,
                                 on_dblclick=None
                                 )

            my_button_2 = Button(text='Edoardo2',
                                 onclick=None,
                                 argument=None,
                                 width=100,
                                 height=36,
                                 selected=False,
                                 disabled=False,
                                 tooltip='',
                                 large=False,
                                 x_large=False,
                                 small=False,
                                 x_small=False,  # TEST
                                 outlined=False,
                                 text_weight=500,
                                 href=None,
                                 target=None,
                                 only_text=False,
                                 text_color=None,
                                 class_="pa-0 ma-0 btn2",
                                 icon=None,
                                 icon_large=False,
                                 icon_small=False,
                                 icon_left=False,
                                 iconcolor='black',
                                 auto_select=False,
                                 dark=True,  # TEST
                                 rounded=False,  # TEST
                                 tile=False,
                                 color_selected=settings.color_first,
                                 color_unselected=settings.color_second,
                                 on_dblclick=None
                                 )

            my_button_3 = Button(text='Edoardo',
                                 class_="btn3",
                                 x_large=True)
            my_button_4 = Button(text='Edoardo',
                                 class_="btn4",
                                 x_large=False)

            display(my_button_1)
            display(my_button_2)
            display(my_button_3)
            display(my_button_4)

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo1")
        my_button_1_sel.wait_for()

        my_button_2_sel = page_session.get_by_role("button", name="Edoardo2")
        my_button_2_sel.wait_for()

        my_button_3_sel = page_session.locator(".btn3").locator('.v-btn')
        my_button_3_sel.wait_for()

        my_button_4_sel = page_session.locator(".btn4").locator('.v-btn')
        my_button_4_sel.wait_for()

        assert_vois_bytes_image(image1=my_button_3_sel.screenshot(animations='disabled'),
                                image2=my_button_4_sel.screenshot(animations='disabled'),
                                differ=True)

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')
        assert_vois_compare_image(image=my_button_2_sel.screenshot(animations='disabled'), postfix='2')

    def test_icon(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                  assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Button

            def click():
                my_button_1.icon_large = False
                my_button_1.icon_small = True
                my_button_1.icon_color = 'red'
                my_button_1.icon = 'mdi-menu'

            my_button_1 = Button(text='Edoardo',
                                 icon='mdi-alpha-e-circle-outline',
                                 class_='pa-0 ma-0 btn1',
                                 icon_large=True,
                                 icon_small=False,
                                 on_click=click,
                                 icon_color='black')

            my_button_2 = Button(text='Edoardo',
                                 class_='pa-0 ma-0 btn2',
                                 icon='mdi-alpha-e-circle-outline',
                                 icon_large=False,
                                 icon_small=True,
                                 on_click=click,
                                 icon_color='black')

            my_button_3 = Button(text='Edoardo',
                                 class_='pa-0 ma-0 btn3',
                                 icon='mdi-alpha-e-circle-outline',
                                 icon_large=False,
                                 icon_small=False,
                                 on_click=click,
                                 icon_color='black')

            display(my_button_1)
            display(my_button_2)
            display(my_button_3)

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.locator(".btn1").locator('.v-btn')
        my_button_2_sel = page_session.locator(".btn2").locator('.v-btn')
        my_button_3_sel = page_session.locator(".btn3").locator('.v-btn')
        my_button_1_sel.wait_for()
        my_button_2_sel.wait_for()
        my_button_3_sel.wait_for()

        assert_vois_bytes_image(image1=my_button_1_sel.screenshot(animations='disabled'),
                                image2=my_button_2_sel.screenshot(animations='disabled'),
                                differ=True)
        assert_vois_bytes_image(image1=my_button_2_sel.screenshot(animations='disabled'),
                                image2=my_button_3_sel.screenshot(animations='disabled'),
                                differ=True)

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.click()
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='2')

    def test_clicks(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Button

            def on_single_click(text):
                my_button_1.text = text

            def on_double_click(*args):
                my_button_1.selected = not my_button_1.selected

            my_button_1 = Button(text='Edoardo',
                                 argument='Arianna',
                                 on_click=on_single_click,
                                 on_dblclick=on_double_click,
                                 color_selected='pink',
                                 color_unselected='blue')

            display(my_button_1)

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo")
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.click()

        my_button_1_sel = page_session.get_by_role("button", name="Arianna")
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='2')

        my_button_1_sel.dblclick()
        my_button_1_sel.wait_for()

        assert_vois_compare_image(image=my_button_1_sel.screenshot(animations='disabled'), postfix='3')

    def test_tooltip(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Button

            my_button_1 = Button(text='Edoardo',
                                 tooltip='this is a tooltip')

            display(my_button_1)

        ipywidgets_vois_runner(kernel_code)

        my_button_1_sel = page_session.get_by_role("button", name="Edoardo")
        my_button_1_sel.wait_for()

        parent = page_session.locator("#rendered_cells")

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='1')

        my_button_1_sel.hover()

        assert_vois_compare_image(image=parent.screenshot(animations='disabled'), postfix='2')
