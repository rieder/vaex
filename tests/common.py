import pytest
import vaex
import vaex.webserver
import numpy as np

import sys
test_port = 29110 + sys.version_info[0] * 10 + sys.version_info[1]
scheme = 'ws'

@pytest.fixture(scope='module')
def webserver():
    webserver = vaex.webserver.WebServer(datasets=[], port=test_port, cache_byte_size=0)
    webserver.serve_threaded()
    yield webserver
    webserver.stop_serving()
    #return webserver

@pytest.fixture(scope='module')
def server(webserver):
    server = vaex.server("%s://localhost:%d" % (scheme, test_port))
    yield server
    server.close()

@pytest.fixture()
def ds_remote(webserver, server):
    ds = ds_trimmed()
    ds.name = 'ds_trimmed'
    webserver.set_datasets([ds])
    return server.datasets(as_dict=True)['ds_trimmed']

@pytest.fixture()
def ds_filtered():
    return create_filtered()

@pytest.fixture()
def ds_half():
    ds = create_base_ds()
    ds.set_active_range(0, 10)
    return ds

@pytest.fixture()
def ds_trimmed():
    ds = create_base_ds()
    ds.set_active_range(0, 10)
    return ds.trim()

@pytest.fixture(params=['ds_filtered', 'ds_half', 'ds_trimmed', 'ds_remote'])
def ds(request, ds_filtered, ds_half, ds_trimmed, ds_remote):
    named = dict(ds_filtered=ds_filtered, ds_half=ds_half, ds_trimmed=ds_trimmed, ds_remote=ds_remote)
    return named[request.param]

@pytest.fixture(params=['ds_filtered', 'ds_half', 'ds_trimmed'])
def ds_local(request, ds_filtered, ds_half, ds_trimmed):
    named = dict(ds_filtered=ds_filtered, ds_half=ds_half, ds_trimmed=ds_trimmed)
    return named[request.param]


@pytest.fixture(params=[ds_half, ds_trimmed], ids=['ds_half', 'ds_trimmed'])
def ds_no_filter(request):
    return request.param()

def create_filtered():
    ds = create_base_ds()
    ds.select('x < 10', name=vaex.dataset.FILTER_SELECTION_NAME)
    return ds

def create_base_ds():
    dataset = vaex.dataset.DatasetArrays("dataset")
    x = x = np.arange(40, dtype=">f8").reshape((-1,20)).T.copy()[:,0]
    y = y = x ** 2
    ints = np.arange(20, dtype="i8")
    ints[0] = 2**62+1
    ints[1] = -2**62+1
    ints[2] = -2**62-1
    ints[0+10] = 2**62+1
    ints[1+10] = -2**62+1
    ints[2+10] = -2**62-1
    dataset.add_column("x", x)
    dataset.add_column("y", y)
    m = x.copy()
    ma_value = 77777
    m[-1+10] = ma_value
    m[-1+20] = ma_value
    m = np.ma.array(m, mask=m==ma_value)

    n = x.copy()
    n[-2+10] = np.nan
    n[-2+20] = np.nan

    nm = x.copy()
    nm[-2+10] = np.nan
    nm[-2+20] = np.nan
    nm[-1+10] = ma_value
    nm[-1+20] = ma_value
    nm = np.ma.array(nm, mask=nm==ma_value)

    mi = mi = np.ma.array(m.data.astype(np.int64), mask=m.data==ma_value, fill_value=88888)
    dataset.add_column("m", m)
    dataset.add_column('n', n)
    dataset.add_column('nm', nm)
    dataset.add_column("mi", mi)
    dataset.add_column("ints", ints)


    name = np.array(list(map(lambda x: str(x) + "bla" + ('_' * int(x)), x)), dtype='S') #, dtype=np.string_)
    dataset.add_column("name", np.array(name))
    return dataset

dsf = create_filtered()