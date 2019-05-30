import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

"""months_list used to determine available months in data"""
months_list = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("\nWhat city would you like to review? Please select from Chicago, New York City, and Washington: ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("That city is not an option. Please review the previous prompt.")
        else:
            break

    while True:
        month = input("\nWe have data for the first six months of 2017. Did you want to see one in particular? " \
                      "Type the full month name (i.e. January, February, March... or type 'All': ").lower()
        if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print("Hmm... We're not registering that month. Please try again.")
        else:
            break

    while True:
        day = input("\nWhat day of the week did you want to see? Please type the full name " \
                    "of the day of the week you'd like to view (i.e. Monday, Tuesday, Wednesday... or type 'All': ").lower()
        if day not in ['monday','tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print("I think we may have misunderstood... Could you please type that again?")
        else:
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['Travel Time'] = df['End Time'] - df['Start Time']
    df['Station Set'] = df['Start Station'] + ' to ' + df['End Station']

    if month != 'all':
        filtered_month = months_list.index(month) + 1
        df = df[df['month'] == filtered_month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month != 'all':
        print("Based on your selection, we are only looking at data from {}.".format(month.title()))
    else:
        popular_month_num = df['month'].mode()[0]
        popular_month = months_list[popular_month_num-1]
        print("The most popular month for travel in {} is {}.".format(city.title(), popular_month.title()))

    if day != 'all':
        print("Based on your selection, we are only looking at data for a single day: {}.".format(day.title()))
    else:
        popular_day = df['day_of_week'].mode()[0]
        print("The most popular day of the week for travel in {} is {}.".format(city.title(), popular_day.title()))

    popular_hour = df['hour'].mode()[0]
    if (popular_hour / 12) > 1:
        print("The most popular time to rent a bike in {} is {}pm.".format(city.title(), popular_hour % 12))
    else:
        print("The most popular time to rent a bike in {} is {}am.".format(city.title(), popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    common_station_set = df['Station Set'].mode()[0]

    print("The most commonly used start station is:", common_start_station)
    print("The most commonly used end station is:", common_end_station)
    print("The most common start and end station trip is:", common_station_set)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    tot_travel_time = df['Travel Time'].sum()
    print("The time spent on bikes in the first 6 months of 2017 in {} is {}. Wow!!".format(city.title(), tot_travel_time))

    print("\nBut now getting into more helpful pieces of information....\n")
    print("The average bike rental was {}.".format(df['Travel Time'].mean()))
    print("The shortest bike rental was {}.".format(df['Travel Time'].min()))
    print("The longest bike rental was {}.".format(df['Travel Time'].max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users.

    Stats include:
    - Types of Users (Subscriber, One-Time Customers)
    - User Gender (Male, Female, Unknown)
    - Earliest, latest, and most common Birth Year"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("When it comes to bike rentals, we have a few different ways of looking at our users...\n")
    print(df['User Type'].value_counts(dropna = False))

    if city == "washington":
        print("For the city of Washington, it looks like we only have data regarding customer type. "\
        "For more information user types like Birth Year and Gender, try a different city.")

    else:
        min_birth_year = df['Birth Year'].min()
        max_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]

        print("\n")
        print(df['Gender'].value_counts(dropna = False))

        print("\nNeat, huh? See what else we can tell:\n")
        print("Our oldest user was born in the year {}!".format(min_birth_year))
        print("By comparison, our youngest user was born in the year {}...Pretty crazy, huh?".format(max_birth_year))
        print("And to round us out, the most common birth year is {}.".format(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_data(df, city):
    """Displays data for 5 lines of raw data and asks the user if they would like to see 5 more.
    User inputs 'yes' or 'no' to continue to review data in groups of 5"""

    start_index = 0
    end_index = 5
    countby = 5

    while True:
        print("\nDisplaying the first 5 lines of data below:\n")
        print_range = range(start_index, end_index)
        for i in print_range:
            print(df.iloc[0:][i:i+1].transpose())
            start_index += countby
            end_index += countby
        show_more = input("\nWould you like to review more data? Enter yes or no.\n")
        if show_more.lower() != 'yes':
            break
                              
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city, month, day)
        station_stats(df)
        trip_duration_stats(df, city)
        user_stats(df, city)
        see_data(df, city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
	main()
