import enum
import threading
import time
from bec_lib.core.devicemanager import DeviceStatus
import numpy as np
import os

from typing import Any, List

from ophyd import EpicsSignal, EpicsSignalRO, EpicsSignalWithRBV
from ophyd import DetectorBase, Device
from ophyd import ADComponent as ADCpt

from std_daq_client import StdDaqClient

from bec_lib.core import BECMessage, MessageEndpoints, threadlocked
from bec_lib.core.file_utils import FileWriterMixin
from bec_lib.core import bec_logger

from ophyd_devices.epics.devices.bec_scaninfo_mixin import BecScaninfoMixin
from ophyd_devices.utils import bec_utils

logger = bec_logger.logger


class EigerError(Exception):
    """Base class for exceptions in this module."""

    pass


class EigerTimeoutError(Exception):
    """Raised when the Eiger does not respond in time during unstage."""

    pass


class SlsDetectorCam(Device):
    """SLS Detector Camera - Eiger 9M

    Base class to map EPICS PVs to ophyd signals.
    """

    threshold_energy = ADCpt(EpicsSignalWithRBV, "ThresholdEnergy")
    beam_energy = ADCpt(EpicsSignalWithRBV, "BeamEnergy")
    bit_depth = ADCpt(EpicsSignalWithRBV, "BitDepth")
    num_images = ADCpt(EpicsSignalWithRBV, "NumCycles")
    num_frames = ADCpt(EpicsSignalWithRBV, "NumFrames")
    trigger_mode = ADCpt(EpicsSignalWithRBV, "TimingMode")
    trigger_software = ADCpt(EpicsSignal, "TriggerSoftware")
    acquire = ADCpt(EpicsSignal, "Acquire")
    detector_state = ADCpt(EpicsSignalRO, "DetectorState_RBV")


class TriggerSource(int, enum.Enum):
    """Trigger signals for Eiger9M detector"""

    AUTO = 0
    TRIGGER = 1
    GATING = 2
    BURST_TRIGGER = 3


class DetectorState(int, enum.Enum):
    """Detector states for Eiger9M detector"""

    IDLE = 0
    ERROR = 1
    WAITING = 2
    FINISHED = 3
    TRANSMITTING = 4
    RUNNING = 5
    STOPPED = 6
    STILL_WAITING = 7
    INITIALIZING = 8
    DISCONNECTED = 9
    ABORTED = 10


