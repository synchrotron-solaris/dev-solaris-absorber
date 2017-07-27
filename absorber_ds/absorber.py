"""
This module contains Absorber Device Class and run method for it
"""

# Imports
from facadedevice import Facade, proxy_attribute, logical_attribute, proxy_command
from tango import DevState, AttrWriteType
from tango.server import command


class Absorber(Facade):
    """
    Tango facade device class for vacuum absorbers

    This class contains four water flow alarms:

    * FSW_1
    * FSW_2
    * FSW_3
    * Achromat_FSW

    as well as attributes to hold names of PLCs for those alarms.

    There is also a whole mechanism of maintaining absorber:

    * name of PLCs for inserting and extracting absorberx
    * name of PLCs for changing state of absorber (inserted or extracted)
    * attribute for holding value of absorber state (inserted or extracted)
    * methods to Insert or Extract the absorber itself
    """
    # device initialization

    def safe_init_device(self):
        """
        This is safe_init_device method overriden from Facade base class. It's
        used to initialize facade device safely
        """
        super(Absorber, self).safe_init_device()
        self.set_state(DevState.ON)
        self.set_status("Device is running")

    # proxy attributes

    waterFlowAlarm_Achromat = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_AchromatFSW",
        description="PLC device and attribute name for alarm from water flow "
                    "in the achromat")

    PlcAttrName_Extract = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_ExtractAttribute",
        description="PLC device and attribute name for extracting absorber")

    PlcAttrName_Insert = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_InsertAttribute",
        description="PLC device and attribute name for inserting absorber")

    waterFlowAlarm_1 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_FSW_1",
        description="PLC device and attribute name for flow alarm")

    waterFlowAlarm_2 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_FSW_2",
        description="PLC device and attribute name for flow alarm")

    waterFlowAlarm_3 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_FSW_3",
        description="PLC device and attribute name for flow alarm")

    PlcAttrName_StateExtracted = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_StateExtractedAttribute",
        description="PLC device and attribute name for extracted state")

    PlcAttrName_StateInserted = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PlcAttrName_StateInsertedAttribute",
        description="PLC device and attribute name for inserted state")

    # logical attributes

    @logical_attribute(
        dtype=bool,
        bind=['PlcAttrName_StateExtracted', 'PlcAttrName_StateInserted'],
        description="True: the absorber is inserted. False: the absorber "
                    "is extracted. Based on PlcAttrName_StateExtracted and "
                    "PlcAttrName_StateInserted")
    def InExStatus(self, ins, exs):
        return ins and not exs

    # proxy commands

    @proxy_command(
        dtype_out=bool,
        property_name="PlcAttrName_InsertAttribute",
        write_attribute=True)
    def _extract_in(self):
        """
        Internal, private method for Extract. It writes False to
        PlcAttrName_Insert when Extract is called
        :return: False to PlcAttrName_Insert
        """
        return False

    @proxy_command(
        dtype_out=bool,
        property_name="PlcAttrName_ExtractAttribute",
        write_attribute=True,
        doc_out="False to PlcAttrName_Insert, then True to PlcAttrName_Extract")
    def Extract(self):
        """
        write False to PlcAttrName_Insert, then write True to PlcAttrName_Extract
        """
        self._extract_in()
        return True

    @proxy_command(
        dtype_out=bool,
        property_name="PlcAttrName_ExtractAttribute",
        write_attribute=True)
    def _insert_in(self):
        """
        Internal, private method for Insert. It writes False to
        PlcAttrName_Extract when Insert is called
        :return: False to PlcAttrName_Extract
        """
        return False

    @proxy_command(
        dtype_out=bool,
        property_name="PlcAttrName_InsertAttribute",
        write_attribute=True,
        doc_out="False to PlcAttrName_Extract, then True to PlcAttrName_Insert")
    def Insert(self):
        """
        write False to PlcAttrName_Extract, then write True to PlcAttrName_Insert
        """
        self._insert_in()
        return True


# run server

run = Absorber.run_server()

if __name__ == '__main__':
    run()
