import sqlite3

db_file = 'airline.db'

def create_database():

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Destinations (
                       DestinationID INTEGER PRIMARY KEY AUTOINCREMENT,
                       City TEXT,
                       Country TEXT,
                       AirportCode TEXT
                       )
        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Pilots (
                        PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT,
                        LastName TEXT,
                        LicenseNumber TEXT UNIQUE,
                        ContactNumber TEXT 
                        )
                       ''') # Contact# is a String due to leading zeros being lost when stored as integer, formatting characters e.g - # or +

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Aircrafts (
                       AircraftID INTEGER PRIMARY KEY AUTOINCREMENT,
                       Model TEXT,
                       Manufacturer TEXT,
                       Capacity INTEGER,
                       RegistrationNumber TEXT UNIQUE,
                       LastMaintenanceDate DATE
                       )
                       ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Flights (
                        FlightNumber TEXT PRIMARY KEY,
                        DepartureDateTime DATETIME,
                        ArrivalDateTime DATETIME,
                        Status TEXT,
                        DestinationID INTEGER,
                        PilotID INTEGER,
                        AircraftID INTEGER,
                        FOREIGN KEY (DestinationID) REFERENCES Destinations(DestinationID),
                        FOREIGN KEY (PilotID) REFERENCES Pilots(PilotID),
                        FOREIGN KEY (AircraftID) REFERENCES Aircrafts(AircraftID)                   
                       )
                       ''')

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Passengers (
                       PassengerID INTEGER PRIMARY KEY AUTOINCREMENT,
                       FirstName TEXT,
                       LastName TEXT,
                       DateOfBirth DATE,
                       PassportNumber TEXT UNIQUE,
                       ContactNumber TEXT,
                       Email TEXT,
                       Nationality TEXT
                       )
                       ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Bookings (
                       BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
                       PassengerID INTEGER,
                       FlightNumber TEXT,
                       BookingDate DATE,
                       SeatNumber TEXT,
                       Class TEXT,
                       BookingStatus TEXT,
                       FOREIGN KEY (PassengerID) REFERENCES Passengers(PassengerID),
                       FOREIGN KEY (FlightNumber) REFERENCES Flights(FlightNumber)
                       )
                       ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Baggage (
                       BaggageID INTEGER PRIMARY KEY AUTOINCREMENT,
                       BookingID INTEGER,
                       Weight REAL,
                       TagNumber TEXT UNIQUE,
                       Description TEXT,
                       FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID)
                       )
                       ''')
        
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS FlightStatusLog (
                       LogID INTEGER PRIMARY KEY AUTOINCREMENT,
                       FlightNumber TEXT,
                       Status TEXT,
                       Timestamp TEXT,
                       Reason TEXT,
                       FOREIGN KEY (FlightNumber) REFERENCES Flights(FlightNumber)
                       )
                       ''')        

        conn.commit()
        print("Database and Tables Created Successfully")

    except sqlite3.Error as e:
        print("An error occured: {e}")

    finally:
        if conn:
            conn.close()

