# HoTSocLOB

TODO:
- [x] DB Contains 2 tables --> Users, Orders, PriceHistory
- Order Book Implementation
    - [x] How to store data over the next 5 days? (Solved: Django + Postgresql)
    - [x] Basic price time priority structure/matching
- QnA
    - [] Question and Answer csv (120 questions) (Timer + Display functionality)
    - [] UI
- Interface (Chart + orderbook)
    - Chart implementation (Requires orderbook to be finished first)
        - [x] Backend functions
        - [] GUI
    - [] Adding Orders GUI (requires interface)
- Username/Account implementation
    - [] Backend functions
    - [] Initial page GUI
- Liquidity Provider Implementation
    - [] Maths functions
    - [] Make LP run in background with every other user
- Userstats
    - [x] Backend
    - [] Unrealized PnL display (would require keeping track of orders)
    - [] Realized PnL display (current_equity - 1000)
    - [] Scrollable pending orders display
