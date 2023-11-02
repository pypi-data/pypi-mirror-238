import base64
import glob
import io
import json
import os
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

from PIL import Image

@dataclass
class V360MetadataFile:
    """
    Class for loading and processing v360 metadata file 0.json
    """
    path: str = None
    filename: str = None
    s3_object: dict = None
    data: dict = None

    def _get_v360_filename(self, path: str) -> str:
        """
        Get v360 filename from path
        """
        filename = os.path.basename(path)
        valid_filenames = ('0.json')
        if filename not in valid_filenames:
            raise ValueError(f"Provided v360 filename {filename} is not in {str(valid_filenames)}")
        return filename

    def get_scrabmle(self) -> str:
        """
        Return v360 scramble
        """
        return self.data.get('scramble')

    def load(self, path) -> dict:
        """
        Load v360 metadata file from path
        """
        self.path = path
        self.filename = self._get_v360_filename(self.path)

        with open(self.path, 'r') as f_in:
            self.data = json.load(f_in)

        return self.data

    def load_from_dict(self, data: dict):
        self.filename = "0.json"
        self.data = data

    def load_from_s3(self, s3_client, s3_path: str) -> dict:
        """
        Load v360 metadata file from s3
        """
        self.path = s3_path
        parsed_s3_path = urlparse(s3_path)
        self.filename = self._get_v360_filename(parsed_s3_path.path)
        self.s3_object = s3_client.get_object(Bucket=parsed_s3_path.netloc, Key=parsed_s3_path.path[1:])
        raw_data = self.s3_object['Body'].read()
        self.data = json.loads(raw_data)
        return self.data

    def save(self, path: str):
        """
        Save v360 metadata file to path
        """
        with open(path, 'w') as f_out:
            json.dump(self.data, f_out, separators=(',', ':'))

    def save_to_s3(self, s3_client, s3_path: str) -> str:
        """
        Save v360 metadata file to s3
        """
        parsed_s3_path = urlparse(s3_path)
        response = s3_client.upload_fileobj(
            Fileobj=io.BytesIO(json.dumps(self.data, separators=(',', ':')).encode('utf-8')),
            Bucket=parsed_s3_path.netloc,
            Key=parsed_s3_path.path[1:]
        )
        return response

    def set_resolution(self) -> list:
        img = Image.open(io.BytesIO(base64.b64decode(self.data['image'])))
        self.data['height'] = img.size[1]
        self.data['width'] = img.size[0]
        return self.data['height'], self.data['width']

    def erase_metadata(self):
        self.data['MachineName'] = 'Uni Diamonds'
        self.data['machineKey'] = 'uni-diamonds'

        if self.data.get('visionProfile', {}).get('currentProfile', {}).get('machineName'):
            self.data['visionProfile']['currentProfile']['machineName'] = 'Uni Diamonds'

        if self.data.get('visionProfile', {}).get('currentProfile', {}).get('machineNumber'):
            self.data['visionProfile']['currentProfile']['machineNumber'] = 'uni-diamonds'

        if self.data.get('visionProfile', {}).get('lockedProfile', {}).get('machineName'):
            self.data['visionProfile']['lockedProfile']['machineName'] = 'Uni Diamonds'

        if self.data.get('visionProfile', {}).get('lockedProfile', {}).get('machineNumber'):
            self.data['visionProfile']['lockedProfile']['machineNumber'] = 'uni-diamonds'


