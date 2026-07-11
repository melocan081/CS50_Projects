-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Firstly, I wanted to know more about the theft using info I had at hand.
SELECT description FROM crime_scene_reports WHERE year = 2024 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Then I wanted to take a look at some interviews and tried to gather info from the witnesses.
SELECT transcript FROM interviews WHERE year = 2024 AND month = 7 AND day = 28;

-- I found some license plates,
SELECT license_plate FROM bakery_security_logs
WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';

--And some phone calls.
SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60;

-- And I checked the atm transactions.
SELECT account_number FROM atm_transactions
WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

--I checked the flights and found the exact flight using this query.
SELECT id, origin_airport_id, destination_airport_id FROM flights
WHERE year = 2024 AND month = 7 AND day = 29 ORDER BY hour ASC, minute ASC LIMIT 1;

-- Here, by combining all the queries I wrote, I found the thief.
SELECT name FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions
WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'))
AND license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit')
AND phone_number IN
(SELECT caller FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60)
AND passport_number IN
(SELECT passport_number FROM passengers WHERE flight_id = 36);


-- I wanted to gather knowledge about the thief to find the accomplice.
SELECT * FROM people WHERE name = 'Bruce';

--By checking calls, I found the accomplice's number.
SELECT receiver FROM phone_calls
WHERE caller = '(367) 555-5533' AND year = 2024 AND day = 28 AND month = 7 AND duration < 60;

-- And lastly with this query I found the accomplice. Job done!
SELECT name FROM people WHERE phone_number = '(375) 555-8161';
