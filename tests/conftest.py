import pytest
from typing import Any, Callable, Dict, Generator, List, Union
from pathlib import Path
import sys
from io import BytesIO
from PIL import Image
import os
from solara.test.pytest_plugin import create_runner_solara, create_runner_voila, create_runner_jupyter_notebook, \
    create_runner_jupyter_lab


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("vois", "Vois Library")
    group.addoption(
        "--vois-update-snapshots",
        action="store_true",
        default=False,
        help="Initialize the snapshots.",
    )

    group.addoption(
        "--runners",
        nargs='+',
        default=['voila'],
        help="Initialize the snapshots.",
    )


# def pytest_generate_tests(metafunc):
#     r_list = metafunc.config.getoption("--runners")
#     metafunc.parametrize("runner", r_list)


# def pytest_generate_tests(metafunc):
#     # called once per each test function
#     print('------------------------')
#     print(metafunc)
#     print(metafunc.cls)
#     print(metafunc.function.__name__)
#     print('------------------------')
#     # funcarglist = metafunc.cls.params[metafunc.function.__name__]
#     # argnames = sorted(funcarglist[0])
#     # print(funcarglist, argnames)
#     # metafunc.parametrize(
#     #     argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
#     # )

@pytest.fixture(scope="session", params=['voila'])
def runner(pytestconfig, request):
    # par = pytestconfig.getoption("--runners")
    # print(par, type(par))
    # return pytestconfig.getoption("--runners")
    return request.param



# @pytest.fixture(scope="session")
# def runners_list(pytestconfig: Any, request) -> List[str]:
#     from solara.test.pytest_plugin import runners
#     r_list = pytestconfig.getoption("--runners")
#     runners = r_list
#     # print(request.param)
#     os.environ["SOLARA_TEST_RUNNERS"] = ','.join(r_list)
#     print(r_list)
#     return runners


@pytest.fixture
def ipywidgets_vois_runner(
        # solara_server,
        # solara_app,
        voila_server,
        # jupyter_server,
        notebook_path,
        page_session: "playwright.sync_api.Page",
        runner,
        pytestconfig: Any,
):
    require_vuetify_warmup = pytestconfig.getoption("solara_vuetify_warmup")
    if runner == "solara":
        with create_runner_solara(solara_server, solara_app, page_session, require_vuetify_warmup) as runner:
            yield runner
    elif runner == "voila":
        yield create_runner_voila(voila_server, notebook_path, page_session, require_vuetify_warmup)
    elif runner == "jupyter_lab":
        yield create_runner_jupyter_lab(jupyter_server, notebook_path, page_session, require_vuetify_warmup)
    elif runner == "jupyter_notebook":
        yield create_runner_jupyter_notebook(jupyter_server, notebook_path, page_session, require_vuetify_warmup)
    else:
        raise RuntimeError(f"Unknown runner {runner}")


def compare_default(reference, result, threshold=0.1):
    from PIL import Image
    from pixelmatch.contrib.PIL import pixelmatch

    difference = Image.new("RGB", reference.size)
    diff = pixelmatch(reference, result, difference, threshold=threshold)
    return diff, difference


@pytest.fixture
def assert_vois_bytes_image(update_snapshot):
    def compare_image(image1, image2, compare: Callable = compare_default, differ: bool = False):
        if not update_snapshot:
            pil_image1 = Image.open(BytesIO(image1))
            pil_image2 = Image.open(BytesIO(image2))

            diff, difference = compare(pil_image1, pil_image2)

            if diff > 0 and differ is False:
                raise AssertionError('The two images are different!')
            elif diff == 0 and differ is True:
                raise AssertionError('The two images are equal!')
            else:
                return

    return compare_image


@pytest.fixture(scope='session')
def update_snapshot(pytestconfig):
    return pytestconfig.getoption("--vois-update-snapshots", default=False)


@pytest.fixture
def assert_vois_compare_image(pytestconfig: Any, request: Any, browser_name: str, vois_snapshots_directory,
                              update_snapshot):
    from PIL import Image

    path_str_split = f"{str(Path(request.node.name))}".replace("[", "-").replace("]", "").replace(" ", "-").replace(
        ",", "-").split('-')
    test_function_name = path_str_split[0]
    runner_name = path_str_split[1]
    test_file_name = request.node.path.name

    path_snapshots_directory = vois_snapshots_directory / test_file_name
    vois_test_results_directory = vois_snapshots_directory / '..' / 'test_results'
    path_test_results_directory = vois_test_results_directory / test_file_name

    if not path_snapshots_directory.exists():
        path_snapshots_directory.mkdir(exist_ok=True, parents=True)

    if not path_test_results_directory.exists():
        path_test_results_directory.mkdir(exist_ok=True, parents=True)

    def compare_snapshots(
            image: bytes,
            custom_format="{testname}-{postfix}-{runner}-{browser}-{platform}-{type}.png",
            postfix="",
            compare: Callable = compare_default,
    ):
        format_kwargs = dict(testname=test_function_name,
                             runner=runner_name,
                             platform=sys.platform,
                             browser=browser_name,
                             postfix=postfix)

        path_reference = path_snapshots_directory / custom_format.format(**format_kwargs, type="reference").format(
            **format_kwargs)
        part_reference_for_comparison = path_test_results_directory / custom_format.format(**format_kwargs,
                                                                                           type="reference").format(
            **format_kwargs)
        path_previous = path_test_results_directory / custom_format.format(**format_kwargs, type="failed").format(
            **format_kwargs)
        path_diff = path_test_results_directory / custom_format.format(**format_kwargs, type="diff").format(
            **format_kwargs)

        def write_bytes(c_image: bytes, c_path):
            c_path.write_bytes(c_image)

        def write_image(c_image: Image, c_path):
            c_image.save(c_path)

        if not path_reference.exists() or update_snapshot:
            if update_snapshot:
                write_bytes(c_image=image, c_path=path_reference)
            else:
                raise AssertionError(
                    f'Snapshot {path_reference} did not exist. Please use "--vois-update-snapshots".'
                )
        else:
            reference = Image.open(path_reference)
            result = Image.open(BytesIO(image))
            difference = None

            if reference.size != result.size:
                write_image(c_image=result, c_path=path_previous)
                raise AssertionError(
                    f"Snapshot {path_reference} has a different size than the result {path_previous}. Size {reference.size} != {result.size}."
                )

            diff, difference = compare(reference, result)

            if diff > 0:
                write_image(c_image=difference, c_path=path_diff)
                write_image(c_image=result, c_path=path_previous)
                write_image(c_image=reference, c_path=part_reference_for_comparison)
                raise AssertionError(
                    f'Snapshot {path_reference} does not match.'
                )

    return compare_snapshots


@pytest.fixture(scope="session")
def vois_snapshots_directory(request: Any) -> Path:
    path = Path(request.config.rootpath) / "tests" / "ui" / "snapshots"
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    return path
