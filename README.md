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

- SSO Data
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


### Project Links:
##### CivTechSa https://www.civtech-sa.com/datathon
##### Datathon 2020 https://sites.google.com/respec.com/smartsa-datathon-2019/home

### CivTechSa's purpose for Datathon:
We are to discover and identify opportunities and/or missing data elements in the data sets and explain how those insights could be applied in practice for the potential benefits of the community and/or partners.


