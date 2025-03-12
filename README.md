# HoTSocLOB
Commands to run (on separate terminals):
python -m celery -A core beat -l info
python -m celery -A core worker -l info -P eventlet 
python manage.py runserver

TODO:
- [x] DB Contains 2 tables --> Users, Orders, PriceHistory
- Order Book Implementation
    - [x] How to store data over the next 5 days? (Solved: Django + Postgresql)
    - [x] Basic price time priority structure/matching
    - [x] Once their unrealized loss > equity, close all positions, set equity to 0 (i.e. can't trade)
    - [x] Display LOB
- QnA
    - [x] Question and Answer csv (31 questions) 
    - [x] UI Display
    - [] UI Timer?
- Interface (Chart + orderbook)
    - Chart implementation (Requires orderbook to be finished first)
        - [x] Backend functions
        - [x] GUI
    - [x] Adding Orders GUI (requires interface)
    - [x] Clear pending orders button
- Username/Account implementation
    - [x] Backend functions
    - [x] Initial page GUI
- Liquidity Provider Implementation
    - [] Maths functions
    - [] Make LP run in background with every other user
    - [] Make LP place limit orders based on distribution (poisson(discrete))
    - Conditions to consider:
        - [x] Orderbook imbalances (lots of asks vs few bids, lots of bids vs few asks)
        - [x] Big spread in the orderbook
        - [x] How to place orders when the market is volatile vs non volatile.
        - [] Avandella Stoikov (Do this if we have extra time)
    - Functions:
        - [x] Market conditions fetch
            - [x] Volatility fetch
        - [x] Inventory/Positions fetch
        - [x] Pending orders fetch
        - [x] Bid quote generator (I.e. Poisson parameter generator, (Poisson RV + 1 or 2))
        - [x] Ask quote generator (I.e. Poisson parameter generator, (Poisson RV + 1 or 2))
        - [x] Unique poisson parameter for both the bids and asks generated
        - [x] Based on volatility, we adjust the constant we add to the poisson RV (to increase/decrease spread) (Keep it the same for both the bid and ask generator)
        - [x] We adjust the poisson parameter based off of orderbook imbalance. E.g. increase the parameter for the bids if there is a likely short
        - [] Clear quotes
        - [] Edit quotes as conditions change
- Userstats
    - [x] Backend
    - [x] Unrealized PnL display (would require keeping track of orders)
    - [x] Realized PnL display (current_equity - 1000)
    - [x] Scrollable pending orders display
- [] Make sure GCP runs a unique instance on every device