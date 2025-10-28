# This project cleans up OSD messages in firmware for NewBeeDrone Hummingbird F4 V4 TinyWhoop drone

Namely, it changes: 
`SEND IT` to
` READY `

`OH SHIT RSSI LOW` to
`WARNING RSSI LOW`

`BATTERY DYING` to
`BATT CRITICAL` 

`DAMN HOT` to
`CORE HOT` 

`  DAYUMN` to
`BATT LOW`

`> SHAME BRO <` to 
`> TURN OVER <`

The goal of the project is achieved by editing the compiled `.hex` file of the firmware provided by NewBeeDrone company, 
since complete source was not available. 

The tools used in the process are two python scripts included here in the [/src](/src) directory.

The resulting firmware `.hex` file is tested and confirmed to work, as it was flashed on the drone and flown, 
confirming the messages are indeed changed. 
