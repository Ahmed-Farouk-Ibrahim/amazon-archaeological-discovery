# Data Sources Documentation

This document provides comprehensive information about all data sources required for the Amazon Archaeological Discovery System.

## Required Datasets Overview

The system requires five primary datasets, all publicly available from official sources:

1. **Amazon Geoglyphs KML** - Known archaeological sites for model training
2. **FABDEM DTM Tiles** - Forest-corrected digital elevation model
3. **NASA HLS Sentinel-2** - Harmonized Landsat Sentinel-2 imagery
4. **Copernicus Sentinel-2** - High-resolution validation imagery
5. **Environmental Context Data** - PRODES deforestation and hydrography

## Detailed Data Source Information

### 1. Amazon Geoglyphs KML Database

**Source:** Academic research databases and archaeological surveys 
**Link** [https://jqjacobs.net/amazon/amazon_geoglyphs.kml]  
**Format:** KML (Keyhole Markup Language)  
**Coverage:** Amazon basin, Northern South America  
**Content:** 1,370+ documented geoglyphs and 83 mound villages

**Download Instructions:**
- Access through academic archaeological databases
- Contact researchers for latest compiled datasets
- Ensure citation, proper attribution and research ethics compliance

**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/amazon-geoglyphs-kml --force 


**File Structure:**
amazon-geoglyphs-kml/
└── amazon_geoglyphs.kml


### 2. FABDEM Digital Terrain Model

**Source:** University of Bristol  
**Website:** https://data.bris.ac.uk/data/dataset/s5hqmjcdj8yo2ibzi9b4ew3sn  
**Format:** GeoTIFF (.tif)  
**Resolution:** 30m spatial resolution  
**Coverage:** Global, forest-corrected elevation data  

**Download Instructions:**
1. Visit the University of Bristol data repository
2. Register for academic access
3. Download tiles covering Amazon basin coordinates
4. Focus on tiles: S09-S17, W061-W080 (approximate coverage)


**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/fabdem-dtm-acre --force 


**File Structure:**
fabdem-dtm-acre/
└── S09W067_FABDEM_V1-2.tif
└── S09W068_FABDEM_V1-2.tif
└── S09W079_FABDEM_V1-2.tif
└── S10W061_FABDEM_V1-2.tif
└── S10W063_FABDEM_V1-2.tif
└── S10W066_FABDEM_V1-2.tif
└── S10W067_FABDEM_V1-2.tif
└── S10W068_FABDEM_V1-2.tif
└── S10W069_FABDEM_V1-2.tif
└── S11W063_FABDEM_V1-2.tif
└── S11W064_FABDEM_V1-2.tif
└── S11W065_FABDEM_V1-2.tif
└── S11W066_FABDEM_V1-2.tif
└── S11W067_FABDEM_V1-2.tif
└── S11W068_FABDEM_V1-2.tif
└── S11W069_FABDEM_V1-2.tif
└── S11W070_FABDEM_V1-2.tif
└── S12W062_FABDEM_V1-2.tif
└── S12W063_FABDEM_V1-2.tif
└── S12W064_FABDEM_V1-2.tif
└── S12W066_FABDEM_V1-2.tif
└── S12W067_FABDEM_V1-2.tif
└── S12W068_FABDEM_V1-2.tif
└── S12W069_FABDEM_V1-2.tif
└── S12W070_FABDEM_V1-2.tif
└── S13W063_FABDEM_V1-2.tif
└── S13W064_FABDEM_V1-2.tif
└── S13W065_FABDEM_V1-2.tif
└── S13W070_FABDEM_V1-2.tif
└── S14W062_FABDEM_V1-2.tif
└── S14W063_FABDEM_V1-2.tif
└── S14W064_FABDEM_V1-2.tif
└── S14W065_FABDEM_V1-2.tif
└── S14W066_FABDEM_V1-2.tif
└── S14W067_FABDEM_V1-2.tif
└── S15W064_FABDEM_V1-2.tif
└── S15W065_FABDEM_V1-2.tif
└── S15W067_FABDEM_V1-2.tif
└── S16W065_FABDEM_V1-2.tif
└── S16W066_FABDEM_V1-2.tif
└── S17W073_FABDEM_V1-2.tif


### 3. NASA HLS Sentinel-2 Data

**Source:** NASA Earthdata  
**Website:** https://earthdata.nasa.gov/  
**Format:** GeoTIFF (.tif)  
**Resolution:** 30m spatial resolution  
**Temporal Coverage:** 2023 growing season  

**Required Bands:**
- B04 (Red): 664.6 nm
- B08 (NIR): 832.8 nm
- B05 (Red Edge): 704.1 nm
- B06 (Red Edge): 740.5 nm
- B07 (Red Edge): 782.8 nm
- B8A (NIR): 864.7 nm
- B11 (SWIR): 1613.7 nm
- B12 (SWIR): 2202.4 nm

**Download Instructions:**
1. Create NASA Earthdata account
2. Access HLS data through AppEEARS or direct download
3. Select tiles: T20LKP, T20LKR, T20LLQ
4. Download scenes 31 August 2023

- Links: 
[https://search.earthdata.nasa.gov/search/granules?p=C2021957295-LPCLOUD&pg[0][v]=f&pg[0][id]=*T20LKP*&pg[0][gsk]=-start_date&g=G2743566340-LPCLOUD&q=HLSS30&sb[0]=-74.42842%2C-23.80314%2C-42.4461%2C3.35343&qt=2023-08-01T00%3A00%3A00.000Z%2C2023-08-31T23%3A59%3A59.999Z&fpj=HLS&tl=1599953843.111!4!!&lat=-10.4393238&long=-65.20483278848315&zoom=8.968601676057522]

[https://search.earthdata.nasa.gov/search/granules?p=C2021957295-LPCLOUD&pg[0][v]=f&pg[0][id]=*T20LLQ*&pg[0][gsk]=-start_date&g=G2743566340-LPCLOUD&q=HLSS30&sb[0]=-74.42842%2C-23.80314%2C-42.4461%2C3.35343&qt=2023-08-01T00%3A00%3A00.000Z%2C2023-08-31T23%3A59%3A59.999Z&fpj=HLS&tl=1599953881.781!4!!&lat=-10.224855&long=-34.59897875000001&zoom=4.204357160354885]

[https://search.earthdata.nasa.gov/search/granules?p=C2021957295-LPCLOUD&pg[0][v]=f&pg[0][id]=*T20LKR*&pg[0][gsk]=-start_date&g=G2743566340-LPCLOUD&q=HLSS30&sb[0]=-74.42842%2C-23.80314%2C-42.4461%2C3.35343&qt=2023-08-01T00%3A00%3A00.000Z%2C2023-08-31T23%3A59%3A59.999Z&fpj=HLS&tl=1599953891.287!4!!&lat=-10.224855&long=-34.59897875000001&zoom=4.204357160354885]


**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023243t143729 --force
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023238t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023228t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023223t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023218t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023240t142719 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023243t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023213t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023238t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023228t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023223t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023235t142721 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023218t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023220t142719 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkr-2023213t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20llq-2023215t142721 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023243t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023238t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023228t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023223t143729 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023218t143731 --force 
kaggle datasets download -d ahmedosmancad/nasa-hls-s30-t20lkp-2023213t143729 --force 

**File Structure:**
nasa-hls-sentinel2-folders/
├── nasa-hls-s30-t20lkp-2023213t143729/
│ ├── HLS.S30.T20LKP.2023213T143729.v2.0.B04.tif
│ ├── HLS.S30.T20LKP.2023213T143729.v2.0.B08.tif
│ └── [additional bands...]
└── [additional scenes...]


### 4. Copernicus Sentinel-2 Data

**Source:** ESA Copernicus Open Access Hub  
**Website:** https://scihub.copernicus.eu/  
**Format:** JPEG2000 (.jp2)  
**Resolution:** 10m and 20m spatial resolution  
**Purpose:** High-resolution validation data  

**Required Bands:**
- B04_10m (Red): 10m resolution
- B08_10m (NIR): 10m resolution
- B05_20m (Red Edge): 20m resolution
- B06_20m (Red Edge): 20m resolution
- B07_20m (Red Edge): 20m resolution
- B8A_20m (NIR): 20m resolution
- B11_20m (SWIR): 20m resolution
- B12_20m (SWIR): 20m resolution

**Download Instructions:**
1. Register at Copernicus Open Access Hub
2. Search for Sentinel-2 Level-2A products
3. Filter by tiles: T20LKP, T20LKR, T20LLQ
4. Download scenes from August 2023

**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/copernicus-t20lkr-20230831t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkr-20230826t143731 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20llq-20230821t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20llq-20230816t143731 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20llq-20230826t143731 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkr-20230821t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20llq-20230831t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkr-20230816t143731 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkp-20230831t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkp-20230821t143729 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkp-20230816t143731 --force 
kaggle datasets download -d ahmedosmancad/copernicus-t20lkp-20230806t143731 --force 

**File Structure:**
copernicus-sentinel2-folders/
├── copernicus-t20lkp-20230806t143731/
│ ├── T20LKP_20230806T143731_B04_10m.jp2
│ ├── T20LKP_20230806T143731_B08_10m.jp2
│ └── [additional bands...]
└── [additional scenes...]



### 5. Environmental Context Data

#### PRODES Deforestation Data

**Source:** INPE (Brazilian National Institute for Space Research)  
**Website:** http://terrabrasilis.dpi.inpe.br/  
**Format:** GeoPackage (.gpkg)  
**Content:** Amazon deforestation polygons  

**Download Instructions:**
1. Visit TerraBrasilis platform
2. Navigate to PRODES Amazon data
3. Download accumulated deforestation layer
4. Select GeoPackage format for compatibility

**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/terrabrasilis-context-data --force 


#### Hydrography Data

**Source:** Brazilian environmental agencies  
**Format:** Shapefile (.shp)  
**Content:** Rivers and water bodies in Amazon basin  

**Download Instructions:**
1. Access through Brazilian geospatial data portals
2. Download Amazon basin hydrography
3. Ensure coordinate system compatibility (EPSG:4326)

**I Uploaded On My Kaggle Datasets For Training**
kaggle datasets download -d ahmedosmancad/hydrography --force 


**File Structure:**
terrabrasilis-context-data/
├── prodes_amazonia_legal.gpkg
├── hydrography.shp
├── hydrography.shx
├── hydrography.dbf
└── hydrography.prj


## Data Preparation Guidelines

### Coordinate Reference Systems

All datasets should be in or convertible to:
- **Primary CRS:** EPSG:4326 (WGS84 Geographic)
- **UTM Zones:** 20S, 21S (for local processing)

### Quality Control Checklist

Before running the pipeline, verify:
- [ ] All required files are present
- [ ] File formats match specifications
- [ ] Coordinate systems are consistent
- [ ] File sizes are reasonable (not corrupted)
- [ ] Temporal coverage aligns with requirements

### Storage Requirements

**Minimum Storage:** 30GB free space  
**Recommended Storage:** 50GB free space  

**Breakdown:**
- FABDEM tiles: ~ 8GB
- NASA HLS scenes: ~ 5GB
- Copernicus scenes: ~ 13GB
- Other data: ~2GB

## Data Ethics and Attribution

### Research Ethics

- Respect Indigenous land rights and cultural heritage
- Follow archaeological research ethics guidelines
- Obtain proper permissions for fieldwork validation
- Collaborate with local archaeological institutions

### Attribution Requirements

When using this system or publishing results, cite:
- NASA for HLS data
- ESA for Copernicus data
- University of Bristol for FABDEM
- Original archaeological survey teams for geoglyph data
- INPE for PRODES data

### Data Sharing Policy

- Model outputs may be shared for research purposes
- Raw satellite data follows original licensing terms
- Archaeological site locations require sensitive handling
- Coordinate with local authorities before field validation

## Troubleshooting Data Issues

### Common Problems

**Missing Files:**
- Check download completion
- Verify file paths in .env configuration
- Ensure proper directory structure

**Coordinate System Errors:**
- Verify CRS definitions
- Check for corrupted projection files
- Ensure consistent geographic extents

**Large File Handling:**
- Use appropriate compression
- Consider cloud storage for large datasets
- Implement incremental download strategies

### Support Resources

- NASA Earthdata Support: https://earthdata.nasa.gov/learn/user-resources
- ESA Copernicus Support: https://scihub.copernicus.eu/userguide/
- University of Bristol FABDEM: Contact data repository administrators

## Data Update Procedures

### Regular Updates

The system can be updated with:
- New satellite imagery for temporal analysis
- Additional archaeological site discoveries
- Updated deforestation data
- Improved elevation models

### Version Control

- Maintain data versioning for reproducibility
- Document data source versions in results
- Archive previous datasets for comparison studies
