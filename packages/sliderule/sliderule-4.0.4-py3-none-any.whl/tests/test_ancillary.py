"""Tests for sliderule icesat2 api."""

import pytest
import sliderule
from sliderule import icesat2
from pathlib import Path
import os.path

TESTDIR = Path(__file__).parent

@pytest.mark.network
class TestAncillary:
    def test_geo(self, init):
        region = sliderule.toregion(os.path.join(TESTDIR, "data/grandmesa.geojson"))
        parms = {
            "poly":             region["poly"],
            "srt":              icesat2.SRT_LAND,
            "atl03_geo_fields": ["solar_elevation"]
        }
        gdf = icesat2.atl06p(parms, resources=["ATL03_20181017222812_02950102_005_01.h5"])
        assert init
        assert len(gdf["solar_elevation"]) == 1180
        assert gdf['solar_elevation'].describe()["min"] - 20.803468704223633 < 0.0000001

    def test_ph(self, init):
        region = sliderule.toregion(os.path.join(TESTDIR, "data/grandmesa.geojson"))
        parms = {
            "poly":             region["poly"],
            "srt":              icesat2.SRT_LAND,
            "atl03_ph_fields":  ["ph_id_count"]
        }
        gdf = icesat2.atl03s(parms, "ATL03_20181017222812_02950102_005_01.h5")
        assert init
        assert sum(gdf["ph_id_count"]) == 626032
        assert len(gdf["ph_id_count"]) == 403462
