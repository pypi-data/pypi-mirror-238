"""Tests for `indicam_client` package."""
import asyncio
import io

from aiohttp import web
from aioresponses import aioresponses

from indicam_client import indicam_client
from indicam_client import GaugeMeasurement


# Recurring valid values
INDICAM_ID = 1
INDICAM_HANDLE = "test_handle"
API_KEY = "Test API Key"
ROOT_URL = "https://app.hausnet.io/indicam/api"
HEADERS = {'Authorization': f'Token {API_KEY}'}


def test_indicam_id_found():
    """Test that a valid indicam handle produces the indicam key."""
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f'{ROOT_URL}/indicams/?handle={INDICAM_HANDLE}',
            status=200,
            payload=[{'id': INDICAM_ID}],
        )
        indicam_id = loop.run_until_complete(service_client.get_indicam_id(INDICAM_HANDLE))
        assert indicam_id == INDICAM_ID
        mock_server.assert_called_once_with(f'{ROOT_URL}/indicams/?handle={INDICAM_HANDLE}')


def test_indicam_id_not_found():
    """Test that an invalid handle is handled correctly."""
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/indicams/?handle={INDICAM_HANDLE + 'x'}",
            status=404,
            payload='',
        )
        camconfig = loop.run_until_complete(service_client.get_indicam_id(INDICAM_HANDLE + 'x'))
        assert camconfig is None
        mock_server.assert_called_once_with(f"{ROOT_URL}/indicams/?handle={INDICAM_HANDLE + 'x'}")


def test_camconfig_retrieved():
    """Test getting the camera configuration."""
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/indicams/{INDICAM_ID}/camconfig_current/",
            headers=HEADERS,
            status=200,
            payload={indicam_client.CAMCONFIG_MIN_KEY: 10, indicam_client.CAMCONFIG_MAX_KEY: 11},
        )
        camconfig = loop.run_until_complete(service_client.get_camconfig(INDICAM_ID))
        assert camconfig is not None
        assert 10 == camconfig.min_perc
        assert 11 == camconfig.max_perc
        mock_server.assert_called_once_with(f"{ROOT_URL}/indicams/{INDICAM_ID}/camconfig_current/")


def test_camconfig_retrieve_failed():
    """Test that when getting the camera configuration fails, None is returned."""
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/indicams/{INDICAM_ID}/camconfig_current/",
            status=404,
            payload=''
        )
        camconfig = loop.run_until_complete(service_client.get_camconfig(INDICAM_ID))
        assert camconfig is None
        mock_server.assert_called_once_with(f"{ROOT_URL}/indicams/{INDICAM_ID}/camconfig_current/")


def test_camconfig_created():
    """ Test that a camconfig can be created. """
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.post(
            f"{ROOT_URL}/camconfigs/",
            status=201,
        )
        new_camconfig = indicam_client.CamConfig(min_perc=11, max_perc=13)
        success = loop.run_until_complete(service_client.create_camconfig(INDICAM_ID, new_camconfig))
        assert success is True
        mock_server.assert_called_once_with(
            f"{ROOT_URL}/camconfigs/",
            method='POST',
            data=({'indicam': INDICAM_ID, 'full_perc_from_top': 13, 'empty_perc_from_bottom': 11},)
        )


def test_camconfig_not_created():
    """ Test that an error creating a new camconfig is handled. """
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.post(
            f"{ROOT_URL}/camconfigs/",
            status=404,
        )
        new_camconfig = indicam_client.CamConfig(min_perc=11, max_perc=13)
        success = loop.run_until_complete(service_client.create_camconfig(INDICAM_ID, new_camconfig))
        assert success is False
        mock_server.assert_called_once_with(
            f"{ROOT_URL}/camconfigs/",
            method='POST',
            data=({'indicam': INDICAM_ID, 'full_perc_from_top': 13, 'empty_perc_from_bottom': 11},)
        )


