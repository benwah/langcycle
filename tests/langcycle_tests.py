import sys
from unittest import mock

from langcycle import (
    cycle_layout,
    get_layout_variant,
    get_layouts_from_args,
    main,
)


@mock.patch("langcycle.sys.exit")
@mock.patch("langcycle.cycle_layout")
def test_exists_if_setxkbmap_does_not_exist(_cycle_layout, mocked_exit):
    """When setxkbmap is not present, exit and display an error."""
    with mock.patch("langcycle.shutil.which", mock.Mock(return_value=None)):
        sys.argv = ["langcycle", "en", "ca"]
        main()
        mocked_exit.assert_called_once_with("Cannot find setxkbmap")


@mock.patch("langcycle.sys.exit")
@mock.patch("langcycle.help")
@mock.patch("langcycle.cycle_layout")
def test_help_called(_cycle_layout, mocked_help, mocked_exit):
    """Help gets called"""
    for argv in [
        ["langcycle"],
        ["langcycle", "-h"],
        ["langcycle", "--help"],
        ["langcycle", "help"],
    ]:
        sys.argv = argv
        main()
        mocked_exit.assert_called_once()
        mocked_help.assert_called_once()
        mocked_exit.reset_mock()
        mocked_help.reset_mock()


@mock.patch("langcycle.sys.exit")
@mock.patch("langcycle.help")
@mock.patch("langcycle.cycle_layout")
def test_cycle_layout_called(cycle_layout, mocked_help, mocked_exit):
    """Cycle_layout is called with expected arguments"""
    sys.argv = ["langcycle", "ca", "en"]
    main()
    mocked_exit.assert_not_called()
    mocked_help.assert_not_called()
    cycle_layout.assert_called_once_with([["ca", None], ["en", None]])


def test_get_layouts_from_args():
    """get_layouts_from_args converts arguments into a list of layouts and
    variants"""
    assert get_layouts_from_args(["langcycle", "ca:fr", "en"]) == [
        ["ca", "fr"],
        ["en", None],
    ]

    assert get_layouts_from_args(
        ["langcycle", "ca:multi", "cn", "ca:eng"]
    ) == [
        ["ca", "multi"],
        ["cn", None],
        ["ca", "eng"],
    ]


def test_get_layouts_variants_without_variant():
    """get currently configured layout and variant when no variant is
    configured"""
    mocked_output = "rules:      evdev\nmodel:      pc105\nlayout:     us\n"
    mocked_stream = mock.Mock(read=mock.Mock(return_value=mocked_output))
    with mock.patch(
        "langcycle.os.popen", mock.Mock(return_value=mocked_stream)
    ):
        assert get_layout_variant() == ["us", None]


def test_get_layouts_variants_with_variant():
    """get currently configured layout and variant when no variant is
    configured"""
    mocked_output = (
        "rules:      evdev\nmodel:      pc105\nlayout:     ca\n"
        "variant:    fr\n"
    )
    mocked_stream = mock.Mock(read=mock.Mock(return_value=mocked_output))
    with mock.patch(
        "langcycle.os.popen", mock.Mock(return_value=mocked_stream)
    ):
        assert get_layout_variant() == ["ca", "fr"]


@mock.patch(
    "langcycle.get_layout_variant", mock.Mock(return_value=["en", None])
)
def test_cycle_layout():
    with mock.patch("langcycle.os.system") as mocked_system:
        cycle_layout([["en", None], ["ca", "fr"]])
        mocked_system.assert_called_once_with("setxkbmap ca fr")


@mock.patch(
    "langcycle.get_layout_variant", mock.Mock(return_value=["en", None])
)
def test_cycle_middle():
    with mock.patch("langcycle.os.system") as mocked_system:
        cycle_layout([["cn", None], ["en", None], ["ca", "fr"]])
        mocked_system.assert_called_once_with("setxkbmap ca fr")


@mock.patch(
    "langcycle.get_layout_variant", mock.Mock(return_value=["ca", "fr"])
)
def test_cycle_end():
    with mock.patch("langcycle.os.system") as mocked_system:
        cycle_layout([["cn", None], ["en", None], ["ca", "fr"]])
        mocked_system.assert_called_once_with("setxkbmap cn")


@mock.patch(
    "langcycle.get_layout_variant", mock.Mock(return_value=["cn", None])
)
def test_cycle_layout_with_unexpected_configured_layout():
    with mock.patch("langcycle.os.system") as mocked_system:
        cycle_layout([["en", None], ["ca", "fr"]])
        mocked_system.assert_called_once_with("setxkbmap en")
