import marshal
from hypothesis import given
from hypothesis import strategies as st


def serialize(obj):
    return marshal.dumps(obj)


@given(st.integers())
def test_int(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.text())
def test_str(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.lists(st.integers()))
def test_list(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.dictionaries(st.text(), st.integers()))
def test_dict(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.booleans())
def test_bool(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.floats(allow_nan=False, allow_infinity=False))
def test_float(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.complex_numbers())
def test_complex(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.binary())
def test_bytes(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.tuples(st.integers(), st.text(), st.booleans()))
def test_tuple(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(st.frozensets(st.text()))
def test_frozenset(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(
    st.lists(
        st.recursive(
            st.integers() | st.booleans() | st.floats(allow_nan=False),
            lambda children: st.lists(children, max_size=3),
            max_leaves=10,
        )
    )
)
def test_nested_list(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3


@given(
    st.recursive(
        st.integers()
        | st.booleans()
        | st.floats(allow_nan=False)
        | st.text(),
        lambda children: st.dictionaries(
            keys=st.text(),
            values=children,
            max_size=3
        ),
        max_leaves=10,
    )
)
def test_nested_dictionary(data):
    r1 = serialize(data)
    r2 = serialize(data)
    r3 = serialize(data)
    assert r1 == r2 and r1 == r3
