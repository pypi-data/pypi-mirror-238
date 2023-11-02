![qd_logo](https://qdusa.com/images/QD_logo.png)
# MultiPyVu

* [Introduction](#intro)
* [Requirements](#requirements)
* [Example Scripts](#examples)
* [Getting Started](#getting-started)
* [Using Using MultiPyVu.Server() and MultiPyVu.Client()](#using)
* [Commands](#commands)
    * [set_temperature() / get_field()](#temp)
    * [set_field() / get_field()](#field)
    * [set_chamber() / get_chamber()](#chamber)
    * [wait_for()](#waitfor)
    * [get_aux_temperature()](#aux_therm)
* [Saving & Opening a MultiVu Data File](#save)
* [Testing the Server Using Scaffolding](#scaffolding)
* [Troubleshooting](#troubleshooting)
* [Changelog](#changelog)
* [Contact](#Contact)
***
---
### Introduction<a class="anchor" id="intro"></a>
MultiPyVu provides the ability to control the temperature, magnetic field, and chamber status of Quantum Design, Inc. products using python.  This module includes MultiPyVu.Server, which runs on the same computer as MultiVu, MultiPyVu.Client, which is used to send commands to the cryostat, and MultiPyVu.DataFile, which is used to save data to a *.dat* file and read a *.dat* file into a Pandas DataFrame.

MultiPyVu.Client can run (1) locally on the same PC as MultiVu + MultiVu>Server, or (2) remotely on another computer that has TCP access to the computer running MultiPyVu.Server.

The components of MultiPyVu enable access to the set and read the temperature, field, and chamber on the following QD platforms: PPMS, DynaCool, VersaLab, MPMS3, and OptiCool. MultiPyVu.Client can run on a PC, Mac, or Linux, including a RaspberryPi.

### Module Requirements<a class="anchor" id="requirements"></a>
MultiPyVu uses the following modules:
- python version 3.8 or higher
- pywin32 - *We recommend using version 300 or higher.*
- pandas - data read back from a *.dat* file is a Pandas Dataframe

For the Python 3 distribution Quantum Design recommends [Anaconda](https://www.anaconda.com/products/individual) as it includes most modules needed for this server and other packages useful for scientific computing.  This code was built and tested using Python 3.8.  If you are not sure which version of Python you are using, from a command prompt type:
```
python --version
```
MultiPyVu can be installed using pip via the following command:
```
pip install update MultiPyVu
```
### Included Example Scripts<a class="anchor" id="examples"></a>
Several examples have been uploaded to [Quantum Design's Pharos database](https://www.qdusa.com/pharos/view.php?fDocumentId=4339) as well as [GitHub](https://github.com/qdusa/MultiPyVu/tree/master/PharosExamples/).  These examples demonstrate various capabilities of the module, and serve as templates upon which users can add their own code to integrate external hardware operations with the environmental controls of the Quantum Design instrument.
| Filename | Description|
-----|-----
example_Local.py | A simple script which starts the server, then the client, on the PC running MultiVu.  It relays instrument parameters and status to demonstrate communication, serving as a minimum working example useful for testing basic functionality.
example_Remote-Server.py | For remote operation; this script must be running on the on the control PC along with the MultiVu executable.
example_Remote-Client.py | For remote operation; this script runs on a separate PC and relays instrument parameters and status to demonstration communication.
example_Command-Demos.py | Utilizes most functions of the module, setting temperature/field/chamber operations, reading back the values and status of those parameters, and waiting for stability conditions to be met.  As-written, it runs in local mode.
example_MVDataFile-VISA.py | Simple example showing how to route environmental parameters and data from external instruments into a single MultiVu-readable *.dat* file.  As-written, it runs in local mode.
example_graph_dat.py | Script showing how to read a MultiVu *.dat* file into a Pandas DataFrame.
whats_my_ip_address.cmd | This batch file script prints out the IP address for the computer, providing an easy way to get the server IP address needed for remote operation.

### Getting Started<a class="anchor" id="getting-started"></a>
 Once the MultiPyVu module has been installed, be sure that the MultiVu executable is running on the PC connected to the cryostat before starting the server. For testing purposes, you can use MultiVu in simulation mode on an office computer.

**Local Operation:**
It is suggested to run first run the 'Local' example with no changes on the MultiVu PC connected to the instrument- this should verify that the underlying resources required by the module are all present and functioning properly.  If this is successful, proceed to the 'example_Command-Demos.py' example for a brief demonstration of the commands used to set and monitor the sample space environmental parameters, as well as the wait command.

**Remote Operation:**
After confirming the local example scripts have executed correctly, remote operation can be attempted.  First, on the MultiVu PC, run the 'Remote-Server' script, being sure to update the IP address to reflect the IPV4 address of the server PC.  To determine this address on a Windows PC, open a command prompt, change the directory to the location of the downloaded example files, and run the following command:
```
whats_my_ip_address
```
This executes a small batch file of the same name which returns the IPV4 address needed to facilitate remote operation.  Update the existing address in the 'flags' variable of the 'example_Remote-Server.py' script and then run it.

Similarly, on the client PC, update the 'host' variable of the 'example_Remote-Client.py' script *with the same server PC IPV4 address* and run it.  The script will report the present temperature and field value/status a few times to show the connection is functioning.

**Next Steps:**
It may sometimes be desirable to combine the sample environment parameters (temperature, field) with readings from a user's own instrumentation into a single *.dat* file which can be plotted in MultiVu.  This functionality, accomplished using the MultiPyVu.DataFile module, is demonstrated using PyVISA to communicate with a VISA-compatible instrument in the  'example_MVDataFile-VISA.py' example.  Note that for this routine to execute properly, the correct instrument bus/address and query string need to be updated in the script.

For further information on the detailed operation of the components of the module, see the following sections.

### Using MultiPyVu.Server() and MultiPyVu.Client()<a class="anchor" id="using"></a>
To start the server on localhost, open MultiVu, and then, using the example script _run_server.py_, go to a command prompt and type:
```python
python run_server.py
```
As mentioned above, if the client and the server are running on the same computer as MultiVu, then one can use example_Local.py as a guide to set up the whole script in one file.

There are a list of useful flags to specify settings.  These can be found by typing -h, which brings up help information:
```python
python run_server.py -h
```

One can specify the PPMS platform, but if MultiVu is running, specifying the platform should not be necessary.  For example:
```python
python run_server.py opticool
```

If the server and client are going to be running on two different computers, the server IP address must be specified using the -ip flag.  For example, to specify an IP address of 127.0.0.1
```python
python run_server.py -ip=127.0.0.1
```
One can also follow example_Remote_Server.py to insert the IP address directly in the script.  If they are on the same computer, then the -ip flag can be omitted and server will use 'localhost.'

To write a script which connects to the server from a client machine, put all of the commands to control the cryostat inside a with block:
```python
import MultiPyVu as mpv

with mpv.Client('127.0.0.1') as client:
    <put scripting commands here>
<do post-processing once the client has been closed>
```

Note that one can use either the command line arguments to specify the host and port, or these can be specified when instantiating the Server.  If the host or parameter are specified in both cases, the command line arguments will be used.

If the host or port are not default values (localhost and 500, respectively), then these parameters must be specified when instantiating MultiPyVu.Client().

Alternatively, one can start a connection to the server using:
```python
client = mpv.Client(host='127.0.0.1')
client.open()
<put scripting commands here>
client.close_client()
<do post-processing once the client has been closed>
```

The client can also end the control scripting commands by closing the server at the same time using
```python
client.close_server()
```
instead of client.close_client().

If the client and server are being run on the same computer, then one could also write one script to control them both.
```python
import MultiPyVu as mpv

with mpv.Server() as server:
    with mpv.Client() as client:
        <put scripting commands here>
<do post-processing now that the client and server have been closed>
```

### Commands<a class="anchor" id="commands"></a>
The commands to set and get the temperature, field, and chamber status are defined here:

**Temperature**<a class="anchor" id="temp"></a>
```python
client.set_temperature(set_point,
                       rate_K_per_min,
                       client.temperature.approach_mode.<enum_option>)
```

Note that the mode is set using the client.temperature.approach_mode enum, which has items *fast_settle* and *no_overshoot.* The temperature and status are read back using:
```python
temperature, status = client.get_temperature()
```

**Field**<a class="anchor" id="field"></a>
```python
client.set_field(set_point,
                 rate_oe_per_sec,
                 client.field.approach_mode.<enum_option>)
```
Note that the approach mode is set using the client.field.approach_mode enum, which has items *linear,* *no_overshoot,* and *oscillate.* The PPMS magnet can be run *driven* or *persistent*, so it has a fourth input
which is specified using the client.field.driven_mode enum.  For the PPMS flavor:
```python
client.set_field(set_point,
                rate_oe_per_sec,
                client.field.approach_mode.<enum_option>,
                client.field.driven_mode.<enum_option>)
```
The field and status are read back using:
```python
field, status = client.get_field()
```

**Chamber**<a class="anchor" id="chamber"></a>
```python
client.set_chamber(client.chamber.mode.<enum_option>)
```
This is set using the client.chamber.mode enum, which has items *seal,* *purge_seal,* *vent_seal,* *pump_continuous,* *vent_continuous,* and *high_vacuum.*
And read back using:
```python
chmbr = client.get_chamber()
```
**Wait For**<a class="anchor" id="waitfor"></a>
```python
client.wait_for(0, 90, client.subsystem.temperature | client.subsystem.field)
```
When a setting on a cryostat is configured, it will take time to reach the new set point.  If desired, one can wait for the setting to become stable using the .wait_for(delay, timeout, bitmask) command.  A delay will set the time in seconds after the setting is stable; timeout is the seconds until the command will give up; bitmask tells the system which settings need to be stable.  This can be set using the client.subsystem enum.  In the example above, the wait_for command will wait at least 90 seconds for the temperature and field to stabilize, and will then immediately go on to the next command.

**OptiCool Auxillary Thermometer**<a class="anchor" id="aux_therm"></a>
To read the OptiCool auxillary thermometer, use the following command.  This will throw a MultiPyVuException if it is called for non-OptiCool platforms.
```python
client.get_aux_temperature()
```

### Saving & Opening a MultiVu Data File<a class="anchor" id="save"></a>
The MultiPyVu.Client class can be used in conjunction with 3rd party tools in order to expand the capabilities of measurements from a Quantum Design cryostat. One can set up a VISA connection to a voltmeter, for example, and then collect information while controlling the cryostat temperature, field, and chamber status.  This data can be collected into a MultiVu data file using MultiPyVu.DataFile.  One can also use this to read a data file into a Pandas Dataframe.

To begin using this in a script to save data, assign the column headers and create the file:
```python
import MultiPyVu as mpv

# configure the MultiVu columns
data = mpv.DataFile()
data.add_multiple_columns(['Temperature', 'Field', 'Chamber Status'])
data.create_file_and_write_header('myMultiVuFile.dat', 'Special Data')
```
Data is loaded into the file using .set_value(column_name, value), and then a line of data is written to the file using .write_data() For example:
```python
temperature, status = client.get_temperature()
data.set_value('Temperature', temperature)
data.write_data()
```

In order to import a data file into a Pandas Dataframe, one would use the following example:
```python
import pandas as pd
import MultiPyVu as mpv

data = mpv.DataFile()

myDataFrame = data.parse_MVu_data_file('myMultiVuFile.dat')
```
Putting all of this together, an example script might look like:
```python
import matplotlib.pyplot as plt
import MultiPyVu as mpv

# configure the data file
data = mpv.DataFile()
data.add_column('myY2Column', data.startup_axis.Y2)
data.add_multiple_columns(['T', 'status'])
data.create_file_and_write_header('my_graphing_file.dat', 'Using Python')

# collect some data
with mpv.Server() as server:
    with mpv.Client() as client:
        temperature, status = client.get_temperature()
        data.set_value('T', temperature)
        data.set_value('status', status)
        data.write_data()

# read data from the file and plot it
my_dataframe = data.parse_MVu_data_file('my_graphing_file.dat')
fig, ax = plt.subplots(1, 1)
fig.suptitle('Fun plot')
ax.scatter(x='Time Stamp (sec)',
           y='T',
           data=my_dataframe,
           )
plt.show()
```

### Testing the Server Using Scaffolding<a class="anchor" id="scaffolding"></a>
For testing the a script, QD has supplied scaffolding for the MultiVu commands to simulate their interactions with the server. This can be helpful for writing scripts on a computer which is not running MultiVu. To use this, start the server in scaffolding mode by using the -s flag.  The scaffolding does not need MultiVu running, so it is also necessary to specify the platform.  For example, to use scaffolding to test a script on a local computer which will be used with Dynacool:
```python
python run_mv_server.py Dynacool -s
```
One could also run in scaffolding mode with one script using the following:
```python
import MultiPyVu as mpv

with mpv.Server(flags=['-s', 'DYNACOOL']) as server:
    with mpv.Client() as client:
        <put scripting commands here>
<do post-processing now that the client and server have been closed>
```

### Troubleshooting<a class="anchor" id="troubleshooting"></a>
Typical connection issues are due to:
- Firewall. You might need to allow connections on port 5000 (the default port number) in your firewall.
- Port conflict. If port 5000 is in use, a different number can be specified when instantiating MultiPyVu.Server() and MultiPyVu.Client().
```python
server = mpv.Server(port=6000)
client = mpv.Client(port=6000)
```
- A log file named QdMultiVu.log shows the traffic between the server and client which can also be useful during troubleshooting.

## Changelog<a class="anchor" id="changelog"></a>
**2.0.0**
- September 2023
- Import full module as MultiPyVu. Instead of loading the three sub-modules as:
```python
from MultiPyVu import MultiVuServer as mvs
from MultiPyVu import MultiVuClient as mvc
from MultiVuDataFile import MultiVuDataFile as mvd
  use: 
import MultiPyVu as mpv
```
- Working with *.dat* files uses MultiPyVu.DataFile() instead of MultiVuDataFile.MultiVuDataFile()
- MultiPyVu.DataFile() enums have been updated:
    - data.TScaleType -> data.scale
    - data.TStartupAxisType -> data.startup_axis
    - data.TTimeUnits -> data.time_units
    - data.TTimeMode -> data.time_mode
- Correct a bug so that a keyboard interrupt will actually close the Server.
- Add MultiPyVu.Client() commands:
    - get_aux_temperature() to read the OptiCool auxiliary thermometer.
    - get_brt_temperature()
    - get_brt_resistance(bridge_number)

**1.2.0**
- January 2022:  Initial release

## Contact<a class="anchor" id="Contact"></a>
Please reach out to apps@qdusa.com with questions or concerns concerning MultiPyVu.

![qd_logo](https://qdusa.com/images/QD_logo.png)