@dataclass
class V360FrameFile:
    """
    Class for loading and processing v360 frame files 1.json, 2.json, 3.json, 4.json, 5.json, 6.json, 7.json
    """
    path: str = None
    filename: str = None
    s3_object: dict = None
    data: list = None

    def _get_v360_filename(self, path: str) -> str:
        """
        Get v360 filename from path
        """
        filename = os.path.basename(path)
        valid_filenames = ('1.json', '2.json', '3.json', '4.json', '5.json', '6.json', '7.json')
        if filename not in valid_filenames:
            raise ValueError(f"Provided v360 filename {filename} is not in {str(valid_filenames)}")
        return filename

    def load(self, path) -> dict:
        """
        Load v360 frame file from path
        """
        self.path = path
        self.filename = self._get_v360_filename(self.path)

        with open(self.path, 'r') as f_in:
            if self.filename == '7.json':
                raw_data = f_in.read()
                fixed_raw_data = re.sub(",]$", "]", raw_data).encode()
                self.data = json.loads(fixed_raw_data)
            else:
                self.data = json.load(f_in)
        return self.data

    def load_from_list(self, name: str, data: list):
        self.filename = name
        self.data = data

        return self.data

    def load_from_s3(self, s3_client, s3_path: str) -> list:
        """
        Load v360 frame file from s3
        """
        self.path = s3_path
        parsed_s3_path = urlparse(s3_path)
        self.filename = self._get_v360_filename(parsed_s3_path.path)
        self.s3_object = s3_client.get_object(Bucket=parsed_s3_path.netloc, Key=parsed_s3_path.path[1:])
        raw_data = self.s3_object['Body'].read()
        if self.filename == '7.json':
            fixed_raw_data = re.sub(",]$", "]", raw_data.decode()).encode()
            self.data = json.loads(fixed_raw_data)
        else:
            self.data = json.loads(raw_data)

        return self.data

    def save_as_images(self, path: str):
        """
        Save v360 frame file as images to path
        """
        for i, frame in enumerate(self.data):
            img = Image.open(io.BytesIO(base64.b64decode(frame)))
            img.save(os.path.join(path, f"{i}.jpg"))

    def save(self, path: str):
        """
        Save v360 frame file to path
        """
        raw_data = json.dumps(self.data, separators=(',', ':'))
        with open(path, 'w') as f_out:
            if self.filename == '7.json':
                raw_data = re.sub("]$", ",]", raw_data)
            f_out.write(raw_data)

    def save_to_s3(self, s3_client, s3_path: str) -> str:
        """
        Save v360 frame file to s3
        """
        parsed_s3_path = urlparse(s3_path)
        raw_data = json.dumps(self.data, separators=(',', ':'))
        if self.filename == '7.json':
            raw_data = re.sub("]$", ",]", raw_data)
        response = s3_client.upload_fileobj(
            Fileobj=io.BytesIO(raw_data.encode('utf-8')),
            Bucket=parsed_s3_path.netloc,
            Key=parsed_s3_path.path[1:]
        )
        return response


