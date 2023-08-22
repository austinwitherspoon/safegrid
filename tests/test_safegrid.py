import io
import contextlib
import safegrid


def test_hello_world():
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        safegrid.hello_world()
        output = buf.getvalue()
    assert output == "Hello World!\n"
