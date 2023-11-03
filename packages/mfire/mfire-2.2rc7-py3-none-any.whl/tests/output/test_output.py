import shutil
from pathlib import Path

import pytest

from mfire.composite.periods import Period
from mfire.output.cdp import (
    CDPAlea,
    CDPComponents,
    CDPDataset,
    CDPPeriod,
    CDPProduction,
)
from mfire.output.cdp.datasets import CDPParam, CDPSummary, CDPValueParam
from mfire.production import ProductionManager
from mfire.settings import Settings
from mfire.utils import JsonFile
from mfire.utils.date import Datetime

TEST_DATA_DIR = Path(__file__).absolute().parent.parent / "test_data"


def change_configuration(conf_name: Path, conf_temp: Path, data_dir: Path):
    """change_configuration
    Permet de mettre le chemin des fichiers en absolu dans la conf.
    Comme ça on peut lancer pytest de n'importe où.

    Args:
        conf_name ([type]): [description]
        conf_temp ([type]): [description]
        data_dir ([type]): [description]
    """
    data = JsonFile(conf_name).load()
    # On va changer les choses
    for bulletin in data.keys():
        for component in data[bulletin]["components"]:
            for level in component["levels"]:
                for evt in level["elements_event"]:
                    evt["geos"]["file"] = data_dir / evt["geos"]["file"]
                    evt["field"]["file"] = data_dir / evt["field"]["file"]
                    if "altitude" in evt:
                        evt["altitude"]["filename"] = (
                            data_dir / evt["altitude"]["filename"]
                        )
    Path(conf_temp).parent.mkdir(parents=True, exist_ok=True)
    JsonFile(conf_temp).dump(data)


class TestOutput:
    """
    Permet de tester si les sorties sont cohérentes.
    """

    expected_prod: str = "expected_output.json"

    @pytest.fixture(scope="session")
    def local_working_dir(self, working_dir: Path) -> Path:
        """pytest fixture adding stuff to the tmp working directory"""

        settings = Settings()

        # prod config
        origin_config = TEST_DATA_DIR / "small_config.json"
        change_configuration(
            origin_config,
            settings.prod_config_filename,
            settings.data_dirname,
        )

        # expected
        origin_exp = TEST_DATA_DIR / self.expected_prod
        local_exp = working_dir / self.expected_prod
        local_exp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origin_exp, local_exp)

        # version
        version_data = {
            "version": "7659855c",
            "drafting_datetime": "2019-12-09T23:00:00+00:00",
            "reference_datetime": "2019-12-09T23:00:00+00:00",
            "production_datetime": "2019-12-10T00:00:00+00:00",
            "configuration_datetime": "2012-01-01T15:00:00+00:00",
        }
        JsonFile(settings.version_config_filename).dump(version_data)
        return working_dir

    @pytest.mark.skip
    @pytest.mark.filterwarnings("ignore: invalid value")
    def test_parameter(self, local_working_dir: Path):
        """
        test_parameter : On teste les paramètres pour un risque sur deux niveaux.
        Le premier niveau est seulement sur la plaine.
        Le second niveau est sur la plaine et sur la montagne.
        """
        # On lance le core
        manager = ProductionManager.load(filename=Settings().prod_config_filename)
        output_dir = Settings().output_dirname
        manager.compute(nproc=1)

        # On récupère le fichier produit
        output_filename = next(
            f for f in output_dir.iterdir() if f.name.startswith("prom_Test_config")
        )
        data = JsonFile(output_filename).load()
        data_ref = JsonFile(local_working_dir / self.expected_prod).load()
        # On pop ce qui retourne l'heure à laquelle PROMETHEE a ete produit.
        data_ref.pop("DateProduction")
        data.pop("DateProduction")
        # On va enlever les commentaires detailles (c'est pas le but du module de
        # tester qu'ils sont correct)
        data_ref["Components"]["Aleas"][0].pop("DetailComment")
        data_ref["Components"]["Aleas"][1].pop("DetailComment")
        data["Components"]["Aleas"][0].pop("DetailComment")
        data["Components"]["Aleas"][1].pop("DetailComment")

        assert data == data_ref