class Eiger9mCsaxs(DetectorBase):
    """Eiger 9M detector for CSAXS

    Parent class: DetectorBase
    Device class: SlsDetectorCam

    Attributes:
        name str: 'eiger'
        prefix (str): PV prefix (X12SA-ES-EIGER9M:)

    """

    # Specify which functions are revealed to the user in BEC client
    USER_ACCESS = [
        "describe",
    ]

    cam = ADCpt(SlsDetectorCam, "cam1:")

    def __init__(
        self,
        prefix="",
        *,
        name,
        kind=None,
        read_attrs=None,
        configuration_attrs=None,
        parent=None,
        device_manager=None,
        sim_mode=False,
        **kwargs,
    ):
        """Initialize the Eiger9M detector
        Args:
        #TODO add here the parameters for kind, read_attrs, configuration_attrs, parent
            prefix (str): PV prefix (X12SA-ES-EIGER9M:)
            name (str): 'eiger'
            kind (str):
            read_attrs (list):
            configuration_attrs (list):
            parent (object):
            device_manager (object): BEC device manager
            sim_mode (bool): simulation mode to start the detector without BEC, e.g. from ipython shell
        """
        super().__init__(
            prefix=prefix,
            name=name,
            kind=kind,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            parent=parent,
            **kwargs,
        )
        if device_manager is None and not sim_mode:
            raise EigerError("Add DeviceManager to initialization or init with sim_mode=True")

        # Not sure if this is needed, comment it for now!
        # self._lock = threading.RLock()
        self._stopped = False
        self.name = name
        self.wait_for_connection()
        # Spin up connections for simulation or BEC mode
        # TODO check if sim_mode still works. Is it needed? I believe filewriting might be handled properly
        if not sim_mode:
            from bec_lib.core.bec_service import SERVICE_CONFIG

            self.device_manager = device_manager
            self._producer = self.device_manager.producer
            self.service_cfg = SERVICE_CONFIG.config["service_config"]["file_writer"]
        else:
            base_path = f"/sls/X12SA/data/{self.scaninfo.username}/Data10/"
            self._producer = bec_utils.MockProducer()
            self.device_manager = bec_utils.MockDeviceManager()
            self.scaninfo = BecScaninfoMixin(device_manager, sim_mode)
            self.scaninfo.load_scan_metadata()
            self.service_cfg = {"base_path": base_path}

        self.scaninfo = BecScaninfoMixin(device_manager, sim_mode)
        self.scaninfo.load_scan_metadata()
        self.filewriter = FileWriterMixin(self.service_cfg)
        self._init()

    # TODO function for abstract class?
    def _init(self) -> None:
        """Initialize detector, filewriter and set default parameters"""
        self._default_parameter()
        self._init_detector()
        self._init_filewriter()

    # TODO function for abstract class?
    def _default_parameter(self) -> None:
        """Set default parameters for Eiger 9M
        readout (float) : readout time in seconds
        """
        self.reduce_readout = 1e-3

    # TODO function for abstract class?
    def _init_detector(self) -> None:
        """Init parameters for Eiger 9m.
        Depends on hardware configuration and delay generators.
        At this point it is set up for gating mode (09/2023).
        """
        self._stop_det()
        self._set_trigger(TriggerSource.GATING)

    # TODO function for abstract class?
    def _init_filewriter(self) -> None:
        """Init parameters for filewriter.
        For the Eiger9M, the data backend is std_daq client.
        Setting up these parameters depends on the backend, and would need to change upon changes in the backend.
        """
        self.std_rest_server_url = "http://xbl-daq-29:5000"
        self.std_client = StdDaqClient(url_base=self.std_rest_server_url)
        self.std_client.stop_writer()
        timeout = 0
        # TODO changing e-account was not possible during beamtimes.
        # self._update_std_cfg("writer_user_id", int(self.scaninfo.username.strip(" e")))
        # time.sleep(5)
        # TODO is this the only state to wait for or should we wait for more from the std_daq client?
        while not self.std_client.get_status()["state"] == "READY":
            time.sleep(0.1)
            timeout = timeout + 0.1
            logger.info("Waiting for std_daq init.")
            if timeout > 5:
                if not self.std_client.get_status()["state"]:
                    raise EigerError(
                        f"Std client not in READY state, returns: {self.std_client.get_status()}"
                    )
                else:
                    return

    def _update_std_cfg(self, cfg_key: str, value: Any) -> None:
        """Update std_daq config with new e-account for the current beamtime"""
        # TODO Do we need all the loggers here, should this be properly refactored with a DEBUG mode?
        cfg = self.std_client.get_config()
        old_value = cfg.get(cfg_key)
        logger.info(old_value)
        if old_value is None:
            raise EigerError(
                f"Tried to change entry for key {cfg_key} in std_config that does not exist"
            )
        if not isinstance(value, type(old_value)):
            raise EigerError(
                f"Type of new value {type(value)}:{value} does not match old value {type(old_value)}:{old_value}"
            )
        cfg.update({cfg_key: value})
        logger.info(cfg)
        logger.info(f"Updated std_daq config for key {cfg_key} from {old_value} to {value}")
        self.std_client.set_config(cfg)

    # TODO function for abstract class?
    def stage(self) -> List[object]:
        """Stage command, called from BEC in preparation of a scan.
        This will iniate the preparation of detector and file writer.
        The following functuions are called (at least):
            - _prep_file_writer
            - _prep_det
            - _publish_file_location
        The device returns a List[object] from the Ophyd Device class.

        #TODO make sure this is fullfiled

        Staging not idempotent and should raise
        :obj:`RedundantStaging` if staged twice without an
        intermediate :meth:`~BlueskyInterface.unstage`.
        """
        self._stopped = False
        self.scaninfo.load_scan_metadata()
        self.mokev = self.device_manager.devices.mokev.obj.read()[
            self.device_manager.devices.mokev.name
        ]["value"]
        # TODO refactor logger.info to DEBUG mode?
        self._prep_file_writer()
        self._prep_det()
        state = False
        self._publish_file_location(done=state, successful=state)
        self._arm_acquisition()
        # TODO Fix should take place in EPICS or directly on the hardware!
        # We observed that the detector missed triggers in the beginning in case BEC was to fast. Adding 50ms delay solved this
        time.sleep(0.05)
        return super().stage()

    # TODO function for abstract class?
    def _prep_file_writer(self) -> None:
        """Prepare file writer for scan

        self.filewriter is a FileWriterMixin object that hosts logic for compiling the filepath
        """
        self.filepath = self.filewriter.compile_full_filename(
            self.scaninfo.scan_number, f"{self.name}.h5", 1000, 5, True
        )
        # TODO needed, should be checked from the filerwriter mixin right?
        while not os.path.exists(os.path.dirname(self.filepath)):
            time.sleep(0.1)

        self._stop_file_writer()
        logger.info(f" std_daq output filepath {self.filepath}")
        # TODO Discuss with Leo if this is needed, or how to start the async writing best
        try:
            self.std_client.start_writer_async(
                {
                    "output_file": self.filepath,
                    "n_images": int(self.scaninfo.num_points * self.scaninfo.frames_per_trigger),
                }
            )
        except Exception as exc:
            time.sleep(5)
            if self.std_client.get_status()["state"] == "READY":
                raise EigerError(f"Timeout of start_writer_async with {exc}")

        while True:
            det_ctrl = self.std_client.get_status()["acquisition"]["state"]
            if det_ctrl == "WAITING_IMAGES":
                break
            time.sleep(0.005)

    # TODO function for abstract class?
    def _stop_file_writer(self) -> None:
        """Close file writer"""
        self.std_client.stop_writer()
        # TODO can I wait for a status message here maybe? To ensure writer returned

    # TODO function for abstract class?
    def _prep_det(self) -> None:
        """Prepare detector for scan.
        Includes checking the detector threshold, setting the acquisition parameters and setting the trigger source
        """
        self._set_det_threshold()
        self._set_acquisition_params()
        self._set_trigger(TriggerSource.GATING)

    def _set_det_threshold(self) -> None:
        """Set correct detector threshold to 1/2 of current X-ray energy, allow 5% tolerance"""
        # threshold energy might be in eV or keV
        factor = 1
        if self.cam.threshold_energy._metadata["units"] == "eV":
            factor = 1000
        setpoint = int(self.mokev * factor)
        energy = self.cam.beam_energy.read()[self.cam.beam_energy.name]["value"]
        if setpoint != energy:
            self.cam.beam_energy.set(setpoint)
        threshold = self.cam.threshold_energy.read()[self.cam.threshold_energy.name]["value"]
        if not np.isclose(setpoint / 2, threshold, rtol=0.05):
            self.cam.threshold_energy.set(setpoint / 2)

    def _set_acquisition_params(self) -> None:
        """Set acquisition parameters for the detector"""
        self.cam.num_images.put(int(self.scaninfo.num_points * self.scaninfo.frames_per_trigger))
        self.cam.num_frames.put(1)

    # TODO function for abstract class? + call it for each scan??
    def _set_trigger(self, trigger_source: TriggerSource) -> None:
        """Set trigger source for the detector.
        Check the TriggerSource enum for possible values
        """
        value = int(trigger_source)
        self.cam.trigger_mode.put(value)

    def _publish_file_location(self, done=False, successful=False) -> None:
        """Publish the filepath to REDIS
        First msg for file writer and the second one for other listeners (e.g. radial integ)
        """
        pipe = self._producer.pipeline()
        msg = BECMessage.FileMessage(file_path=self.filepath, done=done, successful=successful)
        self._producer.set_and_publish(
            MessageEndpoints.public_file(self.scaninfo.scanID, self.name), msg.dumps(), pipe=pipe
        )
        self._producer.set_and_publish(
            MessageEndpoints.file_event(self.name), msg.dumps(), pip=pipe
        )
        pipe.execute()

    # TODO function for abstract class?
    def _arm_acquisition(self) -> None:
        """Arm Eiger detector for acquisition"""
        self.cam.acquire.put(1)
        while True:
            det_ctrl = self.cam.detector_state.read()[self.cam.detector_state.name]["value"]
            if det_ctrl == int(DetectorState.RUNNING):
                break
            if self._stopped == True:
                break
            time.sleep(0.005)

    # TODO function for abstract class?
    def trigger(self) -> DeviceStatus:
        """Trigger the detector, called from BEC."""
        self._on_trigger()
        return super().trigger()

    # TODO function for abstract class?
    def _on_trigger(self):
        """Specify action that should be taken upon trigger signal."""
        pass

    # TODO function for abstract class?
    # TODO threadlocked was attached, in principle unstage needs to be fast and should possibly called multiple times
    @threadlocked
    def unstage(self) -> List[object]:
        """Unstage the device.

        This method must be idempotent, multiple calls (without a new
        call to 'stage') have no effect.

        Functions called:
            - _finished
            - _publish_file_location
        """
        # TODO solution for multiple calls of the function to avoid calling the finished loop.
        # Loop to avoid calling the finished loop multiple times
        old_scanID = self.scaninfo.scanID
        self.scaninfo.load_scan_metadata()
        if self.scaninfo.scanID != old_scanID:
            self._stopped = True
        if self._stopped == True:
            return super().unstage()
        self._finished()
        state = True
        self._publish_file_location(done=state, successful=state)
        self._stopped = False
        return super().unstage()

    # TODO function for abstract class?
    # TODO necessary, how can we make this cleaner.
    @threadlocked
    def _finished(self):
        """Check if acquisition is finished.

        This function is called from unstage and stop
        and will check detector and file backend status.
        Timeouts after given time

        Functions called:
            - _stop_det
            - _stop_file_writer
        """
        sleep_time = 0.1
        timeout = 5
        timer = 0
        # Check status with timeout, break out if _stopped=True
        while True:
            det_ctrl = self.cam.acquire.read()[self.cam.acquire.name]["value"]
            std_ctrl = self.std_client.get_status()["acquisition"]["state"]
            status = self.std_client.get_status()
            received_frames = status["acquisition"]["stats"]["n_write_completed"]
            total_frames = int(self.scaninfo.num_points * self.scaninfo.frames_per_trigger)
            if det_ctrl == 0 and std_ctrl == "FINISHED" and total_frames == received_frames:
                break
            if self._stopped == True:
                self._stop_det()
                self._stop_file_writer()
                break
            time.sleep(sleep_time)
            timer += sleep_time
            if timer > timeout:
                self._stopped == True
                self._stop_det()
                self._stop_file_writer()
                raise EigerTimeoutError(
                    f"Reached timeout with detector state {det_ctrl}, std_daq state {std_ctrl} and received frames of {received_frames} for the file writer"
                )
        self._stop_det()
        self._stop_file_writer()

    def _stop_det(self) -> None:
        """Stop the detector and wait for the proper status message"""
        elapsed_time = 0
        sleep_time = 0.01
        timeout = 5
        # Stop acquisition
        self.cam.acquire.put(0)
        retry = False
        # Check status
        while True:
            det_ctrl = self.cam.detector_state.read()[self.cam.detector_state.name]["value"]
            if det_ctrl == int(DetectorState.IDLE):
                break
            if self._stopped == True:
                break
            time.sleep(sleep_time)
            elapsed_time += sleep_time
            if elapsed_time > timeout // 2 and not retry:
                retry = True
                # Retry to stop acquisition
                self.cam.acquire.put(0)
            if elapsed_time > timeout:
                raise EigerTimeoutError("Failed to stop the acquisition. IOC did not update.")

    def stop(self, *, success=False) -> None:
        """Stop the scan, with camera and file writer"""
        self._stop_det()
        self._stop_file_writer()
        super().stop(success=success)
        self._stopped = True


if __name__ == "__main__":
    eiger = Eiger9mCsaxs(name="eiger", prefix="X12SA-ES-EIGER9M:", sim_mode=True)
