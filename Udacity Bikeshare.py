import time
import pandas as pd

CITY_DATA = {
    'chicago': 'data/chicago.csv',
    'Chicago': 'data/chicago.csv',
    'New York City': 'data/new_york_city.csv',
    'New york city': 'data/new_york_city.csv',
    'new york city': 'data/new_york_city.csv',
    'washington': 'data/washington.csv',
    'Washington': 'data/washington.csv'
}


def get_valid_input(prompt, valid_options):
    """
    General function to get valid user input.

    Args:
        prompt (str): The prompt to display to the user.
        valid_options (list): List of valid input options.

    Returns:
        str: Valid user input.
    """
    user_input = input(prompt).lower()
    while user_input not in valid_options:
        print(f"Invalid input. Please choose from: {', '.join(valid_options)}.")
        print("Restarting...")
        user_input = input(prompt).lower()
    return user_input


def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_valid_input(
        "\nWelcome to this program. Please choose your city:\n1. Chicago 2. New York City 3. Washington\nAccepted input:\nFull name of city; not case sensitive (e.g. chicago or CHICAGO).\nFull name in title case (e.g. Chicago).\n",
        list(CITY_DATA.keys()))
    print(f"\nYou have chosen {city.title()} as your city.")

    month = get_valid_input(
        "\nPlease enter the month, between January to June, for which you're seeking the data:\nAccepted input:\nFull month name; not case sensitive (e.g. january or JANUARY).\nFull month name in title case (e.g. April).\n(You may also opt to view data for all months, please type 'all' or 'All' or 'ALL' for that.)\n",
        ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
    print(f"\nYou have chosen {month.title()} as your month.")

    day = get_valid_input(
        "\nPlease enter a day in the week of your choice for which you're seeking the data:\nAccepted input:\nDay name; not case sensitive (e.g. monday or MONDAY).\nDay name in title case (e.g. Monday).\n(You can also put 'all' or 'All' to view data for all days in a week.)\n",
        ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
    print(f"\nYou have chosen {day.title()} as your day.")
    print(
        f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-' * 80)
    return city, month, day


def display_raw_data(df):
    """
    Displays raw data from the DataFrame in chunks of 5 rows.
    Stops displaying data when the user inputs 'no'.
    """
    pd.set_option('display.max_columns', 200)  # Set maximum columns to display
    i = 0  # Initialize row index
    raw_input = input("Would you like to view the raw data? (yes/no): ").lower()

    while raw_input == 'yes':
        if i + 5 > len(df):
            # If the remaining rows are less than 5, display all remaining rows
            print(df.iloc[i:])
            raw_input = input("Would you like to see more data? (yes/no): ").lower()
            break  # Exit the loop after showing the last chunk
        else:
            # Display the next 5 rows
            print(df.iloc[i:i + 5])
            i += 5
            raw_input = input("Would you like to see more data? (yes/no): ").lower()

    print('-' * 80)  # Print separator


def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city.lower()])
    except:
        dfs = []
        for city_name in ['chicago', 'new york city', 'washington']:
            df_city = pd.read_csv(CITY_DATA[city_name])
            dfs.append(df_city)
        df = pd.concat(dfs, ignore_index=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_idx = months.index(month.lower()) + 1
        df = df[df['month'] == month_idx]
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month = df['month'].mode()[0]
    print('The most common month is:', popular_month)
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week is:', popular_day)
    df['start hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['start hour'].mode()[0]
    print('The most common start hour is:', popular_start_hour)
    print(f"This took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station is:', popular_start_station)
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station is:', popular_end_station)
    top = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start station and end station trip is '{top[0]}' to '{top[1]}'")
    print(f"This took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_time, 'minutes.')
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is:', mean_time, 'minutes.')
    print(f"This took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = df['User Type'].value_counts()
    print('The counts of user types is:', '\n', user_types)
    try:
        df = df.dropna(subset=['Gender', 'Birth Year'])
        gender = df['Gender'].value_counts()
        print('\nThe counts of gender is:', '\n', gender)
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print('\nThe earlierst year of birth is:', earliest_birth)
        print('The most recent year of birth is:', most_recent_birth)
        print('The most common year of birth is:', most_common_year)
    except:
        print('\nSorry,there\'s no such data to analyze.')
    print(f"This took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
