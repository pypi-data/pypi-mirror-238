fn = '/home/cliffk/idm/vietnam_vaccine_impact/vaccine_impact/vietnam-scenarios.msim'

import sciris as sc

remapping = {
    '__main__.num_doses':None,
    '__main__.num_doses2':None,
}
msim = sc.load(fn, remapping=remapping, verbose=True)