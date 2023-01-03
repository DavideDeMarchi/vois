"""Utility functions and classes to manage information on EU countries."""
# Author(s): Davide.De-Marchi@ec.europa.eu
# Copyright © European Union 2022-2023
# 
# Licensed under the EUPL, Version 1.2 or as soon they will be approved by 
# the European Commission subsequent versions of the EUPL (the "Licence");
# 
# You may not use this work except in compliance with the Licence.
# 
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS"
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# 
# See the Licence for the specific language governing permissions and
# limitations under the Licence.
import PIL
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from urllib.request import urlopen
import json


#########################################################################################################################################
# EU countries code taken from:
# https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes
#########################################################################################################################################


# Conversion from iso_a2 country codes to iso_a3 country codes (needed for creating plotly choropleth map)
with urlopen('https://raw.githubusercontent.com/flyingcircusio/pycountry/master/src/pycountry/databases/iso3166-1.json') as response:
    pycountry = json.load(response)

iso2iso3 = {}
iso3iso2 = {}
iso2name = {}
for c in pycountry['3166-1']:
    iso2iso3[c['alpha_2']] = c['alpha_3']
    iso3iso2[c['alpha_3']] = c['alpha_2']
    iso2name[c['alpha_2']] = c['name']

iso2iso3['UK'] = 'GBR'
iso2name['UK'] = 'United Kingdom'

iso2iso3['EU'] = 'EU'
iso2name['EU'] = 'European Union'

iso2iso3['EA'] = 'EA'
iso2name['EA'] = 'Euro Area'

iso2iso3['EU28'] = 'EU28'
iso2name['EU28'] = 'European Union'

iso2iso3['EL'] = 'GRC'
iso2name['EL'] = 'Greece'


# Base URL of the EU flags
baseurlflags = 'https://jeodpp.jrc.ec.europa.eu/services/shared/Notebooks/images/flags/'
    
    
# country class
class country:
    """
    Class to store information on a single EU country.
    
    Parameters
    ----------
        name : str
            Name of the country
        iso2code : str
            Two letter code of the country defined by EUROSTAT (https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes)
        iso3code : str
            Three letter code of the country defined by ISO 3166 (https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
        euro : bool, optional
            Flag that is True for countries belonging to the Euro Area (default is False)
        iscountry : bool, optional
            True if it is a real country (default is True). For instance 'Euro Area' and 'European Union' have this value set to False
        population: int, optional
            Last known population of the country
    """

    def __init__(self, name, iso2code, euro=False, iscountry=True, population=0):
        self.name       = name
        self.iso2code   = iso2code
        self.iso3code   = iso2iso3[iso2code]
        self.euro       = euro
        self.iscountry  = iscountry
        self.population = population
        self.flag       = baseurlflags + iso2code + '.png'
        
        
    def __str__(self):
        """Returns the country name as __str__"""
        return self.name
    
    def __repr__(self):
        """Returns the country name as __repr__"""
        return self.name
    
    def flagImage(self):
        """Returns the flag of the country as a PIL.Image object"""
        response = requests.get(self.flag)
        img = Image.open(BytesIO(response.content))
        return img        
    
    
    
