"""CryoNIRSP calibration pipeline parameters."""
from functools import cached_property
from typing import Any

import numpy as np
from dkist_processing_common.models.parameters import ParameterBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetParameterValue
from dkist_service_configuration import logger


class CryonirspParameters(ParameterBase):
    """Put all CryoNIRSP parameters parsed from the input dataset document in a single property."""

    def __init__(
        self,
        input_dataset_parameters: dict[str, list[InputDatasetParameterValue]],
        wavelength: float | None = None,
        arm_id: str | None = None,
    ):
        super().__init__(input_dataset_parameters)
        self._wavelength = wavelength
        self._arm_id = arm_id

    @property
    def geo_upsample_factor(self) -> float:
        """Pixel precision (1/upsample_factor) to use during phase matching of beam/modulator images."""
        return self._find_most_recent_past_value("cryonirsp_geo_upsample_factor")

    @property
    def geo_max_shift(self) -> float:
        """Max allowed pixel shift when computing spectral curvature."""
        return self._find_most_recent_past_value("cryonirsp_geo_max_shift")

    @property
    def geo_poly_fit_order(self) -> int:
        """Order of polynomial used to fit spectral shift as a function of slit position."""
        return self._find_most_recent_past_value("cryonirsp_geo_poly_fit_order")

    @property
    def geo_spatial_gradient_displacement(self) -> int:
        """Number of spatial pixels to shift by when computing gradient."""
        return self._find_most_recent_past_value("cryonirsp_geo_spatial_gradient_displacement")

    @property
    def geo_strip_spatial_size_fraction(self) -> float:
        """Fraction of full spatial size to use for spatial size of strips used to find the beam angle."""
        return self._find_most_recent_past_value("cryonirsp_geo_strip_spatial_size_fraction")

    @property
    def geo_strip_spectral_size_fraction(self) -> float:
        """Fraction of full spectral size to use for spectral size of strips used to find the beam angle."""
        return self._find_most_recent_past_value("cryonirsp_geo_strip_spectral_size_fraction")

    @property
    def geo_strip_spectral_offset_size_fraction(self) -> float:
        """Fraction of full spectral size to set as the +/- offset from spectral center for the two strips used to find the beam angle."""
        return self._find_most_recent_past_value(
            "cryonirsp_geo_strip_spectral_offset_size_fraction"
        )

    @property
    def polcal_num_spectral_bins(self) -> int:
        """Return Number of demodulation matrices to compute across the entire FOV in the spectral dimension."""
        return self._find_most_recent_past_value("cryonirsp_polcal_num_spectral_bins")

    @property
    def polcal_num_spatial_bins(self) -> int:
        """Return Number of demodulation matrices to compute across the entire FOV in the spatial dimension."""
        return self._find_most_recent_past_value("cryonirsp_polcal_num_spatial_bins")

    @property
    def max_cs_step_time_sec(self):
        """Time window within which CS steps with identical GOS configurations are considered to be the same."""
        return self._find_most_recent_past_value("cryonirsp_max_cs_step_time_sec")

    @property
    def polcal_pac_fit_mode(self):
        """Name of set of fitting flags to use during PAC Calibration Unit parameter fits."""
        return self._find_most_recent_past_value("cryonirsp_polcal_pac_fit_mode")

    @property
    def polcal_pac_init_set(self):
        """Name of set of initial values for Calibration Unit parameter fit."""
        return self._find_most_recent_past_value("cryonirsp_polcal_pac_init_set")

    @property
    def beam_boundaries_smoothing_disk_size(self) -> int:
        """Return the size of the smoothing disk (in pixels) to be used in the beam boundaries computation."""
        return self._find_most_recent_past_value("cryonirsp_beam_boundaries_smoothing_disk_size")

    @property
    def beam_boundaries_upsample_factor(self) -> int:
        """Return the upsample factor to be used in the beam boundaries cross correlation computation."""
        return self._find_most_recent_past_value("cryonirsp_beam_boundaries_upsample_factor")

    @property
    def beam_boundaries_sp_beam_transition_region_size_fraction(self) -> float:
        """
        Fraction of full spectral size to use as the size of the transition region between the two SP beams.

        A region with size = (this parameter * full spectral size) and centered at the center of the spectral dimension
        will be ignored when extracting the beams.
        """
        return self._find_most_recent_past_value(
            "cryonirsp_beam_boundaries_sp_beam_transition_region_size_fraction"
        )

    @property
    def bad_pixel_map_median_filter_size(self) -> list[int, int]:
        """Return the smoothing disk size to be used in the bad pixel map computation."""
        filter_size = self._find_parameter_for_arm("cryonirsp_bad_pixel_map_median_filter_size")
        return filter_size

    @property
    def bad_pixel_map_threshold_factor(self) -> float:
        """Return the threshold multiplicative factor to be used in the bad pixel map computation."""
        return self._find_most_recent_past_value("cryonirsp_bad_pixel_map_threshold_factor")

    @property
    def corrections_bad_pixel_median_filter_size(self) -> int:
        """Return the size of the median filter to be used for bad pixel correction."""
        return self._find_most_recent_past_value(
            "cryonirsp_corrections_bad_pixel_median_filter_size"
        )

    @cached_property
    def linearization_thresholds(self) -> np.ndarray:
        """Name of parameter associated with the linearization thresholds."""
        param_dict = self._find_parameter_for_arm("cryonirsp_linearization_thresholds")
        return self._load_param_value_from_npy_file(param_dict)

    @cached_property
    def linearization_polyfit_coeffs(self) -> np.ndarray:
        """Name of parameter associated with the linearization polyfit coefficients."""
        param_dict = self._find_parameter_for_arm("cryonirsp_linearization_polyfit_coeffs")
        return self._load_param_value_from_npy_file(param_dict)

    @cached_property
    def linearization_max_memory_gb(self) -> float:
        """Get the maximum amount of memory in GB available to the linearity correction task worker."""
        mem_size = self._find_most_recent_past_value("cryonirsp_linearization_max_memory_gb")
        return mem_size

    @property
    def solar_characteristic_spatial_normalization_percentile(self) -> float:
        """Percentile to pass to `np.nanpercentile` when normalizing each spatial position of the characteristic spectra."""
        return self._find_most_recent_past_value(
            "cryonirsp_solar_characteristic_spatial_normalization_percentile"
        )

    @staticmethod
    def _load_param_value_from_npy_file(param_dict: dict) -> np.ndarray:
        """Return the data associated with a parameter file saved in numpy format."""
        file_path = param_dict["param_path"]
        result = np.load(file_path)
        return result

    def _find_parameter_for_arm(self, parameter_name: str) -> Any:
        full_param_name = f"{parameter_name}_{self._arm_id.lower()}"
        param = self._find_most_recent_past_value(full_param_name)
        return param