@dataclass
class V360:
    """
    Class for loading and processing v360 files
    """
    path: str = None
    metadata: V360MetadataFile = None
    s3_objects: list = None
    data: list = field(default_factory=list)
    webp_quality: int = 80
    still_image: str = None

    def get_scramble(self) -> list:
        """
        Return scramble for v360 file
        """
        return self.metadata.get_scrabmle()

    def load(self, metadata: V360MetadataFile, data: "list[V360FrameFile]"):
        """
        Load v360 file from preloaded metadata and frame files
        """
        self.metadata = metadata
        self.data = data

    def load_from_path(self, base_path: str):
        """
        Load v360 file from path
        """
        self.path = base_path
        for filepath in sorted(glob.glob(f"{base_path}/*.json")):
            if filepath.endswith('0.json'):
                self.metadata = V360MetadataFile()
                self.metadata.load(filepath)
            else:
                frame_file_data = V360FrameFile()
                frame_file_data.load(filepath)
                self.data.append(frame_file_data)

    def load_from_dict(self, data: dict):
        """
        Load v360 file from dict. Dict should contain metadata and frame files like this:
        {
            "0": {}, # metadata
            "1": [], # frame file 1
            ...
            "7": [] # frame file 7
        }
        """
        for key, object in data.items():
            if key == '0':
                self.metadata = V360MetadataFile()
                self.metadata.load_from_dict(object)
            else:
                frame_file_data = V360FrameFile()
                filename = f"{key}.json"
                frame_file_data.load_from_list(filename, object)
                self.data.append(frame_file_data)

    def load_from_list(self, data_list: list):
        """
        Load v360 file from list. List should contain metadata and frame files like this:
        [
            {}, # metadata
            [], # frame file 1
            ...
            []  # frame file 7
        ]
        """
        for index, object in enumerate(data_list):
            if index == 0:
                if type(object) is dict:
                    self.metadata = V360MetadataFile()
                    self.metadata.load_from_dict(object)
                else:
                    raise ValueError(
                        f"Error while trying to load the v360 video. The first element in list should be type of dict, but its {type(object)}."
                    )
            else:
                if type(object) is list:
                    frame_file_data = V360FrameFile()
                    filename = f"{index}.json"
                    frame_file_data.load_from_list(filename, object)
                    self.data.append(frame_file_data)
                else:
                    raise ValueError(
                        f"Error while trying to load the v360 video. The {index} element in list should be type of list, but its {type(object)}."
                    )

    def load_from_s3(self, s3_client, s3_path: str) -> None:
        """
        Load v360 file from s3
        """
        self.path = s3_path
        parsed_s3_path = urlparse(s3_path)
        bucket = parsed_s3_path.netloc
        objects = s3_client.list_objects(Bucket=bucket, Prefix=parsed_s3_path.path[1:])['Contents']
        self.s3_objects = [x for x in objects if x['Key'].endswith('.json')]
        for s3_object in self.s3_objects:
            if s3_object['Key'].endswith('0.json'):
                self.metadata = V360MetadataFile()
                self.metadata.load_from_s3(s3_client, f"s3://{bucket}/{s3_object['Key']}")
            else:
                frame_file = V360FrameFile()
                frame_file.load_from_s3(s3_client, f"s3://{bucket}/{s3_object['Key']}")
                self.data.append(frame_file)

    def save_as_images(self, base_path: str):
        """
        Save v360 file as images to path
        """
        for frame_file in self.data:
            frame_file.save_as_images(base_path)

    def save(self, base_path: str):
        """
        Save v360 file to path
        """
        self.metadata.save(os.path.join(base_path, self.metadata.filename))
        for frame_file in self.data:
            frame_file.save(os.path.join(base_path, frame_file.filename))

    def save_to_s3(self, s3_client, s3_path: str) -> str:
        """
        Save v360 files to s3
        """
        parsed_s3_path = urlparse(s3_path)
        bucket = parsed_s3_path.netloc
        key = parsed_s3_path.path[1:]
        self.metadata.save_to_s3(s3_client, f"s3://{bucket}/{key}/{self.metadata.filename}")
        for frame_file in self.data:
            frame_file.save_to_s3(s3_client, f"s3://{bucket}/{key}/{frame_file.filename}")

        if self.still_image:
            s3_client.upload_fileobj(
                Fileobj=io.BytesIO(base64.b64decode(self.still_image)),
                Bucket=bucket,
                Key=f"{key}/still.jpg"
            )

    def validate(self, check_frame_count: bool = False, allowed_frame_count: int = None, min_allowed_frame_count: int = None) -> bool:
        """
        Validate v360 video

        check_frame_count: bool - check if frame count is valid
        allowed_frame_count: int - check exact match of frame file count
        min_allowed_frame_count: int - check minimum frame file count required
        """
        if check_frame_count:
            if allowed_frame_count:
                if len(self.data) != allowed_frame_count:
                    raise RuntimeError(f"Invalid frame file count. Expected {allowed_frame_count}, got {len(self.data)}")

            if min_allowed_frame_count:
                if len(self.data) < min_allowed_frame_count:
                    raise RuntimeError(f"Invalid frame file count. Expected at least {min_allowed_frame_count}, got {len(self.data)}")

        check_image(base64.b64decode(self.metadata.data['image']))
        for frame_file in self.data:
            for frame in frame_file.data:
                check_image(base64.b64decode(frame))

        return True

    def _convert_image(self, image: Image) -> str:
        """
        Convert image to webp format
        """
        image_io = io.BytesIO()
        image.save(image_io, format='webp', quality=self.webp_quality)
        image_io.seek(0)
        return base64.b64encode(image_io.read()).decode('utf-8')

    def _convert_frame(self, frame: dict) -> dict:
        """
        Convert frame image to webp format
        """
        image = Image.open(io.BytesIO(base64.b64decode(frame)))
        frame = self._convert_image(image)
        return frame

    def _convert_frame_file(self, frame_file: V360FrameFile) -> V360FrameFile:
        """
        Convert frame file to webp format
        """
        frame_file.data = [self._convert_frame(x) for x in frame_file.data]
        return frame_file

    def _convert_metadata(self, metadata: V360MetadataFile) -> V360MetadataFile:
        """
        Convert metadata to webp format
        """
        image = Image.open(io.BytesIO(base64.b64decode(metadata.data['image'])))
        metadata.data['image'] = self._convert_image(image)
        return metadata

    def to_webp(self, quality: int = None):
        """
        Convert v360 file to webp format
        """
        if quality:
            self.webp_quality = quality
        self.data = [self._convert_frame_file(x) for x in self.data]
        self.metadata = self._convert_metadata(self.metadata)
        # if self.still_image:
        #     image = Image.open(io.BytesIO(base64.b64decode(self.still_image)))
        #     self.still_image = self._convert_image(image)
        self.metadata.data['image_format'] = 'webp'
        return self

    def set_resolution(self):
        self.metadata.set_resolution()

    def erase_metadata(self):
        self.metadata.erase_metadata()