def populate_data():

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
                      INSERT INTO Destinations (City, Country, AirportCode) VALUES
                       ('New York','USA','JFK'),
                       ('London','UK','LHR'),
                       ('Tokyo', 'Japan', 'HND'),
                       ('Paris', 'France', 'CDG'),
                       ('Sydney', 'Australia', 'SYD'),
                       ('Moscow', 'Russia', 'SVO'),
                       ('Rome', 'Italy', 'FCO'),
                       ('Madrid', 'Spain', 'MAD'),
                       ('Seoul', 'South Korea', 'ICN'),
                       ('Bangkok', 'Thailand', 'BKK')
                       ''')
        
        cursor.execute('''
                      INSERT INTO Pilots (FirstName, LastName, LicenseNumber, ContactNumber) VALUES
                      ('John', 'Doe', '12345', '555-1234'),
                      ('Jane', 'Smith', '67890', '555-5678'),
                      ('Alice', 'Johnson', '13579', '555-9012'),
                      ('Michael', 'Jackson', '24680', '555-3456'),
                      ('Emily', 'Davis', '98765', '555-7890'),
                      ('David', 'Wilson', '54321', '555-2345'),
                      ('Sarah', 'Garcia', '11223', '555-6789'),
                      ('Robert', 'Rodriguez', '44556', '555-0123'),
                      ('Linda', 'Martinez', '77889', '555-4567'),
                      ('Christopher', 'Anderson', '99001', '555-8901')  
                       ''')

        cursor.execute('''
                      INSERT INTO Aircrafts (Model, Manufacturer, Capacity, RegistrationNumber, LastMaintenanceDate) VALUES
                      ('737', 'Boeing', 180, 'N737AA', '2024-10-26'),
                      ('A320', 'Airbus', 150, 'A320BB', '2024-11-01'),
                      ('777', 'Boeing', 350, 'N777CC', '2024-10-15'),
                      ('A330', 'Airbus', 300, 'A330DD', '2024-11-10'),
                      ('787', 'Boeing', 250, 'N787EE', '2024-10-20'),
                      ('A350', 'Airbus', 320, 'A350FF', '2024-11-05'),
                      ('190', 'Embraer', 100, 'E190GG', '2024-10-30'),
                      ('767', 'Boeing', 280, 'N767II', '2024-10-22'),
                      ('A321', 'Airbus', 200, 'A321JJ', '2024-11-08'),
                      ('747', 'Boeing', 400, 'N747KK', '2024-10-18')   
                       ''')

        cursor.execute('''
                       INSERT INTO Flights (FlightNumber, DepartureDateTime, ArrivalDateTime, Status, DestinationID, PilotID, AircraftID) VALUES
                       ('FL101', '2024-12-01 08:00:00', '2024-12-01 12:00:00', 'Scheduled', 1, 1, 1),
                       ('FL102', '2024-12-02 14:00:00', '2024-12-02 18:00:00', 'Departed', 2, 2, 2),
                       ('FL103', '2024-12-03 09:30:00', '2024-12-03 13:30:00', 'Arrived', 3, 3, 3),
                       ('FL104', '2024-12-04 15:15:00', '2024-12-04 19:15:00', 'Scheduled', 4, 4, 3),
                       ('FL105', '2024-12-05 11:00:00', '2024-12-05 15:00:00', 'Cancelled', 5, 5, 3),
                       ('FL106', '2024-12-06 16:45:00', '2024-12-06 20:45:00', 'Departed', 1, 6, 6),
                       ('FL107', '2024-12-07 10:30:00', '2024-12-07 14:30:00', 'Arrived', 2, 7, 6),
                       ('FL108', '2024-12-08 17:00:00', '2024-12-08 21:00:00', 'Scheduled', 3, 8, 8),
                       ('FL109', '2024-12-09 12:15:00', '2024-12-09 16:15:00', 'Cancelled', 4, 9, 9),
                       ('FL110', '2024-12-10 18:30:00', '2024-12-10 22:30:00', 'Departed', 5, 10, 10)
                       ''')

        cursor.execute('''
                       INSERT INTO Passengers (FirstName, LastName, DateOfBirth, PassportNumber, ContactNumber, Email, Nationality) VALUES
                       ('Alice', 'Smith', '1990-05-15', 'PA123456', '555-1111', 'alice.smith@gmail.com', 'USA'),
                       ('Bob', 'Johnson', '1985-10-20', 'PB789012', '555-2222', 'bob.johnson@gmail.com', 'Canada'),
                       ('Carol', 'Williams', '1992-03-08', 'PC345678', '555-3333', 'carol.williams@gmail.com', 'UK'),
                       ('David', 'Brown', '1988-12-01', 'PD901234', '555-4444', 'david.brown@gmail.com', 'Australia'),
                       ('Eve', 'Jones', '1995-07-25', 'PE567890', '555-5555', 'eve.jones@gmail.com', 'Japan'),
                       ('Frank', 'Miller', '1983-09-10', 'PF123789', '555-6666', 'frank.miller@gmail.com', 'France'),
                       ('Grace', 'Davis', '1998-02-18', 'PG456012', '555-7777', 'grace.davis@gmail.com', 'Russia'),
                       ('Henry', 'Garcia', '1987-06-03', 'PH789345', '555-8888', 'henry.garcia@gmail.com', 'Italy'),
                       ('Ivy', 'Rodriguez', '1991-11-28', 'PI012678', '555-9999', 'ivy.rodriguez@gmail.com', 'Spain'),
                       ('Jack', 'Martinez', '1989-04-12', 'PJ345901', '555-0000', 'jack.martinez@gmail.com', 'South Korea')
                       ''')
        
        cursor.execute('''
                       INSERT INTO Bookings (PassengerID, FlightNumber, BookingDate, SeatNumber, Class, BookingStatus) VALUES
                       (1, 'FL101', '2024-11-20', '1A', 'Business', 'Confirmed'),
                       (2, 'FL102', '2024-11-21', '5B', 'Economy', 'Confirmed'),
                       (3, 'FL103', '2024-11-22', '10C', 'Economy', 'Pending'),
                       (4, 'FL104', '2024-11-23', '2D', 'Business', 'Confirmed'),
                       (5, 'FL105', '2024-11-24', '15E', 'Economy', 'Cancelled'),
                       (6, 'FL106', '2024-11-25', '3A', 'Business', 'Confirmed'),
                       (7, 'FL107', '2024-11-26', '8B', 'Economy', 'Confirmed'),
                       (8, 'FL108', '2024-11-27', '12C', 'Economy', 'Pending'),
                       (9, 'FL109', '2024-11-28', '4D', 'Business', 'Cancelled'),
                       (10, 'FL110', '2024-11-29', '18E', 'Economy', 'Confirmed')
                       ''')

        cursor.execute('''
                       INSERT INTO Baggage (BookingID, Weight, TagNumber, Description) VALUES
                       (1, 25.5, 'BG1001', 'Large suitcase'),
                       (2, 15.0, 'BG1002', 'Carry-on bag'),
                       (3, 30.2, 'BG1003', 'Oversized luggage'),
                       (4, 20.8, 'BG1004', 'Medium suitcase'),
                       (5, 10.5, 'BG1005', 'Small bag'),
                       (6, 22.3, 'BG1006', 'Suitcase with documents'),
                       (7, 18.7, 'BG1007', 'Sports equipment'),
                       (8, 28.1, 'BG1008', 'Heavy luggage'),
                       (9, 12.9, 'BG1009', 'Personal items'),
                       (10, 26.4, 'BG1010', 'Travel bag')
                       ''')

        cursor.execute('''
                       INSERT INTO FlightStatusLog (FlightNumber, Status, Timestamp, Reason) VALUES
                       ('FL101', 'Scheduled', '2024-12-01 08:00:00', 'Flight scheduled'),
                       ('FL101', 'Departed', '2024-12-01 12:00:00', 'Flight departed on time'),
                       ('FL102', 'Scheduled', '2024-12-02 14:00:00', 'Flight scheduled'),
                       ('FL102', 'Departed', '2024-12-02 18:00:00', 'Flight departed on time'),
                       ('FL103', 'Scheduled', '2024-12-03 09:30:00', 'Flight scheduled'),
                       ('FL103', 'Arrived', '2024-12-03 13:30:00', 'Flight arrived on time'),
                       ('FL104', 'Scheduled', '2024-12-04 15:15:00', 'Flight scheduled'),
                       ('FL104', 'Scheduled', '2024-12-04 19:15:00', 'Flight scheduled'),
                       ('FL105', 'Scheduled', '2024-12-05 11:00:00', 'Flight scheduled'),
                       ('FL105', 'Cancelled', '2024-12-05 15:00:00', 'Adverse weather conditions')
                       ''')

        conn.commit()
        print("Data Populated Successfully")

    except sqlite3.Error as e:
        print("An error occured: {e}")

    finally:
        if conn:
            conn.close()


def display_menu():
    print("\nAirline Database - Welcome!")
    print("1. Add a New Flight")
    print("2. View Flights by Criteria")
    print("3. Update Flight Information")
    print("4. Assign Pilot to Flight")
    print("5. View Pilot Schedule")
    print("6. View/Update Destination Information")
    print("7. Exit Program")
    print("8. Bonus - Stats Mode")

def get_user_input():
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 8:
                return choice
            
        except ValueError:
            print("Invalid Input. Please enter a number from the list.")


def add_new_flight():
    print("Adding New Flight - Please Enter Details below:\n")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Prompt the user for flight details
        flight_number = input("Enter Flight Number: ")
        departure_datetime = input("Enter Departure DateTime (YYYY-MM-DD HH:MM:SS): ")
        arrival_datetime = input("Enter Arrival DateTime (YYYY-MM-DD HH:MM:SS): ")
        status = input("Enter Status: ")
        destination_id = input("Enter Destination ID: ")
        pilot_id = input("Enter Pilot ID: ")
        aircraft_id = input("Enter Aircraft ID: ")

        sql = '''
              INSERT INTO Flights (FlightNumber, DepartureDateTime, ArrivalDateTime, Status, DestinationID, PilotID, AircraftID) 
              VALUES (?,?,?,?,?,?,?)
              '''
        cursor.execute(sql, (flight_number, departure_datetime, arrival_datetime, status, destination_id, pilot_id, aircraft_id))

        conn.commit()
        print("Flight Added Successfully!")


    except sqlite3.Error as e:
        print("An error occured: {e}")

    finally:
        if conn:
            conn.close()


def query_flights():
    print("Querying Flights")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        sql = "SELECT * FROM Flights WHERE 1=1"
        params = []  # Initialize an empty list to store parameters

        destinationID = input("Please enter a Destination ID (leave blank if not required): ")
        if destinationID.strip():
            sql += " AND DestinationID = ?"
            params.append(destinationID)

        status = input("Please enter a Status (leave blank if not required): ")
        if status.strip():
            sql += " AND Status = ?"
            params.append(status)

        departuredatetime = input("Enter Departure Date/Time (YYYY-MM-DD HH:) (or leave blank): ")
        if departuredatetime.strip():
            sql += " AND DepartureDateTime = ?"
            params.append(departuredatetime)

        cursor.execute(sql, tuple(params))  # Pass parameters as a tuple
        flights = cursor.fetchall()

        if flights:
            print("\nRetrieved Flights:")
            print("Flight Number | Departure Date/Time | Arrival Date/Time | Status | Destination ID | Pilot ID | Aircraft ID")
            print("-" * 130)  # Separator line

            for flight in flights:
                print(f"{flight[0]:<13} | {flight[1]:<20} | {flight[2]:<20} | {flight[3]:<8} | {flight[4]:<14} | {flight[5]:<8} | {flight[6]:<11}")
        
        else:
            print("No Flights found Matching the criteria.")

    except sqlite3.Error as e:
        print("An error occured: {e}")

    finally:
        if conn:
            conn.close()


def update_flight():
    print("Updating Flight")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        flight_number = input("Enter Flight Number to update: ")
        cursor.execute("SELECT * FROM Flights WHERE FlightNumber = ?", (flight_number,))
        flight = cursor.fetchone()

        if flight:
            print("\nCurrent Flight Details:")
            print("Flight Number:", flight[0])
            print("Departure Time:", flight[1])
            print("Arrival Time:", flight[2])
            print("Status:", flight[3])

            # Prompt for fields to update
            new_departure_time = input("Enter new Departure Time (YYYY-MM-DD HH:MM:SS, or leave blank): ")
            new_arrival_time = input("Enter new Arrival Time (YYYY-MM-DD HH:MM:SS, or leave blank): ")
            new_status = input("Enter new Status (or leave blank): ")

            # Construct the UPDATE query
            sql = "UPDATE Flights SET"
            params = []

            if new_departure_time:
                sql += " DepartureDateTime = ?,"
                params.append(new_departure_time)

            if new_arrival_time:
                sql += " ArrivalDateTime = ?,"
                params.append(new_arrival_time)

            if new_status:
                sql += " Status = ?,"
                params.append(new_status)

            # Remove trailing comma from SQL query
            sql = sql.rstrip(',')

            if params:  # Only execute update if there are changes
                sql += " WHERE FlightNumber = ?"
                params.append(flight_number)

                cursor.execute(sql, tuple(params))
                conn.commit()
                print("Flight schedule updated successfully.")
            else:
                print("No changes made.")

    except sqlite3.Error as e:
        print("An error occured: {e}")

    finally:
        if conn:
            conn.close()


def assign_pilot():
    print("Assign Pilot to Flight")
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        flight_number = input("Enter the Flight Number to assign a pilot to: ")

        # Check if the flight exists
        cursor.execute("SELECT * FROM Flights WHERE FlightNumber = ?", (flight_number,))
        flight = cursor.fetchone()

        if flight:
            print("\nCurrent Flight Details:")
            print("Flight Number:", flight[0])
            print("Departure Time:", flight[1])
            print("Arrival Time:", flight[2])
            print("Current Pilot ID:", flight[5] if flight[5] else "Not assigned") # Index 5 is PilotID

            # Display available pilots
            cursor.execute("SELECT PilotID, FirstName, LastName FROM Pilots")
            pilots = cursor.fetchall()

            if pilots:
                print("\nAvailable Pilots:")
                for pilot in pilots:
                    print(f"{pilot[0]}: {pilot[1]} {pilot[2]}")

                pilot_id_to_assign = input("Enter the Pilot ID to assign to this flight")

                    # Check if the entered Pilot ID exists
                cursor.execute("SELECT PilotID FROM Pilots WHERE PilotID = ?", (pilot_id_to_assign,))
                existing_pilot = cursor.fetchone()

                if existing_pilot:
                    update_sql = "UPDATE Flights SET PilotID = ? WHERE FlightNumber = ?"
                    cursor.execute(update_sql, (pilot_id_to_assign, flight_number))
                    conn.commit()
                    print(f"Pilot {pilot_id_to_assign} assigned to Flight {flight_number} successfully.")
                
                else:
                    print("Invalid Pilot ID. No changes made.")

            else:
                print("No pilots available to assign.")

        else:
            print(f"Flight {flight_number} not found.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


def view_pilot_schedule():
    print("Viewing Pilot Schedule")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        pilot_id = input("Enter the Pilot ID to view the schedule for: ")

        # Check if the Pilot ID exists
        cursor.execute("SELECT PilotID, FirstName, LastName FROM Pilots WHERE PilotID = ?", (pilot_id,))
        pilot = cursor.fetchone()

        if pilot:
            print(f"\nSchedule for Pilot: {pilot[1]} {pilot[2]} (ID: {pilot[0]})")
            print("-" * 60)

            # Retrieve flights for the given Pilot ID
            cursor.execute("""
                SELECT FlightNumber, DepartureDateTime, ArrivalDateTime, Status,
                    (SELECT City FROM Destinations WHERE DestinationID = Flights.DestinationID) AS DestinationCity
                FROM Flights
                WHERE PilotID = ?
                           """, (pilot_id,))
            
            flights = cursor.fetchall()

            if flights:
                print("Flight Number | Departure Date/Time    | Arrival Date/Time    | Status      | Destination")
                print("-" * 100)
                for flight in flights:
                    print(f"{flight[0]:<13} | {flight[1]:<23} | {flight[2]:<23} | {flight[3]:<12} | {flight[4]}")
            else:
                print("No flights scheduled for this pilot.")

        else:
            print(f"Pilot with ID {pilot_id} not found.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()


def update_destination_info():
    print("Updating Destination Information")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        destination_id_to_update = input("Enter the Destination ID to update: ")

        # Check if the destination exists
        cursor.execute("SELECT * FROM Destinations WHERE DestinationID = ?", (destination_id_to_update,))
        destination = cursor.fetchone()

        if destination:
            print("\nCurrent Destination Information:")
            print("Destination ID:", destination[0])
            print("City:", destination[1])
            print("Country:", destination[2])
            print("Airport Code:", destination[3])

            new_city = input("Enter new City (leave blank to keep current): ")
            new_country = input("Enter new Country (leave blank to keep current): ")
            new_airport_code = input("Enter new Airport Code (leave blank to keep current): ")

            sql = "UPDATE Destinations SET"
            params = []

            if new_city:
                sql += " City = ?,"
                params.append(new_city)

            if new_country:
                sql += " Country = ?,"
                params.append(new_country)

            if new_airport_code:
                sql += " AirportCode = ?,"
                params.append(new_airport_code)

            # Remove trailing comma if any updates were added
            sql = sql.rstrip(',')

            if params:
                sql += " WHERE DestinationID = ?"
                params.append(destination_id_to_update)

                cursor.execute(sql, tuple(params))
                conn.commit()
                print("Destination information updated successfully.")
            else:
                print("No destination information updated.")

        else:
            print(f"Destination with ID {destination_id_to_update} not found.")

    except sqlite3.Error as e:
        print("An error occurred: {e}")

    finally:
        if conn:
            conn.close()


def statistic_mode():
    try:
        conn = sqlite3.Connection(db_file)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                d.City,
                COUNT(f.FlightNumber) AS NumberOfFlights
            FROM
                Destinations d
            JOIN
                Flights f ON d.DestinationID = f.DestinationID
            GROUP BY
                d.City
            ORDER BY
                NumberOfFlights DESC;
                      """)

        results_destination = cursor.fetchall()

        if results_destination:
            print("\nNumber of Flights to Each Destination:")
            print("{:<15} | {}".format("Destination", "Flight Count"))
            print("-" * 30)
            for row in results_destination:
                print("{:<15} | {}".format(row[0], row[1]))
        else:
            print("No flights found in the database.")


        cursor.execute("""
            SELECT
                p.FirstName,
                p.LastName,
                COUNT(f.FlightNumber) AS NumberOfFlights
            FROM
                Pilots p
            LEFT JOIN
                Flights f ON p.PilotID = f.PilotID
            GROUP BY
                p.PilotID, p.FirstName, p.LastName
            ORDER BY
                NumberOfFlights DESC;
                      """)

        results_pilot = cursor.fetchall()

        if results_pilot:
            print("\nNumber of Flights Assigned to Each Pilot:")
            print("{:<10} | {:<10} | {}".format("First Name", "Last Name", "Flight Count"))
            print("-" * 35)
            for row in results_pilot:
                print("{:<10} | {:<10} | {}".format(row[0], row[1], row[2]))
        else:
            print("No pilots found in the database.")


        cursor.execute("""
            SELECT
                a.Model,
                a.Manufacturer,
                COUNT(f.AircraftID) AS UsageCount
            FROM
                Aircrafts a
            LEFT JOIN
                Flights f ON a.AircraftID = f.AircraftID
            GROUP BY
                a.AircraftID, a.Model, a.Manufacturer
            ORDER BY
                UsageCount DESC;
                       """)

        results_aircraft = cursor.fetchall()

        if results_aircraft:
            print("\nMost Used Aircraft:")
            print("{:<15} | {:<15} | {}".format("Model", "Manufacturer", "Usage Count"))
            print("-" * 45)
            for row in results_aircraft:
                print("{:<15} | {:<15} | {}".format(row[0], row[1], row[2]))
        else:
            print("No aircraft found in the database.")
       
    except sqlite3.Error as e:
        print("An error has occured: {e}")

    finally:
        if conn:
            conn.close()



def main():
    create_database()
    populate_data()

    while True:
        display_menu()
        choice = get_user_input()

        if choice == 1:
            add_new_flight()
        elif choice ==2:
            query_flights()
        elif choice ==3:
            update_flight()
        elif choice ==4:
            assign_pilot()
        elif choice ==5:
            view_pilot_schedule()
        elif choice ==6:
            update_destination_info()
        elif choice == 7:
            print("Exiting Program")
            break
        elif choice == 8:
            statistic_mode()


if __name__ == "__main__":
    main()