# eucountries class            
class countries:
    """
    Class to store information on all the EU countries.
    
    Parameters
    ----------
        countries_list : list of eucountries.country instances
            List of countries in the European Union
            
    Examples
    --------
    Get the list of all European Union or Euro Area countries::
    
        from vois import eucountries as eu

        countriesEU = eu.countries.EuropeanUnion()
        print(countriesEU)
        
        countriesEuro = eu.countries.EuroArea()
        print(countriesEuro)
        
    
    Display the flag image of a country given its code::
    
        from vois import eucountries as eu
        display( eu.countries.byCode('IT').flagImage() )
        
        
    Display the flag image of a country given its name::
    
        from vois import eucountries as eu
        display( eu.countries.byName('Lithuania').flagImage() )
        
    .. figure:: figures/flag.png
       :scale: 100 %
       :alt: Flag of a country

       Display of the flag of an EU country
    
    Get the list of all the European Union country codes::
    
        from vois import eucountries as eu
        display( eu.countries.EuroAreaCodes() )
        
    """
    
    countries_list = []
    
    @classmethod
    def add(cls, name, iso2code, euro=False, iscountry=True, population=0):
        """
        Static method to add a country to the countries_list
    
        Parameters
        ----------
        name : str
            Name of the country
        iso2code : str
            Two letter code of the country defined by EUROSTAT (https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes)
        euro : bool, optional
            Flag that is True for countries belonging to the Euro Area (default is False)
        iscountry : bool, optional
            True if it is a real country (default is True). For instance 'Euro Area' and 'European Union' have this value set to False
        population: int, optional
            Last known population of the country
        """
        cls.countries_list.append( country(name, iso2code, euro=euro, iscountry=iscountry, population=population))
    
    
    
    # Returns the list of all the country belonging to the Euro Area
    @classmethod
    def EuroArea(cls, sortByName=True):
        """
        Static method that returns the list of all the country belonging to the Euro Area
        
        Parameters
        ----------
            sortByName : bool, optional
                If True, the returned list of countries is sorted by the name of the country (default is True)
        """
        res = []
        for c in cls.countries_list:
            if c.iscountry and c.euro:
                res.append(c)
        if sortByName:
            return sorted(res, key=lambda x: x.name, reverse=False)
        else:
            return sorted(res, key=lambda x: x.iso2code, reverse=False)

        
    # Returns the list of all the iso2codes of the countries belonging to the Euro Area
    @classmethod
    def EuroAreaCodes(cls):
        """
        Static method that returns the list of all the iso2codes of the countries belonging to the Euro Area
        """
        countries = cls.EuroArea()
        return [c.iso2code for c in countries]


    
    # Returns the list of all the country belonging to the European Union
    @classmethod
    def EuropeanUnion(cls, sortByName=True):
        """
        Static method that returns the list of all the country belonging to the European Union
        
        Parameters
        ----------
            sortByName : bool, optional
                If True, the returned list of countries is sorted by the name of the country (default is True)
        """
        res = []
        for c in cls.countries_list:
            if c.iscountry:
                res.append(c)
        if sortByName:
            return sorted(res, key=lambda x: x.name, reverse=False)
        else:
            return sorted(res, key=lambda x: x.iso2code, reverse=False)

        
    # Returns the list of all the iso2codes of the countries belonging to the European Union
    @classmethod
    def EuropeanUnionCodes(cls):
        """
        Static method that returns the list of all the iso2codes of the countries belonging to the European Union
        """
        countries = cls.EuropeanUnion()
        return [c.iso2code for c in countries]
        

    # Returns the list of all the names of the countries belonging to the European Union
    @classmethod
    def EuropeanUnionNames(cls):
        """
        Static method that returns the list of all the names of the countries belonging to the European Union
        """
        countries = cls.EuropeanUnion()
        return [c.name for c in countries]
    
    
    @classmethod
    def byCode(cls, iso2code):
        """
        Static method that returns a country given its iso2code, or None if not existing
        
        Parameters
        ----------
            iso2code : str
                Two letter code of the country defined by EUROSTAT (https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes)
                
        Returns
        -------
            Instance of country or None
            
        """
        res = [c for c in cls.countries_list if c.iso2code == iso2code]
        if len(res) > 0: return res[0]
                
    @classmethod
    def byName(cls, name):
        """
        Static method that returns a country given its name, or None if not existing
        
        Parameters
        ----------
            name : str
                Name of the country
                
        Returns
        -------
            Instance of country or None
            
        """
        res = [c for c in cls.countries_list if c.name == name]
        if len(res) > 0: return res[0]
            

            
# Population data for 2018 obtained from https://data.worldbank.org/indicator/SP.POP.TOTL CSV file
eu_total_population = 446786293

countries.add('Belgium',     'BE',euro=True,population=11433256)
countries.add('Greece',      'EL',euro=True,population=10731726)
countries.add('Lithuania',   'LT',euro=True,population=2801543)
countries.add('Portugal',    'PT',euro=True,population=10283822)
countries.add('Bulgaria',    'BG',population=7025037)
countries.add('Spain',       'ES',euro=True,population=46796540)
countries.add('Luxembourg',  'LU',euro=True,population=607950)
countries.add('Romania',     'RO',population=19466145)
countries.add('Czechia',     'CZ',population=10629928)
countries.add('France',      'FR',euro=True,population=66977107)
countries.add('Hungary',     'HU',population=9775564)
countries.add('Slovenia',    'SI',euro=True,population=2073894)
countries.add('Denmark',     'DK',population=5793636)
countries.add('Croatia',     'HR',euro=True,population=4087843)
countries.add('Malta',       'MT',euro=True,population=484630)
countries.add('Slovakia',    'SK',euro=True,population=5446771)
countries.add('Germany',     'DE',euro=True,population=82905782)
countries.add('Italy',       'IT',euro=True,population=60421760)
countries.add('Netherlands', 'NL',euro=True,population=17231624)
countries.add('Finland',     'FI',euro=True,population=5515525)
countries.add('Estonia',     'EE',euro=True,population=1321977)
countries.add('Cyprus',      'CY',euro=True,population=1189265)
countries.add('Austria',     'AT',euro=True,population=8840521)
countries.add('Sweden',      'SE',population=10175214)
countries.add('Ireland',     'IE',euro=True,population=4867309)
countries.add('Latvia',      'LV',euro=True,population=1927174)
countries.add('Poland',      'PL',population=37974750)

#countries.add('United Kingdom', 'UK')

