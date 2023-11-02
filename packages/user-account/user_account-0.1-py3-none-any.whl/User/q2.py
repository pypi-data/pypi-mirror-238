class AlreadySubscribedError(Exception):
    pass
 
class UnauthorizedAccessError(Exception):
    pass
 
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.subscription_plan = None
        self.watched_content = []
 
    def subscribe(self, plan_name):
        if self.subscription_plan is None:
            self.subscription_plan = [plan_name]
            return f"Subscribed to {plan_name}"
        elif plan_name in self.subscription_plan:
            raise AlreadySubscribedError("You are already subscribed to this plan")
        else:
            self.subscription_plan.append(plan_name)
            return f"Subscribed to {plan_name}"
 
    def watch(self, content_name):
        if self.subscription_plan is None:
            raise UnauthorizedAccessError("You don't have access to this content")
        else:
            self.watched_content.append(content_name)
            return f"Watching {content_name}"
 
    def get_watch_history(self):
        return self.watched_content
    

# Example
 
# user1 = User(1, "Alice")
# print(user1.subscribe("Premium"))
# print(user1.watch("Batman"))
# print(user1.get_watch_history())