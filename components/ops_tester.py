from epmt_query import get_procs, get_ops
def my_ops():
    print(get_ops(['625172'], tags=['op'], fmt='orm')[:1])


def my_procs():
    print(get_procs()[:1])