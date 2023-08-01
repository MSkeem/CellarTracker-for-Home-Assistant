# CellarTracker-for-Home-Assistant
With this custom component you will be able to get your wines from CellarTracker into Home Assistant.<br>
<br>
THe component will make the following entities (and not individual entities for each bottle):<br>
CT_red: contains a list of all red wine and a total number of bottles<br>
CT_white: contains a list of all white wine and a total number of bottles<br>
CT_rose: contains a list of all rosé wine and a total number of bottles<br>
CT_sparkling: contains a list of all sparkling wine and a total number of bottles<br>
CT_fortified: contains a list of all fortified wine and a total number of bottles<br>
CT_other: contains a list of all other wines/spirits/beer etc. and the total number of bottles<br>
CT_total: contains the total number of bottles, the total price and the average price pr. bottle<br>
<br>
**Installation:**    
<br>
Add the following to your **configuration.yaml**:  
sensor: #ensure that your cellartracker username and password are added in the secrets.yaml file.  
  - platform: CT_winelist  
    username: !secret CT_winelist_username  
    password: !secret CT_winelist_password  
<br>
**Custom component folder:**<br>  
Add the **CT_winelist** folder from this repository to your custom_component folder.  
<br>
**Lovelace:**
The individual winelist is done using flex-table and viewed in a lovelace-subview.<br>
Add the **lovelace.yaml** content to your lovelace.yaml file.<br>
Prereqs for this is the following custom components which can be installed through HACS Frontend:<br>
**vertical-stack-in-card** - https://github.com/ofekashery/vertical-stack-in-card<br>
**layout-card** - https://github.com/thomasloven/lovelace-layout-card<br>
**flex-table** - https://github.com/custom-cards/flex-table-card<br>
<br>
Graphics used in the overview, should be put in a folder called **CT_winelist_gfx** in the www-folder. Note: the graphics is white and requires a dark background.
