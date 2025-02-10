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

