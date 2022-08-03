import asyncio
import numpy as np

import pandas as pd
# Copyright (c) 2008-2012, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
def main():
        
    data = pd.read_csv('data.csv')

    # Define empty objects for insering
    cfo     = pd.Series([np.nan]*data.shape[0],dtype=float)


    # Making a list of observations for the for-loop
    ind = data['orgform']=='AS'
    ind = ind & (data['SUM EIENDELER'].fillna(0)>=5e5)
    ind = ind & (data['naeringskoder_level_1']!='L') # Real estate activities
    ind = ind & (data['naeringskoder_level_1']!='K') # Financial and insurance activities

    observations_to_include = list(ind[ind].index.values)

    # CFO
    cfo_input =\
        data['Ordinaert resultat foer skattekostnad'].fillna(0)\
        - data['Gevinst ved avgang anleggsmidler'].fillna(0)
    cfo_input_endring =\
        data['Leverandoergjeld'].fillna(0)\
        + data['Annen kortsiktig gjeld'].fillna(0)
    Betalbar_skatt = data['Betalbar skatt'].fillna(0)

    data_regnaar = data['regnaar']
    data_orgnr = data['orgnr']
    # o_c = Observation Current year
    # o_p = Observation Previous year
    for o_c in observations_to_include:
        prev_regnaar = data_regnaar.loc[o_c]-1
        if prev_regnaar in (data_regnaar[data_orgnr==data_orgnr.loc[o_c]]).tolist():
            temp = data_regnaar[data_orgnr==data_orgnr.loc[o_c]]
            o_p = temp[temp==prev_regnaar].index[0]

            cfo.loc[o_c] = cfo_input[o_c] - Betalbar_skatt[o_p] + cfo_input_endring[o_c] - cfo_input_endring[o_p]

if __name__ == "__main__":
    asyncio.run(main())