# HoTSocLOB

TODO:
- [x] DB Contains 2 tables --> Users, Orders, PriceHistory
- Order Book Implementation
    - [x] How to store data over the next 5 days? (Solved: Django + Postgresql)
    - [x] Basic price time priority structure/matching
    - [x] Once their unrealized loss > equity, close all positions, set equity to 0 (i.e. can't trade)
- QnA
    - [x] Question and Answer csv (31 questions) 
    - [] UI (Timer + Display functionality)
- Interface (Chart + orderbook)
    - Chart implementation (Requires orderbook to be finished first)
        - [x] Backend functions
        - [x] GUI
    - [x] Adding Orders GUI (requires interface)
    - [] Clear pending orders button
- Username/Account implementation
    - [x] Backend functions
    - [x] Initial page GUI
- Liquidity Provider Implementation
    - [] Maths functions
    - [] Make LP run in background with every other user
- Userstats
    - [x] Backend
    - [x] Unrealized PnL display (would require keeping track of orders)
    - [x] Realized PnL display (current_equity - 1000)
    - [x] Scrollable pending orders display
- [] Make sure GCP runs a unique instance on every device