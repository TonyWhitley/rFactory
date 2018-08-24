"""
Accessing the data for rFactory.

This reads rFactory's data files - one for each car, one for each track.
File naming matches the name used by rFactor.  Data in the files is derived
from rFactor but then enhanced - e.g. S397 cars and tracks do not specify that
S397 is the author.  Additional data such as 
cars:
* type (open-wheeler, sports, GT, Indy, endurance, etc)
* class (F1, GT3, GTE, etc)
* type of gearshift (H, dogleg, paddles, sequential, auto, preselector!) 
* what driving aids the car has (TC, ABS, etc)  [a list?]
* year and decade of manufacture
* star rating

tracks:
* year and decade
* continent
* country
* type (permanent, temporary, road, speedway, fictional, historic, etc)
* star rating

It also handles writing the files if they've been edited.
"""

cars = {
  'dummyData' : [
          ['Ferrari',  '458', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Corvette', 'C7', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Bentley',  'Continental', 'GT3', 'S397', 'GT', 'RWD', '2016', '2010-', '*****', 'car DB file'],
          ['Eve',      'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_EVE_1968'],
          ['Spark',    'F1', 'F1', 'ISI', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'Historic Challenge_spark_1968'],
          ['Porsche',  '917K', 'Gp.C', 'Apex', 'GT', 'RWD', '1967', '1960-', '*****', 'FLAT12_917k_1971'],
          ['Lola',     'T70', 'Gp.C', 'Crossply', 'GT', 'RWD', '1974', '1970-', '***', 'car DB file'],
          ['Sauber',   'C11', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Sauber_C11'],
          ['Porsche',  '962C', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Porsche_062C'],
          ['Mazda',    '787B', 'Gp.C', 'MAK-Corp', 'GT', 'RWD', '1978', '1970-', '*****', 'MAK_Mazda_787B'],
          ['Ferrari',  '312', 'F1', 'Chief Wiggum/Postipate', 'Open-wheel', 'RWD', '1967', '1960-', '*****', 'car DB file'],
          ['Caterham', '7', 'C7', 'MikeeCZ', 'Sports', 'RWD', '2016', '2010-', '****', 'car DB file']
        ]
  }