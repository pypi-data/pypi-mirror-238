#!/usr/bin/python3

import time
import asyncio
import logging

from emmi.api.exports import ConnectorKinds, SignalConnector, ActorConnector, \
    PropertyConnector    

class MockMotor(object):
    '''
    The simplest of the simplest motors: can only move, report position and stop.

    Also exports `.errors` and `.flags`. The first is expected to be an empty
    list when the motor state is "ok" (i.e. no error), or a list with one
    or several objects (e.g. strings) when errors with the motor persit.
    Calling `.clear()` clears the error list.

    The `.flags` member is expected to be an enumerable data type (list,
    tuple, dictionary, set or something similar) to convey supplementary
    information about motor events, e.g. triggering of low / high switch
    limits etc.

    With the exception of limit switches (see `.__init__()`), `MockMotor`
    does not intrinsically handle or simulate any other switches.
    '''

    def __init__(self, *args, **kwargs):
        ''' Creates a mock-up of an EDA Motor.

        Accepts all args as a courtesy of being a good mock-up class,
        but ignores most of them. A number of arguments are specific
        to the mock class. They are listed below.

        Args:
            mock_timeslice: a measure of how "fast" a mock motor is moving.
              Every `.goto()` call on a mock motor will execute a movement
              of the specified distance in exactly `mock_timeslice` seconds,
              regardless of the distance.

            limits: tuple of `(low, high)` to simulate the lower,
              respectively higher hardware limits. If any of those
              is reached in the mocking position, `.flags` will contain
              `"LLIM"` or `"HLIM"`, respectively. Alternatively, this can
              also be a dictionary with two or three items. If it's two
              items, it's used as the low/high limits, and the
              keys are used in `.flags` instead of `"HLIM"`/`"LLIM"`.
            
        '''
        self.mock_timeslice = kwargs.get('mock_timeslice', 5.0)
        self.start = 0.0
        self.target = 0.0
        self.tstamp = 0.0
        self.errors = []
        self._limits = kwargs.get('limits', None)
    
    def where(self):
        '''
        Returns current position -- that is the position that we'd be currently
        having if we'd wanted to go from "current" towards "target" within
        the timeslice "mock_timeslice"
        '''
        tdelta = (time.time()-self.tstamp)
        if tdelta > self.mock_timeslice:
            tdelta = self.mock_timeslice
        dist = self.target-self.start
        return self.start + dist * (tdelta/self.mock_timeslice)

    def goto(self, val):
        '''
        Sends command to move to position (doesn't wait)
        '''
        self.start = self.where()
        self.target = val
        self.tstamp = time.time()

    def stop(self):
        '''
        Sends command to stop (doesn't wait). Technically, we'll be still
        in state "moving" for a while after this, but we'd be moving
        towards the position we're already onto.
        '''
        if self.moves():
            self.goto(self.where())

    def moves(self):
        '''
        Returns True if the motor moves. We fake this by testing whether
        we're still within the "timeslice". This has the added benefit
        that sometimes moves() returns False right away (i.e. if we weren't
        moving in the first place), and sometimes still returns False
        for a considerate amount of time (i.e. until the end of the current
        slice) if we were moving and just received a stop() command.
        '''
        now = time.time()
        return (now - self.tstamp) <= self.mock_timeslice

    def clear(self):
        '''
        Clears all outstanding error flags (they may pop up again).
        '''
        self.errors = []

    @property
    def flags(self):
        ''' Check for HLIM / LLIM and return the appropriate strings.

        Strings are either default "HLIM", "LLIM" respectively, or
        the keys of the `._limits` parameter.
        '''
        if self._limits is None:
            return set()

        f = set()

        lk = [k for k in self._limits.keys()]

        low = ('LLIM', self._limits[0]) if not isinstance(self._limits, dict) \
            else (lk[0], self._limits[lk[0]])

        high = ('HLIM', self._limits[-1]) if not isinstance(self._limits, dict) \
            else (lk[-1], self._limits[lk[-1]])

        p = self.where()
        
        if p <= low[1]:
            f.add(low[0])

        if p >= high[1]:
            f.add(high[0])

        return f
        
    

