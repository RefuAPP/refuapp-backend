from io import BytesIO

import geojson
import requests
from PIL import Image
from geojson import Feature
from requests.exceptions import ConnectionError

from models.admins import Admins
from models.database import get_db
from models.supervisors import Supervisors
from schemas.refuge import CreateRefugeRequest, Coordinates, Capacity
from security.security import get_password_hash
from services.refuges import create_refuge

LONGITUDE_INDEX = 0
LATITUDE_INDEX = 1

PROPERTIES = 'properties'
GEOMETRY = 'geometry'
NAME = 'name'
REGION = 'region'
IMAGE = 'photo'
ALTITUDE = 'altitude'
COORDINATES = 'coordinates'
CAPACITY_WINTER = 'cap_hiver'
CAPACITY_SUMMER = 'cap_ete'

IMAGE_SOURCE_PATH = 'https://www.pyrenees-refuges.com/media/photo/'
IMAGE_DESTINATION_PATH = 'static/images/refuges/'

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


class InvalidRequest(Exception):
    pass


class CreateRefugeRequestBuilder:
    def __init__(self):
        self.name = None
        self.image = None
        self.region = None
        self.altitude = None
        self.coordinates_latitude = None
        self.coordinates_longitude = None
        self.capacity_winter = None
        self.capacity_summer = None

    def set_name(self, name: str) -> 'CreateRefugeRequestBuilder':
        if not name:
            raise InvalidRequest("Refuge name is empty")

        if not name.strip(' ')[0].istitle():
            name = name.strip(' ')[0].upper() + name.strip(' ')[1:]

        self.name = name
        return self

    def set_image(self, image: str) -> 'CreateRefugeRequestBuilder':
        if not image:
            self.image = image

        self.image = image
        self._save_image_to_static()
        return self

    def set_region(self, region: str) -> 'CreateRefugeRequestBuilder':
        if not region:
            raise InvalidRequest("Refuge region is empty")

        if not region.istitle():
            self.region = region[0].upper() + region[1:]
        else:
            self.region = region
        return self

    def set_altitude(self, altitude: str):
        if not altitude:
            raise InvalidRequest("Refuge altitude is empty")

        try:
            self.altitude = int(altitude)
        except ValueError:
            raise InvalidRequest(
                f"Refuge altitude is an invalid integer ({altitude})"
            )
        return self

    def set_latitude(self, latitude: str):
        if not latitude:
            raise InvalidRequest("Refuge latitude is empty")

        try:
            self.coordinates_latitude = float(latitude)
        except ValueError:
            raise InvalidRequest(
                f"Refuge latitude is an invalid float ({latitude})"
            )
        return self

    def set_longitude(self, longitude: str):
        if not longitude:
            raise InvalidRequest("Refuge longitude is empty")

        try:
            self.coordinates_longitude = float(longitude)
        except ValueError:
            raise InvalidRequest(
                f"Refuge longitude is an invalid float ({longitude})"
            )
        return self

    def set_capacity_winter(self, capacity_winter: str):
        if not capacity_winter:
            raise InvalidRequest("Refuge winter capacity is empty")

        try:
            self.capacity_winter = int(capacity_winter)
        except ValueError:
            raise InvalidRequest(
                f"Refuge winter capacity is an invalid integer ({capacity_winter})"
            )
        return self

    def set_capacity_summer(self, capacity_summer: str):
        if not capacity_summer:
            raise InvalidRequest("Refuge summer capacity is empty")

        try:
            self.capacity_summer = int(capacity_summer)
        except ValueError:
            raise InvalidRequest(
                f"Refuge summer capacity is an invalid integer ({capacity_summer})"
            )
        return self

    def build(self):
        if None in [
            self.name,
            self.image,
            self.region,
            self.altitude,
            self.coordinates_latitude,
            self.coordinates_longitude,
            self.capacity_winter,
            self.capacity_summer,
        ]:
            raise InvalidRequest("Refuge has empty data, skipping...")

        return CreateRefugeRequest(
            name=self.name,
            image=self.image,
            region=self.region,
            altitude=self.altitude,
            coordinates=Coordinates(
                latitude=self.coordinates_latitude,
                longitude=self.coordinates_longitude,
            ),
            capacity=Capacity(
                winter=self.capacity_winter,
                summer=self.capacity_summer,
            ),
        )

    def _save_image_to_static(self) -> None:
        try:
            response = requests.get(
                f"{IMAGE_SOURCE_PATH}{self.image}", headers=headers
            )
            image = Image.open(BytesIO(response.content))
            image.save(f"{IMAGE_DESTINATION_PATH}{self.image}")
        except ConnectionError:
            raise InvalidRequest(
                f"Refuge image is an invalid url ({self.image})"
            )


def build_refuge_request(refuge_json: Feature) -> CreateRefugeRequest:
    properties = refuge_json[PROPERTIES]
    coordinates = refuge_json[GEOMETRY][COORDINATES]

    refuge_request_builder = CreateRefugeRequestBuilder()
    (
        refuge_request_builder.set_name(properties[NAME])
        .set_region(properties[REGION])
        .set_image(properties[IMAGE])
        .set_altitude(properties[ALTITUDE])
        .set_latitude(coordinates[LATITUDE_INDEX])
        .set_longitude(coordinates[LONGITUDE_INDEX])
        .set_capacity_winter(properties[CAPACITY_WINTER])
        .set_capacity_summer(properties[CAPACITY_SUMMER])
    )

    return refuge_request_builder.build()


if __name__ == '__main__':
    db = next(get_db())

    with open('refuges.geojson') as f:
        gj = geojson.load(f)
        features = gj['features']
        errors = 0
        print(f"[INFO]: {len(features)} refuges found")
        for refuge in features:
            try:
                refuge_request = build_refuge_request(refuge)
                create_refuge(refuge_request, db)
            except InvalidRequest as e:
                errors += 1
                print(f"[INFO]: {e}")
        print(
            f"[INFO]: {len(features) - errors} refuges created, {errors} errors"
        )


def create_admins():
    db = next(get_db())
    if db.query(Admins).filter_by(username='admin').first() is None:
        admin = Admins(
            username='admin',
            password=get_password_hash('admin'),
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)


def create_supervisors():
    db = next(get_db())
    if db.query(Supervisors).filter_by(username='supervisor').first() is None:
        supervisor = Supervisors(
            username='supervisor',
            password=get_password_hash('supervisor'),
        )
        db.add(supervisor)
        db.commit()
        db.refresh(supervisor)
