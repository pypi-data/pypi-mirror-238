def test_import():
    from pkg.hi import hi
    assert hi() == '\U0001F40D'
