import pandas as pd
import numpy as np

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval
import logging
from cellartracker import cellartracker

_LOGGER = logging.getLogger(__name__)

username = None
password = None

# List of columns to keep, except iWine which is only used as a unique identifier
columns = ["iWine", "Type", "Country", "Region", "Vintage", "Varietal", "Wine", "BeginConsume", "EndConsume", "CT", "Size", "Price", "Location", "Bin"]

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=7200)

# Global variable to store fetched data
data = None

async def async_get_data(hass):

    client = cellartracker.CellarTracker(username, password)
    inventory_list = await hass.async_add_executor_job(client.get_inventory)
    df = pd.DataFrame(inventory_list)

    #If no price for a wine in a group of wines, then add the max price to all wines in the group 
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
    df['Price'] = df.groupby('iWine')['Price'].apply(lambda group: group.replace(0, group[group > 0].max()).fillna(group[group > 0].max())).reset_index(level=0, drop=True)
    
    #count the same wine and group them
    df['Quantity'] = df.groupby('iWine')['iWine'].transform('count')
    df = df.drop_duplicates(subset='iWine').drop(columns='iWine')

    # Add 'CT_' prefix to 'Type' column
    df['Type'] = 'CT_' + df['Type']

    # New grouping logic
    df['Group'] = df['Type']  # Initially set the group to the wine type
    df.loc[df['Type'].str.contains('sparkling', case=False, na=False), 'Group'] = 'CT_Sparkling'
    df.loc[df['Type'].str.contains('fortified', case=False, na=False), 'Group'] = 'CT_Fortified'
    df.loc[~df['Group'].isin(['CT_Red', 'CT_White', 'CT_Rosé', 'CT_Sparkling', 'CT_Fortified']), 'Group'] = 'CT_Other'
    df = df.drop(columns='Type')
    df = df.rename(columns={'Group': 'Type'})
        
    # Excluding 'iWine' from the columns to iterate over since it has been dropped
    iter_columns = [col for col in columns if col != 'iWine']
    #checking if some of the groups are empty and if so, fill one row with data (no data if string and zero if number)
    required_types = ['CT_Red', 'CT_White', 'CT_Rosé', 'CT_Sparkling', 'CT_Fortified', 'CT_Other']
    for req_type in required_types:
        if req_type not in df['Type'].values:
            blank_row = {}
            for col in iter_columns:
                if col == 'Type':
                    blank_row[col] = req_type
                elif col == 'Quantity' or np.issubdtype(df[col].dtype, np.number):
                    blank_row[col] = 0  # Filling numeric columns with 0
                else:
                    blank_row[col] = 'No data'  # Filling non-numeric columns with "No data"
            blank_row_df = pd.DataFrame([blank_row])
            df = pd.concat([df, blank_row_df], ignore_index=True) #merge new blank rows with cellartracker

    #fix potential numbering problems
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
    df['CT'] = pd.to_numeric(df['CT'], errors='coerce').fillna(0).round(1)
    df['BeginConsume'] = pd.to_numeric(df['BeginConsume'], errors='coerce').fillna(0).astype(int)
    df['EndConsume'] = pd.to_numeric(df['EndConsume'], errors='coerce').fillna(0).astype(int)

    #data for the total-entity
    total_bottles = df['Quantity'].sum()
    total_price = (df['Quantity'] * df['Price']).sum()
    average_price = float(total_price) / float(total_bottles) if total_bottles else 0
    grouped = df.groupby('Type')
    return total_bottles, total_price, average_price, grouped
    
async def async_update_data(hass, now=None):
    """Update the global data."""
    global data
    data = await async_get_data(hass)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    global username, password, data
    username = config.get('username')
    password = config.get('password')
    data = await async_get_data(hass)
    total_bottles, total_price, average_price, grouped = data
    entities = [CTwineSensor(hass, name, group) for name, group in grouped]
    entities.append(CTtotalSensor(hass, 'CT_total', total_bottles, total_price, average_price))
    async_add_entities(entities)

    async def interval_callback(now):
        """This function is called every MIN_TIME_BETWEEN_UPDATES and calls async_update_data with the correct hass object."""
        await async_update_data(hass)

    # Schedule a single update for all entities
    async_track_time_interval(hass, interval_callback, MIN_TIME_BETWEEN_UPDATES)

class CTwineSensor(Entity):
    def __init__(self, hass, type, group):
        self._hass = hass
        self._type = type
        self._state = group['Quantity'].sum()
        self._attributes = group.to_dict(orient='records')
        self._unique_id = f"winelist_{self._type}"

    @property
    def name(self):
        return self._type

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {'Data': self._attributes}

    @property
    def unique_id(self):
        return self._unique_id

    async def async_update(self, now=None):
        global data
        #_LOGGER.info(f"Type of hass in async_get_data: {type(self._hass)}")
        #_LOGGER.info(f"Updating {self._unique_id} at {now}")
        total_bottles, total_price, average_price, grouped = data
        #if self._type not in grouped.groups:
        #    _LOGGER.error(f"Group '{self._type}' not found in dataframe")
        #    return
        group = grouped.get_group(self._type)
        self._state = group['Quantity'].sum()
        self._attributes = group.to_dict(orient='records')

class CTtotalSensor(Entity):
    def __init__(self, hass, name, total_bottles, total_price, average_price):
        self._hass = hass
        self._name = name
        self._state = int(total_bottles)
        self._attributes = {'Total Price': int(total_price), 'Average Price': int(average_price)}
        self._unique_id = f"winelist_{self._name}"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def unique_id(self):
        return self._unique_id

    async def async_update(self, now=None):
        global data
        #_LOGGER.info(f"Type of hass in async_get_data: {type(self._hass)}")
        #_LOGGER.info(f"Updating {self._unique_id} at {now}")
        total_bottles, total_price, average_price, grouped = data
        self._state = int(total_bottles)
        self._attributes = {'Total Price': int(total_price), 'Average Price': int(average_price)}