def check_image(image: bytes) -> bool:
    try:
        img = Image.open(io.BytesIO(image))
        img.verify()
        img.close()
        img = Image.open(io.BytesIO(image))
        img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        img.close()
    except Exception as e:
        raise RuntimeError(f'Image format error: {e}')

    return True


def sort_images(unsorted_images: list) -> list:
    """
    Receive list of unsorted_images images.
    Sort images accoring to sort_order and return sorted list.
    """
    sort_order = [
        # 1.json
        0,
        127,
        191,
        63,
        # 2.json
        159,
        95,
        223,
        31,
        # 3.json
        15,
        111,
        143,
        239,
        79,
        207,
        175,
        47,
        # 4.json
        199,
        167,
        8,
        119,
        23,
        231,
        151,
        215,
        71,
        182,
        135,
        87,
        247,
        39,
        103,
        55,
        # 5.json
        211,
        203,
        195,
        243,
        51,
        187,
        123,
        35,
        99,
        75,
        131,
        163,
        91,
        43,
        115,
        67,
        251,
        155,
        3,
        83,
        139,
        219,
        19,
        179,
        11,
        27,
        147,
        227,
        171,
        59,
        235,
        107,
        # 6.json
        1,
        53,
        37,
        121,
        225,
        141,
        241,
        6,
        89,
        129,
        81,
        153,
        161,
        237,
        125,
        209,
        133,
        205,
        201,
        193,
        109,
        137,
        21,
        57,
        177,
        77,
        221,
        45,
        69,
        9,
        145,
        149,
        65,
        117,
        189,
        165,
        85,
        61,
        73,
        113,
        181,
        157,
        229,
        217,
        93,
        29,
        17,
        33,
        173,
        213,
        249,
        185,
        105,
        13,
        97,
        245,
        253,
        197,
        169,
        25,
        41,
        49,
        101,
        233,
        # 7.json
        56,
        2,
        122,
        138,
        120,
        44,
        98,
        202,
        74,
        70,
        118,
        188,
        160,
        198,
        206,
        194,
        252,
        152,
        230,
        5,
        80,
        208,
        236,
        200,
        238,
        28,
        20,
        34,
        183,
        12,
        42,
        178,
        64,
        174,
        132,
        148,
        126,
        86,
        216,
        128,
        240,
        102,
        114,
        94,
        48,
        154,
        108,
        84,
        116,
        130,
        144,
        58,
        76,
        96,
        250,
        66,
        124,
        218,
        46,
        214,
        36,
        10,
        142,
        82,
        186,
        232,
        16,
        136,
        184,
        180,
        190,
        244,
        228,
        210,
        26,
        156,
        52,
        40,
        90,
        60,
        222,
        4,
        196,
        14,
        248,
        68,
        242,
        92,
        224,
        168,
        204,
        24,
        104,
        192,
        220,
        78,
        254,
        166,
        7,
        30,
        88,
        50,
        150,
        112,
        18,
        226,
        164,
        22,
        106,
        32,
        110,
        212,
        170,
        100,
        146,
        246,
        158,
        54,
        134,
        140,
        38,
        176,
        62,
        234,
        72,
        162,
        172,
        255,
    ]

    return [unsorted_images[x[1]] for x in zip(unsorted_images, sort_order)]


