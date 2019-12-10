import time
import pandas as pd
import numpy as np
import sys

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user for their name and city
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #Introductions. Get name and residence of user
    new_name = 'yes'
    while new_name == 'yes':
        try:
            name_and_city = input('Hey there! What\'s your firstname [space] and which city are you from?: [e.g Eunice Kampala]\n')
            break
        except:
            print('Something is wrong. Please input the correct format\n')
            new_name = input('Try again? \n')

    print(' ')

    #greetings to the user. try statement to handle any errors
    try:
        print('Hello {} from {}. Happy to have you here! Let\'s explore some US bikeshare data!\n'.format(name_and_city.split(' ')[0].title(), name_and_city.split(' ')[1]).title())
    except:
        print('Something\'s not right. Did you include your first name, a space then where you are from? [e.g Eunice Kampala]')
        print('Re-run program and input correct details')
        print(' ')
        sys.exit()

    print(' ')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('{}, we would like to help you filter your data so that you can quickly drill down to what you are interested in. Please enter your responses below to tell us what you want to see :-)'.format(name_and_city.split(' ')[0]).title())

    print(' ')

    new_filters  = 'yes'
    while new_filters =='yes':
        try:
            city = input("Which city would you like to look at? \n")
            if(city.lower() not in ['chicago', 'washington', 'new york city']):
                print('The city you have entered doesn\'t seem right. Please input the correct city name\n')
                new_filters == 'yes'
            else:
                break
        except:
            print('Something is wrong. Please input the correct format \n')
            new_filters = input('Try again? ')
    print(' ')
    
    # get user input for month (all, january, february, ... , june)
    while new_filters == 'yes':
        try:
            month = input('Which month would you like to look at? (enter full months names [e.g January] to filter or \'all\' for no filter) \n')
            if(month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']):
                print('Data in this database is only for the first six months of the year. What you have entered doesn\'t seem right. Please input the correct month\n')
                new_filters == 'yes'
            else:
                break
        except:
            print('Something is wrong. Please input the correct format\n')
            new_filters = input('Try again? ')
    print(' ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while new_filters == 'yes':
        try:
            day = input('Which day would you like to analyse? (enter full day name [e.g. Monday] \'all\' for no filter) \n')
            if(day.lower() not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']):
                print('The day you have entered doesn\'t seem right. Please input the correct day of the week\n')
                new_filters == 'yes'
            else:
                break
        except:
            print('Something is wrong. Please input the correct format \n')
            new_filters = input('Try again? ')
    print(' ')

    print('-'*80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    try:
        df = pd.read_csv(CITY_DATA[city.lower()])
    except:
        print('Something is not right. The file {} cannot be found. Place the file in the same directory as the script and re-run the program'.format(CITY_DATA[city.lower()]))
        print(' ')
        sys.exit()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format = True)

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    try:
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month.lower())+1
            
            is_month = df['month'] == month
        
            # filter by month to create the new dataframe
            df = df[is_month]
    except:
        print('Something is not right. The month you have given does not exist in our database. Re-run program and input correct month')
        sys.exit()


    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        is_day = df['day_of_week'] == day.title()
        df = df[is_day]

    return df

def statistics_overview(df):
    """This function displays the data in chunks of 5 rows using dictionaries nested within a list
    
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        str - Returns a thank you note to the user

    """
    start = 0
    interval = 5
    view_data = input('Would you like to view 5 lines of records in the data? \n')
    data_list = []

    while view_data == 'yes':
        data_list.clear()
        for i in range(start, start+interval):
            data_dict = {}
            for column in df.columns.values:
                data_dict[column] = df[column][df.index.values[i]]
            data_list.append(data_dict)
            start+=interval
        print(data_list)
        print(' ')
        view_data = input('Would you like to view some more records? \n')

    return('Thank you for your time')


def time_stats(df, city, month, day_of_week):
    """Displays statistics on the most frequent times of travel.

        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day

        returns:
            time taken to perform the task
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    #if statement to check if there are month filters. Do not calculate mode if there are no month filters as there is only one month
    if month.lower() == 'all':
        print('Most common month for {} is: {}\n'.format(city.title(), months[df['month'].mode()[0]-1].title()))
    else:
        print('There is no most common month as you have chosen only one month: {}\n'. format(month.title()))
     
    # display the most common day of week

    #if statment to check which filters the user has set
    if day_of_week == 'all' and month.lower() == 'all':
        print('Most common day of week for {} is: {}\n'.format(city.title(), df['day_of_week'].mode()[0]))
    elif day_of_week == 'all' and month.lower() != 'all':
        print('Most common day of week for {} in month {} is: {}\n'.format(city.title(), month.title(), df['day_of_week'].mode()[0]))
    else:
        print('There is no most common day of week as you have chosen only one day of week: {}\n'.format(day_of_week.title()))

    # display the most common start hour

    #if statment to check which filters the user has set
    if month.lower() != 'all' and day_of_week != 'all':
        print('Most common start hour in {} for the month {} on the day {} is: {}\n'.format(city.title(), month.title(), day_of_week.title(), df['hour'].mode()[0]))
    elif month == 'all' and day_of_week != 'all':
        print('Most common start hour in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['hour'].mode()[0]))
    elif month != 'all' and day_of_week == 'all':
        print('Most common start hour in {} for the month {} for all days of the week is: {}\n'.format(city.title(), month.title(), df['hour'].mode()[0]))
    else:
        print('Most common start hour in {} is: {}\n'.format(city.title(), df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df, city, month, day_of_week):
    """Displays statistics on the most popular stations and trip.

        Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day

        returns:
            time taken to perform the task
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Most commonly used start station in {} for the month {} on the day {} is: {}\n'.format(city.title(), month.title(), day_of_week.title(), df['Start Station'].mode()[0]))
    elif month == 'all' and day_of_week != 'all':
        print('Most commonly used start station in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['Start Station'].mode()[0]))
    elif month != 'all' and day_of_week == 'all':
        print('Most commonly used start station in {} for the month {} for all days of the week is: {}\n'.format(city.title(), month.title(), df['Start Station'].mode()[0]))
    else:
        print('Most commonly used start station in {} is: {}\n'.format(city.title(), df['Start Station'].mode()[0]))


    # display most commonly used end station

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Most commonly used end station in {} for the month {} on the day {} is: {}\n'.format(city.title(), month.title(), day_of_week.title(), df['End Station'].mode()[0]))
    elif month == 'all' and day_of_week != 'all':
        print('Most commonly used end station in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['End Station'].mode()[0]))
    elif month != 'all' and day_of_week == 'all':
        print('Most commonly used end station in {} for the month {} for all days of the week is: {}\n'.format(city.title(), month.title(), df['End Station'].mode()[0]))
    else:
        print('Most commonly used end station in {} is: {}\n'.format(city.title(), df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip

    #Derive the route from the Start Station and End Station Values
    df['start_end_comb'] = df['Start Station'] + " to " + df['End Station']

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Most frequent combination of start station and end station trip in {} for the month {} on the day {} is: {}\n'.format(city.title(), month.title(), day_of_week.title(), df['start_end_comb'].mode()[0]))
    elif month == 'all' and day_of_week != 'all':
        print('Most frequent combination of start station and end station trip in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['start_end_comb'].mode()[0]))
    elif month != 'all' and day_of_week == 'all':
        print('Most frequent combination of start station and end station trip in {} for the month {} for all days of the week is: {}\n'.format(city.title(), month.title(), df['start_end_comb'].mode()[0]))
    else:
        print('Most frequent combination of start station and end station trip in {} is: {}\n'.format(city.title(), df['start_end_comb'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df, city, month, day_of_week):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    #compute the days, hours, minutes and seconds for mean travel time
    ttt_seconds = round((((df['Trip Duration'].sum())%(24*3600))%3600)%60,2)
    ttt_minutes = round((((df['Trip Duration'].sum())%(24*3600))%3600)/60,2)
    ttt_hours = round(((df['Trip Duration'].sum())%(24*3600))/3600,2)
    ttt_days = int((df['Trip Duration'].sum())/(24*3600))

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Total travel time in {} for the month {} on the day {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), month.title(), day_of_week.title(), ttt_days, ttt_hours, ttt_minutes, ttt_seconds))
    elif month == 'all' and day_of_week != 'all':
        print('Total travel time in {} for all months on the day {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), day_of_week.title(), ttt_days, ttt_hours, ttt_minutes, ttt_seconds))
    elif month != 'all' and day_of_week == 'all':
        print('Total travel time {} for the month {} for all days of the week is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), month.title(),ttt_days, ttt_hours, ttt_minutes, ttt_seconds))
    else:
        print('Total travel time in {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), ttt_days, ttt_hours, ttt_minutes, ttt_seconds))
    print(' ')

    # display mean travel time

    #compute the days, hours, minutes and seconds for mean travel time
    mtt_seconds = round((((df.loc[:,'Trip Duration'].mean())%(24*3600))%3600)%60,2)
    mtt_minutes = round((((df.loc[:,'Trip Duration'].mean())%(24*3600))%3600)/60,2)
    mtt_hours = round(((df.loc[:,'Trip Duration'].mean())%(24*3600))/3600,2)
    mtt_days = int((df.loc[:,'Trip Duration'].mean())/(24*3600))

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Mean travel time in {} for the month {} on the day {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), month.title(), day_of_week.title(), mtt_days, mtt_hours, mtt_minutes, mtt_seconds))
    elif month == 'all' and day_of_week != 'all':
        print('Mean travel time in {} for all months on the day {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), day_of_week.title(), mtt_hours, mtt_days, mtt_minutes, mtt_seconds))
    elif month != 'all' and day_of_week == 'all':
        print('Mean travel time {} for the month {} for all days of the week is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), month.title(), mtt_days, mtt_hours, mtt_minutes, mtt_seconds))
    else:
        print('Mean travel time in {} is: {} days {} hours {} minutes {} seconds\n'.format(city.title(), mtt_days, mtt_hours, mtt_minutes, mtt_seconds))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df, city, month, day_of_week):
    """Displays statistics on bikeshare users
        
        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
            (DataFrame) df - Pandas DataFrame containing city data filtered by month and day

         returns:
            time taken to perform the task
    ."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nInformation about user types......\n')

    #if statment to check which filters the user has set
    if month != 'all' and day_of_week != 'all':
        print('Number of riders per user type in {} for the month {} on the day {}:\n {}\n'.format(city.title(), month.title(), day_of_week.title(), df['User Type'].value_counts()))
    elif month == 'all' and day_of_week != 'all':
        print('Number of riders per user type in {} for all months on the day {}:\n {} \n'.format(city.title(), day_of_week.title(), df['User Type'].value_counts()))
    elif month != 'all' and day_of_week == 'all':
        print('Number of riders per user type in {} for the month {} for all days of the week:\n {} \n'.format(city.title(), month.title(), df['User Type'].value_counts()))
    else:
        print('Number of riders per user type in {}:\n {}\n'.format(city.title(), df['User Type'].value_counts()))
        
    print(' ')

    # Display counts of gender
    print('\nInformation about user\'s gender......\n')

    """outer if statement used to check if the data is for chicago or new york to determine if to calculate the gender information"""
    if city.lower() == 'chicago' or city.lower() == 'new york city':
        #inner if statment to check which filters the user has set
        if month != 'all' and day_of_week != 'all':
            print('Number of riders per gender in {} for the month {} on the day {}:\n {} \n'.format(city.title(), month.title(), day_of_week.title(), df['Gender'].value_counts()))
        elif month == 'all' and day_of_week != 'all':
            print('Number of riders per gender in {} for all months on the day {}:\n {}\n'.format(city.title(), day_of_week.title(), df['Gender'].value_counts()))
        elif month != 'all' and day_of_week == 'all':
            print('Number of riders per gender in {} for the month {} for all days of the week:\n {} \n'.format(city.title(), month.title(), df['Gender'].value_counts()))
        else:
            print('Number of riders per gender in {}:\n {} \n'.format(city.title(), df['Gender'].value_counts()))
    else:
        print('This data does not contain gender details\n')
    print(' ')  

    # Display earliest, most recent, and most common year of birth
    print('\nInformation about user\'s birth years......\n')

    """outer if statement used to check if the data is for chicago or new york to determine if to calculate the birth year information"""
    if city.lower() == 'chicago' or city.lower() == 'new york city': 
        
        #inner if statment to check which filters the user has set
        if month != 'all' and day_of_week != 'all':
            print('Earliest year of birth in {} for the month {} on the day {} is: {} \n'.format(city.title(), month.title(), day_of_week.title(), df['Birth Year'].min()))
            print('Most recent year of birth in {} for the month {} on the day {} is: {} \n'.format(city.title(), month.title(), day_of_week.title(), df['Birth Year'].max()))
            print('Most common year of birth in {} for the month {} on the day {} is: {} \n'.format(city.title(), month.title(), day_of_week.title(), df['Birth Year'].mode()[0]))
        elif month == 'all' and day_of_week != 'all':
            print('Earliest year of birth in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['Birth Year'].min()))
            print('Most recent year of birth in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['Birth Year'].max()))
            print('Most common year of birth in {} for all months on the day {} is: {}\n'.format(city.title(), day_of_week.title(), df['Birth Year'].mode()[0]))
        elif month != 'all' and day_of_week == 'all':
            print('Earliest year of birth in {} for the month {} for all days of the week is:\n {} \n'.format(city.title(), month.title(), df['Birth Year'].min()))
            print('Most recent year of birth in {} for the month {} for all days of the week is:\n {} \n'.format(city.title(), month.title(), df['Birth Year'].max()))
            print('Most common year of birth in {} for the month {} for all days of the week is:\n {} \n'.format(city.title(), month.title(), df['Birth Year'].mode()[0]))
        else:
            print('Earliest year of birth in {} is:\n {} \n'.format(city.title(), df['Birth Year'].min()))
            print('Most recent year of birth in {} is:\n {} \n'.format(city.title(), df['Birth Year'].max())) 
            print('Most common year of birth in {} is:\n {} \n'.format(city.title(), df['Birth Year'].mode()[0]))
    else:
        print('This data does not contain year of birth year details\n')      

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)



def force_end_program():
    while True:
        break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        #call all the functions needed to carry out the tasks one by one
        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)
        print(statistics_overview(df))

        #ask user if they want to restart program or leave
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
