# We Came, We SAWS, We Conquered Capstone Project

## Data Science Analysis of San Antonio Water System (SAWS) 
We are building a classification model for our codeup capstone project/entry for the 2020 San Antonio CivTech Datathon: to predict root cause of sewer spills and damages, using sewer data, 311 data and multitude of other sources from the city of San Antonio.

### Hypothesis:
- Amount of rain and root cause are related.
- Whether it rains and root cause are related.
- Temperature and root cause are related.
- Low 311 call response rate and root cause are related.
    ### Secondary Hypothesis
    - SSO events and water quality are related.


### Team
Jeremy Cobb, Ryan McCall, Cameron Taylor, David Wederstrandt Sr


### Data Dictionary

### SSO Data
|      Field | Data Description                  
|-----------:|-----------------------------------|
| SSO_ID     | Internal ID                       |  
| SERVNO     | Service Req # (internal use only) |
| REPORTDATE | Date Reported                     |
| SPILL_ADDRESS | Street number of spill         |
| SPILL_ST_NAME | Streen name of spill           |
| TOTAL_GAL | Total gallons spilled              |
| GALSRET | Gallons returned to collection system |
| SPILL_START | When SAWS received information about the spill or arrived at the location|
| SPILL_STOP | Spill actually stopped (no more coming out) |
| HRS | Hours it was spilling (without intemritten stopping starting) |
| CAUSE | Intitial stated cause |
| COMMENTS | Comments |
| ACTIONS | Action taken to stop the SSO |
| WATERSHED | Destination treatment plant of the sewer |
| UNITID | Upstream manhole number |
| UNITID2 | Downstream manhole nunmber (if it is blank, the spill was on the sewer main or lift station) |
| DISCHARGE_TO | spill discharge type area/feature |
| DISCHARGE_ROUTE | Creek name where SSO discharged. NONE = did not discharge to creek |
| COUNCIL_DISTRICT | City Council district of SSO location |
| FERGUSON | Old mapping system reference (internal only) |
| Month | Report Month |
| Year | Report Year |
| Week | Report Week Number |
| EARZ_ZONE | Edwards Aquifer Recharge Zone of SSO location. 0 or NULL = Not in recharge zone. |
| PIPEDIAM | Pipe diameter of the sewer main |
| PIPELEN | Length in feet between manholes (blank means SSO was on main or lift station) |
| PIPETYPE | Pipe material / type |
| INSTYEAR | Main installation date |
| Inches_No | Inches of rainfall the day of SSO |
| RainFall_Less3 | Total rainfall previous 3 days |
| SPILL ADDRESS | Full Address |
| NUM_SPILLS_COMPKEY | Number of recorded spills on the asset (main) |
| NUM_SPILLS_24MOS | Num of spills on asset witih 24 months |
| PREVSPILL_24MOS | Previous spill in the last 24 months |
| UNITTYPE | Main type |
| ASSETTYPE | Asset type emitting spill |
| LASTCLND | Last time we cleaned it - Gravity, Outfall, or Syphon |
| ResponseTime | Time it took for crew to arrive (from call to boots on the ground) |
| ResponseDTTM | When crew arrived on scene |
| Public Notice | Was a public notice required/sent out |
| TIMEINT | Cleaning shcedule in Months that was implemented after the spil |
| Root_Cause | Official, determined cause of the event |
| STEPS_TO_PREVENT | Steps taken to prevent future SSO:\nFCS - clean Schedule, \nDesign Request - need to replace pipe \nPoint - did the repair onsite\nI/I - investigate the inflow and inflitration |
| SPILL_START_2 | NaN |
| SPILL_STOP_2 | NaN |
| HRS_2 | NaN |
| SPILL_START_3 | NaN |
| SPILL_STOP_3 | NaN |
| HRS_3 | NaN | 
| GAL_3 | NaN |

