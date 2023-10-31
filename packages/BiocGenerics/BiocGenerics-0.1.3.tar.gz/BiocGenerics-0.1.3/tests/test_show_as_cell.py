from biocgenerics import show_as_cell, format_table


def test_show_as_cell():
    assert show_as_cell([1, 2, 3, 4], range(4)) == ["1", "2", "3", "4"]
    assert show_as_cell([1, 2, 3, 4], [1, 3]) == ["2", "4"]


def test_format_table():
    contents = [
        ["asdasd", "1", "2", "3", "4"],
        [""] + ["|"] * 4,
        ["asyudgausydga", "A", "B", "C", "D"],
    ]
    print(format_table(contents))
    print(format_table(contents, floating_names=["", "aarg", "boo", "ffoo", "stuff"]))
    print(format_table(contents, window=10))
    print(
        format_table(
            contents, window=10, floating_names=["", "AAAR", "BBBB", "XXX", "STUFF"]
        )
    )
