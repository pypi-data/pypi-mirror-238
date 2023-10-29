"""DICOM file Flywheel utils."""
import io
import re
import typing as t
from datetime import datetime

import pydicom
from fw_utils import AnyFile, get_datetime, open_any

from ..utils import birthdate_to_age
from .config import UID_PREFIX

DCM_BYTE_SIG_OFFSET = 128
DCM_BYTE_SIG = b"DICM"


def sniff_dcm(file: AnyFile) -> bool:
    """Look at file byte signature and determine if it is a DICOM."""
    with open_any(file, "rb") as fp:
        fp.seek(DCM_BYTE_SIG_OFFSET, 0)
        sig = fp.read(len(DCM_BYTE_SIG))
        return sig == DCM_BYTE_SIG


def generate_uid(
    prefix: t.Optional[str] = f"{UID_PREFIX}.2.",
    entropy_srcs: t.Optional[t.List[str]] = None,
) -> pydicom.uid.UID:
    """Return a 64 character UID which starts with the given prefix.

    Args:
        prefix (str, optional): UID prefix to use. Defaults to the Flywheel
            fw-file UID prefix for generation, "2.16.840.1.114570.2.".
        entropy_srcs (list[str], optional): List of strings to use SHA512 on
            when generating the UID characters after the prefix, making the
            result deterministic. Default is None, generating a random suffix.

    Reference:
        https://github.com/pydicom/pydicom/blob/v2.1.2/pydicom/uid.py#L382
    """
    return pydicom.uid.generate_uid(prefix=prefix, entropy_srcs=entropy_srcs)


def create_dcm(preamble=None, file_meta=None, **dcmdict) -> io.BytesIO:
    """Create and return a DICOM file as BytesIO object from a tag dict."""
    dcm = io.BytesIO()
    dataset = pydicom.FileDataset(dcm, create_dataset(**dcmdict))
    dataset.preamble = preamble or b"\x00" * 128
    dataset.file_meta = pydicom.dataset.FileMetaDataset()
    update_dataset(dataset.file_meta, file_meta)
    pydicom.dcmwrite(dcm, dataset, write_like_original=bool(file_meta))
    dcm.seek(0)
    return dcm


def create_dataset(**dcmdict) -> pydicom.Dataset:
    """Create and return a pydicom.Dataset from a simple tag dictionary."""
    dataset = pydicom.Dataset()
    update_dataset(dataset, dcmdict)
    return dataset


def update_dataset(dataset: pydicom.Dataset, dcmdict: dict) -> None:
    """Add dataelements to a dataset from the given tag dictionary."""
    dcmdict = dcmdict or {}
    for key, value in dcmdict.items():
        # if value is a list/tuple, it's expected to be a (VR,value) pair
        if isinstance(value, (list, tuple)):
            VR, value = value
        # otherwise it's just the value, so get the VR from the datadict
        else:
            VR = pydicom.datadict.dictionary_VR(key)
        dataset.add_new(key, VR, value)


