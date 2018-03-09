import vaex
import numpy as np
import numpy.ma
# https://startupsventurecapital.com/essential-cheat-sheets-for-machine-learning-and-deep-learning-researchers-efb6a8ebd2e5?gi=4fe61ea10614

df_a = vaex.from_arrays(a=np.array(   ['A', 'B', 'C']),
                        x=np.array(   [0., 1., 2.]),
                        y=np.ma.array([0., 9., 2.], mask=[False, True, False])
                        )
df_b = vaex.from_arrays(b=np.array(['A', 'B', 'D']),
                        x=np.array([2., 1., 0.]),
                        y=np.ma.array([9., 1., 2.], mask=[True, False, False])
                        )
def test_left_a_b():
    df = df_a.join(other=df_b, left_on='a', right_on='b', rsuffix='_r')
    assert df.evaluate('a').tolist() == ['A', 'B', 'C']
    assert df.evaluate('b').tolist() == ['A', 'B', None]
    assert df.evaluate('x'  ).tolist() == [0, 1, 2]
    assert df.evaluate('x_r').tolist() == [2, 1, None]
    assert df.evaluate('y'  ).tolist() == [0, None, 2]
    assert df.evaluate('y_r').tolist() == [None, 1, None]

def test_left_a_b_filtered():
    df_af = df_a[df_a.x > 0]
    df = df_af.join(other=df_b, left_on='a', right_on='b', rsuffix='_r')
    assert df.evaluate('a').tolist() == ['B', 'C']
    assert df.evaluate('b').tolist() == ['B', None]
    assert df.evaluate('x'  ).tolist() == [1, 2]
    assert df.evaluate('x_r').tolist() == [1, None]
    assert df.evaluate('y'  ).tolist() == [None, 2]
    assert df.evaluate('y_r').tolist() == [1, None]

    # actually, even though the filter is applied, all rows will be matched
    # since the filter can change
    df.set_selection(None, vaex.dataset.FILTER_SELECTION_NAME)
    assert df.evaluate('a').tolist() == ['A', 'B', 'C']
    assert df.evaluate('b').tolist() == ['A', 'B', None]
    assert df.evaluate('x'  ).tolist() == [0, 1, 2]
    assert df.evaluate('x_r').tolist() == [2, 1, None]
    assert df.evaluate('y'  ).tolist() == [0, None, 2]
    assert df.evaluate('y_r').tolist() == [None, 1, None]

    # if we extract, that shouldn't be the case
    df_af = df_a[df_a.x > 0].extract()
    df = df_af.join(other=df_b, left_on='a', right_on='b', rsuffix='_r')
    df.set_selection(None, vaex.dataset.FILTER_SELECTION_NAME)
    assert df.evaluate('a').tolist() == ['B', 'C']
    assert df.evaluate('b').tolist() == ['B', None]
    assert df.evaluate('x'  ).tolist() == [1, 2]
    assert df.evaluate('x_r').tolist() == [1, None]
    assert df.evaluate('y'  ).tolist() == [None, 2]
    assert df.evaluate('y_r').tolist() == [1, None]

def test_right_x_x():
    df = df_a.join(other=df_b, on='x', rsuffix='_r', how='right')
    assert df.evaluate('a').tolist() == ['C', 'B', 'A']
    assert df.evaluate('b').tolist() == ['A', 'B', 'D']
    assert df.evaluate('x'  ).tolist() == [2, 1, 0]
    assert df.evaluate('x_r').tolist() == [2, 1, 0]
    assert df.evaluate('y'  ).tolist() == [2, None, 0]
    assert df.evaluate('y_r').tolist() == [None, 1, 2]