countries.add('European Union','EU', iscountry=False, population=eu_total_population)
countries.add('Euro Area',     'EA', iscountry=False, population=341858176+4087843)


# language class
class language:
    """
    Class to store information on a language of the European Union.
    
    Parameters
    ----------
        name : str
            Name of the language
        abbreviation: str
            Abbreviation used for the language
        population : int, optional
            Last known population that uses the language
                
    """

    def __init__(self, name, abbreviation, population=0):
        self.name         = name
        self.abbreviation = abbreviation
        self.population   = population
        
    def __str__(self):
        """Returns the language name as __str__"""
        return self.name
    
    def __repr__(self):
        """Returns the language name as __repr__"""
        return self.name

    
# language class            
class languages:
    """
    Class to store information on all the European Union languages.
    
    Parameters
    ----------
        languages_list : list of eucountries.language instances
            List of languages in the European Union
            
    Examples
    --------
    Print the list of all European Union languages::
    
        from vois import eucountries as eu
        names = eu.languages.EuropeanUnionLanguages(sortByName=False)
        print(names)
        
    Print the list of all European Union languages abbreviations::
    
        from vois import eucountries as eu
        abbrev = eu.languages.EuropeanUnionAbbreviations()
        print(abbrev)
        
    """
    
    languages_list = []
    
    @classmethod
    def add(cls, name, abbreviation, population=0):
        cls.languages_list.append( language(name, abbreviation, population) )
    

    
    # Returns the list of all the official languages to the European Union
    @classmethod
    def EuropeanUnionLanguages(cls, sortByName=True):
        """
        Static method that returns the list of all the languages of the European Union
        
        Parameters
        ----------
            sortByName : bool, optional
                If True, the returned list of languages is sorted by the name of the language (default is True)
        """
        if sortByName:
            return sorted(cls.languages_list, key=lambda x: x.name, reverse=False)
        else:
            return sorted(cls.languages_list, key=lambda x: x.abbreviation, reverse=False)

        
    # Returns the list of all the abbreviations of the official languages to the European Union
    @classmethod
    def EuropeanUnionAbbreviations(cls):
        """
        Static method that returns the list of all the abbreviations of the EU languages
        """
        return sorted([lang.abbreviation for lang in cls.languages_list])
        
        
    @classmethod
    def byAbbreviation(cls, abbreviation):
        """
        Static method that returns a language given its abbreviation, or None if not existing
        
        Parameters
        ----------
            abbreviation : str
                Two letter code of the language
                
        Returns
        -------
            Instance of language class or None
            
        """
        res = [c for c in cls.languages_list if c.abbreviation == abbreviation]
        if len(res) > 0: return res[0]
                
    @classmethod
    def byName(cls, name):
        """
        Static method that returns a language given its name, or None if not existing
        
        Parameters
        ----------
            name : str
                Name of the language
                
        Returns
        -------
            Instance of language class or None
            
        """
        res = [c for c in cls.languages_list if c.name == name]
        if len(res) > 0: return res[0]


# Languages population from https://en.wikipedia.org/wiki/Languages_of_the_European_Union
languages.add('Bulgarian',    'bg', int(0.02*eu_total_population) )
languages.add('Czech',        'cs', int(0.03*eu_total_population) )
languages.add('German',       'de', int(0.36*eu_total_population) )
languages.add('Greek',        'el', int(0.03*eu_total_population) )
languages.add('English',      'en', int(0.44*eu_total_population) )
languages.add('Spanish',      'es', int(0.17*eu_total_population) )
languages.add('French',       'fr', int(0.29*eu_total_population) )
languages.add('Croatian',     'hr', int(0.01*eu_total_population) )
languages.add('Hungarian',    'hu', int(0.03*eu_total_population) )
languages.add('Italian',      'it', int(0.18*eu_total_population) )
languages.add('Lithuanian',   'lt', int(0.01*eu_total_population) )
languages.add('Dutch',        'nl', int(0.06*eu_total_population) )
languages.add('Polish',       'pl', int(0.10*eu_total_population) )
languages.add('Portuguese',   'pt', int(0.03*eu_total_population) )
languages.add('Romanian',     'ro', int(0.06*eu_total_population) )
languages.add('Slovene',      'sl', int(0.005*eu_total_population) )
languages.add('Swedish',      'sv', int(0.03*eu_total_population) )

# Languages NOT found: check abbreviation!
languages.add('Danish',       'dk', int(0.01*eu_total_population) )
languages.add('Estonian',     'ee', int(0.005*eu_total_population) )
languages.add('Finnish',      'fi', int(0.01*eu_total_population) )
languages.add('Irish',        'ie', int(0.005*eu_total_population) )
languages.add('Latvian',      'lv', int(0.005*eu_total_population) )
languages.add('Maltese',      'mt', int(0.005*eu_total_population) )
languages.add('Slovak',       'sk', int(0.02*eu_total_population) )
        