class MotorEngine(object):
    '''
    Generic motor engine class. Essentially cycles through the states
    as it should, and serves the most basic properties `position` and
    `position_relative` correctly. It's based on generic True/False
    conditional procedures to decide when to switch.

    In its default incarnation, the conditionals are just generic waiting
    functions (1 second for anything), so it can be used as a mock-up for
    unit testing. But if you replace the conditionals by things that do
    "real stuff", it's actually usable for production.
    '''
    
    def __init__(self, motor=None):
        
        self.__motor = motor or MockMotor()

        # current state
        self.__state = "INIT"

        # Scheduled absolute or relative position change.
        # We move by storing the new positional values here first,
        # then sending them on their way when we're IDLE.
        self.__scheduled_goto = None
        self.__scheduled_moveby = None

        # Current errors list
        self.errors = []        

        # mock-up position setter 
        self.hardware_where  = self.__motor.where       
        self.hardware_ready  = lambda: True
        self.hardware_goto   = self.__motor.goto
        self.hardware_moveby = None
        self.hardware_brake  = self.__motor.stop
        self.hardware_moves  = self.__motor.moves
        self.hardware_clear  = self.__motor.clear


    def __clear_goto(self):
        self.__scheduled_goto = None
        self.__scheduled_moveby = None


    def state_enter(self, state):
        '''
        This is called exactly once, at the beginning, for every
        state that is newly entered. Returns the state string,
        for convenience.
        '''
        logging.info ("State: %s -> %s" % (self.__state, state))
        if state == "STOP":
            self.__clear_goto()
            if self.hardware_moves():
                self.hardware_brake()
        elif state == "BUSY":
            if self.__scheduled_moveby is not None:
                logging.info("BUSY state: relative move scheduled by %r" % self.__scheduled_moveby)
                if self.hardware_moveby:
                    self.hardware_moveby(self.__scheduled_moveby)
                else:
                    self.hardware_goto(self.hardware_where()+self.__scheduled_moveby)
            elif self.__scheduled_goto is not None:
                logging.info("BUSY state: absolute move scheduled to %r" % self.__scheduled_goto)
                self.hardware_goto(self.__scheduled_goto)
            self.__clear_goto()
        elif state == "IDLE":
            self.hardware_clear()
            self.errors = []
        else:
            pass
        return state
             

    ## State procedures -- return the new state they need to switch to.
    ## We're essentially delegating everything to __generic_state_proc().
    def state_proc(self, state):

        # These are the states we can advance to from here
        advances = {
            'INIT': { 'IDLE':  lambda: self.hardware_ready() },
            'IDLE': { 'STOP':  lambda: len(self.errors) > 0,
                      'BUSY':  lambda: self.__scheduled_goto is not None or \
                                       self.__scheduled_moveby is not None},
            'BUSY': { 'STOP':  lambda: len(self.errors) > 0 or not self.hardware_moves() },
            'STOP': { 'ERROR': lambda: len(self.errors) > 0 and not self.hardware_moves(),
                      'IDLE':  lambda: len(self.errors) == 0 and not self.hardware_moves() },
            'ERROR': { 'IDLE': lambda: len(self.errors) == 0 },
            'FAIL': {}
        }

        try:
            adv = advances[state]
        except KeyError as e:
            # BUSY needs to get some extra treatment because it can be extended
            if state.startswith('BUSY'):
                adv = advances['BUSY']

        # execute current state proc
        try:
            for k,v in adv.items():
                #print ("%s/Testing for %s: %r" % (state, k, v))
                if v():
                    return self.state_enter(k)
        except Exception as e:
            logging.error ("Unexpected exception in state %s:" % state, str(e))
            return "FAIL"

        return state
    
    
    # Current position -- getter reads out the hardware, setter
    # is a bit more complicated because we have to acknowledge
    # the current state (i.e. can't just override current states).
    @property
    def position(self):
        return self.hardware_where()

    @position.setter
    def position(self, val):
        if self.state == "IDLE":
            self.__scheduled_goto = val
        trig = self.state

             
    # Increment/decrement position by relative values -- the getter returns
    # 0 as soon as the scheduled move has been triggered, the setter just
    # sends the command / schedules the move.
    @property
    def position_relative(self):
        return self.__scheduled_moveby or 0
    
    @position_relative.setter
    def position_relative(self, val):
        if self.state == "IDLE":
            self.__scheduled_moveby = val
        trig = self.state
        

    def leave_ERROR(self, new_state):
        '''
        The only way we can leave ERROR is by clearing/going to IDLE
        '''
        if new_state == "IDLE":
             self.errors = []
             return self.state_enter("IDLE")
        return "ERROR"
             

    def leave_BUSY(self, new_state):
        '''
        The only way we can leave BUSY is by issuing a STOP.
        We accept that for `new_state` either as being STOP
        or ERROR.
        '''
        logging.info ("Leaving BUSY:", new_state)
        if new_state in [ "STOP", "ERROR" ]:
             return self.state_enter("STOP")
        return "BUSY"


    @property
    def state(self):
        self.__state = self.state_proc(self.__state)
        return self.__state
             
    @state.setter
    def state(self, new_state):
        '''
        This is only an API point -- i.e. for external use, not
        internal. There are only specific combinations of
        "current state" / "end state" that the user is allowed
        to perform. Everything else we ignore.
        '''
        if self.__state == 'ERROR':
            self.__state = self.leave_ERROR(new_state)
        elif self.__state.startswith("BUSY"):
            self.__state = self.leave_BUSY(new_state)


