from dataclasses import dataclass, field
from typing import Dict
from django.conf import settings

DEFAULT_BODY = {
    "label": "---",
    "description": "Sample description",
    "trigger": {
        "simpleTrigger": {
            "timezone": "America/Costa_Rica",
            "startType": 1,
            "occurrenceCount": 1,
            "recurrenceInterval": 1,
            "recurrenceIntervalUnit": "DAY"
        }
    },
    "baseOutputFilename": "-----",
    "exportType": "DEFAULT",
    "outputLocale": "es_CR",
    "outputTimeZone": "America/Costa_Rica",
    "source": {
        "reportUnitURI": "--------",
        "parameters": {
            "parameterValues": {}  # parameter
        }
    },
    "outputFormats": {
        "outputFormat": [
            "PDF"
        ]
    },
    "repositoryDestination": {
        "folderURI": "/CARPETA_DE_PRUEBA",
        "overwriteFiles": True,
        "sequentialFilenames": False,
        "saveToRepository": False,
        "usingDefaultReportOutputFolderURI": False,
        "outputFTPInfo": {}
    }
}


DEFAULT_URL = 'http://jasperserver.dev.istmocenter.com/jasperserver/rest_v2/jobs/'


OUTPUT_FTP_INFO = {
    "userName": "system",
    "password": "None123",
    "folderPath": "----",
    "serverName": "nfs.dev.istmocenter.com",
    "type": "sftp",
    "port": 22,
    "implicit": True,
    "pbsz": 0,
    "propertiesMap": {}
}


def get_default_body() -> Dict:
    return settings.PDF_DEFAULT_BODY if hasattr(
        settings, 'PDF_DEFAULT_BODY') else DEFAULT_BODY


def get_default_url() -> str:
    return settings.PDF_DEFAULT_URL if hasattr(
        settings, 'PDF_DEFAULT_URL') else DEFAULT_URL


def get_default_ftp() -> Dict:
    return settings.PDF_OUTPUT_FTP_INFO if hasattr(
        settings, 'PDF_OUTPUT_FTP_INFO') else OUTPUT_FTP_INFO


@dataclass
class PdfItem:
    default_body: Dict = field(default_factory=get_default_body)
    default_url: str = field(default_factory=get_default_url)
    default_ftp: Dict = field(default_factory=get_default_ftp)
    username: str = settings.PDF_DEFAULT_USERNAME if hasattr(
        settings, 'PDF_DEFAULT_USERNAME') else 'jasperadmin'
    password: str = settings.PDF_DEFAULT_PASSWORD if hasattr(
        settings, 'PDF_DEFAULT_PASSWORD') else 'bitnami'


@dataclass
class ConfigItem:
    pdf: PdfItem = field(default_factory=lambda: PdfItem())


@dataclass
class NextCloudItem:
    """
    Clase de datos que representa los parámetros de configuración para la conexión de Nextcloud.

    Args:
        username (str): Nombre de usuario para autenticación en Nextcloud.
        password (str): Contraseña para autenticación en Nextcloud.
        host (str): URL del servidor Nextcloud.
    """
    username: str = settings.NEXTCLOUD_DEFAULT_USERNAME if hasattr(
        settings, 'NEXTCLOUD_DEFAULT_USERNAME') else 'istmocenter'
    password: str = settings.NEXTCLOUD_DEFAULT_PASSWORD if hasattr(
        settings, 'NEXTCLOUD_DEFAULT_PASSWORD') else 'pZWq7E85EEEun7g'
    host: str = settings.NEXTCLOUD_DEFAULT_HOST if hasattr(
        settings, 'NEXTCLOUD_DEFAULT_HOST') else 'http://nextcloudserver.dev.istmocenter.com'
    path_share: str = settings.NEXTCLOUD_PATH_SHARE if hasattr(
        settings, 'NEXTCLOUD_PATH_SHARE') else 'apps/sharingpath/istmocenter/'
    path_webdav: str = settings.NEXTCLOUD_PATH_WEBDAV if hasattr(
        settings, 'NEXTCLOUD_PATH_WEBDAV') else 'remote.php/webdav/'


next_cloud_config = NextCloudItem()
config = ConfigItem()