def test_image_uploaded() -> None:
    """ Test the image upload function. """
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.post(
            f"{ROOT_URL}/images/{INDICAM_ID}/upload/",
            status=200,
            payload={"image_id": 5678},
        )
        dummy_img = b"Hello"
        image_id = loop.run_until_complete(service_client.upload_image(INDICAM_ID, dummy_img))
        assert 5678 == image_id
        mock_server.assert_called_once()


def test_image_upload_fails() -> None:
    """ Test the image upload function when it fails. """
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.post(
            f"{ROOT_URL}/images/{INDICAM_ID}/upload/",
            status=404,
            body="error in ....",
        )
        image_id = loop.run_until_complete(service_client.upload_image(INDICAM_ID, b"Hello"))
        assert not image_id
        mock_server.assert_called_once()


def test_get_measurement() -> None:
    """ Test getting a measurement. """
    test_measurement = {
        'id': 1234,
        'prediction_model': 5,
        'error': 0,
        'value': 30.0,
        'gauge_left_col': 10,
        'gauge_right_col': 100,
        'gauge_top_row': 5,
        'gauge_bottom_row': 500,
        'float_top_col': 200,
        'decorated_image': 'http://dummyhost.com/media/images/uid_1/testdev/20230821163518545474-decorated-v5.jpg',
        'src_image': 5678,
    }
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/measurements/?src_image={5678}",
            status=200,
            payload=[test_measurement, ]
        )
        measurement = loop.run_until_complete(service_client.get_measurement(5678))
        expected_measurement = GaugeMeasurement(
            body_left=int(test_measurement['gauge_left_col']),
            body_right=int(test_measurement['gauge_right_col']),
            body_top=int(test_measurement['gauge_top_row']),
            body_bottom=int(test_measurement['gauge_bottom_row']),
            float_top=int(test_measurement['float_top_col']),
            value=float(test_measurement['value'])
        )
        assert expected_measurement == measurement
        mock_server.assert_called_once_with(f"{ROOT_URL}/measurements/?src_image={5678}")


def test_get_measurement_failed() -> None:
    """ Test a failed measurement retrieval. """
    test_measurement = {
        'id': 1234,
        'prediction_model': 5,
        'error': 2,
        'value': 0.0,
        'gauge_left_col': None,
        'gauge_right_col': None,
        'gauge_top_row': None,
        'gauge_bottom_row': None,
        'float_top_col': None,
        'decorated_image': None,
        'src_image': 5678,
    }
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/measurements/?src_image={5678}",
            status=200,
            payload=[test_measurement, ]
        )
        measurement = loop.run_until_complete(service_client.get_measurement(5678))
        assert measurement is None
        mock_server.assert_called_once_with(f"{ROOT_URL}/measurements/?src_image={5678}")


def test_measurement_not_available() -> None:
    """ Test that a measurement not yet available is detected. """
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/measurements/?src_image={5678}",
            status=404,
            payload=""
        )
        ready = loop.run_until_complete(service_client.measurement_ready(5678))
        assert ready is False
        mock_server.assert_called_once_with(f"{ROOT_URL}/measurements/?src_image={5678}")


def test_measurement_available() -> None:
    """ Test that a measurement that is available is detected. """
    test_measurement = {
        'id': 1234,
        'prediction_model': 5,
        'error': 2,
        'value': 0.0,
        'gauge_left_col': None,
        'gauge_right_col': None,
        'gauge_top_row': None,
        'gauge_bottom_row': None,
        'float_top_col': None,
        'decorated_image': None,
        'src_image': 5678,
    }
    loop = asyncio.get_event_loop()
    service_client = indicam_client.IndiCamServiceClient(ROOT_URL, api_key=API_KEY)
    with aioresponses() as mock_server:
        mock_server.get(
            f"{ROOT_URL}/measurements/?src_image={5678}",
            status=200,
            payload=[test_measurement,]
        )
        ready = loop.run_until_complete(service_client.measurement_ready(5678))
        assert ready
        mock_server.assert_called_once_with(f"{ROOT_URL}/measurements/?src_image={5678}")
