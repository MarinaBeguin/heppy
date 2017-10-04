'''Select stable generated charged hadrons from b-quark decay'''


from heppy.framework.analyzer import Analyzer
from heppy.particles.genbrowser import GenBrowser

class ChargedHadronsFromW(Analyzer):
    # '''Select stable generated charged hadrons from W boson decay'''

    def process(self, event):
        '''event should contain:

        * gen_particles: list of all stable gen particles
        '''
        ptc_stable = getattr(event, self.cfg_ana.input_particle)

        output_W_minus = None
        output_W_plus = None

        charged_hadrons = []
        for ptc in ptc_stable:
            if ptc.q():
                charged_hadrons.append(ptc)

        event.genbrowser = GenBrowser(event.gen_particles,
                                      event.gen_vertices)

        event.hadrons_from_W_minus = []
        event.hadrons_from_W_plus = []
        for hadron in charged_hadrons:
            is_from_W_minus = is_ptc_from_W_minus(event, hadron, event.genbrowser)
            if is_from_W_minus:
                event.hadrons_from_W_minus.append(hadron)
            else:
                event.hadrons_from_W_plus.append(hadron)

        setattr(event, self.cfg_ana.output_W_minus, event.hadrons_from_W_minus)
        setattr(event, self.cfg_ana.output_W_plus, event.hadrons_from_W_plus)


def is_ptc_from_W_minus(event, hadron, browser):

    ancestors = browser.ancestors(hadron)
    is_from_W_minus = False

    for ancestor in ancestors:
        if ancestor.pdgid() == -24:
            is_from_W_minus = True

    return is_from_W_minus
