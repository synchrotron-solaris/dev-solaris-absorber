"""
This module contains Absorber Device Class and run method for it
"""

# Imports
from facadedevice import Facade, proxy_attribute, logical_attribute, triplet
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
        access=AttrWriteType.READ,
        property_name="PLCAttrName_AchromatFSW",
        description="PLC device and attribute name for alarm from water flow "
                    "in the achromat")

    PLCAttrName_Extract = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PLCAttrName_ExtractAttribute",
        description="PLC device and attribute name for extracting absorber")

    PLCAttrName_Insert = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ_WRITE,
        property_name="PLCAttrName_InsertAttribute",
        description="PLC device and attribute name for inserting absorber")

    waterFlowAlarm_1 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_FSW_1",
        description="PLC device and attribute name for flow alarm")

    waterFlowAlarm_2 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_FSW_2",
        description="PLC device and attribute name for flow alarm")

    waterFlowAlarm_3 = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_FSW_3",
        description="PLC device and attribute name for flow alarm")

    PLCAttrName_StateExtracted = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_StateExtractedAttribute",
        description="PLC device and attribute name for extracted state")

    PLCAttrName_StateInserted = proxy_attribute(
        dtype=bool,
        access=AttrWriteType.READ,
        property_name="PLCAttrName_StateInsertedAttribute",
        description="PLC device and attribute name for inserted state")

    # logical attributes

    @logical_attribute(
        dtype=bool,
        bind=['PLCAttrName_StateExtracted', 'PLCAttrName_StateInserted'],
        description="True: the absorber is inserted. False: the absorber "
                    "is extracted. Based on PLCAttrName_StateExtracted and "
                    "PLCAttrName_StateInserted")
    def InExStatus(self, ins, exs):
        return ins and not exs

    # commands

    @command()
    def Extract(self):
        """
        :return: False to PLCAttrName_Insert, then True to PLCAttrName_Extract
        :rtype: bool
        """
        # write False to PlcAttrName_Insert
        in_node = self.graph['PLCAttrName_Insert']
        value, stamp, quality = in_node.result()
        value = False
        new_result = triplet(value)
        in_node.set_result(new_result)
        # write True to PlcAttrName_Extract
        ex_node = self.graph['PLCAttrName_Extract']
        value, stamp, quality = ex_node.result()
        value = True
        new_result = triplet(value)
        ex_node.set_result(new_result)

    @command()
    def Insert(self):
        """
        :return: False to PLCAttrName_Extract, then True to PLCAttrName_Insert
        :rtype: bool
        """
        # write False to PlcAttrName_Extract
        ex_node = self.graph['PLCAttrName_Extract']
        value, stamp, quality = ex_node.result()
        value = False
        new_result = triplet(value)
        ex_node.set_result(new_result)
        # write True to PlcAttrName_Insert
        in_node = self.graph['PLCAttrName_Insert']
        value, stamp, quality = in_node.result()
        value = True
        new_result = triplet(value)
        in_node.set_result(new_result)

# run server

run = Absorber.run_server()

if __name__ == '__main__':
    run()
