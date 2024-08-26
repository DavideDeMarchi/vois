from IPython.display import display


class Test_progress:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import progress
            from ipywidgets import widgets, Layout

            output = widgets.Output(layout=Layout(width='250px', height='150px'))
            display(output)

            my_progress_1 = progress.progress(output,
                                              text='Loading...',  # Tested
                                              show=False,
                                              size=200,  # Tested
                                              width=25,  # Tested
                                              outputheight=150,
                                              color='green')  # Tested

            my_progress_1.show()

        ipywidgets_vois_runner(kernel_code)

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='1')


class Test_Progress:

    def test_simple_init(self, ipywidgets_vois_runner, page_session, assert_vois_compare_image,
                         assert_vois_bytes_image):
        def kernel_code():
            import sys
            sys.path.append('/Users/edoardo/JRC_Projects/vois/src/')

            import warnings
            warnings.filterwarnings("ignore")

            from vois.vuetify import Progress
            from ipywidgets import widgets, Layout

            output = widgets.Output(layout=Layout(width='250px', height='150px'))
            display(output)

            my_progress_1 = Progress(output,
                                     text='Loading...',  # Tested
                                     show=False,
                                     size=200,  # Tested
                                     width=25,  # Tested
                                     output_height=150,
                                     color='green')  # Tested

            my_progress_1.show()

        ipywidgets_vois_runner(kernel_code)

        output_box_locator = page_session.locator('.widget-output')

        output_box_locator.wait_for()

        assert_vois_compare_image(image=output_box_locator.screenshot(animations='disabled'), postfix='1')
