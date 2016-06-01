-- mysql -u user -p -h research.czxveiixjbkr.us-east-1.rds.amazonaws.com "twitterresearch" < "/Users/mattstringer/research/twitter-research/Geotagging/geotag.sql"
-- mysql -u root -pyourpassword "twitterresearch" < "/Users/mattstringer/research/twitter-research/Geotagging/geotag.sql"

DROP TABLE IF EXISTS geotag_location;

CREATE TABLE IF NOT EXISTS geotag_location (
	gazetikiid varchar(10) COMMENT	'integer id of record in gazetiki database. To differentiate between sources, place names from Wikipedia start at 50000000 and place names extracted from other sources start at 70000000.',
	name varchar(200) COMMENT 'name of geographical point (utf8) varchar(200). For automatically extracted names, name and asciiname are the same and all names are in lower case.',
	asciiname varchar(200) COMMENT 'name of geographical point in plain ascii characters, varchar(200)',
	alternatenames varchar(200) COMMENT 'alternatenames, comma separated varchar(5000). For Geonames elements, it is possible to get the language of alternate names. This option is not available for the other elements.',
	latitude DECIMAL(10,7) COMMENT 'latitude in decimal degrees (wgs84). For geotagged Wikipedia places, latitude is that given in Wikipedia. For other places, latitude was calculated automatically from geotagged information and it is approximate. This information should not be used as such for applications requiring good location precision, such as tourist guides!',
	longitude DECIMAL(10,7) COMMENT 'longitude in decimal degrees (wgs84). For geotagged Wikipedia places, longitude is that given in Wikipedia. For other places, longitude was calculated automatically from geotagged information and it is approximate. This information should not be used as such for applications requiring good location precision, such as tourist guides!',
	feature_class char(1) COMMENT 'see http://www.geonames.org/export/codes.html, char(1). The same codes used in Geonames are provided. This information should not be used as such for applications requiring good categorization precision, such as tourist guides!',
	feature_code varchar(10) COMMENT 'see http://www.geonames.org/export/codes.html, varchar(10). This information should not be used as such for applications requiring good categorization precision, such as tourist guides!',
	country_code varchar(2) COMMENT 'ISO-3166 2-letter country code, 2 characters. For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	cc2 varchar(60) COMMENT 'alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters. Same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	admin1_code varchar(20) COMMENT 'fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	admin2_code varchar(80) COMMENT 'code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	admin3_code varchar(20) COMMENT 'code for third level administrative division, varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	admin4_code varchar(20) COMMENT ' code for fourth level administrative division, varchar(20). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	population BIGINT COMMENT 'bigint (8 byte int). Not available for places extracted from the Web.',
	elevation INT COMMENT 'in meters, integer. Not available for places extracted from the Web.',
	gtopo30 INT COMMENT "average elevation of 30' by 30' (ca 900mx900m) area in meters, integer. Not available for places extracted from the Web.",
	timezone varchar(20) COMMENT 'the timezone id (see file timeZone.txt). For places extracted from the Web, same as Geonames codes of the nearest neighbor of the automatically extracted element.',
	modification_date DATE COMMENT 'date of last modification in yyyy-MM-dd format for all elements.',
	popularity varchar(20) COMMENT 'contains two scores, separated by by semicolon and white space ("; "). The main score is based on the number of different users which have annotated their geotagged photos with the place name. To break ties between elements with the same user score, a finer grained score based on the number of photos tagged with the place names is also provided. The higher this score is, the better the chances are for the element to be correctly extracted.',
	other varchar(200) COMMENT '',
	PRIMARY KEY (gazetikiid))
	DEFAULT CHARSET=UTF8;


LOAD DATA LOCAL INFILE '/Users/mattstringer/Desktop/SchoolWork/SolarResearchPapers/Geotagging/geonames.txt'  
	INTO TABLE geotag_location
	FIELDS TERMINATED BY '\t' 
	LINES TERMINATED BY '\n';

	