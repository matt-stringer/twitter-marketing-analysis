-- Use this as a resource http://www.geonames.org/export/codes.html

-- Show all feature codes in CA
SELECT name, asciiname, alternatenames, latitude, longitude, feature_code 
	FROM geotag_location WHERE admin1_code="CA" AND feature_class="A";

-- Show states
SELECT name, asciiname, alternatenames
	FROM geotag_location WHERE country_code="US" AND feature_code="ADM1";


-- Show CA counties (does include county in all descriptions)
SELECT name, asciiname, alternatenames
	FROM geotag_location WHERE country_code="US" AND feature_code="ADM2" AND admin1_code="CA";

-- Show in CA cities and places
SELECT name, asciiname, alternatenames
	FROM geotag_location WHERE country_code="US" AND feature_code="PPL" AND admin1_code="CA";


SELECT name, asciiname, latitude, longitude
	FROM geotag_location WHERE country_code="SV";

Search
SELECT name, asciiname, alternatenames, latitude, longitude FROM geotag_location 
	WHERE country_code="US" 
	AND feature_code="PPL" 
	AND admin1_code="CA" 
	AND (name LIKE '%Fremont%' 
	OR name LIKE '%Hirsch Elementary%');

## Creating new tables
CREATE TABLE ca_locations LIKE geotag_location;

INSERT INTO ca_locations (SELECT * 
	FROM geotag_location
	WHERE country_code="US"
	AND admin1_code="CA");  