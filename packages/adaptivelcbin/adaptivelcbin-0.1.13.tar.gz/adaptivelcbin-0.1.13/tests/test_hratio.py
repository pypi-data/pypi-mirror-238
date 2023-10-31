def test_default():
    import hratio
    out_fn = "test1.qdp"
    hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', out_fn, 15)

    import os
    assert os.path.exists(out_fn)
    os.remove(out_fn)

def test_external_write():
    import hratio
    out_fn = "test.qdp"
    ss, hh, rr = hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', None, 15)

    hratio.write_qdp(ss, hh, rr, out_fn, -1)
    import os
    assert os.path.exists(out_fn)
    os.remove(out_fn)

def test_rebin_hard():
    import hratio
    out_fn = "test2.qdp"
    hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', out_fn, 15, flag_rebin=2)

    import os
    assert os.path.exists(out_fn)
    os.remove(out_fn)

def test_rebin_sum():
    import hratio
    out_fn = "test3.qdp"
    hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', out_fn, 15, flag_rebin=3)

    import os
    assert os.path.exists(out_fn)
    os.remove(out_fn)

def test_rebin_hr():
    import hratio
    out_fn = "test4.qdp"
    hratio.hratio_func('data/PNsrc_lc_01s_005-030.fits', 'data/PNsrc_lc_01s_030-100.fits', out_fn, 15, flag_rebin=4)

    import os
    assert os.path.exists(out_fn)
    os.remove(out_fn)