class MotorConnector(object):
    '''
    Implements a simple EPICS motor record, with a small subset of the
    [EPICS motor record](https://epics.anl.gov/bcda/synApps/motor/R7-1/motorRecord.html)
    variables. Relies on a motor inteface as described by `MotorEngine`, i.e.
    a class with the following properties:

      - `position`: returns the current motor values, respectively moves
        to the specified relative value

      - `position_relative`: facilitates a movement relative to the current
        position

      - `state`: a string that begins with one of the following:
    
          - "INIT" (preparing to take commands)
    
          - "IDLE" (not moving, ready to take commands)
    
          - "BUSY" (not able to accept commands, most likely already moving)
    
          - "ERROR" (stopped, reached a situation which requires external action)

          - "STOP" (stopping)
    
          - "FAIL" (unefined state, best effort to be stopped, unrecoverable error)
    
        The state string is intentionally checked only for its beginning part.
        States may be explicitly extended by appending information to strings,
        e.g. "BUSY.TRACKING" or "BUSY.HOMING" to distinguish different flavors
        of states. `SimpleMotor` will not react to anything beyond the five
        1st-level state information, but other software layers may.

    This class needs to be used with a
    [pythonSoftIOC](https://dls-controls.github.io/pythonSoftIOC)
    compatible EPICS IOC Python API. It uses `asyncio` for all asynchronous
    work.

    It implements the EPICS motor record variables VAL, RBV, RVL, HOMF/HOMB,
    STOP.

    FIXME: need to add support for supplementary actions / properties / signals
    (e.g. extend by additional "BUSY" states, or read/write specific properties
    like limits, force probe thresholds etc).
    '''    

    def __init__(self, motor_prefix, motor_engine, ioc_dispatcher,
                 poll_period=0.1, separator="_", style="simple"):
        '''
        Initializes the IOC variables. Parameters:
        
          - `motor_prefix`: a string to prepend to the motor variables.
        
          - `motor_engine`: the `MotorEngine` object we'll be talking to.
        
          - `ioc_dispatcher`: a pythonSoftIOC asyncio dispatcher compatible
            instance (typically a `softioc.asyncio_dispatcher.AsyncioDispatcher()`)
        '''

        self.pollPeriod = poll_period

        #from softioc import builder as ioc_builder

        # SPEC needs the following:
        #
        # Can be ignored / business of the controller?
        #  o ACCL: acceleration time in seconds (0.0)
        #  o BDST: backlash distance egu (0)
        #  o BVAL: backlash velocity egu/s (0)
        #  o VBAS: base velocity (minimum velocity?) egu/s (0)
        #  o ERES: encoder step size egu (0)
        #  o MRES: motor step size egu (0)
        #
        # Calibration fields and coordinate system transformations:
        #  - SET: set/use switch for calibration fields (0: use, 1: set)
        #  - FOFF: offset freeze switch -- is the user prevented from
        #          writing the offset?
        #  - OFF: user offset egu
        #  + DIR: user direction        
        #  - RRBV: raw readback value
        #  - RVAL: raw desired value        
        #
        # Unclear:
        #  o UEIP: use encoder if present (always 1?)
        #  o VELO: velocity egu/s (set to 0?)
        #
        # Need to have / already have:
        #  o STOP: stop
        #  o VAL: user desired value
        #  - SPMG: stop/pause/move/go -- complicated beast
        #    - Stop: same as STOP?        
        #
        # Nice to have, but not part of the EDA Motor Model:
        #  + DHLM: dial high-limit
        #  + DLLM: dial low-limit
        #  + HLS: at high-limit switch
        #  + LLS: at low-limit switch        
        #  o DMOV: done moving to value
        #
        # Unknown:
        #  + DISP: disable (turn off motor/unusable)        
        #
        # Nice to have, not needed by SPEC:
        #  o EGU: engineering unit names
        #  - RLV: relative-move value: when changed, changes VAL,
        #    then resets itself to 0
        #  
        
        self.engine = motor_engine

        # VAL/RBV
        self.con_pos = PropertyConnector(ioc_dispatcher,
                                         prefix=motor_prefix+separator,
                                         access=(motor_engine, "position"),
                                         signal={ 'poll_period': poll_period },
                                         kind="analog")

        # STATEVAL/RBV
        self.con_state = PropertyConnector(ioc_dispatcher,
                                           prefix=motor_prefix+separator+"STATE",
                                           access=(motor_engine, "state"),
                                           signal={ 'poll_period': poll_period },
                                           kind="strings",
                                           validator={ 'values': [
                                               'INIT', 'IDLE', 'BUSY', 'STOP', 'ERROR', 'FATAL'
                                           ]})

        # STOP
        self.con_stop = ActorConnector(var=motor_prefix+separator+"STOP",
                                       access=self.conExecStop,
                                       kind="values",
                                       validator={'values': [0, 1]})

        if style == "spec":

            # lots of variables expected by spec but which we don't really serve
            self.con_constants = [
                SignalConnector(ioc_dispatcher,
                                var=motor_prefix+separator+suffix,
                                access=lambda: value,
                                kind=kind,
                                poll_period=10.0)
                for suffix,kind,value in [ ("ACCL", "analog", 0),
                                           ("BDST", "analog", 0),
                                           ("BVAL", "analog", 0),
                                           ("VBAS", "analog", 0),
                                           ("ERES", "analog", 0),
                                           ("MRES", "analog", 0),
                                           ("UEIP", "analog", 1),
                                           ("VELO", "analog", 0)]]
            #("EGU",  "text", "mm")] ]

            # DMOV - set to 0 when motor begins moving
            self.con_dmov = SignalConnector(ioc_dispatcher,
                                            var=motor_prefix+separator+"DMOV",
                                            access=lambda: int(self.engine.state == "IDLE"),
                                            kind="integer",
                                            poll_period=self.pollPeriod)

            
            self.con_status = SignalConnector(ioc_dispatcher,
                                              var=motor_prefix+separator+"STATUS",
                                              access=lambda: 0x02 if self.engine.state == "BUSY" else 0x00,
                                              kind="integer",
                                              poll_period=self.pollPeriod)
        
                   
        ## Enable 'HOMF' command
        #self.pv_homf = builder.aOut(axvar+"_HOMF", initial_value=0, always_update=True,
        #                            on_update=TriggerAndStatus(lambda: axobj.homing = True,
        #lambda: axobj.homing)]

        #class rel_add(object):
        #    def __init__(self, pos_prop):
        #        self.pos_prop = pos_prop
        #        self.my_pv = None
        #    def __call__(self, value):
        #        self.pos_prop += val
        #        if self.my_pv:
        #            self.my_pv.set(0)
        #           
        #self.rel_mover = rel_add(motor_engine.position)
        #
        #self.pv_relpos = ActorConnector(var=motor_prefix+"_RLV",
        #                                access=self.rel_mover,
        #                                kind='analog',
        #                                validator=None)
        #
        #self.rel_mover = self.pv_relpos

    def conPollDmov(self):
        return int(self.engine.state == "IDLE")

    async def conExecStop(self, val):
        '''
        EPICS motor STOP command: if val==1, it executes the STOP command,
        then it sets VAL to current position and resets itself to 0.
        '''
        if val != 1:
            return

        self.engine.state = "STOP"
        self.con_stop.pv.set(0)
        
        while self.engine.state != "IDLE":
            await asyncio.sleep(self.pollPeriod)
            
        self.con_val.set(self.engine.position)
            

