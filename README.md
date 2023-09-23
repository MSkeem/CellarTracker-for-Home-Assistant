# Home Assistant Integration for CellarTracker 
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/ct_logo.png" alt="CellarTracker logo" width="25%"/>
</p>

This custom integration enables you to seamlessly import your wine collections from CellarTracker into Home Assistant.

The integration generates the following distinct entities, each representing a category of wine as opposed to individual bottles:

- `CT_red`: Houses a list of all red wines along with their total bottle count.
- `CT_white`: Contains all your white wines with their respective bottle count.
- `CT_rose`: Details a list of all rosé wines and their corresponding bottle count.
- `CT_sparkling`: Holds a list of all sparkling wines with their total count.
- `CT_fortified`: Maintains a list of all fortified wines and their collective bottle count.
- `CT_other`: Encapsulates a list of other alcoholic beverages such as spirits and beer, along with their total bottle count.
- `CT_total`: Represents the aggregate number of bottles, their combined price, and the average price per bottle.

## Installation Guide:
Choose either 1.a. or 1.b. for the initial step:<br>

**1.a. Easy Method:**<br>
Add the integration via HACS under Custom Integration:<br>
Repository: https://github.com/MSkeem/CellarTracker-for-Home-Assistant<br>
Category: Integration<br>

**1.b. Manual Method:**<br>
Download the `CT_winelist` directory from this repository and place it in your `custom_component` directory in Home Assistant.<br>

**2. Final Step:**<br>
Post completion of either 1.a. or 1.b., <b>restart Home Assistant</b> and add the following snippet to your `configuration.yaml` file (or in your `sensor.yaml` file):

```yaml
sensor:
  - platform: CT_winelist  
    username: !secret CT_winelist_username  
    password: !secret CT_winelist_password  
```

**Database management note:**<br>
Wine details are stored as entity attributes. To avoid database overload and warnings from Home Assistant, consider excluding these entities from the recorder. Update the `recorder` section in your `configuration.yaml` as follows:

```yaml
recorder:
  exclude:
    entities:
      - sensor.ct_fortified
      - sensor.ct_other
      - sensor.ct_red
      - sensor.ct_rose
      - sensor.ct_sparkling
      - sensor.ct_white
```

**Username and password for CellarTracker:**<br>
Include your CellarTracker username and password in the `secrets.yaml` file as shown:

```yaml
CT_winelist_username: your_username
CT_winelist_password: your_password
```
Remember to <b>restart Home Assistant</b> once more.

## Lovelace Overview:

Here is a snapshot of how the overview looks in Lovelace (example given in Danish):

<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/overview.PNG" alt="Lovelace overview" width="100%"/>
</p>

From the overview you can also view individual wine lists using the flex-table feature in a Lovelace sub-view.
To enable the overview and detailed view, add the content of the `ui-lovelace.yaml` file from this repository to your own `ui-lovelace.yaml` file.

Here is an example of a sub-view, e.g., when pressing the "White wine" icon:

<p align="center">
  <img src="https://github.com/MSkeem/CellarTracker-for-Home-Assistant/blob/main/img/subview.PNG" alt="Lovelace subview" width="100%"/>
</p>

The graphics used in the overview should be placed in a directory named `CT_winelist_gfx` within the www-folder. Please note that these graphics are designed for dark backgrounds, hence their white color scheme.

## Prerequisites:

This integration relies on the following custom components. These can be installed via the HACS Frontend:
- `vertical-stack-in-card`: [GitHub](https://github.com/ofekashery/vertical-stack-in-card)
- `layout-card`: [GitHub](https://github.com/thomasloven/lovelace-layout-card)
- `flex-table`: [GitHub](https://github.com/custom-cards/flex-table-card)

<i>Please note that the component updates every two hours. To avoid violating CellarTracker's regulations, do not set this frequency lower than once per hour.</i>

## Disclaimer:
This integration for CellarTracker with Home Assistant is unofficial. The developer is in no way affiliated with CellarTracker! LLC. 

"CellarTracker!" is a registered trademark of CellarTracker! LLC.
