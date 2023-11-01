import _threading_local
from ctypes import ArgumentError
from datetime import datetime, timedelta
import os
import threading

# our package imports.
from .siargumentnullexception import SIArgumentNullException
from .smartinspect import SmartInspect

# auto-generate the "__all__" variable with classes decorated with "@export".
from .siutils import export


@export
class SIConfigurationTimer:
    """
    Monitors a SmartInspect configuration settings file for changes
    and reloads the configuration when it does.

    Use this class to monitor and automatically reload SmartInspect
    configuration files.  This class periodically checks if the
    related configuration file has changed (by comparing the last
    modified datetime) and automatically tries to reload the configuration
    properties. You can pass the SmartInspect object to configure,
    the path of the configuration file to monitor, and the interval
    in which the path should check for changes.

    For information about SmartInspect configuration files, please
    refer to the documentation of the SmartInspect.LoadConfiguration
    method.

    Threadsafety:
        This class is fully thread-safe.

    <details>
        <summary>Sample Code</summary>
    ``` python
    .. include:: ../docs/include/samplecode/SIConfigurationTimer/LoadConfiguration.py
    ```
    <br/>
    The following is the configuration settings file contents:
    ``` ini
    .. include:: ../docs/include/samplecode/smartinspect.cfg
    ```
    </details>
    """

    def __init__(self, smartInspect:SmartInspect, fileName:str, interval:int=60) -> None:
        """
        Initializes a new instance of the class.

        Args:
            smartInspect (SmartInspect):
                The SmartInspect object to configure.
            fileName (str):
                The path of the configuration file to monitor.
            interval (int):
                The interval (in seconds) in which this timer should check for changes
                to the configuration file.
                Default value is 60 (seconds).

        Raises:
            SIArgumentNullException:
                The smartInspect or fileName parameter is null.
            ArgumentError:
                The interval parameter is less than 1 or greater than 300 (seconds).

        The monitoring of the file begins immediately.
        """
        # validations:
        if (smartInspect == None):
            raise SIArgumentNullException("smartInspect")
        if (fileName == None):
            raise SIArgumentNullException("fileName")
        if ((interval < 1) or (interval > 300)):
            raise ArgumentError("Interval argument must be in the range of 1 to 300 (seconds).")

        # initialize instance.
        self._fLock:object = _threading_local.RLock()
        self._fSmartInspect = smartInspect
        self._fFileName:str = fileName
        self._fInterval:int = interval
        self._fIntervalNextCheck:datetime = datetime.utcnow()
        self._fFileDateModified:datetime = datetime.min
        self._fMonitorCondition:threading.Condition = threading.Condition(self._fLock)
        self._fStarted = False
        self._fStopped = False

        # start monitoring the file for changes.
        self.Start()


    @staticmethod
    def _GetFileAge(fileName:str) -> bool:
        """
        Gets the last modified date time of the specified file path.

        Args:
            fileName (str):
                The path of the configuration file to monitor.

        Returns:
            (bool):
                True if the function was successful; otherwise, false.
            (datetime):
                datetime of file last modified date if the function was successful;
                otherswise, datetime.min if not.

        No exception will be thrown by this method.
        """
        result:bool = False
        age:datetime = None

        try:
            
            # get last modified date time of file.
            ts = os.path.getmtime(fileName)     # returns timestamp
            age = datetime.fromtimestamp(ts)    # converts timestamp to datetime
            result = True
        
        except Exception as ex:
        
            # if file info could not be obtained, then return False to indicate failure.
            age = datetime.min
            result = False

        return result, age


    def Start(self) -> None:
        """
        Starts monitoring the configuration file for changes.

        This method is called automatically when a new instance of the class 
        is created.  It can also be called after issuing a "Stop" method
        call, to restart monitoring of the configuration file.

        It will start a new thread named "SiConfigFileMonitorTask" that will
        monitor a specified configuration file for changes at a selected
        interval, and reload the configuration automatically.
        """
        with (self._fLock):

            # if threadtask is already running then don't bother.
            if (self._fStarted):
                return

            # get last modified date time of specified configuration file path.
            result, self._fFileDateModified = SIConfigurationTimer._GetFileAge(self._fFileName)

            # reset stop requested status.
            self._fStopped = False

            # start the thread task to monitor the file.
            self._fThread = threading.Thread(target=self._MonitorFileTask, args=(self,))
            self._fThread.name = "SiConfigFileMonitorTask"
            self._fThread.start()

            # indicate we are monitoring.
            self._fStarted = True


    def Stop(self) -> None:
        """
        Stops monitoring the configuration file for changes.
        """
        with (self._fLock):

            # if threadtask has not started yet then we are done.
            if (not self._fStarted):
                return

            # inform the thread task we want it to stop.
            self._fStopped = True
            self._fMonitorCondition.notify_all()

        # wait for the monitoring threadtask to finish up.
        if (self._fThread != None):
            self._fThread.join()

        # reset threadtask object.
        self._fThread = None


    def _MonitorFileTask(self, instance) -> None:
        """
        Periodically checks the last modified datetime of a configuration
        file to see if it has changed, and reloads the configuration if so.
        """
        try:

            # process until we are asked to stop by main thread.
            while (True):

                with (self._fLock):
        
                    # were we asked to stop?  if so, then we are done.
                    if (self._fStopped):
                        break

                    # is main thread still alive?  if not, then we are done.
                    if (not threading.main_thread().is_alive()):
                        break

                    # has interval been reached since last check?
                    if (datetime.utcnow() >= self._fIntervalNextCheck):

                        # calculate next interval check datetime.
                        self._fIntervalNextCheck = datetime.utcnow() + timedelta(seconds=self._fInterval)

                        # get last modified date time of specified configuration file path.
                        lastUpdate:datetime = None
                        result, lastUpdate = SIConfigurationTimer._GetFileAge(self._fFileName)

                        # did we get the last modified datetime?
                        if (result):

                            # yes - has file changed since the last time we checked?
                            # if so, then save the last modified date and reload configuration.
                            if (lastUpdate > self._fFileDateModified):
                                self._fFileDateModified = lastUpdate
                                self._fSmartInspect.RaiseInfoEvent("SI Configuration File change detected - reloading configuration from file \"{0}\"".format(self._fFileName))
                                self._fSmartInspect.LoadConfiguration(self._fFileName)

                        # wait until we receive a pulse from the main thread
                        # that it asked us to stop, or a timeout of 1 second occurs.
                        # this keeps the thread responsive and prevents shutdown hanging.
                        self._fMonitorCondition.wait(1)

        except Exception as ex:
        
            # ignore exceptions.
            pass
