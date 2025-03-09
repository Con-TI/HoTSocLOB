# HoTSocLOB

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
        - [] Orderbook imbalances (lots of asks vs few bids, lots of bids vs few asks)
        - [] Big spread in the orderbook
        - [] How to place orders when the market is volatile vs non volatile.
        - [] Avandella Stoikov (Do this if we have extra time)
    - Functions:
        - [] Market conditions fetch
            - [] Volatility fetch
        - [x] Inventory/Positions fetch
        - [x] Pending orders fetch
        - [] Bid quote generator (I.e. Poisson parameter generator, (Poisson RV + 1 or 2))
        - [] Ask quote generator (I.e. Poisson parameter generator, (Poisson RV + 1 or 2))
        - Generator details:
            - Unique poisson parameter for both the bids and asks generated
            - Based on volatility, we adjust the constant we add to the poisson RV (to increase/decrease spread) (Keep it the same for both the bid and ask generator)
            - We adjust the poisson parameter based off of orderbook imbalance. E.g. increase the parameter for the bids if there is a likely short
        - [] Clear quotes/edits quotes as conditions change
- Userstats
    - [x] Backend
    - [x] Unrealized PnL display (would require keeping track of orders)
    - [x] Realized PnL display (current_equity - 1000)
    - [x] Scrollable pending orders display
- [] Make sure GCP runs a unique instance on every device