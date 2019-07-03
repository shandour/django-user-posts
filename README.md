A simple Django app, using JWT for authentication. Exposes 2 models: User and Post.
Minimally, the app backend would require the following envvars for the app to function as expected: DATABASE_URL, SECRET_KEY, CLEARBIT_API_KEY, EMAIL_HUNTER_API_KEY.
Exposes a custom create_fixtures_from_config command which takes a --path argument (the path to the config file) and creates fixtures based on the 3 required values: 'user_number', 'max_posts_per_user' and 'max_reactions_per_user'. Expects a JSON file.
