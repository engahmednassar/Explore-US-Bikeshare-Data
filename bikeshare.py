import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def check_inputs(user_input, input_type):
    while True:
        read_input = input(user_input).lower()
        if read_input in ['chicago', 'new york city', 'washington'] and input_type == 1:
            break
        elif read_input in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
            break
        elif read_input in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']  and input_type == 3:
            break 
        else:
            if input_type == 1:
                print('Invalid city name! Choose one of the cities given in the question.')
            if input_type == 2:
                print('Invalid month name! Choose one of the months given in the question.')
            if input_type == 3:
                print('Invalid day name! Choose one of the days given in the question.')
        
    return read_input
      


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_inputs("Whould you like to see data for  chicago, new york city or washington?\n", 1)

    # get user input for month (all, january, february, ... , june)
    month = check_inputs("Which month you want to filter by?  january, february, march, april, may, june  or  'all' for all months?\n" , 2)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_inputs("Which day you want to filter by?  sunday, monday, tuesday, wednesday, thursday, friday, saturday  or 'all'  for all days\n", 3)
    print('\nJust one momment... loading the data')
    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week and hour  from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_name()
    df['start hour'] = df['Start Time'].dt.hour
    
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day of week'] == day.title()]
        
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('What is the most popular month for traveling?\n', df['month'].mode()[0])

    # display the most common day of week
    print('What is the most popular day for traveling?\n', df['day of week'].mode()[0])

    # display the most common start hour
    print('What is the most popular hour of the day to start your travels?\n', df['start hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('What is the most popular start station?\n', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nWhat is the most popular end station?\n', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    station_groups = df.groupby(['Start Station', 'End Station'])
    print('\nWhat is the most popular trip from start to end?\n', station_groups.size().sort_values(ascending=False).head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days = total_travel_time.days
    hours = total_travel_time.seconds // (60*60)
    minutes = total_travel_time.seconds % (60*60) // 60
    seconds = total_travel_time.seconds % (60*60) % 60
    print("What was the total traveling done for 2014 through June?\n{} days {}:{}:{}\n".format(days, hours, minutes, seconds))
    
    # display mean travel time
    average_travel_time = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days = average_travel_time.days
    hours = average_travel_time.seconds // (60*60)
    minutes = average_travel_time.seconds % (60*60) // 60
    seconds = average_travel_time.seconds % (60*60) % 60
    print("What was the average time spent on each trip?\n{} days {}:{}:{}".format(days, hours, minutes, seconds))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('What is the breakdown of users?\n', df['User Type'].value_counts())
    
    # Display counts of gender
    if city != 'washington':
        print('\nWhat is the breakdown of gender?\n', df['Gender'].value_counts())
    
    # Display earliest, most recent, and most common year of birth
        print('\nWhat is the oldest year or birth?\n', df['Birth Year'].min())
        print('What is the youngest year or birth?\n', df['Birth Year'].max())
        print('What is the most popular year or birth?\n', df['Birth Year'].mode()[0])
    else:
        print("\nNo 'gender' or 'birth year'  data to share for Washington.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_row_data(df):
    """Asks the user if he wants to display raw data. 5 rows at time."""
    row_data = input('Whould you like to display row data?  yes or no \n')
    if row_data.lower() == 'yes':
        count = 0
        while True:
            print(df.iloc[count : count+5])
            count += 5
            more_data = input('Want to see the next 5 raws? yes or no \n')
            if more_data.lower() != 'yes':
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_row_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
 	main()