class TestOutputCDPDataModel:
    """
    Permet de tester si données de sorties sont au bon format avec Pydantic.
    """

    def test_unknown_customer(self):
        p = Datetime(2019, 1, 1)
        cdp_prod = CDPProduction(
            ProductionId="prod_id",
            ProductionName="prod_name",
            DateBulletin=p,
            DateProduction=p,
            DateConfiguration=p,
            Components=CDPComponents(),
        )
        assert cdp_prod.CustomerId == "unknown"
        assert cdp_prod.CustomerName == "unknown"

    def test_cdp_production(self):
        """
        teste la validité d'un objet Output à partir d'un fichier json
        """
        filename = TEST_DATA_DIR / "expected_output.json"
        cdp_prod = CDPProduction(**JsonFile(str(filename)).load())

        assert cdp_prod.CustomerId == "JeSuisUnClient"
        assert cdp_prod.CustomerName == "MySpecialCustomer"
        assert cdp_prod.ProductionName == "Test_config_name"
        assert cdp_prod.ProductionId == "Test_config"
        assert cdp_prod.DateBulletin == Datetime("2019-12-10T00:00:00+00:00")
        assert cdp_prod.DateProduction == Datetime("2020-10-05T14:57:41+00:00")
        assert cdp_prod.DateConfiguration == Datetime("2012-01-01T15:00:00+00:00")
        assert cdp_prod.Components == CDPComponents(
            Aleas=[
                CDPAlea(
                    ComponentId="my_super_component",
                    ComponentName="my_name",
                    Period=CDPPeriod(
                        PeriodId="Les 24 prochaines heures",
                        PeriodName="J-J+24H",
                        DateDebutPeriode=Datetime(
                            2019,
                            12,
                            10,
                            0,
                            0,
                        ),
                        DateFinPeriode=Datetime(
                            2019,
                            12,
                            10,
                            2,
                            0,
                        ),
                    ),
                    GeoId="FirstArea",
                    GeoName="unknown",
                    HazardId="temp_test",
                    HazardName="Mon super risque",
                    Dataset=CDPDataset(
                        ShortSummary=CDPSummary(
                            ValidityDate=None,
                            Level=1,
                            Values=[
                                CDPValueParam(
                                    ValueType="density",
                                    Unit="1",
                                    Value=0.77,
                                    Param=None,
                                ),
                                CDPValueParam(
                                    ValueType="max_plain",
                                    Unit="°C",
                                    Value=5.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                                CDPValueParam(
                                    ValueType="min_plain",
                                    Unit="°C",
                                    Value=-0.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                                CDPValueParam(
                                    ValueType="occurrence",
                                    Unit="1",
                                    Value=1.0,
                                    Param=None,
                                ),
                                CDPValueParam(
                                    ValueType="rep_value_plain",
                                    Unit="°C",
                                    Value=4.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                            ],
                        ),
                        Summary=[
                            CDPSummary(
                                ValidityDate=Datetime(
                                    2019,
                                    12,
                                    10,
                                    1,
                                    0,
                                ),
                                Level=0,
                                Values=[
                                    CDPValueParam(
                                        ValueType="density",
                                        Unit="1",
                                        Value=0.29,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="max_plain",
                                        Unit="°C",
                                        Value=3.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="min_plain",
                                        Unit="°C",
                                        Value=-2.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="occurrence",
                                        Unit="1",
                                        Value=0.0,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="rep_value_plain",
                                        Unit="°C",
                                        Value=2.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                ],
                            ),
                            CDPSummary(
                                ValidityDate=Datetime(
                                    2019,
                                    12,
                                    10,
                                    3,
                                    0,
                                ),
                                Level=1,
                                Values=[
                                    CDPValueParam(
                                        ValueType="density",
                                        Unit="1",
                                        Value=0.68,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="max_plain",
                                        Unit="°C",
                                        Value=5.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="min_plain",
                                        Unit="°C",
                                        Value=-0.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="occurrence",
                                        Unit="1",
                                        Value=1.0,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="rep_value_plain",
                                        Unit="°C",
                                        Value=4.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    DetailComment="Alerte cette fin de nuit de lundi à mardi. La "
                    "température atteint 4 °C.",
                ),
                CDPAlea(
                    ComponentId="my_super_component",
                    ComponentName="my_name",
                    Period=CDPPeriod(
                        PeriodId="Les 24 prochaines heures",
                        PeriodName="J-J+24H",
                        DateDebutPeriode=Datetime(
                            2019,
                            12,
                            10,
                            0,
                            0,
                        ),
                        DateFinPeriode=Datetime(
                            2019,
                            12,
                            10,
                            2,
                            0,
                        ),
                    ),
                    GeoId="SecondArea",
                    GeoName="unknown",
                    HazardId="temp_test",
                    HazardName="Mon super risque",
                    Dataset=CDPDataset(
                        ShortSummary=CDPSummary(
                            ValidityDate=None,
                            Level=1,
                            Values=[
                                CDPValueParam(
                                    ValueType="density",
                                    Unit="1",
                                    Value=0.78,
                                    Param=None,
                                ),
                                CDPValueParam(
                                    ValueType="max_plain",
                                    Unit="°C",
                                    Value=5.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                                CDPValueParam(
                                    ValueType="min_plain",
                                    Unit="°C",
                                    Value=-2.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                                CDPValueParam(
                                    ValueType="occurrence",
                                    Unit="1",
                                    Value=1.0,
                                    Param=None,
                                ),
                                CDPValueParam(
                                    ValueType="rep_value_plain",
                                    Unit="°C",
                                    Value=4.0,
                                    Param=CDPParam(Name="T__HAUTEUR", Stepsize=None),
                                ),
                            ],
                        ),
                        Summary=[
                            CDPSummary(
                                ValidityDate=Datetime(
                                    2019,
                                    12,
                                    10,
                                    1,
                                    0,
                                ),
                                Level=1,
                                Values=[
                                    CDPValueParam(
                                        ValueType="density",
                                        Unit="1",
                                        Value=0.33,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="max_plain",
                                        Unit="°C",
                                        Value=3.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="min_plain",
                                        Unit="°C",
                                        Value=-2.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="occurrence",
                                        Unit="1",
                                        Value=1.0,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="rep_value_plain",
                                        Unit="°C",
                                        Value=2.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                ],
                            ),
                            CDPSummary(
                                ValidityDate=Datetime(
                                    2019,
                                    12,
                                    10,
                                    3,
                                    0,
                                ),
                                Level=1,
                                Values=[
                                    CDPValueParam(
                                        ValueType="density",
                                        Unit="1",
                                        Value=0.69,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="max_plain",
                                        Unit="°C",
                                        Value=5.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="min_plain",
                                        Unit="°C",
                                        Value=-0.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                    CDPValueParam(
                                        ValueType="occurrence",
                                        Unit="1",
                                        Value=1.0,
                                        Param=None,
                                    ),
                                    CDPValueParam(
                                        ValueType="rep_value_plain",
                                        Unit="°C",
                                        Value=4.0,
                                        Param=CDPParam(Name="T__HAUTEUR", Stepsize=2),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    DetailComment="Alerte sur toute la période et toute la zone. La "
                    "température atteint 4 °C.",
                ),
            ],
            Text=None,
        )

        cdp_prod = cdp_prod.append(cdp_prod)
        assert len(cdp_prod.Components.Aleas) == 4

    def test_cdp_period_from_composite(self):
        assert CDPPeriod.from_composite(
            Period(
                id="idPeriod",
                name=None,
                start=Datetime(2019, 12, 10, 1),
                stop=Datetime(2019, 12, 10, 3),
            )
        ) == CDPPeriod(
            PeriodId="idPeriod",
            DateDebutPeriode="2019-12-10T01:00:00+00:00",
            DateFinPeriode="2019-12-10T03:00:00+00:00",
            PeriodName="Du 2019-12-10T01:00:00+00:00 au 2019-12-10T03:00:00+00:00",
        )

    def test_cdp_alea(self):
        """
        teste la validité des objets fils de Output
        """

        period = CDPPeriod(
            PeriodId="idPeriod",
            DateDebutPeriode="2019-12-10T01:00:00+00:00",
            DateFinPeriode="2019-12-10T03:00:00+00:00",
            PeriodName="Du 2019-12-10T01:00:00+00:00 au 2019-12-10T03:00:00+00:00",
        )

        assert period.PeriodId == "idPeriod"
        assert period.DateDebutPeriode == Datetime("2019-12-10T01:00:00+00:00")
        assert period.DateFinPeriode == Datetime("2019-12-10T03:00:00+00:00")
        assert (
            period.PeriodName
            == "Du 2019-12-10T01:00:00+00:00 au 2019-12-10T03:00:00+00:00"
        )

        dataset = CDPDataset(
            **{
                "ShortSummary": {
                    "Level": 0,
                    "Values": [
                        {
                            "ValueType": "max_plain",
                            "Unit": "celsius",
                            "Value": 5,
                            "Param": {"Name": "T__HAUTEUR2"},
                        }
                    ],
                },
                "Summary": [
                    {
                        "ValidityDate": "2021-02-12T08:00:00",
                        "Level": 0,
                        "Values": [{"ValueType": "density", "Unit": "1", "Value": 0}],
                    }
                ],
            }
        )

        assert dataset.ShortSummary.Level == 0
        assert len(dataset.ShortSummary.Values) == 1
        assert dataset.ShortSummary.Values[0].Unit == "celsius"
        assert dataset.Summary[0].ValidityDate == Datetime("2021-02-12T08:00:00")
        assert dataset.Summary[0].Values[0].ValueType == "density"

        alea = CDPAlea(
            Period=period,
            ComponentName="MSB CD31",
            ComponentId="f7a7109a-446f-455a-90b7-43182ea593d0",
            HazardId="e0c80aab-4e8d-453b-a931-57d7c7a8a413",
            HazardName="Vent",
            GeoId="354ec7d2-bb08-4c84-bdef-8ac30aa38426",
            GeoName="Haute-Garonne",
            Dataset=dataset,
            DetailComment="R.A.S.",
        )

        assert alea.ComponentName == "MSB CD31"
        assert alea.HazardName == "Vent"
        assert alea.DetailComment == "R.A.S."
        assert isinstance(alea.Period, CDPPeriod)
        assert isinstance(alea.Dataset, CDPDataset)
