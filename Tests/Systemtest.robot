*** Settings ***
Documentation     Requirements based system test of Beercooler
Library           Zapfenkuehler_Testlib.py


*** Test Cases ***
RQ-1.1.1. Activate Cooling
    [Documentation]  Temperature Range: -10°C to +10°C
    Set Temperature  -10
    wait seconds    1
    get cooler output
    Result should be  0
    Set Temperature  10
    wait seconds    200
    get cooler output
    Result should be  1


RQ-1.1.2. Deactivate Cooling
    [Documentation]  Temperature Range: -10°C to +10°C
    Set Temperature     10
    wait seconds        200
    get cooler output
    Result should be    1
    Set Temperature     -10
    wait seconds        1
    get cooler output
    Result should be    0


RQ-1.1.4. Compressor Equalization time
    [Documentation]  System shall equalize its pressure for more than 90 seconds
    Set Temperature     10
    wait seconds        200
    get cooler output
    Result should be    1
    Set Temperature     -10
    wait seconds        1
    get cooler output
    Result should be    0
    wait seconds        90
    Set Temperature     20
    wait seconds        1
    get cooler output
    Result should be    0
    wait seconds        15
    get cooler output
    Result should be    1
