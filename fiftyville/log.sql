-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Step 1: Find crime details on July 28, 2023, at Humphrey Street.
SELECT *
FROM crime_scene_reports
WHERE year = 2023 AND month = 7 AND day = 28
AND street = 'Humphrey Street';

-- Step 2: Look for witness statements related to the crime.
SELECT *
FROM interviews
WHERE year = 2023 AND month = 7 AND day = 28;

-- Step 3: Check financial transactions on the day of the crime.
SELECT *
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28;

-- Step 4: Look for flights on July 28, 2023, to see if anyone left the city.
SELECT *
FROM flights
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute;

-- Step 5: Find passengers who traveled on those flights.
SELECT *
FROM passengers
JOIN people ON passengers.passport_number = people.passport_number
WHERE flight_id IN (
    SELECT id FROM flights
    WHERE year = 2023 AND month = 7 AND day = 28
);

-- Step 6: Check security logs from the bakery for suspicious activity.
SELECT *
FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28
ORDER BY hour, minute;

-- Step 7: Check phone calls made on the day of the crime to identify accomplices.
SELECT *
FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28;

