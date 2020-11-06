import DataProcessingTools as DPT
import matplotlib.pyplot as plt
import hickle as hkl
import os
import numpy as np
from .misc import getChannelInArray

class Waveform(DPT.DPObject):
    filename = 'waveform.hkl'  # this is the filename that will be saved if it's run with saveLevel=1
    argsList = []  # these is where arguments used in the creation of the object are listed
    level = 'channel'  # this is the level that this object will be created in

    def __init__(self, *args, **kwargs):
        DPT.DPObject.__init__(self, *args, **kwargs)

    def create(self, *args, **kwargs):
        pwd = os.path.normpath(os.getcwd());
        self.channel_filename = [os.path.basename(pwd)]  
        template_filename = os.path.join(
            DPT.levels.resolve_level('day', self.channel_filename[0]),
            'mountains', self.channel_filename[0], 'output', 'templates.hkl')
        templates = hkl.load(template_filename)
        self.data = [np.squeeze(templates)]
        aname = DPT.levels.normpath(os.path.dirname(pwd))
        self.array_dict = dict()
        self.array_dict[aname] = 0
        self.numSets = 1
        self.current_plot_type = None
        
        if len(self.data) != 0:
            DPT.DPObject.create(self, *args, **kwargs)
        else:
            DPT.DPObject.create(self, dirs=[], *args, **kwargs)            
        
    def append(self, wf):
        DPT.DPObject.append(self, wf)  # append self.setidx and self.dirs
        self.data = self.data + wf.data
        for ar in wf.array_dict:
            self.array_dict[ar] = self.numSets
        self.numSets += 1
        
    def plot(self, i = None, ax = None, getNumEvents = False, getLevels = False,\
             getPlotOpts = False, overlay = False, **kwargs):
        plotOpts = {'PlotType': DPT.objects.ExclusiveOptions(['Channel', 'Array'], 0), \
            'LabelsOff': False, 'TitleOff': False, 'TicksOff': False}

        for (k, v) in plotOpts.items():
                    plotOpts[k] = kwargs.get(k, v)  
                    
        plot_type = plotOpts['PlotType'].selected()  # this variable will store the selected item in 'Type'

        if getPlotOpts:  # this will be called by PanGUI.main to obtain the plotOpts to create a menu once we right-click on the axis
            return plotOpts
        
        if self.current_plot_type is None:
            self.current_plot_type = plot_type

        if getNumEvents:  
            if self.current_plot_type == plot_type:
                if plot_type == 'Channel':
                    return self.numSets, i
                elif plot_type == 'Array':
                    return len(self.array_dict), i
            elif self.current_plot_type == 'Array' and plot_type == 'Channel':
                self.current_plot_type = 'Channel'
                return self.numSets, i
            elif self.current_plot_type == 'Channel' and plot_type == 'Array':
                self.current_plot_type = 'Array'
                return len(self.array_dict), i
                
        if ax is None:
            ax = plt.gca()

        if not overlay:
            ax.clear()
        
        fig = ax.figure  # get the parent figure of the ax
        if plot_type == 'Channel':
            isCorner = True
            self.remove_subplots(fig)
            ax = fig.add_subplot(1,1,1)
            self.plot_data(i, ax, plotOpts, isCorner)
        elif plot_type == 'Array':
            self.remove_subplots(fig)
            advals = np.array([*self.array_dict.values()])
            if i == 0:
                cstart = 0
            else:
                cstart = advals[i-1] + 1
            cend = advals[i]
            currch = cstart
            isCorner = True
            while currch <= cend :
                # get channel name
                currchname = self.dirs[currch]
                # get axis position for channel
                ax = getChannelInArray(currchname, fig)
                self.plot_data(currch, ax, plotOpts, isCorner)
                isCorner = False
                currch += 1
            
        return ax
    
    def plot_data(self, i, ax, plotOpts, isCorner):
        y = self.data[i]
        x = np.arange(y.shape[0])
        ax.plot(x, y)

        if not plotOpts['TitleOff']:
            ax.set_title(self.dirs[i])
                
        if (not plotOpts['LabelsOff']) or isCorner:
            ax.set_xlabel('Time (sample unit)')
            ax.set_ylabel('Voltage (uV)')

        if plotOpts['TicksOff'] or (not isCorner):
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            
    def remove_subplots(self, fig):
        for x in fig.get_axes():  # remove all axes in current figure
            x.remove()  