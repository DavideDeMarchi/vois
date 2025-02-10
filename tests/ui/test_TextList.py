from IPython.display import display


class Test_textlist:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import textlist, settings

            m1 = textlist.textlist(titles=['Name', 'Surname', 'Address', 'Role'],
                                   texts=['Davide', 'De Marchi', 'via Eduardo 34, Roccacannuccia (PE)',
                                          'Software developer'],
                                   titlesbold=['Surname'],
                                   titlefontsize=14,
                                   textfontsize=16,
                                   titlecolumn=3,
                                   textcolumn=10,
                                   titlecolor='#003300',
                                   textcolor='#000000',
                                   lineheightfactor=1.4)

            m2 = textlist.textlist(titles=['Name', 'Surname', 'Address', 'Role'],
                                   texts=['Edoardo', 'Ramalli', 'via ghirlandaio, Firenze',
                                          'Nobody knows'],
                                   titlesbold=['Surname', 'Name'],
                                   titlefontsize=22,
                                   textfontsize=20,
                                   titlecolumn=5,
                                   textcolumn=15,
                                   titlecolor='blue',
                                   textcolor='red',
                                   lineheightfactor=1.8)

            display(m1.draw())
            display(m2.draw())

        ipywidgets_vois_runner(kernel_code)

        my_text_1_locator = page_session.get_by_text("Davide").locator('..').locator('..').locator('..')
        my_text_1_locator.wait_for()

        assert_vois_compare_image(image=my_text_1_locator.screenshot(animations='disabled'), postfix='1')

        my_text_2_locator = page_session.get_by_text("Edoardo").locator('..').locator('..').locator('..')
        my_text_2_locator.wait_for()

        assert_vois_compare_image(image=my_text_2_locator.screenshot(animations='disabled'), postfix='2')


class Test_TextList:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import TextList, settings

            m1 = TextList(titles=['Name', 'Surname', 'Address', 'Role'],
                          texts=['Davide', 'De Marchi', 'via Eduardo 34, Roccacannuccia (PE)',
                                 'Software developer'],
                          titles_bold=['Surname'],
                          title_font_size=14,
                          text_font_size=16,
                          title_column=3,
                          text_column=10,
                          title_color='#003300',
                          text_color='#000000',
                          line_height_factor=1.4)

            m2 = TextList(titles=['Name', 'Surname', 'Address', 'Role'],
                          texts=['Edoardo', 'Ramalli', 'via ghirlandaio, Firenze',
                                 'Nobody knows'],
                          titles_bold=['Surname', 'Name'],
                          title_font_size=22,
                          text_font_size=20,
                          title_column=5,
                          text_column=15,
                          title_color='blue',
                          text_color='red',
                          line_height_factor=1.8)

            display(m1)
            display(m2)

        ipywidgets_vois_runner(kernel_code)

        my_text_1_locator = page_session.get_by_text("Davide").locator('..').locator('..').locator('..')
        my_text_1_locator.wait_for()

        assert_vois_compare_image(image=my_text_1_locator.screenshot(animations='disabled'), postfix='1')

        my_text_2_locator = page_session.get_by_text("Edoardo").locator('..').locator('..').locator('..')
        my_text_2_locator.wait_for()

        assert_vois_compare_image(image=my_text_2_locator.screenshot(animations='disabled'), postfix='2')
