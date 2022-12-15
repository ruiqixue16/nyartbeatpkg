from nyartbeatpkg import nyartbeatpkg
import pytest
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
import datetime

def test_transform():
    x = ["http://www.nyartbeat.com/list/event_type_print_graphicdesign.en.xml"]
    actual = isinstance(nyartbeatpkg.transform(x), pd.DataFrame)
    expected = True
    assert actual == expected

def test_transform_clean_a():
    x = ["http://www.nyartbeat.com/list/event_type_print_graphicdesign.en.xml"]
    actual = isinstance(nyartbeatpkg.transform_clean(x), pd.DataFrame)
    expected = True
    assert actual == expected
    
def test_transform_clean_b():
    x = ["http://www.nyartbeat.com/list/event_type_print_graphicdesign.en.xml"]
    actual = nyartbeatpkg.transform_clean(x)["Date End"].dtypes
    expected = 'datetime64[ns]'
    assert actual == expected

d= []
Name = "Test Event 1"
Type = "Cultural Center"
Media = "2D: Painting 2D: Drawing"
Description = "Ruido / Noise, the first international survey of Colombian American artist Karen Lamassonne, will be shown in SI’s ground floor and second floor galleries. Gina Fischli’s first institutional exhibition in the United States, I love being creative, will be presented in the lower level. Karen Lamassonne (b. 1954, New York) lives and works in Atlanta, GA. She has had solo exhibitions at the Museo de Arte Moderno la Tertulia, Cali (1989 and 2017); Museo Rayo, Roldanillo (2019); and Facultad de Artes ASAB, Bogotá (2019). Recent group shows include Radical Women: Latin American Art, 1960-85 at the Hammer Museum, Los Angeles, the Brooklyn Museum, New York and Pinacoteca, São Paulo; The Art of Disobedience at the Museo de Arte Moderno, Bogotá (2018); and Voces íntimas, Museo Nacional, Bogotá (2017).Gina Fischli (b. 1989, Zürich, CH) lives and works in Zürich. She has had solo exhibitions at Neuer Essener Kunstverein, Essen (2020); DELF, Vienna (2017); Forde, Geneva (2016), amongst others. Recent group exhibitions include the Miniatur Biennale Düsseldorf, Düsseldorf (2022); Nothing to Write Home About, Kim?, Contemporary Art Centre, Riga (2022); Winterfest, Aspen Art Museum, Aspen (2020); SculptureGarden Geneva Biennale, Geneva (2020); A home is not a house, Fri Art, Fribourg (2020); The Garden, Royal Academy, London (2019); and SI ONSITE, Swiss Institute, New York (2019). In 2021, Fischli presented Ravenous and Predatory for the Cork Street Banner Commission, London."
Image = None
Karma = "0.0"
Price = "Free"
Datestart = "2022-09-14 00:00:00"
Dateend = "2023-01-08 00:00:00"
Datum = "wgs84"
Longitude = "-73.987548"
Latitude = "40.728416"
Address = "38 St. Mark's Pl  New York, NY 10003"
Area = "Villages"
Phone = "212-925-2035"
d = pd.DataFrame({"Name":Name,
                         "Type":Type,
                         "Media":Media,
                         "Description":Description,
                         "Image":Image, 
                         "Karma":Karma,
                         "Price":Price,
                         "Date Start":Datestart,
                         "Date End":Dateend, 
                         "Datum":Datum,
                         "Longitude":Longitude, 
                         "Latitude":Latitude,
                         "Address":Address,
                         "Area":Area,
                         "Phone":Phone}, index=[0])
d2= []
Name = "Test Event 2”"
Type = "Museum"
Media = "2D: Painting 2D: Drawing"
Description = "Ruido / Noise, the first international survey of Colombian American artist Karen Lamassonne, will be shown in SI’s ground floor and second floor galleries. Gina Fischli’s first institutional exhibition in the United States, I love being creative, will be presented in the lower level. Karen Lamassonne (b. 1954, New York) lives and works in Atlanta, GA. She has had solo exhibitions at the Museo de Arte Moderno la Tertulia, Cali (1989 and 2017); Museo Rayo, Roldanillo (2019); and Facultad de Artes ASAB, Bogotá (2019). Recent group shows include Radical Women: Latin American Art, 1960-85 at the Hammer Museum, Los Angeles, the Brooklyn Museum, New York and Pinacoteca, São Paulo; The Art of Disobedience at the Museo de Arte Moderno, Bogotá (2018); and Voces íntimas, Museo Nacional, Bogotá (2017).Gina Fischli (b. 1989, Zürich, CH) lives and works in Zürich. She has had solo exhibitions at Neuer Essener Kunstverein, Essen (2020); DELF, Vienna (2017); Forde, Geneva (2016), amongst others. Recent group exhibitions include the Miniatur Biennale Düsseldorf, Düsseldorf (2022); Nothing to Write Home About, Kim?, Contemporary Art Centre, Riga (2022); Winterfest, Aspen Art Museum, Aspen (2020); SculptureGarden Geneva Biennale, Geneva (2020); A home is not a house, Fri Art, Fribourg (2020); The Garden, Royal Academy, London (2019); and SI ONSITE, Swiss Institute, New York (2019). In 2021, Fischli presented Ravenous and Predatory for the Cork Street Banner Commission, London."
Image = None
Karma = "0.0"
Price = "Free"
Datestart = "2022-09-14 00:00:00"
Dateend = "2011-01-08 00:00:00"
Datum = "wgs84"
Longitude = "-73.987548"
Latitude = "40.728416"
Address = "38 St. Mark's Pl  New York, NY 10003"
Area = "Villages"
Phone = "212-925-2035"
d2 = pd.DataFrame({"Name":Name,
                         "Type":Type,
                         "Media":Media,
                         "Description":Description,
                         "Image":Image, 
                         "Karma":Karma,
                         "Price":Price,
                         "Date Start":Datestart,
                         "Date End":Dateend, 
                         "Datum":Datum,
                         "Longitude":Longitude, 
                         "Latitude":Latitude,
                         "Address":Address,
                         "Area":Area,
                         "Phone":Phone}, index=[0])
d = pd.concat([d,d2],ignore_index = True)
d["Date End"] = pd.to_datetime(d["Date End"],errors='coerce')

def test_get_event_info_a():
    actual = nyartbeatpkg.get_event_info(d,Type = "cul")
    expected = "Cultural Center"
    assert actual.iloc[0,1] == expected

def test_get_event_info_b():
    actual = nyartbeatpkg.get_event_info(d,Type = "mu")
    expected = "Museum"
    assert actual.iloc[0,1] == expected

def test_get_current_event_info():
    actual = nyartbeatpkg.get_current_event_info(d)
    expected = "Test Event 1"
    assert actual.iloc[0,0] == expected
