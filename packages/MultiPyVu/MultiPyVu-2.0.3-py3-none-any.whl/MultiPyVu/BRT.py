'''
BRT.py is an abstraction of the BRT module.
'''

from typing import Tuple

from .sdo_object import SdoObject, val_type


class Brt():
    def __init__(self, client):
        '''
        Container for BRT module temperature and resistance

        Parameters:
        -----------
        client: MultiPyVu.Client object
        '''
        self.client = client

    def get_temperature(self) -> Tuple[float, str]:
        '''
        This is used to get the temperature, in Kelvin, from the
        BRT.  This command gets it's value directly from
        the module rather than reading the value from MultiVu.

        Returns:
        --------
        A tuple of (temperature, read_status).
        '''
        channel_4_temperature = SdoObject(21, 0x6030, 0x1, val_type.double_t)
        temperature, status = self.client.get_sdo(channel_4_temperature)
        return float(temperature), status

    def get_resistance(self, bridge_number: int) -> Tuple[float, str]:
        '''
        This is used to get the resistance from the BRT module.  This
        command gets it's value directly from the module rather than
        reading the value from MultiVu.

        Parameters:
        -----------
        bridge_number: int
            Indicate the bridge number to read.  This must be 1, 2, or 3.

        Returns:
        --------
        A tuple of (temperature, read_status).

        Raises:
        -------
        ValueError
            Returned if bridge_number is out of bounds
        '''
        resistance = {}
        resistance[1] = SdoObject(21, 0x6001, 0x1, val_type.double_t)
        resistance[2] = SdoObject(21, 0x6002, 0x1, val_type.double_t)
        resistance[3] = SdoObject(21, 0x6003, 0x1, val_type.double_t)

        sdo = resistance.get(bridge_number, None)
        if sdo is None:
            msg = f'bridge_number must be 1, 2, or 3 ({bridge_number = })'
            raise ValueError(msg)
        res, status = self.client.get_sdo(sdo)
        return float(res), status
