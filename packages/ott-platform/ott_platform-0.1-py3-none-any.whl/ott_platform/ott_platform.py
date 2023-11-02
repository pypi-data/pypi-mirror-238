# User class for modeling a user on an OTT platform
class User:

    def __init__(self, user_id, name):
        # Initialize user attributes
        self.user_id = user_id
        self.name = name
        self.subscription_plan = None # Initially, no subscription plan
        self.watched_content = [] # Initialize an empty list for watched content
        print(f'Welcome to Sflix {self.name}!')

    def subscribe(self, plan_name):

        # Method to subscribe to a plan
        if self.subscription_plan is not None:
            # If the user already has a subscription, raise an error
            raise AlreadySubscribedError(f'Already subscribed to {self.subscription_plan}')
        
        self.subscription_plan = plan_name # Set the subscription plan
        return f'Subscribed to {plan_name}' # Return a confirmation message

    def watch(self, content_name):

        # Method to watch content
        if self.subscription_plan is None:
            # Check if the user has a subscription plan
            return "You don't have access to this content" # Return an error message
        
        else:
            self.watched_content.append(content_name) # Add content to the watched list
            return f"Watching {content_name}" # Return a confirmation message

    def get_watch_history(self):
        # Method to get the user's watch history
        return self.watched_content # Return the list of watched content
    
# Custom exception class for handling subscription error
class AlreadySubscribedError(Exception):
    pass

#suryajeet = User(user_id = 1, name="Suryajeet Bhosale")
#suryajeet.subscribe('Premium')
#suryajeet.watch('Bojack Horseman')