import pandas as pd
from vois import svgMap


#######################################################################################################################
# Mapping of codes to names and viceversa (use svgMap codes)
#######################################################################################################################
code2name = svgMap.country_name
code2name['EU27_2020'] = 'Europe27'
name2code = {v: k for k, v in code2name.items()}
eucodes = svgMap.country_codes
eunames = sorted([svgMap.country_name[x] for x in eucodes])


#######################################################################################################################
# Loads input data and returns a pandas dataframe
#######################################################################################################################
def loadData():
    # Load energy data (downloaded from https://ec.europa.eu/eurostat/databrowser/view/ten00124/default/map?lang=en)
    df = pd.read_csv('./ten00124_linear.csv')

    # Remove columns that are not useful
    df.drop(['OBS_FLAG'], axis=1, inplace=True)

    # Assign Country to df
    df['Country'] = df['geo'].map(code2name)    
    
    # Load population data (downloaded from https://ec.europa.eu/eurostat/databrowser/view/tps00001/default/table?lang=en)
    dfpop = pd.read_csv('./tps00001_tabular.tsv', delimiter='\t')

    # Dict key=Code2char  value=Population
    countrypop = {}

    dfpop.rename(columns={'freq,indic_de,geo\TIME_PERIOD': 'geo'}, inplace=True)
    columns = dfpop.columns
    for index, row in dfpop.iterrows():
        geo = row['geo'].split(',')[2]
        for col in reversed(columns):
            if len(row[col]) > 2:
                pop = int(row[col].split(' ')[0])
                if pop > 0:
                    countrypop[geo] = pop
                    break

    # Assign population to df
    df['Population2021'] = df['geo'].map(countrypop)
    
    return df