from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *

from ROOT import TFile

class TreeProducer(Analyzer):

    def beginLoop(self, setup):

        super(TreeProducer, self).beginLoop(setup)

        self.rootfile = TFile('/'.join([self.dirName, self.cfg_ana.file_name]), 'recreate')
        self.tree = Tree( 'events', '')

        self.taggers = ''
        bookJet(self.tree, 'jet1', self.taggers)
        bookJet(self.tree, 'jet2', self.taggers)
        bookJet(self.tree, 'jet3', self.taggers)
        bookJet(self.tree, 'jet4', self.taggers)
        bookParticle(self.tree, 'W1')
        bookParticle(self.tree, 'W2')


    def process(self, event):
        self.tree.reset()

        Ws = getattr(event, self.cfg_ana.Ws)
        for iW, w in enumerate(Ws):
            if iW == 2:
                break

            if w.pdgid() == 24:
                fillParticle(self.tree, 'W1', w)
            else:
                fillParticle(self.tree, 'W2', w)


        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == 4:
                break
            fillJet(self.tree, 'jet{ijet}'.format(ijet = ijet+1), jet, self.taggers)

        self.tree.tree.Fill()


    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
