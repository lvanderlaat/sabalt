import numpy as np


def audacity(df, out):
    df[['onset', 'onset', 'pitch']].to_csv(out, index=False, sep='\t')
    return


def lilypond(df, out):
    f = open(out, 'w')
    f.write('\\language "english"\n\n{\n\t\\clef "bass"\n\t')
    for i, row in df.iterrows():
        f.write(row.notation+' ')
    f.write('\n}')
    return
