from __future__ import annotations

import os
import base64
import logging
from nc_py_api._exceptions import NextcloudException
from nc_py_api import Nextcloud as Next
from v7e_utils.utils.config import next_cloud_config, NextCloudItem
from datetime import datetime
from PIL import Image
from io import BytesIO


logger = logging.getLogger(__name__)


def img_b64decode(img_encoded:str, extension:str)->bytes:
    """
        Descodifica la imagen y la guarda en el buffer.

        Args:
            img_encoded (str): Imagen codifica en base 64.
            extension (str): Extensión de la imgen.

        Returns:
            bytes: La imagen en bytes guarda en el buffer.
    """
    extension = extension.replace('.', '').upper()
    decoded_img = BytesIO(base64.b64decode(img_encoded))
    img_buffer = BytesIO()
    match = extension == 'JPG' or extension == 'JPEG'
    if match:
        extension = 'PNG'
    Image.open(decoded_img).save(img_buffer, extension)
    img_buffer.seek(0)
    return img_buffer

def exceeds_max_file_size_by_bytes(file:bytes, max_size:int=5242880) -> bool:
    """
        Verifica si el tamaño del archivo supera los 5MB.

        Args:
            file (bytes): El archivo en bytes guardo en el buffer.
            max_size (int): Tamaño máximo permitido para el archivo en bytes.

        Returns:
            bool: True si pasa el tamaño máximo, en caso contrario devuelve False.
    """
    size = file.getbuffer().nbytes
    return size > max_size


