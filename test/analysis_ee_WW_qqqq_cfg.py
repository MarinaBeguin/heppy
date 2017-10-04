'''Example configuration file for an ee->WW analysis in the 4 jet channel, wihout detector

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_WW_qqqq_cfg import * 

'''

import os
import logging

import heppy.framework.config as cfg


# next 2 lines necessary to deal with reimports from ipython
# logging.shutdown()
# reload(logging)
logging.basicConfig(filename = "./Output/info_WW_qqqq.log", level=logging.INFO)


# definition of the collider
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240

# input definition
comp = cfg.Component(
    'ee_WW_qqqq_240_10K_M80_genkt',
    files = ['../../fcc-physics/ee_WW_qqqq_240_10K_M80.root']
    )
selectedComponents = [comp]

# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

# # the papas simulation and reconstruction sequence
from heppy.test.papas_cfg import gen_particles_stable
# from heppy.test.papas_cfg import papas_sequence, detector
# from heppy.test.papas_cfg import papasdisplay as display


# Get info of W bosons
from heppy.analyzers.Selector import Selector
Ws = cfg.Analyzer(
    Selector,
    output = 'Ws',
    input_objects = 'gen_particles',
    filter_func = lambda x : x.status() == 22 and abs(x.pdgid()) == 24
)

#Get the ancestor of each particle
from heppy.analyzers.examples.WW_qqqq.ChargedHadronsFromW import ChargedHadronsFromW
history_from_W = cfg.Analyzer(
    ChargedHadronsFromW,
    output_W_minus = 'from_W_minus',
    output_W_plus = 'from_W_plus',
    input_particle = 'gen_particles_stable'
)


# make 4 exclusive jets with stable gen particles collection
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'gen_particles_stable',
    algorithm = 'ee_kt',
    fastjet_args = dict( njets = 4)
)


# Analysis-specific ntuple producer
# please have a look at the ZHTreeProducer class
from heppy.analyzers.examples.WW_qqqq.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    file_name = 'ee_WW_qqqq_240_10K_M80_genkt.root',
    jets = 'jets',
    Ws = 'Ws'
)


# definition of the sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_particles_stable,
    Ws,
    history_from_W,
    hard_particles,
    jets,
    tree
)

# Specifics to read FCC events 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)
