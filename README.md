# CellarTracker Integration for Home Assistant

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


First, download the `CT_winelist` directory from this repository and add it to your `custom_component` directory in Home Assistant<br>
<br>
<b>Restart home assistant.</b>

Next, add the following to your `configuration.yaml` file, ensuring your CellarTracker username and password are correctly entered in the `secrets.yaml` file:

```yaml
sensor:
  - platform: CT_winelist  
    username: !secret CT_winelist_username  
    password: !secret CT_winelist_password  
```
<br>
<b>Restart home assistant.</b>

## Customizing Lovelace:

You can view individual wine lists using the flex-table feature in a Lovelace sub-view. To enable this, add the contents of the `lovelace.yaml` file from this repository to your own `lovelace.yaml` file.

For the graphics used in the overview, place them in a directory named `CT_winelist_gfx` within the www-folder. Please note, the graphics are designed for dark backgrounds due to their white color scheme.

## Prerequisites:

This integration depends on the following custom components, which can be installed via the HACS Frontend:
- `vertical-stack-in-card`: [GitHub](https://github.com/ofekashery/vertical-stack-in-card)
- `layout-card`: [GitHub](https://github.com/thomasloven/lovelace-layout-card)
- `flex-table`: [GitHub](https://github.com/custom-cards/flex-table-card)

<i>The component updates every second hour - do not set this lower than every hour, to avoid compromising CellarTracker regulation.</i>