class WorkerObject(object):
    '''
    Interface for a worker object to be managed by a WorkerEngine.
    '''
    def work(self, params):
        pass

    def abort(self):
        pass

    def clear(self):
        pass

    def isBusy(self):
        pass


class WorkerEngine(object):
    '''
    This models an EPICS device that "does something." It's the precursor of
    a positioner (e.g. a Motor) in the sense that it has a simple state
    diagram which shows whether the device is currently busy performing a
    task ("BUSY"), or free to accept tasks ("IDLE").

    The complete state diagram is as follows:

      - INIT: starting up, ends up in IDLE

      - IDLE: waiting for tasks, can exit through BUSY or ERROR

      - BUSY: currently performing, can exit through DONE or ERROR

      - DONE: done performing, cleaning up / waiting to go to IDLE

      - ERROR: error, user needs to acknowledge

      - FAIL: irrecoverable error

    The state names are configurable.
    '''
    
    def __init__(self, stateNames=None):

        self.states = stateNames or {
            'INIT': 'INIT',
            'IDLE': 'IDLE',
            'BUSY': 'BUSY',
            'DONE': 'DONE',
            'ERROR': 'ERROR',
            'FAIL': 'FAIL'
        }

        # All should return the 
        self.state_workers = {
            'INIT': self.state_INIT,
            'IDLE': self.state_IDLE,
            'BUSY': self.state_BUSY,
            'DONE': self.state_DONE,
            'ERROR': self.state_ERROR,
            'FAIL': self.state_FAIL
        }

        # Initial work do be done when entering a state -- no return value.
        self.state_entries = {
            'INIT': self.enter_state_INIT,
            'IDLE': self.enter_state_IDLE,
            'BUSY': self.enter_state_BUSY,
            'DONE': self.enter_state_DONE,
            'ERROR': self.enter_state_ERROR,
            'FAIL': self.enter_state_FAIL
        }

        self.__state = self.states["INIT"]
        self.__do_run = True
        

    def enter_state_generic(self):
        pass

    # Ignore INIT for now, jump straight to IDLE
    enter_state_INIT = enter_state_generic
    def state_INIT(self):
        return "IDLE"
    
    # FAIL is easy, it does nothing.
    def enter_state_FAIL(self):
        log.error("Entered FAIL -- tttthat's all, folks!")
    def state_FAIL(self):
        return "FAIL"

    # The rest... just wait.
    enter_state_IDLE = enter_state_generic
    enter_state_BUSY = enter_state_generic
    enter_state_DONE = enter_state_generic
    enter_state_ERROR = enter_state_generic

    async def run(self, period=0.1):
        while self.__do_run:
            tstart = time.time()
            current_state = self.__state
            new_state = self.state_workers[current_state]()
            if new_state != current_state:
                logging.info("State: %r -> %r" % (current_state, new_state))
                self.__state = new_state
                self.state_entries[new_state]()
            tdiff = time.time()-tstart
            await asyncio.sleep(tdiff)
        
