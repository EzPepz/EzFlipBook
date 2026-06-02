import pytest

from project import calc_dur, calc_est_size, parse_seq_name

#test duration
def test_calc_dur():
    assert calc_dur(500, 25) == 20.0
    assert calc_dur(250, 25) == 10.0
    assert calc_dur(250, 30) == pytest.approx(8.33, rel=1e-2)
    assert calc_dur(250, 120) == pytest.approx(2.083, rel=1e-2)
    
#test estimate file size
def test_calc_est_size():
    assert calc_est_size(500, 10) == pytest.approx(0.610, rel=1e-2)
    assert calc_est_size(2000, 10) == pytest.approx(2.44, rel=1e-2)
    assert calc_est_size(10000, 20) == pytest.approx(24.41, rel=1e-2)
    assert calc_est_size(2000, 14.5) == pytest.approx(3.54, rel=1e-2)

#test parse sequence name
def test_parse_seq_name():
    assert parse_seq_name("frame_001.png") == ("frame", "_", 3, ".png")
    assert parse_seq_name("shot-0042.tiff") == ("shot", "-", 4, ".tiff")
    assert parse_seq_name("frame_001.tif") == ("frame", "_", 3, ".tif")
    assert parse_seq_name("comp.0010.jpg") == ("comp", ".", 4, ".jpg")
    assert parse_seq_name("render0001.tga") == ("render", "", 4, ".tga")
    assert parse_seq_name("noframe.png") == None