import uuid

# User class
class User():
    def __init__(self, first_name, last_name, email, config=None, id="", verified=False, running=False):
        # Main initializer
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.config = self._initialize_config(config)  # Initialize config with default values or an empty dictionary
        self.id = uuid.uuid4().hex if not id else id
        self.verified = verified
        self.running = running

    @classmethod
    def make_from_dict(cls, d):
        # Initialize User object from a dictionary
        return cls(d['first_name'], d['last_name'], d['email'], d.get('config', {}), d['id'], d['verified'],  d['running'])

    def dict(self):
        # Return dictionary representation of the object
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "config": self.config,
            "verified": self.verified,
            "running": self.running
        }

    def display_name(self):
        # Return concatenation of name components
        return self.first_name + " " + self.last_name

    def get_config(self):
        # Return user's config
        return self.config

    def update_config(self, new_config):
        # Update user's config with new values
        self.config.update(new_config)

    def _initialize_config(self, config):
        # Initialize config with default values or an empty dictionary
        default_config = {
            "minimum_savings_threshold": 30,
            "cleanup_days_threshold": 5,
            "maximum_posts_per_session": 0,
            "delay_between_posts": 0,
            "delay_between_sessions": 0,
            "recently_updated_hour_threshold": 5,
            "special_message_threshold": 0,
            "random_image_toggle": True,
            "associate_tag": "",
            "start_time": "",
            "end_time": "",
            "fb_group_link": "",
            "fb_page_id": "",
            "access_token": "",
            "logins": [{"email": "", "password": ""}, {"email": "", "password": ""}, {"email": "", "password": ""}],
        }
        return default_config if config is None else config

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


# Anonymous user class
class Anonymous():

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None