def parse_datetime_str(value: str) -> t.Optional[datetime]:
    """Parse datetime string.

    Args:
        value (str): DICOM DT formatted timestamp: YYYYMMDDHHMMSS.FFFFFF&ZZXX
            The year is required, but everything else has defaults:
            month=day=1, hour=12, minute=second=microsecond=0

    Reference:
        http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    try:
        dt_obj = get_datetime(f"{value[:8]} {value[8:]}")
    except ValueError:
        return None
    if len(value) < 10:
        dt_obj = dt_obj.replace(hour=12)
    return dt_obj


def get_timestamp(
    dcm: t.Mapping[str, t.Any], tag_prefix: str = "Series"
) -> t.Optional[datetime]:
    """Get timestamp from Study-, Series- or Acquisition Date/Time tags.

    Args:
        dcm (dicom.DICOM): DICOM instance
        tag_prefix (str, optional): Date/time tag prefix: Study|Series|Acquisition
            Defaults to "Series".

    Reference of DA/TM/DT VR types:
        http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
    """
    assert tag_prefix in {"Study", "Series", "Acquisition"}
    datetime_str = ""
    if tag_prefix == "Acquisition" and dcm.get("AcquisitionDateTime"):
        datetime_str = dcm["AcquisitionDateTime"]
    elif dcm.get(f"{tag_prefix}Date"):
        date = dcm.get(f"{tag_prefix}Date")
        time = dcm.get(f"{tag_prefix}Time") or ""
        datetime_str = f"{date}{time}"
    elif tag_prefix != "Acquisition" and get_uid_timestamp(dcm, tag_prefix):
        datetime_str = t.cast(str, get_uid_timestamp(dcm, tag_prefix))
    else:
        return None
    # get offset from TimezoneOffsetFromUTC if not in the datetime string yet
    if not re.match(r"[+-]\d{4}$", datetime_str):
        offset = dcm.get("TimezoneOffsetFromUTC", "")
        if offset and offset[0] not in "+-":
            # make sure offset is sign-prefixed (sign optional in this tag)
            offset = f"+{offset}"
        datetime_str = f"{datetime_str}{offset}"
    return parse_datetime_str(datetime_str)


def get_uid_timestamp(
    dcm: t.Mapping[str, t.Any], tag_prefix: str = "Series"
) -> t.Optional[str]:
    """Attempt to get a timestamp string from the Study- or Series UID."""
    assert tag_prefix in {"Study", "Series"}
    uid = dcm.get(f"{tag_prefix}InstanceUID") or ""
    uid_timestamp_re = r"\d+(\.\d+)*\.(?P<timestamp>(19|20)\d{12,})(\.\d+)*"
    match = re.match(uid_timestamp_re, uid)
    if match:
        return match.group("timestamp")[:14]
    return None


def get_patient_name(
    dcm: t.Mapping[str, t.Any]
) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """Return firstname, lastname tuple from a DICOM."""
    name = dcm.get("PatientName")
    if not name:
        return None, None
    return parse_patient_name(name)


def parse_patient_name(name: str) -> t.Tuple[t.Optional[str], t.Optional[str]]:
    """Return firstname, lastname tuple from a PatientName string."""
    if "^" in name:
        lastname, _, firstname = name.partition("^")
    else:
        firstname, _, lastname = name.rpartition(" ")
    return (firstname.strip().title() or None, lastname.strip().title() or None)


def get_session_age(dcm: t.Mapping[str, t.Any]) -> t.Optional[int]:
    """Return patient age in seconds."""
    if dcm.get("PatientAge"):
        age_str = dcm.get("PatientAge", "")
        match = re.match(r"(?P<value>[0-9]+)(?P<scale>[dwmyDWMY])?", age_str)
        if match:
            # convert to days
            conversion = {"Y": 365.25, "M": 30, "W": 7, "D": 1}
            value = match.group("value")
            scale = (match.group("scale") or "Y").upper()
            return int(int(value) * conversion[scale] * 86400)

    birth_date = parse_datetime_str(dcm.get("PatientBirthDate", ""))  # type: ignore
    acq_timestamp = get_acquisition_timestamp(dcm)
    if not (birth_date and acq_timestamp):
        return None

    return birthdate_to_age(birth_date, acq_timestamp)


def get_session_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return session label.

    1. StudyDescription
    2. Session timestamp (YYYY-mm-ddTHH-MM-SS)
    3. StudyInstanceUID
    """
    label = dcm.get("StudyDescription")
    if not label and (ts := get_session_timestamp(dcm)):
        label = ts.strftime("%Y-%m-%dT%H-%M-%S")
    return label or dcm.get("StudyInstanceUID")


def get_session_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[datetime]:
    """Return session timestamp.

    1. StudyDate + Time
    2. StudyInstanceUID
    3. SeriesDate + Time
    4. SeriesInstanceUID
    5. AcquisitionDateTime
    6. AcquisitionDate + Time
    """
    return (
        get_timestamp(dcm, "Study")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Acquisition")
    )


def get_acquisition_uid(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition UID."""
    # TODO GE: separate UID per AcquisitionNumber
    return dcm.get("SeriesInstanceUID")


def get_acquisition_label(dcm: t.Mapping[str, t.Any]) -> t.Optional[str]:
    """Return acquisition label.

    1. [SeriesNumber - ]SeriesDescription
    2. [SeriesNumber - ]ProtocolName
    3. [SeriesNumber - ]Acquisition timestamp (YYYY-mm-ddTHH-MM-SS)
    4. [SeriesNumber - ]SeriesInstanceUID
    """
    label = dcm.get("SeriesDescription") or dcm.get("ProtocolName")
    if not label and (ts := get_acquisition_timestamp(dcm)):
        label = ts.strftime("%Y-%m-%dT%H-%M-%S")
    label = label or dcm.get("SeriesInstanceUID")
    if label and (series_number := dcm.get("SeriesNumber")):
        label = f"{series_number} - {label}"
    return label


def get_acquisition_timestamp(dcm: t.Mapping[str, t.Any]) -> t.Optional[datetime]:
    """Return acquisition timestamp.

    1. AcquisitionDateTime
    2. AcquisitionDate + Time
    3. SeriesDate + Time
    4. SeriesInstanceUID
    5. StudyDate + Time
    6. StudyInstanceUID
    """
    return (
        get_timestamp(dcm, "Acquisition")
        or get_timestamp(dcm, "Series")
        or get_timestamp(dcm, "Study")
    )


def get_instance_filename(dcm: t.Mapping[str, t.Any]) -> str:
    """Return recommended DICOM instance filename."""
    instance_uid = dcm.get("SOPInstanceUID")
    modality = dcm.get("Modality") or "NA"
    return f"{instance_uid}.{modality}.dcm"
