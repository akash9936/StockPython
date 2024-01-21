import streamlit as st
from datetime import datetime
import pymongo
import pandas as pd

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://akash9936:Tree9936@cluster0.f1wthph.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection = db.nse50

def main():
    st.write()
    st.title("Trying to get insider candle, dekh le ab kya karna h:")

    # Add "from" date and time input fields
    from_date = st.date_input("From Date")
    from_time = st.time_input("From Time")

    # Add "to" date and time input fields
    to_date = st.date_input("To Date")
    to_time = st.time_input("To Time")

    # Add a button to trigger data analysis
    analyze_button = st.button("Analyze Data")

    # Display HTML content
    st.markdown("""
        <div id="data-container"></div>
        <div id="record-sizes"></div>
        <footer>
            <p>&copy; 2023 Shubham Singh. All rights reserved.</p>
        </footer>
    """, unsafe_allow_html=True)

    if analyze_button:
        # Call a function to analyze data and update the HTML content
        analyze_data(from_date, from_time, to_date, to_time)

def highlight_buy_signal(s):
    return ['background-color: lightgreen' if v else '' for v in s]

def analyze_data(from_date, from_time, to_date, to_time):
    try:
        format_str = '%d-%b-%Y %H:%M:%S'
        from_datetime = datetime.combine(from_date, from_time)
        to_datetime = datetime.combine(to_date, to_time)

        total_data = 30
        slice_data = total_data // 2

        half_time = (from_datetime + (to_datetime - from_datetime) // 2).strftime(format_str)

        last_records_cursor = collection.find({
            'timestamp': {'$gte': half_time, '$lt': to_datetime.strftime(format_str)}
        }).sort('_id', pymongo.DESCENDING).limit(slice_data)
        last_records = list(last_records_cursor)

        if not last_records:
            st.error('Error: No data found in lastRecords MongoDB.')
        else:
            print("last_records found")

        previous_records_cursor = collection.find({
            'timestamp': {'$gte': from_datetime.strftime(format_str), '$lt': half_time}
        }).sort('_id', pymongo.DESCENDING).limit(slice_data)

        previous_records = list(previous_records_cursor)

        if not previous_records:
            st.error('Error: No data found in lastRecords MongoDB.')
        else:
            print("Previous records found")

        symbols_last_prices_last = []
        symbols_last_prices_previous = []

        for entry in last_records:
            for stock in entry['data']:
                symbols_last_prices_last.append({
                    'symbol': stock['symbol'],
                    'lastPrice': stock['lastPrice'],
                    'timestamp': entry['timestamp'],
                })

        for entry in previous_records:
            for stock in entry['data']:
                symbols_last_prices_previous.append({
                    'symbol': stock['symbol'],
                    'lastPrice': stock['lastPrice'],
                    'timestamp': entry['timestamp'],
                })

        symbols_data = pd.DataFrame(symbols_last_prices_last).groupby('symbol').agg({
            'lastPrice': ['max', 'min', 'first', 'last'],
            'timestamp': ['first', 'last']
        }).reset_index()

        symbols_data.columns = ['symbol', 'max_last_price_last', 'min_last_price_last',
                                'first_last_price_last', 'last_last_price_last',
                                'first_timestamp_last', 'last_timestamp_last']

        symbols_data_previous = pd.DataFrame(symbols_last_prices_previous).groupby('symbol').agg({
            'lastPrice': ['max', 'min', 'first', 'last'],
            'timestamp': ['first', 'last']
        }).reset_index()

        symbols_data_previous.columns = ['symbol', 'max_last_price_previous', 'min_last_price_previous',
                                         'first_last_price_previous', 'last_last_price_previous',
                                         'first_timestamp_previous', 'last_timestamp_previous']

        symbols_data = pd.merge(symbols_data, symbols_data_previous, on='symbol', how='inner')

        symbols_data['buy_signal'] = (symbols_data['min_last_price_last'] > symbols_data['min_last_price_previous']) & \
                                    (symbols_data['max_last_price_last'] < symbols_data['max_last_price_previous'])

        symbols_data = symbols_data.sort_values(by='buy_signal', ascending=False)

        st.dataframe(symbols_data.style.apply(highlight_buy_signal, subset=['buy_signal']))

        st.success("Data analysis successful!")
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    main()