### 311 Data
| Field Name | Description | Data Type | Comment 
|------------:|------------|-----------|---------|
| CASEID | Unique case number assigned by the 311 Lagan System | 10 numeric characters | NaN |
| CASEREF | A composite key created by the 311 Lagan system that combines the unique key from the destination system with the unique key from the Lagan system seperated by a hyphen. | Variable length alphanumeric characters	 | NaN |
| OPENEDDATETIME | The date and time that a case was submitted. | mm/dd/yyyy hh:mm:ss AM/PM | NaN |
| CLOSEDDATETIME | The date and time that a case was closed by the investigating department. | mm/dd/yyyy hh:mm:ss AM/PM | NaN |
| SLA_Date | The due date and time for the work to be investigated and closed by the department. Each case reference type has a different SLA date determined by the responsible department. | mm/dd/yyyy hh:mm:ss AM/PM | NaN |
| Subject To SLA | Check if there is a service level agreement for this case type. | YES/NO | NaN |
| Late (Yes/No) | Check if this case has exceeded the service level agreement date. | YES/NO | NaN |
| LATEDAYS | Measurement of days a case has exceeded the service level agreement (SLA) if applicable. A negative value indicates a case is still in compliance with the SLA. A positive value indicates the number of days the SLA date has been exceeded. | Decimal | NaN |
| Closed (Yes/No) | Check if the case has been closed. | YES/NO | NaN |
| Dept | The city department to which the service request type is assigned. | Text | NaN |
| SUBJECTNAME | The city sub-department to which the service request is assigned. | Text | NaN |
| REASONNAME | The department division to which the service request is assigned. | Text | NaN |
| TYPENAME | The service request type for the concern being reported. | Text | NaN |
| SLADays | Set number of days to meet the service level agreement for this type of case. | Decimal | NaN |
| CaseStatus | The status of a case. | Open/Closed | NaN |
| SOURCEID | The source id from which the service request was received when submitted. | Text | Alphanumeric or numeric = 311 operator, svcCFlag=New mobile app , CRM_Listener=Proactive cases created by city staff , svcCRMSS=Cases submitted through web portal 311 website , svcCRMLS=Cases from original mobile app |
| SOURCEUSERID | The specific user name for the submitted service request. | Text | Name= 311 operator, CityFlag=New mobile app , CRM_Listener=Proactive cases created by city staff , svcCRMSS=Cases submitted through website , svcCRMLS=Cases from original mobile app |
| OBJECTDESC | The service request address or intersection for concern. Note - Due to the way data is stored, intesections will not have zipcodes. | Text | Approximately 15%-17% of addresses are intersections and will not contain zip codes. |
| Council District | The City Council district number for which the issue occurred. | Numeric (0-10) | NaN |
| ALLOCATEDTODEPTID | The internal system coding of the receiving department. | 3 alpha characters | NaN |
| interactiondate | The date that there was an interaction with this case. | mm/dd/yyyy | NaN |
| CLIENTID | The system generated unique id given for the individual reporting the case, if theie contact information was recorded with case. | NaN | If blank, that means no ccustomer information was recorded with request. |
| XCOORD | The X coordinate of this case incident. | 8 numeric character | NaN |
| YCOORD | The Y coordinate of this case incident. | 8 numeric character | NaN |
| Select Dept? | Check if this department is part of the standardized reporting. | YES/NO | NaN |
| Dept (to) | The standardized department names. (8 Departments) | Text | NaN |
| Report Starting Date | The start date range for the case open date for this extract file. | mm/dd/yyyy | NaN |
| Report Ending Date | The end date range for the case open date for this extract file. | mm/dd/yyyy | NaN |

### NOAA Weather Data
| Field Name | Description 
|------------:|-------------|
STATION | Is the station identification code |
DATE | the year of the record followed by the month and day |
AWND | Average daily wind speed (meters per second or miles per hour as per user preference) |
FMTM | Time of fastest mile for fastest-1-minute wind (hours and minutes, i.e., HHMM) |
PGTM | Peak gust time (hours and minutes, i.e., HHMM) |
PRCP | Precipitation (mm or inches as per user preference, inches to hundredths on Daily Form pdf file) |
SNOW | Snowfall (mm or inches as per user preference, inches to tenths on Daily Form pdf file) |
SNWD | Snow depth (mm or inches as per user preference, inches on Daily Form pdf file) |
TAVG | Average temperature (Fahrenheit or Celsius as per user preference, Fahrenheit to tenths on Daily Form PDF) |  
TMAX | Maximum temperature (Fahrenheit or Celsius as per user preference, Fahrenheit to tenths on Daily Form PDF) |  
TMIN | Minimum temperature (Fahrenheit or Celsius as per user preference, Fahrenheit to tenths on Daily Form PDF) |  
WDF2 | Direction of fastest 1-minute wind (degrees) |
WDF5 | Direction of fastest 5-second wind (degrees) |
WSF2 | Fastest 2-minute wind speed (Miles per hour or meters per second as per user preference) |
WSF5 | Fastest 5-second wind speed (Miles per hour or meters per second as per user preference) |
WT01 | Fog, ice fog, or freezing fog (may include heavy fog) |
WT02 | Heavy fog or heavy freezing fog (not always distinguished from fog) |
WT03 | Thunder |
WT05 | Hail (may include small hail) |
WT06 | Glaze or rime |
WT07 | Dust, volcanic ash, blowing dust, blowing sand, or blowing obstruction |
WT08 | Smoke or haze |
WT09 | Blowing or drifting snow |
WT10 | Tornado, waterspout, or funnel cloud | 
WT11 | High or damaging winds |
WT13 | Blowing spray |
WT16 | Rain (May include freezing rain, drizzle, and freezing drizzle) |
WT17 | Freezing Rain |
WT18 | Snow, snow pellets, snow grains, or ice crystals |
WT19 | Unknown source of precipitation |





### Project Links:
##### CivTechSa https://www.civtech-sa.com/datathon
##### Datathon 2020 https://sites.google.com/respec.com/smartsa-datathon-2019/home

### CivTechSa's purpose for Datathon:
We are to discover and identify opportunities and/or missing data elements in the data sets and explain how those insights could be applied in practice for the potential benefits of the community and/or partners.


