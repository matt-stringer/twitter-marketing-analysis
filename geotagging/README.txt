README for Gazetiki: 

=======================================================================
LICENSING
This work is licensed under a Creative Commons Attribution 3.0 License,
see http://creativecommons.org/licenses/by/3.0/
The Data is provided "as is" without warranty or any representation of accuracy, timeliness or completeness.

The data format is tab-delimited text in utf8 encoding.
=======================================================================


Gazetiki is a geographical database which was constituted at CEA LIST (http://www-list.cea.fr/gb/index_gb.htm) by using information fro 
Geonames (geonames.org) and from different Web sources. This work was supported via the French ANR Georama project (ANR-08-CORD-009). 
Gazetiki_v1 contains 8323702 geographical names, with 7584617 coming from Geonames and another 1043807 extracted from Wikipedia, DBPedia
and Flickr. For Geonames elements, the main modification is the addition
of a popularity score which was calculated based on the usage of a place name in a geotagged dataset. For the other elements of the dataset,
the name(s) of the place, its geographical category, its coordinates and its popularity and were extracted using Web data. Data about 
encompassing entities and timezone were added using those of the Geonames nearest neighbor. The automatically discovered place names have the 
same format as Geonames elements. Given that the accuracy of the extraction is different for the different data sources used (Geonames elements 
are more accurate than DBPedia geotagged elements, which are more accurate than other Wikipedia elements and Flickr elements), information 
about the data source it was extracted from is provided for each element of the dataset. When merging the data sources, we tried to remove as many
multiple elements as possible and priority was given to Geonames elements, followed by DBPedia elements and by other data sources. 

=======================================================================
The gazetiki dump file has the following fields (the first 19 fields are similar to those found in Geonames):
1. gazetikiid         : integer id of record in gazetiki database. To differentiate between sources, place names from Wikipedia start at 50000000 and place names extracted from other sources start at 70000000.
2. name              : name of geographical point (utf8) varchar(200). For automatically extracted names, name and asciiname are the same and all names are in lower case.
3. asciiname         : name of geographical point in plain ascii characters, varchar(200)
4. alternatenames    : alternatenames, comma separated varchar(5000). For Geonames elements, it is possible to get the language of alternate names. This option is not available for the other elements.
5. latitude          : latitude in decimal degrees (wgs84). For geotagged Wikipedia places, latitude is that given in Wikipedia. For other places, latitude was calculated automatically from geotagged information and it is approximate. This information should not be used as such for applications requiring good location precision, such as tourist guides!
6. longitude         : longitude in decimal degrees (wgs84). For geotagged Wikipedia places, longitude is that given in Wikipedia. For other places, longitude was calculated automatically from geotagged information and it is approximate. This information should not be used as such for applications requiring good location precision, such as tourist guides!
7. feature class     : see http://www.geonames.org/export/codes.html, char(1). The same codes used in Geonames are provided. This information should not be used as such for applications requiring good categorization precision, such as tourist guides!  
8. feature code      : see http://www.geonames.org/export/codes.html, varchar(10). This information should not be used as such for applications requiring good categorization precision, such as tourist guides!
9. country code      : ISO-3166 2-letter country code, 2 characters. For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
10. cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters. Same as Geonames codes of the nearest neighbor of the automatically extracted element.
11. admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
12. admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
13. admin3 code       : code for third level administrative division, varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
14. admin4 code       : code for fourth level administrative division, varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
15. population        : bigint (8 byte int). Not available for places extracted from the Web.
16. elevation         : in meters, integer. Not available for places extracted from the Web.
17. gtopo30           : average elevation of 30'x30' (ca 900mx900m) area in meters, integer. Not available for places extracted from the Web.
18. timezone          : the timezone id (see file timeZone.txt). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.
19. modification date : date of last modification in yyyy-MM-dd format for all elements.
20. popularity        :	contains two scores, separated by by semicolon and white space ("; "). The main score is based on the number of different users which have annotated their geotagged photos with the place name. To break ties between elements with the same user score, a finer grained score based on the number of photos tagged with the place names is also provided. The higher this score is, the better the chances are for the element to be correctly extracted.
21. other             : For Geonames place names, this field contains only "G" to indicate the data source. For DBPedia place names, the field contains only "D" to indicate the data source. For the other elements, there are three sub-fields separated by semicolon and white space ("; "). The first subfield indicates which is the data source (other than Geonames and DBPedia). "W"  means that the place name exists in Wikipedia (i.e. is the title of a Wikipedia article which is considered related to the geographic domain but is not necessarily geotagged). "S" means that the element's name is extracted directly from photo annotations. The second sub-field gives the proportion of lower-case usages of the place name in a Web search engine. The smaller this proportion is, the better the chances are for the name to be a proper one. The third sub-field corresponds to the number of exact occurrences of the place name in search engine results. The higher this number, the better the chances are for the place name to be correct.


SINCE THE EXTRACTION PROCESS IS AUTOMATIC, ALL DATA ARE PROVIDED WITH NO WARRANTY WHATSOEVER CONCERNING THEIR ACCURACY! 
Users can use popularity, lower-case occurrences and exact occurrences on the Web (see fields 20 and 21) in order to get elements an improved overall precision of the dataset. 

All Geonames files referenced above can be found at: http://download.geonames.org/export/dump/


=======================================================================
DATA SOURCES
* GEONAMES - geonames.org -online geographical database which integrates a large number of primary sources such as NGA, GNIS, geobase.ca etc. For a complete list of Geonames sources, please visit http://www.geonames.org/data-sources.html
* DBPedia - http://dbpedia.org/ - a list of Wikipedia georeferenced articles available on the DBPedia site was processed
* Wikipedia - http://www.wikipedia.org
* Flickr - georeferenced textual metadata was collected using the Flickr API and then processed in order to extract information about places in Gazetiki

=======================================================================
FEEDBACK
This is an initial version of the gazetteer. If you find errors or have any comments concerning its current content and features that are missing, feedback is welcome at
adrian.popescu (_at_) cea.fr

=======================================================================
REFERENCES
Early descriptions of the way POIs are automatically extracted (which are pretty similar to what was done for the current database) can be found in: 
Adrian Popescu, Gregory Grefenstette, Pierre-Alain MoÃ«llic. Gazetiki: Automatic Creation of a Geographical Gazetteer, JCDL 2008 , June 16 - 20, Pittsburgh, USA.  
Adrian Popescu, Gregory Grefenstette, Houda Bouamor. Mining a Multilingual Geographical Gazetteer from the Web, WI 2009, September 15 - 18, Milan, Italy.