def list_of_imgs_to_json(images: list) -> dict:
    """
    Get a list of ordered images.
    Return them as a dict, where each key represents the json file number (like 1.json) and each value is a data for it.
    """
    result = {}

    result["0"] = get_v360_metadata()
    result["1"] = images[0:4]
    result["2"] = images[4:8]
    result["3"] = images[8:16]
    result["4"] = images[16:32]
    result["5"] = images[32:64]
    result["6"] = images[64:128]
    result["7"] = images[128:256]

    return result


def get_v360_metadata():
    """
    Return dict for 0.json file.
    The important parameter is scramble, it determines the image order in json files.
    Should be kept the same for all constructed videos.
    """
    return {
        "remarks": "vs2%253Cbr%2f%253E0.30",
        "quality": "4",
        "height": "450",
        "width": "600",
        "version": "1",
        "visionProfile": {
            "currentProfile": {
                "visionProfile": "V360",
                "LevelHistory": {
                    "MinInputLevel": "20",
                    "MaxInputLevel": "255",
                    "MinOutputLevel": "0",
                    "MaxOutputLevel": "255",
                    "Gamma": "1"
                },
                "quality": "Ideal",
                "AV": "11",
                "TV": "1/30",
                "ISO": "ISO 200",
                "WB": "Custom",
                "K": "5200",
                "sharpness": "7",
                "contrast": "0",
                "saturation": "0",
                "colorTone": "0",
                "lightName": "v360",
                "lightTrackValue": "0,0,700,700,700,0,0,0,0,0",
                "stoneType": "V360",
                "crop": "3",
                "pictureStyle": "Auto",
                "colorRGB": "1,1,1",
                "width": "600",
                "height": "450",
                "R": "147",
                "G": "147",
                "B": "147",
                "tolerance": "10",
                "isFreeze": "False",
                "version": "1",
                "hostName": "VRM-2",
                "machineName": "Uni Diamonds",
                "machineNumber": "uni-diamonds",
                "cameraAppVersion": "5.0.0.35",
                "ImageQuality": "100",
                "OldRGB": "rgb(162,162,164)",
                "NewRGB": "rgb(154,154,154)",
                "MinInputLevel": "0",
                "MaxInputLevel": "0",
                "MinOutputLevel": "0",
                "MaxOutputLevel": "0",
                "Gamma": "0"
            },
            "lockedProfile": {
                "visionProfile": "V360",
                "LevelHistory": {
                    "MinInputLevel": "20",
                    "MaxInputLevel": "255",
                    "MinOutputLevel": "0",
                    "MaxOutputLevel": "255",
                    "Gamma": "1"
                },
                "quality": "4",
                "AV": "11",
                "TV": "1/25",
                "ISO": "ISO 200",
                "WB": "Custom",
                "K": "5200",
                "sharpness": "7",
                "contrast": "0",
                "saturation": "0",
                "colorTone": "0",
                "lightName": "v360",
                "lightTrackValue": "0,0,800,800,800,0,0,0,0,0",
                "stoneType": "V360",
                "crop": "20",
                "pictureStyle": "Auto",
                "colorRGB": "0",
                "width": "581",
                "height": "388",
                "R": "150",
                "G": "150",
                "B": "150",
                "tolerance": "10",
                "isFreeze": "False",
                "version": "1",
                "hostName": "VRM-2",
                "machineName": "Uni Diamonds",
                "machineNumber": "uni-diamonds",
                "cameraAppVersion": "5.0.0.35",
                "ImageQuality": "100",
                "OldRGB": "rgb(162,162,164)",
                "NewRGB": "rgb(154,154,154)",
                "MinInputLevel": "0",
                "MaxInputLevel": "0",
                "MinOutputLevel": "0",
                "MaxOutputLevel": "0",
                "Gamma": "0"
            }
        },
        "scramble": "1KYZqyR7dTUK+gYIBDNuR0fogoj+MZCVG1FaoU4twiaCl34k2+Kh/HqKbz9wCxlNlndQRyZzIPcs9MHM5DZHJ5G1eVIHxjOY0ySlnucTt+U6cJTfVgUBtZfFbZwrP+m78MigXL7wrlv2kVmXWx1JC5V6O1Vn6vYiD02aYtH7LdVKhqW926Fd6ItUodof0/EKMP37gRqNGLKaX4EO5jldy4k91ECAnoLhV9UhnugRY03PQqO5wLrmVUVODx7tpZ7K0nZrlwoiD5mR9xq1JZVtI5UZygYhwXUF9vYDufDixPWfzJk4APNzc1/tqayPiEdAXQbv7MsIZ6xDGBzTP095vn1Y6xg1zKh2cG74afzaFhV0EkI5pHeeN3Un2VW7kZMpssf//P4zqOOqMN8kxvZGKknVr0z28utV6qKUh31S9eoTyrgX8xMOUqUUd1KMI2q/eB03mc/UeVqjludCCce5NS6cY0rn0eTx1DDoKSU+CwxYtmA1Oj1awFT38oWyXvf8xGkrlNaOoUsv+UWSoQeA/nuI+wRasN8OqGG4na+bszc6Ti35kushMP5EQki1SbHjiz5GsZ/zr3JZuXR6LVIsCFsMKEQdUqcgA3JJ1sKwDliICzlnQLGICpsU+rrzxQcnINJhNESX4ovh912niZXyWpODSbV1iUO2sXUTzJHXI81ICyui0v1Gi+Rt+P98gvfFMuCmFj14MFp7uw7vWX6x773UyNzB6bw4HqCpuirgh8dOjHm6HNyi3MYdPf6TUEGj6cAZtujJCOUJvZWCso+5pBF185p05tfinzREOpy6l+4SOf0uXE188Zn+juPBUlKIcOANX8mPiwYQxdu+0j4bJjBwcwsTweBDOb3OuYH3gsk32Evji2gp6aKSBHRFiTDsnghrXhdRgcBJthcQZIqxJ+9pS6jcYcwKSAMktE5X46GinwUBBGCDWBE29jLM0QCrB6A1m6CB72ozA/oYWYkd+WCZSq8hJjRx/+H2rji7/M9qwD/Q4P5pnYuh6T8tJ7Bd",
        "softwareVersion": "5.0.0.35",
        "createdDate": "2020-08-16T10:48:32Z",
        "machineKey": "uni-diamonds",
        "MachineName": "Uni Diamonds",
        "ImageQuality": "100",
        "OldRGB": "rgb(162,162,164)",
        "NewRGB": "rgb(154,154,154)",
        "MinInputLevel": "0",
        "MaxInputLevel": "0",
        "MinOutputLevel": "0",
        "MaxOutputLevel": "0",
        "Gamma": "0",
        "Camera": "Canon EOS 6D Mark II",
        "CameraSerialNo": "413461720",
        "LensName": "EF100mm f/2.8 Macro USM",
        "StartTime": "10:47:16",
        "StopTime": "10:48:32",
        "TotalTime": "00:01:16"
    }
