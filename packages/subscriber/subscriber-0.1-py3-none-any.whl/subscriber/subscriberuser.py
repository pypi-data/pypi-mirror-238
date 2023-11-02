class AlreadySubscribedError(Exception):
    pass

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.subscription_plan = None
        self.watched_content = []
        
    def subscribe(self, plan_name):
        if self.subscription_plan == plan_name:
            raise AlreadySubscribedError(f'Already subscribed to {plan_name}')
        self.subscription_plan = plan_name
        return f'Subscribed to {plan_name}'
    
    def watch(self, content_name):
        if self.subscription_plan is None:
            return "You don't have an active subscription. Please subscribe to a plan to watch content."
        elif content_name in self.watched_content:
            return f'You have already watched {content_name}'
        else:
            self.watched_content.append(content_name)
            return f'Watching {content_name}'
    
    def get_watch_history(self):
        return self.watched_content

# Example usage:

# Creating a user instance
user1 = User(user_id=1, name='Alice')

# Subscribing to a plan
print(user1.subscribe('Premium'))

# Watching content
print(user1.watch('Movie A'))  # User has not subscribed yet, should return error message

# Subscribing to a plan
print(user1.subscribe('Basic'))

# Watching content
print(user1.watch('Movie A'))  # Watching Movie A

# Watching the same content again
print(user1.watch('Movie A'))  # You have already watched Movie A

# Getting watch history
print(user1.get_watch_history())  # ['Movie A']
