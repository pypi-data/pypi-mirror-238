# ECTweaker
ECTweaker Library for python allows users to read/write and control the EC of laptops, specially MSI!

# INSTALLATION
- pip install ectweaker
  - If the above method doesn't work please install in a virtual environment and call it in scripts from the virtual environments only!

# Preparing the EC to be read/write friendly
- Disable secure boot
- To check one of the example to use this code properly, visit https://github.com/YoCodingMonster/OpenFreezeCenter-Lite/tree/main and check ```OpenFreezeCenter-Lite.py``` file

# Updating 
- pip install ECTweaker --upgrade

# Functions

## ```check()```
- This prepare the OS for EC read/write functionality and reboots the system for the first time only.
    - ```Return Type``` - int
    - ```Returns```
        - ```1``` if EC read/write is enabled.
        - ```0``` if EC read/write is not enabled.
    - Example
    ```
    import os
    CHECK = ECT.check()
    if CHECK == 1:
        # your_script_here
    else:
        os.system("shutdown -r +1")
        print("Rebooting system within 1 min!\nPlease save all work before it happens!")
    ```

## ```write(BYTE ADDRESS, VALUE)```
- This will allow you to write any INTEGER value to BYTE ADDRESS.
    - ```Parameters```
        - ```BYTE ADDRESS``` - Hex address of the memory where VALUE needs to be written.
        - ```VALUE``` - content which needs to be written at BYTE ADDRESS.
    - Example
    ```
    import ECTweaker as ECT
    ECT.write(0xd4, 121)
    ```

## ```read(BYTE ADDRESS, SIZE)```
- This will allow you to read INTEGER value from BYTE ADDRESS.
    - ```Return Type``` - int
    - ```Returns``` - VALUE stored at BYTE ADDRESS fo memory provided.
    - ```Parameters```
        - ```BYTE ADDRESS``` - Hex address of the first memory from where VALUE is retrived.
        - ```SIZE``` - How many adjacent BYTE ADDRESS stores the complete VALUE.
    - Example
    ```
    import ECTweaker as ECT
    VALUE = ECT.read(0xd4, 1)
    ```

## ```fan_profile(PROFILE, VALUES)```
- This allows for MSI laptops with intel CPU to set Fan profiles.
    - ```Parameters```
        - ```PROFILE``` - Fan profile which needs to be, considered values are as follows.
            - ```auto```, ```advanced```, ```cooler booster```
        - ```ONOFF``` - This is a list of address and values which needs to be set in order to change the fan profile.
            - [[ADDRESS, VALUE ON],[COOLER BOOSTER ADDRESS, VALUE OFF]]
        - ```ADDRESS``` - This is the list of addresses for CPU and GPU fan speeds as [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
        - ```SPEED``` - This is the list of speed percentages for CPU and GPU fans at set temps as [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
           
    - Example - Auto is turned on on MSI laptop with 11th gen processor and (Cooler Booster is being turned off as precaution)
    ```
    import ECTweaker as ECT
    ECT.fan_profile("auto", ONOFF = [[0xd4, 141], [0x98, 2]], ADDRESS, SPEED)
    ```
    - Example - Cooler booster is being turned on
    ```
    import ECTweaker as ECT
    ECT.fan_profile("auto", ONOFF = [0x98, 130])
    ```

## ```speed_writer(ADDRESS, SPEED)```
- Internal function used by ```fan_profile(PROFILE, VALUES)``` function to set the fan speed curve.
    - ```Parameters```
        - ```ADDRESS``` - This is the list of addresses for CPU and GPU fan speeds as [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
        - ```SPEED``` - This is the list of speed percentages for CPU and GPU fans at set temps as [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
