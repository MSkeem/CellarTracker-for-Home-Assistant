# CellarTracker Integration for Home Assistant

<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/ct_logo.png" alt="CellarTracker logo" width="25%"/>
</p>


This custom integration enables you to import your wine collections from CellarTracker into Home Assistant.

The integration generates the following entities which represent categories of wine rather than individual bottles:
- `CT_red`: Contains a list of all red wines and their total bottle count.
- `CT_white`: Contains a list of all white wines and their total bottle count.
- `CT_rose`: Contains a list of all rosé wines and their total bottle count.
- `CT_sparkling`: Contains a list of all sparkling wines and their total bottle count.
- `CT_fortified`: Contains a list of all fortified wines and their total bottle count.
- `CT_other`: Contains a list of all other alcoholic beverages like spirits and beer, and their total bottle count.
- `CT_total`: Contains the total number of bottles, their combined price and the average price per bottle.

## Installation:
Do either 1.a. or 1.b.:<br>
<br>
**1.a. (the easy wat):**<br>
Add the integration through HACS under Custom Integration:<br>
Repository: https://github.com/MSkeem/CellarTracker-for-Home-Assistant<br>
Category: Integration<br>
<br>
**1.b.:**<br>
First, download the `CT_winelist` directory from this repository and add it to your `custom_component` directory in Home Assistant<br>
<b>Restart home assistant.</b>
<br>
**2.**<br>
And when you have done either 1.a. or 1.b. you should add the following to your `configuration.yaml` file:

```yaml
sensor:
  - platform: CT_winelist  
    username: !secret CT_winelist_username  
    password: !secret CT_winelist_password  
```
Add your CellarTracker username and password in the `secrets.yaml` file:<br>
```yaml
CT_winelist_username: your_username
CT_winelist_password: your_password
```
<br>
<b>Restart home assistant.</b>

## Lovelace:
The overview in Lovelace looks like this (Danish):

<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/overview.PNG" alt="Lovelace overview" width="100%"/>
</p>


You can view individual wine lists using the flex-table feature in a Lovelace sub-view. To enable this, add the contents of the `lovelace.yaml` file from this repository to your own `lovelace.yaml` file.

Example of a sub-view e.g. when pressing the "White wine" icon:
<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/subview.PNG" alt="Lovelace subview" width="100%"/>
</p>


For the graphics used in the overview, place them in a directory named `CT_winelist_gfx` within the www-folder. Please note, the graphics are designed for dark backgrounds due to their white color scheme.

## Prerequisites:

This integration depends on the following custom components, which can be installed via the HACS Frontend:
- `vertical-stack-in-card`: [GitHub](https://github.com/ofekashery/vertical-stack-in-card)
- `layout-card`: [GitHub](https://github.com/thomasloven/lovelace-layout-card)
- `flex-table`: [GitHub](https://github.com/custom-cards/flex-table-card)

<i>The component updates every second hour - do not set this lower than every hour, to avoid compromising CellarTracker regulation.</i>


## Disclaimer:
This is an unofficial integration of Cellar Tracker for Home Assistant, the developer and the contributors are not, in any way, affiliated to CellarTracker! LLC.

"CellarTracker!" is a trademark of CellarTracker! LLC
