from collections import defaultdict
from typing import Dict, List, Optional, Tuple, cast

import numpy as np
import xarray as xr

from mfire import Datetime
from mfire.composite import WeatherComposite
from mfire.localisation import AltitudeInterval
from mfire.localisation.area_algebra import compute_IoL
from mfire.settings import get_logger
from mfire.text.base import BaseReducer
from mfire.text.period_describer import PeriodDescriber
from mfire.utils.calc import round_to_previous_multiple
from mfire.utils.date import Period, Periods
from mfire.utils.dict_utils import KeyBasedDefaultDict
from mfire.utils.list_utils import (
    all_combinations_and_remaining,
    combinations_and_remaining,
)
from mfire.utils.string_utils import concatenate_string, decapitalize
from mfire.utils.unit_converter import fromW1ToWWMF
from mfire.utils.wwmf_utils import (
    WWMF_FAMILIES,
    are_wwmf_precipitations,
    are_wwmf_visibilities,
    is_severe_phenomenon,
    is_snow_family,
    is_wwmf_precipitation,
    is_wwmf_visibility,
    wwmf_families,
    wwmf_label,
    wwmf_subfamilies,
)

# Logging
LOGGER = get_logger(name="weather_reducer.mod", bind="weather_reducer")


class WeatherReducer(BaseReducer):
    """Classe Reducer pour le module weather.

    La méthode "compute" ici prend en entrée un "WeatherComposite" contenant
    exactement un "field" "weather".
    """

    # Structure of computed data
    _ts_info: defaultdict = KeyBasedDefaultDict(
        lambda wwmf: {
            "temporality": Periods(),
        }
    )

    # Dictionary giving the minimum values to be considered not isolated
    # The key are the corresponding WWMF code
    required_DT: defaultdict = defaultdict(lambda: 0.05)
    required_DHmax: defaultdict = defaultdict(lambda: 0.05)

    _times: Optional[List[Datetime]] = None
    _idAxis: Optional[str] = None

    @property
    def id_axis(self) -> str:
        if self._idAxis is None:
            self._idAxis = str(
                next(
                    id
                    for id in self.data.id
                    if self.data.sel(id=id)["areaType"].data == "Axis"
                ).data
            )
        return self._idAxis

    @property
    def request_time(self) -> Datetime:
        weather_compo = cast(WeatherComposite, self.compo)
        return weather_compo.production_datetime

    def _pre_process(self):
        # clean of old values
        self._ts_info.clear()
        self._idAxis = None

        self._times = [Datetime(d) for d in self.data.valid_time.to_numpy()]

        self._snowMap = xr.DataArray(
            data=np.full((self.data.latitude.size, self.data.longitude.size), False),
            dims=["latitude", "longitude"],
            coords=dict(
                latitude=self.data.latitude,
                longitude=self.data.longitude,
            ),
        )

        # we convert if necessary
        if self.data["wwmf"].units == "w1":
            self.data["wwmf"] = fromW1ToWWMF(self.data["wwmf"])

        # we replace currently codes with nebulosity
        def _replace_u_func(x):
            return np.select(
                [x == 72, x == 73, x == 78, x == 82, x == 83], [71, 70, 77, 81, 80], x
            )

        self.data["wwmf"] = xr.apply_ufunc(_replace_u_func, self.data["wwmf"])

    def _process(self):
        """
        La méthode récupère tous les codes TS sensibles en gardant en mémoire les
        valid_time pour lesquels ils se produisent
        """
        if len(self._times) > 1:
            previous_time = self._times[0] - (self._times[1] - self._times[0])
        else:
            LOGGER.warning("There is only one valid_time to compute weather text.")
            previous_time = self._times[0]

        dt_visibility, dh_max_visibility = 0.0, 0.0
        dt_precipitation, dh_max_precipitation = 0.0, 0.0

        for idx, time in enumerate(self._times):
            data_for_fixed_time: xr.DataArray = self.data.wwmf.sel(valid_time=time)
            all_ts, counts = np.unique(data_for_fixed_time, return_counts=True)

            dh_visibility, dh_precipitation = 0.0, 0.0
            for ts, count in zip(all_ts, counts):
                ts_families = wwmf_families(ts)
                if not ts_families:  # that it isn't a TS
                    continue

                self._ts_info[ts]["temporality"].append(
                    Period(begin_time=previous_time, end_time=time)
                )

                # we store the DT and DHMax in order to remove (later) the isolated
                # phenomenon
                dh = (count / data_for_fixed_time.count()).item()

                if is_wwmf_visibility(ts):
                    dh_visibility += dh
                else:
                    dh_precipitation += dh

            dt_visibility += dh_visibility / len(self._times)
            dt_precipitation += dh_precipitation / len(self._times)
            dh_max_visibility = max(dh_max_visibility, dh_visibility)
            dh_max_precipitation = max(dh_max_precipitation, dh_precipitation)

            previous_time = time

        # We exclude the isolated phenomenon
        ts_to_exclude = []
        if (
            not any(is_severe_phenomenon(ts) for ts in self._ts_info)
            and dt_precipitation < self.required_DT["precipitation"]
            and dh_max_precipitation < self.required_DHmax["precipitation"]
        ):
            ts_to_exclude += [ts for ts in self._ts_info if is_wwmf_precipitation(ts)]
        if (
            dt_visibility < self.required_DT["visibility"]
            and dh_max_visibility < self.required_DHmax["visibility"]
        ):
            ts_to_exclude += [ts for ts in self._ts_info if is_wwmf_visibility(ts)]
        for ts in ts_to_exclude:
            del self._ts_info[ts]

        # We apply different rules
        self._process_temporalities()

    def _describe(self, *args) -> Dict[str, Dict[str, Optional[str]]]:
        """
        This function takes into argument the list of ts and
        returns a dict of all description
        """
        tuples = sorted(
            args,
            key=lambda x: x[1]["temporality"].begin_time,
        )

        result = {}
        period_describer = PeriodDescriber(self.request_time)
        for i, (label, info) in enumerate(tuples):
            if info.get("is_severe"):
                result["TSsevere"] = decapitalize(label)
            else:
                if (
                    len(info["temporality"]) > 1
                    or info["temporality"][0].begin_time > self._times[0]
                    or info["temporality"][0].end_time < self._times[-1]
                ):
                    temporality = period_describer.describe(
                        info["temporality"], to_reduce=False
                    )
                else:
                    temporality = None

                result[f"TS{i + 1}"] = {
                    "label": label if temporality is None else decapitalize(label),
                    "temporality": temporality.capitalize()
                    if temporality is not None
                    else None,
                    "localisation": info.get("localisation"),
                }

        return result

    def _concat_infos(self, *args, is_severe: bool = False) -> dict:
        """
        This function concatenates information by summing the temporalities.
        The argument is the list of TS codes. It returns a dict of concatenated
        information.
        If argument is_severe is True, an information is added to handle the display
        of severe phenomenon
        """
        period_describer = PeriodDescriber(self.request_time)

        all_temporalities = Periods()
        for ts in args:
            all_temporalities += self._ts_info[ts]["temporality"]

        result = {"temporality": period_describer.reduce(all_temporalities)}

        loc = self._ts_info[args[0]].get("localisation")
        if loc is not None:
            result["localisation"] = loc
        if is_severe:
            result["is_severe"] = True
        return result

    def _process_temporalities(self):
        """
        This method process all temporalities in order to remove short phenomenon.
        It will help to generate the sentences and apply grouping rules.
        """
        ts_to_remove = []

        nbr_temporalities_to_keep = 1 + (self._times[-1] - self._times[0]).days
        for ts, info in self._ts_info.items():
            info["temporality"] = PeriodDescriber(self.request_time).reduce(
                info["temporality"], n=nbr_temporalities_to_keep
            )
            if info["temporality"].total_hours < 3:
                ts_to_remove.append(ts)
        for ts in ts_to_remove:
            del self._ts_info[ts]

    def _process_localisation(self, *args):
        weather_compo = cast(WeatherComposite, self.compo)
        geos_descriptive = weather_compo.geos_descriptive
        altitudes_da = weather_compo.altitudes("wwmf")

        map_size = weather_compo.geos.compute().sum().data
        for grp in args:
            if WWMF_FAMILIES.SNOW not in wwmf_families(*grp):
                continue

            only_snow_ts = [ts for ts in grp if is_snow_family(ts)]
            snow_map = self.data.wwmf.isin(only_snow_ts).sum(("id", "valid_time")) > 0
            if snow_map.sum().data / map_size >= 0.9:
                snow_loc = "sur tout le domaine"
            else:
                ratio_iol = compute_IoL(geos_descriptive, snow_map)
                if ratio_iol is not None:
                    snow_loc = (
                        concatenate_string(ratio_iol.areaName.values)
                        if ratio_iol.sum().data / map_size < 0.9
                        else "sur tout le domaine"
                    )
                else:
                    min_altitude = round_to_previous_multiple(
                        altitudes_da.where(snow_map).min(), 100
                    )
                    snow_loc = AltitudeInterval((min_altitude, np.inf)).name()

            for ts in grp:
                self._ts_info[ts]["localisation"] = snow_loc

    def _merge_same_ts_family(self, *args) -> List[Tuple[str, dict]]:
        """
        This function takes as argument the list of TS of same family, merges and
        returns a list of tuple of (list of ts, infos) of all description
        """
        ts1, ts2 = args[0], args[1]
        info1, info2 = self._ts_info[ts1], self._ts_info[ts2]

        nbr_args = len(args)
        if nbr_args == 2:
            different_temp = False
            if any(is_severe_phenomenon(wwmf) for wwmf in args):
                hours_intersection = info1["temporality"].hours_of_intersection(
                    info2["temporality"]
                )
                hours_union = info1["temporality"].hours_of_union(info2["temporality"])
                if hours_intersection / hours_union < 0.75:
                    different_temp = True
            elif not info1["temporality"].are_same_temporalities(info2["temporality"]):
                different_temp = True

            # If TS are considered to have different temporalities
            if different_temp:
                self._process_localisation([ts1], [ts2])
                return [(wwmf_label(ts1), info1), (wwmf_label(ts2), info2)]

            self._process_localisation([ts1, ts2])
            return [(wwmf_label(ts1, ts2), self._concat_infos(ts1, ts2))]

        elif nbr_args == 3:
            ts3 = args[2]

            # We try to gather two of them according to same possible temporality and TS
            all_combinations = [ts1, ts2, ts3]
            for [_ts1, _ts2], [_ts3] in combinations_and_remaining(all_combinations, 2):
                _temp1 = self._ts_info[_ts1]["temporality"]
                _temp2 = self._ts_info[_ts2]["temporality"]
                _temp3 = self._ts_info[_ts3]["temporality"]

                if (
                    _temp1.are_same_temporalities(_temp2)
                    and not _temp1.are_same_temporalities(_temp3)
                    and not _temp2.are_same_temporalities(_temp3)
                ):
                    label = wwmf_label(_ts1, _ts2)
                    if label:
                        self._process_localisation([_ts1, _ts2], [_ts3])
                        return [
                            (label, self._concat_infos(_ts1, _ts2)),
                            (wwmf_label(_ts3), self._ts_info[_ts3]),
                        ]

            # If we can't gather two of them to same temporality and TS
            self._process_localisation([ts1, ts2, ts3])
            label = wwmf_label(ts1, ts2, ts3)
            return [(label, self._concat_infos(ts1, ts2, ts3))]

    def _post_process(self) -> dict:
        """
        This method post-process data in order to be treated by the template
        key selector
        """
        nbr_ts = len(self._ts_info)
        if nbr_ts == 0:
            return {}
        elif nbr_ts == 1:
            return self._post_process_1_ts()
        elif nbr_ts == 2:
            return self._post_process_2_ts()
        elif nbr_ts == 3:
            return self._post_process_3_ts()
        else:
            return self._post_process_more_than_3_ts()

    def _post_process_1_ts(self) -> dict:
        items_iter = iter(self._ts_info.items())
        ts1, info1 = next(items_iter)

        self._process_localisation([ts1])
        return self._describe((wwmf_label(ts1), info1))

    def _post_process_2_ts(self) -> dict:
        items_iter = iter(self._ts_info.keys())
        ts1 = next(items_iter)
        ts2 = next(items_iter)

        # If families are different we don't merge even if temporalities are the same
        if is_wwmf_visibility(ts1) ^ is_wwmf_visibility(ts2):
            info1, info2 = [self._ts_info[ts] for ts in [ts1, ts2]]

            # We add location for snow codes
            self._process_localisation([ts1], [ts2])
            return self._describe(
                (wwmf_label(ts1), info1),
                (wwmf_label(ts2), info2),
            )

        descriptions = self._merge_same_ts_family(ts1, ts2)
        return self._describe(*descriptions)

    def _post_process_3_ts(self) -> dict:
        items_iter = iter(self._ts_info.items())
        ts1, info1 = next(items_iter)
        ts2, info2 = next(items_iter)
        ts3, info3 = next(items_iter)

        # Same family
        if are_wwmf_visibilities(ts1, ts2, ts3) or are_wwmf_precipitations(
            ts1, ts2, ts3
        ):
            descriptions = self._merge_same_ts_family(ts1, ts2, ts3)
            return self._describe(*descriptions)

        # Different families
        all_combinations = [ts1, ts2, ts3]
        for [_ts1, _ts2], [_ts3] in combinations_and_remaining(all_combinations, 2):
            if are_wwmf_visibilities(_ts1, _ts2) or are_wwmf_precipitations(_ts1, _ts2):
                label = wwmf_label(_ts1, _ts2)
                self._process_localisation([_ts1, _ts2], [_ts3])
                return self._describe(
                    (label, self._concat_infos(_ts1, _ts2)),
                    (wwmf_label(_ts3), self._ts_info[_ts3]),
                )

    def _post_process_more_than_3_ts(self) -> dict:
        description_args = []

        visibility_codes, precipitation_codes = [], []
        for wwmf in self._ts_info.keys():
            (visibility_codes, precipitation_codes)[
                int(is_wwmf_precipitation(wwmf))
            ].append(wwmf)

        nbr_visibility_codes = len(visibility_codes)
        if nbr_visibility_codes > 0:
            visibility_infos = (
                self._concat_infos(*(wwmf for wwmf in visibility_codes if wwmf != 31))
                if visibility_codes != [31]
                else self._ts_info[31]
            )

            if nbr_visibility_codes == 1:
                visibility_label = wwmf_label(visibility_codes[0])
            elif nbr_visibility_codes == 2 and 31 in visibility_codes:
                code = (
                    visibility_codes[0]
                    if visibility_codes[0] != 31
                    else visibility_codes[1]
                )
                visibility_label = wwmf_label(code)
            else:
                visibility_label = wwmf_label(*visibility_codes)
            description_args.append((visibility_label, visibility_infos))

        nbr_precipitation_codes = len(precipitation_codes)
        if nbr_precipitation_codes > 0:

            subfamilies = wwmf_subfamilies(*precipitation_codes)
            nbr_A_grp = sum(int(subfam.is_A_group) for subfam in subfamilies)

            ts1 = precipitation_codes[0]
            infos1 = self._ts_info[ts1]

            if nbr_precipitation_codes == 1:
                self._process_localisation([ts1])
                description_args.append((wwmf_label(ts1), infos1))
            elif nbr_precipitation_codes in [2, 3]:
                description_args += self._merge_same_ts_family(*precipitation_codes)
            # We don't treat severe phenomenon as distinct
            elif nbr_A_grp == len(subfamilies) or nbr_A_grp < 3:
                for (combined_ts_1, combined_ts_2) in all_combinations_and_remaining(
                    precipitation_codes, is_symmetric=True
                ):
                    combined_temp_1 = [
                        self._ts_info[ts]["temporality"] for ts in combined_ts_1
                    ]
                    combined_temp_2 = [
                        self._ts_info[ts]["temporality"] for ts in combined_ts_2
                    ]
                    if not combined_temp_1[0].are_same_temporalities(
                        *combined_temp_1[1:]
                    ) or not combined_temp_2[0].are_same_temporalities(
                        *combined_temp_2[1:]
                    ):
                        continue

                    union_temp_1 = sum(combined_temp_1, start=Periods())
                    union_temp_2 = sum(combined_temp_2, start=Periods())
                    if not union_temp_1.are_same_temporalities(union_temp_2):
                        combined_label_1 = wwmf_label(
                            *combined_ts_1, concat_if_not_found=False
                        )
                        combined_label_2 = wwmf_label(
                            *combined_ts_2, concat_if_not_found=False
                        )
                        if combined_label_1 and combined_label_2:
                            self._process_localisation(combined_ts_1, combined_ts_2)
                            description_args.append(
                                (
                                    combined_label_1,
                                    self._concat_infos(*combined_ts_1),
                                )
                            )
                            description_args.append(
                                (
                                    combined_label_2,
                                    self._concat_infos(*combined_ts_2),
                                )
                            )
                            break
                else:
                    self._process_localisation(precipitation_codes)
                    precipitation_infos = self._concat_infos(*precipitation_codes)
                    precipitation_label = wwmf_label(*precipitation_codes)
                    description_args.append((precipitation_label, precipitation_infos))
            # We treat severe phenomenon as distinct
            else:
                grp_A_ts, grp_B_ts = [], []
                for ts in precipitation_codes:
                    if ts in [49, 59, 84, 85, 98, 99]:
                        grp_B_ts.append(ts)
                    else:
                        grp_A_ts.append(ts)

                self._process_localisation(grp_A_ts, grp_B_ts)
                label_group_A = wwmf_label(*grp_A_ts)
                infos_group_A = self._concat_infos(*grp_A_ts)
                description_args.append((label_group_A, infos_group_A))
                label_group_B = wwmf_label(*grp_B_ts, concat_if_not_found=True)
                infos_group_B = self._concat_infos(*grp_B_ts, is_severe=True)
                description_args.append((label_group_B, infos_group_B))
        return self._describe(*description_args)

    def compute(self, compo: WeatherComposite, metadata: dict = None) -> dict:
        super().compute(compo=compo)

        self._pre_process()
        self._process()
        return self._post_process()
