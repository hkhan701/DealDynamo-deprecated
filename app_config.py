# Config class
class AppConfig():

    # Main initializer
    def __init__(self, minimum_savings_threshold,
                 cleanup_days_threshold, maximum_posts_per_session, delay_between_posts, delay_between_sessions,
                 recently_updated_hour_threshold, special_message_threshold, random_browser_toggle,
                 random_image_toggle, associate_tag, start_time, end_time, fb_group_link, fb_page_id, logins,
                 access_token):
        self.minimum_savings_threshold = minimum_savings_threshold
        self.cleanup_days_threshold = cleanup_days_threshold
        self.maximum_posts_per_session = maximum_posts_per_session
        self.delay_between_posts = delay_between_posts
        self.delay_between_sessions = delay_between_sessions
        self.recently_updated_hour_threshold = recently_updated_hour_threshold
        self.special_message_threshold = special_message_threshold
        self.random_browser_toggle = random_browser_toggle
        self.random_image_toggle = random_image_toggle
        self.associate_tag = associate_tag
        self.start_time = start_time
        self.end_time = end_time
        self.fb_group_link = fb_group_link
        self.fb_page_id = fb_page_id
        self.logins = logins
        self.access_token = access_token

    # Return dictionary representation of object
    def dict(self):
        return {
            "MINIMUM_SAVINGS_THRESHOLD": self.minimum_savings_threshold,
            "CLEANUP_DAYS_THRESHOLD": self.cleanup_days_threshold,
            "MAXIMUM_POSTS_PER_SESSION": self.maximum_posts_per_session,
            "DELAY_BETWEEN_POSTS": self.delay_between_posts,
            "DELAY_BETWEEN_SESSIONS": self.delay_between_sessions,
            "RECENTLY_UPDATED_HOUR_THRESHOLD": self.recently_updated_hour_threshold,
            "SPECIAL_MESSAGE_THRESHOLD": self.special_message_threshold,
            "RANDOM_BROWSER_TOGGLE": self.random_browser_toggle,
            "RANDOM_IMAGE_TOGGLE": self.random_image_toggle,
            "ASSOCIATE_TAG": self.associate_tag,
            "START_TIME": self.start_time,
            "END_TIME": self.end_time,
            "FB_GROUP_LINK": self.fb_group_link,
            "FB_PAGE_ID": self.fb_page_id,
            "LOGINS": self.logins,
            "ACCESS_TOKEN": self.access_token
        }