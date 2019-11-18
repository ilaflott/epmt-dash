import pandas as pd


def make_refs(x,name=''):
    refs = []
    from layouts import df
    joblist = df['job id'].sample(n = 10).tolist()
    featureli = ['duration','cpu_time','num_procs']
    print(joblist)
    for n in range(x):
        from random import randint,getrandbits
        jobs = [ joblist[i] for i in range(randint(5,8))]
        features = [featureli[i] for i in range(randint(1,3))]
        ref_active = bool(getrandbits(1)  < 0.95)
        refs.append(['ref'+str(n)+name, {"taga":"tagb"}, jobs,
                     features, ref_active])
    return refs


class ref_gen:
    def __init__(self):
        import numpy as np
        references = make_refs(5)
        self.df = pd.DataFrame(references, columns=['Model','Tags','Jobs','Features','Active'])
        self.df['Active'] = np.where(self.df['Active'], 'Yes', 'No')
        # Reorder
        self.df = self.df[['Model','Active','Tags','Jobs','Features']]