class Nextcloud:
    """
    Clase que encapsula la funcionalidad para interactuar con una instancia de Nextcloud.

    Args:
        config_parameters (NextCloudItem): Parámetros de configuración para la instancia de Nextcloud.

    Methods:
        get_file_url(): Obtiene la URL del archivo en Nextcloud.
        get_file_share_url(): Obtiene la URL de compartir del archivo en Nextcloud.
        get_file_name(): Obtiene el nombre del archivo.
        get_file_path(): Obtiene el path del archivo en Nextcloud.
        get_file_extension(): Obtiene la extensión del archivo.
        mkdir(): Crea un directorio en la instancia de Nextcloud.
        file_move(): Mueve un archivo de una carpeta a otra en Nextcloud.
        upload_file(): Sube un archivo a Nextcloud.
        path_exists(): Comprueba la existencia de una ruta en Nextcloud.
        download_file(): Descarga un archivo de Nextcloud.
        file_soft_delete(): Mueve un archivo de NextCloud a la carpeta temp.
    """

    def __init__(self, config_parameters: NextCloudItem | None=None) -> None:

        self.username = config_parameters.username if config_parameters else next_cloud_config.username
        self.password = config_parameters.password if config_parameters else next_cloud_config.password
        self.host = self._path_format(config_parameters.host) if config_parameters else self._path_format(next_cloud_config.host)
        # self.path_webdav = self._path_format(config_parameters.path_webdav) if config_parameters else self._path_format(next_cloud_config.path_webdav)
        self.path_share = self._path_format(config_parameters.path_share) if config_parameters else self._path_format(next_cloud_config.path_share)
        self.nc = Next(nextcloud_url=self.host,
                       nc_auth_user=self.username, 
                       nc_auth_pass=self.password)

    def get_file_url(self, path:str) -> str:
        """
        Obtiene la url del archivo en NextCloud.

        Args:
            path (str): Ruta del archivo.

        Returns:
            str: Ruta del archivo con el host de NextCloud.
        """
        return f'{self.host}{path}'
    
    def get_file_share_url(self, path:str) -> str:
        """
        Obtiene la url de compartir del archivo en NextCloud.

        Args:
            path (str): Ruta del archivo.

        Returns:
            str: Ruta del archivo con el host y path_share de NextCloud.
        """
        return f'{self.host}{self.path_share}{path}'

    # def get_file_webdav_url(self, path:str) -> str:
    #     """
    #     Obtiene la url de descarga del archivo en NextCloud.

    #     Args:
    #         path (str): Ruta del archivo.

    #     Returns:
    #         str: Ruta del archivo con el host y share_webdav de NextCloud.
    #     """
    #     return f'{self.host}{self.path_webdav}{path}'

    def get_file_name(self, url:str) -> str:
        """
        Obtiene el nombre del archivo.

        Args:
            url (str): Ruta del archivo.

        Returns:
            str: El nombre del archivo.
        """
        return os.path.basename(url)

    def get_file_path(self, url:str) -> str:
        """
        Obtiene el path del archivo de NextCloud.

        Args:
            url (str): Ruta del archivo.

        Returns:
            str: Path del archivo sin el host, path_webdav y path_share de NextCloud.
        """
        return url.replace(self.host, '').replace(self.path_share, '')
        # return url.replace(self.host, '').replace(self.path_share, '').replace(self.path_webdav, '')

    def get_file_extension(self, url:str) -> str:
        """
        Obtiene la extrensión del archivo.

        Args:
            url (str): Ruta del archivo.

        Returns:
            str: La extensión del archivo.
        """
        return url[url.rfind('.'):]

    def _path_format(self, path:str) -> str:
        """
        Agrega al final del path el '/' si este no viene.

        Args:
            path (str): Ruta a revisar.

        Returns:
            str: Ruta formateada.
        """
        if '/' == path[-1]:
            return path
        return f'{path}/'

    def mkdir(self, path: str) -> bool:
        """
        Crea un directorio y subdirectorios en la instancia de Nextcloud.

        Args:
            path (str): Ruta del directorio a crear.

        Returns:
            bool: True si el directorio se crea exitosamente, False si no.
        """
        path = path.strip()
        if path:
            try:
                # path = path of the directories to be created.
                # exist_ok= ignore error if any of pathname components already exists.
                self.nc.files.makedirs(path=path, exist_ok=True)
                return True
            except NextcloudException as e:
                logger.error(
                    f"nextcloud connection error: reason: {e.reason}, path:{path}, username:{self.username}, password:{self.password}, host:{self.host}")
        return False

    def file_move(self, file_url:str, folder_path_dest:str, new_file_name:str=None, overwrite:bool=False) -> str:
        """
        Mueve el archivo de una carpeta a otra en NextCloud.

        Args:
            file_url (str): Ruta del archivo.
            folder_path_dest (str): Ruta del directorio de destino. 
            new_file_name (str): Nuevo nombre que se le asigna al archivo.
            overwrite (bool): True para sobreescribir el archivo con el mismo nombre, False caso contrario. Defecto False.

        Returns:
            str: Ruta nueva del archivo.
        """
        file_name = f'{new_file_name}{self.get_file_extension(file_url)}' if new_file_name else self.get_file_name(file_url)
        path_dest = f'{self._path_format(folder_path_dest)}{file_name}'
        self.nc.files.move(path_src=self.get_file_path(file_url), path_dest=path_dest, overwrite=overwrite)
        return path_dest

    def upload_file(self, file: bytes, extension:str, new_name_file: str = None, folder_path: str = 'temp/') -> str:
        """
        Sube el archivo a NextCloud.

        Args:
            file (bytes): El archivo en bytes guardo en el buffer.
            extension (str): Extensión del archivo.
            new_file_name (str): Nuevo nombre que se le asigna al archivo.
            folder_path (str): Ruta del directorio de destino.

        Returns:
            str: Ruta nueva del archivo.
        """
        if not extension.startswith('.'):
            extension = f'.{extension}'
        folder_path = self._path_format(folder_path)
        file_path = f'{folder_path}{new_name_file}{extension}' if new_name_file else f'{folder_path}{int(datetime.timestamp(datetime.now()))}{extension}'    
        self.nc.files.upload_stream(path=file_path, fp=file)
        return file_path

    def path_exists(self, path:str) -> bool:
        """
        Comprueba la existencia del path en NextCloud.

        Args:
            path (str): Ruta a combrobar.

        Returns:
            bool: True si existe y False si no existe.
        """
        try:
            if path == '':
                return False
            self.nc.files.by_path(path)
            return True
        except NextcloudException:
            return False
    
    def download_file(self, path:str) -> bytes | None:
        """
        Descarga un archivo de NextCloud.

        Args:
            path (str): Ruta del archivo a descargar.

        Returns:
            bytes: Archivo en bytes o None en caso de no existir.
        """
        file = None
        if self.path_exists(path=path):
            file = self.nc.files.download(path)
        return file
    
    def file_soft_delete(self, path:str) -> str:
        """
        Mueve un archivo de NextCloud a la carpeta temp.

        Args:
            path (str): Ruta del archivo a eliminar.

        Returns:
            str: Ruta del archivo en la carpeta temp en Nextcloud.
        """
        file_name = self.get_file_name(path)
        path_dest = f'temp/{file_name}'
        if self.path_exists(path_dest):
            self.nc.files.delete(path_dest, not_fail=True)
        self.nc.files.move(path_src=path, path_dest=path_dest)
        return path_dest
