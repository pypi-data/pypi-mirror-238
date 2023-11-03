import collections
import os
from abc import ABC, abstractmethod


def _validate_reference_snp_value(reference_snp_value):
    if not isinstance(reference_snp_value, str):
        raise TypeError("reference_snp_values values must be strings")
    # verify reference_snp_value contains only A, C, G, T, D or I
    if not set(reference_snp_value).issubset({"A", "C", "G", "T", "D", "I"}):
        raise ValueError(
            "reference_snp_values values must contain only A, C, G, T, D, or I"
        )


def _validate_reference_snp_id(reference_snp_id):
    if not isinstance(reference_snp_id, str):
        raise TypeError("reference_snp_id must be a sequence of strings")
    if not reference_snp_id.startswith("rs"):
        raise ValueError("reference_snp_ids must start with 'rs'")
    if not reference_snp_id[2:].isdigit():
        raise ValueError("reference_snp_ids must start with 'rs' followed by digits")


def _validate_rsId_collection(reference_snp_ids):
    if not isinstance(reference_snp_ids, list):
        raise TypeError("reference_snp_ids must be a list of strings")
    if not reference_snp_ids:
        raise ValueError("reference_snp_ids must not be empty")
    for reference_snp_id in reference_snp_ids:
        _validate_reference_snp_id(reference_snp_id)


def _validate_reference_snp_values(reference_snp_values):
    # verify that reference_snp_values is a dict
    if not isinstance(reference_snp_values, dict):
        raise TypeError("reference_snp_ids_mock must be a dict")
    # verify reference_snp_id and reference_snp_value types are strings
    for reference_snp_id, reference_snp_value in reference_snp_values.items():
        _validate_reference_snp_id(reference_snp_id)
        _validate_reference_snp_value(reference_snp_value)


class GenomixHubFrame(ABC):
    """Abstract class for dynamic frames."""

    @abstractmethod
    def _load(self, reference_snp_ids):
        """Load data into the frame."""
        pass

    @abstractmethod
    def mock(self, rsIds):
        """Mock data into the frame."""
        pass

    @abstractmethod
    def get_value(self, reference_snp_id):
        """Get reference_snp_id."""
        pass


class _GenomixHubFrameProd(GenomixHubFrame):
    """Production class for dynamic frames."""

    def __init__(self):
        self._reference_snp_ids = []
        self._reference_snp_values = {}

    def _load(self, reference_snp_ids):
        """Load data into the frame."""

        self._reference_snp_ids = reference_snp_ids

        import requests

        # read from ENV
        url = os.getenv("GENOMIXHUB_BACKEND_URL")
        token = os.getenv("GENOMIXHUB_BACKEND_TOKEN")
        user_id = os.getenv("GENOMIXHUB_BACKEND_USERID")

        data = {"user_id": user_id, "rsIds": reference_snp_ids}

        response = requests.post(
            url, headers={"Authorization": f"token {token}"}, data=data
        )

        if response.status_code != 200:
            raise Exception(
                f"Error loading data from backend. Status code: {response.status_code} message {response.text}"
            )

        data = response.json()

        for item in data:
            reference_snp_id = "rs" + item["rsId"]
            _validate_reference_snp_id(reference_snp_id)
            reference_snp_value = item["value"]
            _validate_reference_snp_value(reference_snp_value)
            self._reference_snp_values[reference_snp_id] = reference_snp_value

    def get_value(self, reference_snp_id):
        """Get reference_snp_id."""
        _validate_reference_snp_id(reference_snp_id)
        if not reference_snp_id in self._reference_snp_ids:
            raise ValueError(
                "reference_snp_id not loaded. Use the load method to load all required reference_snp_ids."
            )
        return self._reference_snp_values.get(reference_snp_id)

    def mock(self, reference_snp_key_values):
        """Do Nothing."""


class _GenomixHubFrameDev(GenomixHubFrame):
    """Development class for dynamic frames."""

    def __init__(self):
        self._reference_snp_ids = []
        self._reference_snp_values = {}

    def _load(self, reference_snp_ids):
        """Load data into the frame."""
        self._reference_snp_ids = reference_snp_ids

    def mock(self, reference_snp_key_values):
        """Mock data into the frame."""
        _validate_reference_snp_values(reference_snp_key_values)
        self._reference_snp_values = reference_snp_key_values

    def get_value(self, reference_snp_id):
        """Get reference_snp_id."""
        _validate_reference_snp_id(reference_snp_id)
        if not reference_snp_id in self._reference_snp_ids:
            raise ValueError(
                "reference_snp_id not loaded. Use the load method to load all required reference_snp_ids."
            )
        return self._reference_snp_values.get(reference_snp_id)


def load(reference_snp_ids) -> GenomixHubFrame:
    """Load data into the frame."""
    _validate_rsId_collection(reference_snp_ids)

    frame: GenomixHubFrame

    current_environment = os.getenv("GENOMIXHUB_ENVIRONMENT", "DEV")

    if current_environment in ["PROD", "TEST"]:
        frame = _GenomixHubFrameProd()
    else:
        frame = _GenomixHubFrameDev()

    frame._load(reference_snp_ids)

    return frame
