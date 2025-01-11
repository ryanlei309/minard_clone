import pandas as pd
import sqlite3

class CreateMinardDB:
    def __init__(self):
        # Read txt file
        with open("data/minard.txt") as f:
            lines = f.readlines()

        column_names = lines[2].split()
        # print(column_names)

        # Data cleaning
        patterns_to_be_replaced = {"(", ")", "$", ","}
        adjusted_column_names = []
        for column_name in column_names:
            for pattern in patterns_to_be_replaced:
                if pattern in column_name:
                    column_name = column_name.replace(pattern, "")
            adjusted_column_names.append(column_name)
        # print(adjusted_column_names)
        self.lines = lines
        # Seperate the column into three group
        self.column_names_city = adjusted_column_names[:3]
        self.column_names_temperature = adjusted_column_names[3:7]
        self.column_names_troop = adjusted_column_names[7:]

    # Load city data. City data is from line 7 to 26.
    def create_city_dataframe(self):
        i = 6
        longitudes, latitudes, cities = [], [], []
        while i <= 25:
            long, lat, city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        city_data = (longitudes, latitudes, cities)

        # Create df to store city data
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city, city_data):
            city_df[column_name] = data
        return city_df

    # Load temperature data. Temperature data is from line 7 to 15.
    def create_temperature_dataframe(self):
        i = 6
        longitudes, temperatures, days, dates = [], [], [], []
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(int(lines_split[4]))
            days.append(int(lines_split[5]))
            
            # Becuase the data in line 11 is missing, add Nov.24 in line 11.
            if i == 10:
                dates.append("Nov 24")
            else:
                date_str = lines_split[6] + " " + lines_split[7]
                dates.append(date_str)
            i += 1
        temperature_data = (longitudes, temperatures, days, dates)

        # Create df to store temperature data
        temperature_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_temperature, temperature_data):
            temperature_df[column_name] = data
        return temperature_df

    # Load troop data. It's easier to seperate from right to left. Because from right to left the logic will be different
    def create_troop_dataframe(self):
        i = 6
        longitudes, latitudes, survivals, directions, divisions = [], [], [], [], []
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i += 1
        troop_data = (longitudes, latitudes, survivals, directions, divisions)

        # Create df to store troop data.
        troop_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_troop, troop_data):
            troop_df[column_name] = data
        return troop_df

    # Create database
    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities": city_df,
            "temperatures": temperature_df,
            "troops": troop_df
        }
        for k, v in df_dict.items():
            v.to_sql(name=k, con=connection, index=False, if_exists="replace")
        connection.close()

create_minard_db = CreateMinardDB()
create_minard_db.create_database()