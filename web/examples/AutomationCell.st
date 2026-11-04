(* CODESYS IEC 61131-3 teaching example. Create a standard PROGRAM POU PLC_PRG.
   Put VAR declarations in its declaration editor and statements in implementation.
   Requires standard TON and R_TRIG function blocks. Configure a cyclic task.
   Inputs below are simulation tags, not physical I/O mappings. Not a safety program.
   Not compiled in CODESYS as part of browser tests. *)
PROGRAM PLC_PRG
VAR
    Start : BOOL;
    ResetFault : BOOL;
    StopHealthy : BOOL := TRUE;
    PressureOK : BOOL;
    HomeSensor : BOOL := TRUE;
    ExtendedSensor : BOOL;
    ExtendRequest : BOOL;
    RetractRequest : BOOL;
    Fault : BOOL;
    State : INT := 0; (* 0 Idle, 10 Extend, 20 Retract, 90 Fault *)
    StartEdge : R_TRIG;
    ResetEdge : R_TRIG;
    TravelTimeout : TON;
END_VAR

StartEdge(CLK := Start);
ResetEdge(CLK := ResetFault);
(* Called every scan. Timer resets during the idle/fault scans. *)
TravelTimeout(IN := (State = 10) OR (State = 20), PT := T#5s);

IF NOT StopHealthy OR NOT PressureOK OR (HomeSensor AND ExtendedSensor) THEN
    State := 90;
END_IF;

CASE State OF
    0:
        IF StartEdge.Q AND HomeSensor AND NOT ExtendedSensor THEN
            State := 10;
        END_IF;
    10:
        IF TravelTimeout.Q THEN
            State := 90;
        ELSIF ExtendedSensor AND NOT HomeSensor THEN
            State := 15; (* One scan to reset the shared travel timer. *)
        END_IF;
    15:
        State := 20;
    20:
        IF TravelTimeout.Q THEN
            State := 90;
        ELSIF HomeSensor AND NOT ExtendedSensor THEN
            State := 0;
        END_IF;
    90:
        IF ResetEdge.Q AND StopHealthy AND PressureOK AND HomeSensor AND NOT ExtendedSensor THEN
            State := 0; (* A new Start edge is required for another cycle. *)
        END_IF;
ELSE
    State := 90;
END_CASE;

Fault := State = 90;
ExtendRequest := (State = 10) AND StopHealthy AND PressureOK;
RetractRequest := (State = 20) AND StopHealthy AND PressureOK;
(* Requests must be connected to an engineered actuator/valve and safety design.
   Outputs are not retained. Decide de-energised behaviour from the actual valve. *)
