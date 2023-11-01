#!/usr/bin/python3

import asyncio, time, logging

from caproto.sync import client as ca_client
import numpy as np

from xarray import DataArray

class PvRetry(RuntimeError):
    '''
    Raised by GuidedPvReader when the PVs are not yet ready / guide does
    not yet signal readiness for signal readout.
    '''
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)


#def pv2xa(pvname, unpackScalar=False):
#    '''
#    '''
#    ca_client.read(self.prefix+k)    
#    pass


class GuidedPvReader:
    '''
    Observes a "guide" variable to determine when a specific EPICS PV signal is
    available, then collects the PV signal (which can come in a list of other PVs).
    '''

    def __init__(self, pv=None, guides=None, prefix=''):
        '''Initialises the reader.

        Args:
        
            pv: A single PV, or a list of PVs, to read out. If not
              specified here, it can be specified later.
        
            guides: A dicitonary of guide variable(s) and their respective
              value to use. The `pv` values will be acquired on the first occasion
              when *all* of the guides' values have changed *to* the value specified
              in the dictionary. If the dictionary value is a callable, it will be
              called with the current (i.e. new) guide values as its sole
              parameters and the `pv` value will be obtained the first time the
              return value changes to `True`.

            prefix: If specified, it will be prepended to all of the
              PVs' and guides' EPICS names.
        '''
        
        self.prefix = prefix or ''
        
        self.pv = (pv,) if isinstance(pv, str) \
            else tuple([ i for i in (pv or []) ])
        
        self.guides = {} if guides is None \
            else { prefix+k: v if hasattr(v, "__call__") else lambda x: x == v \
                   for k,v in guides.items() }
        
        self.guide_evals = { k:None for k in self.guides }

        
    def extract_data(self, response, pvName=None):
        '''
        Extracts "useful" data out of a response telegram.
        '''

        # Channel types can be: CHAR, DOUBLE, FLOAT, STRING, ENUM, LONG, INT.
        # The intention is to get an automatic useful native Python data type,
        # scalar or array. This means different things for different data
        # types.
        # In addition, we implement some heuristics to decorate waveforms
        # (== arrays) if our obscure array markers are present (shape, dimensions,
        # axis scaling -- to be documented ;-) )
        
        if response.data_type in (ca_client.ChannelType.STRING,):
            return response.data[0].decode('utf-8')
        
        elif response.data_type in (ca_client.ChannelType.DOUBLE,
                                    ca_client.ChannelType.FLOAT,
                                    ca_client.ChannelType.LONG,
                                    ca_client.ChannelType.INT):
            
            if len(response.data) == 1:
                return response.data[0]

            if not pvName or not pvName.endswith("_SIGNAL"):
                return response.data
            
            # If we have an array and it ends on _SIGNAL, we also try to
            # load _OFFSET and _DELTA for intrinsic scaling information
            axis = None
            try:
                offs = self.extract_data(ca_client.read(pvName.replace("_SIGNAL", "_OFFSET")))
                dlta = self.extract_data(ca_client.read(pvName.replace("_SIGNAL", "_DELTA")))
                
                axis = offs+np.array(range(len(response.data)))*dlta
            
            except Exception as e:
                #print("Reading %r: %r" % (pvName, str(e)))
                axis = np.array(range(len(response.data)))
                
            return DataArray(data=response.data, dims=["x"], coords=[axis])

        # else: how to handle ENUM / CHAR?
            
        else:
            logging.warning ("Unhandled data type: %r" % (response.data_type,))
            return response.data[0]

    
    def retr(self, pv=None, raiseRetry=True):
        ''' Synchronously checks the guides for readiness and retrieves the PV values.
        
        If `pv` is not `None`, they will be retrieved in addition to the ones
        already specified at the initialisation of the class. If `prefix` is
        specified (not `None`), it will override whatever was specified at the
        initialisation of the class, but only for the PVs specified here.
        '''

        good_guides = 0

        for (k,v) in self.guides.items():
            data = self.extract_data(ca_client.read(k))
            if v(data) and (not self.guide_evals[k]):
                good_guides += 1
            self.guide_evals[k] = v(data)

        if good_guides == len(self.guides):
            pv = [k for k in (pv or {}) ]
            pv.extend([k for k in self.pv])
            return { k: self.extract_data(ca_client.read(self.prefix+k), pvName=self.prefix+k) \
                     for k in pv }

        raise PvRetry()


    async def value(self, timeout=-1, pollPeriod=0.001):
        '''
        Asynchronousluy waits for retr() to deliver a valid dataset.
        Cancels after `timeout` seconds (if timeout >= 0).
        '''
        tstart = time.time()
        while True:
            try:
                return self.retr()
            except PvRetry:
                if (timeout > 0) and (time.time()-tstart >= timeout):
                    raise
            await asyncio.sleep(pollPeriod)



class GuidedAsyncReader(GuidedPvReader):
    ''' Same as GuidedPvreader but uses the asyncio caproto client to do the reading.
    '''
    
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

        self.guide_pvs = None
        self.data_pvs = None

        
    async def connect(self):
        guides = [k for k in self.guides.keys()]
        pvnames = [self.prefix+k for k in self.pv ]
        
        self.guide_pvs = await self.ctx.get_pvs(*guides)
        self.data_pvs = await self.ctx.get_pvs(*pvnames)


    async def wait_for_guides(self):
        good_guides = 0
        guides = await asyncio.gather(*[v.read() for v in self.guide_pvs ])
        for (k,v),d in zip(self.guides.items(),guides):
            d = self.extract_data(d)
            if v(data) and (not self.guide_evals[k]):
                good_guides += 1
            self.guide_evals[k] = v(data)
        return good_guides

    
    async def value(self, timeout=-1, pollPeriod=0.001):
        
        if self.guide_pvs is None or self.data_pvs is None:
            await self.connect()

        try:            
            tstart = time.time()
            while True:
                good_guides = await self.wait_for_guides()

                if good_guides == len(self.guides):
                    data = await asyncio.gather(*[v.read() for v in self.data_pvs ])
                    return {k:self.extract_data(v) for k,v in zip(self.pv, data) }

                if (timeout > 0) and (time.time()-tstart >= timeout):
                    raise PvRetry()

                await asyncio.sleep(pollPeriod)
        except ConnectionRefusedError as e:
            print("Connection refused; Waiting...")
            await asyncio.sleep(pollPeriod*1000)
            self.guide_pvs = None
            self.data_pvs = None
            print("Reconnecting...")

            
    def retr(self):
        raise NotImplemented("retr() not available in async mode")
