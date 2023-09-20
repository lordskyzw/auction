# Django Auction App

## Overview
This Django web application simulates an eBay-like auction site where users can create auctions, bid on items, and manage their listings.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and registration.
- Create, edit, and manage auctions.
- Place bids on auctions.
- Search for auctions based on various criteria.
- Real-time updates on auction status.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/laminjawla1/auction
    ```

2. Navigate to the project directory:

    ```bash
    cd auction
    ```

3. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

4. Create and apply database migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser to access the Django admin:

    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the application at [http://localhost:8000](http://localhost:8000).

## Usage

1. Register a new account or log in using an existing one.
2. Create auctions for items you want to sell.
3. Browse and bid on auctions listed by other users.
4. View your dashboard to monitor your auctions and bids.
5. Manage your auctions by editing or deleting them.

## Database Schema

The application uses the following Django models to define the database schema:

- `User`: Represents a registered user.
- `AuctionListing`: Represents an auction listing with details such as title, description, starting bid, etc.
- `Bid`: Represents a bid placed on an auction.
- `Comment`: Represents comments made on an auction listing.
- `WatchList`: Represents listings on you watch list.

For a more detailed view of the database schema, refer to the models in the `auctions/models.py` file.

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest new features.

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature
    ```
3. Make your changes and commit them:
    ```bash
    git add .
    git commit -m "Add your feature or fix"
    ```
4. Push to your fork and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).