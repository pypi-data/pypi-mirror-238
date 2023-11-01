# The EPIC Monday-Morning Integration Toolkit

[![pipeline status](https://codebase.helmholtz.cloud/emmitools/emmi/badges/master/pipeline.svg)](https://codebase.helmholtz.cloud/emmitools/emmi/-/commits/master)
[![coverage report](https://codebase.helmholtz.cloud/emmitools/emmi/badges/master/coverage.svg)](https://codebase.helmholtz.cloud/emmitools/emmi/-/commits/master)
[![Latest Release](https://codebase.helmholtz.cloud/emmitools/emmi/-/badges/release.svg)](https://codebase.helmholtz.cloud/emmitools/emmi/-/releases)
[![pylint](https://codebase.helmholtz.cloud/emmitools/emmi/-/badges/pylint.svg)](https://codebase.helmholtz.cloud/emmitools/emmi/-/lint/)

EMMItool is the "Swiss army knife" for rapid ad-hoc integration of
scientific instrumentation into [EPICS](https://epics.anl.gov/)-based
[beamline control sytems](https://blueskyproject.io/).

## Concepts and Components

EMMI is separated in different layers of which either can be used
for specific types of integrations, ranging from rapid "Monday morning"
hacks for attaching an existing non-EPICS capable device to a beamline,
to a writing full-fledged EPICS-IOC support for your device:

  - [The EMMI Device Architecture (EMA)](#emmi-device-architecture) offers
    abstraction layers for access to motors, signals and switches
  
  - [EMMIdaemon](#emmi-daemon) is a stand-alone application that runs
    and presents an ad-hoc IOC on one side, with a REST-like HTTPS API
	support on the other side

### EMMI Device Architecture

#### Controlling Motors

EMMI uses a simple yet extensible motor interface. The philosophy is that
we're considering an *ideal* motor in our model. We don't concern ourselves
with backlash compensation, acclereation ramps etc. We care about ***what** the
motor is supposed to do*, as opposed to ***how** it is going to do it*.

For this, we consider the following properties:
  
  - `position`: R/W property which returns the current motor values,
    respectively moves to the specified absolute value when written to

  - `position_relative`: R/W property that facilitates a movement relative
     to the current position when written to; always returns 0.

  - `state`: a R/W property that indicates the current state of the
    (abstract) motor device; can be explicitly set within specific
	parameters to advance to specific states.
	
The state diagram of a motor looks like this in its most simple form:
```
          ┌──────────┐
          │   INIT   ├┄┄┄┄┄┄┄┄┄┄┄┄►┄┄┐
          └────┬─────┘               ┊
               ▼                     ┊
          ┌────┴─────┐               ┊
          │          ├┄┄┄┄┄┄┄┄┄┄┄┄►┄┄┤
  ┌───►───│   IDLE   ├┄┄┄┄┄►┄┄┐      ┊
  │       └────┬─────┘        ┊      ┊
  │            ▼              ┊      ┊
  │   ┌┈┈┈┈┈┈┈┈┴┈┈┈┈┈┈┈┈┈┐    ┊      ┊
  │   ┊                  ├┄┄┄┄┄┄┄┄►┄┄┤
  │   ┊     BUSY...      ├    ┤      ┊
  │   ┊                  ┊    ┊      ┊
  │   └┈┈┈┈┈┈┈┈┬┈┈┈┈┈┈┈┈┈┘    ┊      ┊
  │            ▼              ┊      ┊
  │       ┌────┴─────┐        ┊      ┊
  ├───◄───┤          ├┄┄┄┄┄◄┄┄┘      ┊
  │       │   STOP   ├┄┄┄┄┄┄┄┄┄┄┄┄►┄┄┤
  │       └────┬─────┘               ┊
  │            ▼                     ▼
  │       ┌────┴─────┐           ┌───┴────┐
  └───◄───┤  ERROR   ├┄┄┄┄┄┄┄┄►┄┄┤  FAIL  │
          └──────────┘           └────────┘
```

Which translates to:

  - `INIT` is the initial states after startup, device is undergoing
    custom configuration and is not ready yet.

  - `IDLE` device is ready to perform according to commands
	 
  - `BUSY` is the state in which device is performing, most likely moving
  
  - `STOP` is the state in which the device is decelerating with the
    intention of coming to a standstill. This can be part of a regular
    `IDLE`-`BUSY` cycle (i.e. returning to `IDLE` once standstill is reached),
	or can be an intermediate state towards an `ERROR` state, ensuring
	that the device is stopped for handling of errors.
    
  - `ERROR` is a well-defined state which represents the device *not*
    peforming, but which is still part of the "well defined" behavior of
	the device. Such a state, for instance, is reaching hardware limits
	or impossibility to execute a command (e.g. because coordinates are
	outside of allowed range). The device is always in a standstill
	when in `ERROR`, which is ensured by the fact that `ERROR` is only
	entered through `STOP`. `ERROR` can be entered from all "regular"
	operational states (`IDLE`, `BUSY` or `STOP`), but not from `INIT`
	-- initialisation errors result in `FAIL`.
    
  - `FAIL` is the state of a fatal error, incompatible with "defined
    behavior" of the device. It is a terminal state, meaning that there
	is no system-supported from this state. A complete reinitialisation,
	typically encompanied by a power cycle or hardware reset is the
	action to be performed to advance from `FAIL`. It can be entered
	from any other state.


The `BUSY` state deserves extra explanation, as it's the main mechanism
for extending the functionality of a motor.

In its most simple form, a motor has only one task: to move an (abstract)
axis to a specified value. However, slightly more complex real-world
applications may differentiate more strictly on the type of movement
to be performed:

  - a **slewing** movement is performed autonomously with maximum
    speed within parameters, towards a specific target;

  - a **jogging** movement, e.g. triggered by a joystick, is performed
    with a predefined speed as long as a condition (button press)
	actively persists;
	
  - a **tracking** movement is a movement that is bound to time
    constraints, e.g. hitting specific coordinates at specific times;
	
  - a **homing** movement may be used to define a slewing towards
    a hard-coded parking position;
	
  - a **dialing** or **tweaking** movement may be a manual correction
    on top of a predefined tracking path, etc.

Even more complex moves require several stacked types of movements
(e.g. a *tracking* requires a *slewing* into position first, and
accept *tweaking* input while performing the actual tracking).

As far as EMMI is concerned, we don't care about the complexity of
the movement itself, we only care about representing high-level
states of operation at an EPICS interface level -- roughly speaking,
to us, the motor "does" or "doesn't do" anything. To model this,
we allow splitting the `BUSY` state into sub-states, hiearchically
denoted (e.g. `BUSY.SLEW` or `BUSY.TRACK`...). The restriction is
that they all must either end in `STOP`, before returning to `IDLE`
or entering `ERROR`, or must definitively fail directly into `FAIL`.

These supplementary states my be controlled by variables and properties
which EMMI will happily manage and pass through to the EPICS interface,
but will not understand or touch -- e.g. speed limits, accelerations,
homing coordinates etc.

However, as it is customary with EPICS, EMMI will manage designated
boolean PVs to trigger these states and indicate the successful
performance of the action. This allows to a certain degree easy
implementation of the "HOMF/D", "TWF/D" or "JOG" class of commands of
an [EPICS motor record](https://epics.anl.gov/bcda/synApps/motor/R7-1/motorRecord.html).

This results in a 4-layer architecture that leads from the hardware
controls to the EPICS variables:
 
  - The **Axis Control** is the layer (within Python) which
    directly serves the hardware interface API, e.g. typically a 
	lass wrapped around a pySerial interface.
	
  - The **Engine** is a layer which enforces an API compatible
    the state diagram above, with the properties `position`, `position_relative`
	and `state` as described.
	
  - The **Connector** is a translator between the motor engine and 
    a generic EPICS IOC generator, e.g. as provided by pythonSoftIOC.
	
  - The **IOC Generator** is a library that does the actual EPICS work.
  
In the spirit of "integration", we acknowledge that typically the first
layer has already been written, and there is legitimate concern to reuse
it. The only restriction EMMI imposes is for the *Axis Control*
to not block. For the last layer, EMMI makes heavy use of pythonSoftIOC.
	
What remains is the *Engine* and *Connector*, which EMMI
implements in the classes [`MotorEngine`]() and [`MotorConnector`]()
within [`emmi.eda`](./src/emmi/eda.py).

Typically, `MotorConnector` needs to specifically dock to user-supplied
*Axis Control* code. There are three ways to do this:
  
  1. Write from scratch or re-write your *Axis Control* to be *Engine*
     compatible. This is, of course, the preferred method, but not
	 always available.
	 
  2. Use the supplied `MotorConnector`, which is a highly configurable
     template that makes heavy use of Python's "duck typing" to attach
	 to a more-or-less compatible *Axis Control*. This has the advantage
	 that it doesn't require tampering with "tried and true" hardware
	 control code of the *Axis Control* layer.
	 
  3. Write your own *Motor Controller* from scratch, paying attention
     to reflect the *Engine* API, as described above.
	 
As a side note, this architecture also gives a natural layer at which
to attach useful, yet hardware-independent, unit testing: by replacing
the `MotorConnector` with a mock-up class that behaves as it's supposed
to, all the layers between there and the EPICS interface can be tested
in a suitable, automated CI/CD environment.
