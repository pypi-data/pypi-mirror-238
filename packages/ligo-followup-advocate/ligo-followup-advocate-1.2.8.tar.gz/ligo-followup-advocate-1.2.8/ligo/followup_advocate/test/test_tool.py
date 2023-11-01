import json
import os

# import astropy.utils.data
import pkg_resources
import pytest

from ..tool import main


class MockGraceDb(object):

    def __init__(self, service):
        assert service == 'https://gracedb.invalid/api/'
        self.service_url = service

    def _open(self, graceid, filename):
        if '.fits.gz' in filename:
            # url = ('https://dcc.ligo.org/public/0145/T1700453/001/'
            #        'LALInference_v1.fits.gz')
            # filename = astropy.utils.data.download_file(url, cache=True)
            filename = os.path.join('data', graceid, filename)
            return open(pkg_resources.resource_filename(__name__,
                                                        filename), 'rb')
        else:
            filename = os.path.join('data', graceid, filename)
            if 'bayestar-gbm' in filename:
                filename += '.gz'
                return open(pkg_resources.resource_filename(
                    __name__, filename), 'rb')

            elif '.fits' in filename:
                return open(pkg_resources.resource_filename(
                    __name__, filename), 'rb')

            else:
                f = open(pkg_resources.resource_filename(__name__, filename))

                def get_json():
                    return json.load(f)

                f.json = get_json
                return f

    def superevent(self, graceid):
        return self._open(graceid, 'superevent.json')

    def event(self, graceid):
        return self._open(graceid, 'event.json')

    def logs(self, graceid):
        return self._open(graceid, 'logs.json')

    def voevents(self, graceid):
        return self._open(graceid, 'voevents.json')

    def files(self, graceid, filename=None, raw=True):
        if filename is None:
            return self._open(graceid, 'files.json')
        else:
            return self._open(graceid, os.path.join('files', filename))


def remove_nones(list):
    return [x for x in list if x is not None]


@pytest.fixture
def mock_gracedb(monkeypatch):
    return monkeypatch.setattr('ligo.gracedb.rest.GraceDb', MockGraceDb)


@pytest.fixture
def mock_webbrowser_open(mocker):
    return mocker.patch('webbrowser.open')


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_cbc_compose(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose', 'S1234']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_burst_compose(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose', 'S2468']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_skymap_update(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_update', 'S5678', ['sky_localization']]))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_raven_update(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_update', 'S5678', ['raven']]))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_general_update(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_update', 'S5678',
                      ['sky_localization', 'p_astro', 'em_bright', 'raven']]))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_classification_update(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_update', 'S5678', ['p_astro', 'em_bright']]))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_compose_mailto(mock_gracedb, mock_webbrowser_open, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose', '--mailto', 'S1234']))
    assert mock_webbrowser_open.called_once()


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_raven_with_initial_circular(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_raven', 'S1234']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_raven_with_snews(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_raven', 'S2468']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_raven_without_initial_circular(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_raven', 'S5678']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_medium_latency_cbc_only_detection(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_grb_medium_latency', 'E1235']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_medium_latency_cbc_detection(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_grb_medium_latency', 'E1234']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_medium_latency_cbc_burst_detection(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_grb_medium_latency', 'E1122',
                       '--use_detection_template']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_medium_latency_cbc_exclusion(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_grb_medium_latency', 'E1134']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_medium_latency_cbc_burst_exclusion(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_grb_medium_latency', 'E2244',
                       '--use_exclusion_template']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_llama_neutrino_track(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_llama', 'S2468']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_llama_icecube_alert(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_llama', 'S2468',
                       '--icecube_alert', 'IceCubeCascade-230430a']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_retraction(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_retraction', 'S1234']))


@pytest.mark.parametrize('wrap_text', [None, '--remove_text_wrap'])
def test_retraction_early_warning(mock_gracedb, wrap_text):
    main(remove_nones(['--service', 'https://gracedb.invalid/api/', wrap_text,
                       'compose_retraction', 'S5678']))
