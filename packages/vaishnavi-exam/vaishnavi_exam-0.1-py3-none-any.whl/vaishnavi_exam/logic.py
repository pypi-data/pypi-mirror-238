class AlreadySubscribedError(Exception):
    pass
 
class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.subscription_plan = None
        self.watched_content = []
 
    def subscribe(self, plan_name):
        if self.subscription_plan is not None and plan_name in self.subscription_plan:
            raise AlreadySubscribedError("You are already subscribed to this plan.")
        else:
            if self.subscription_plan is None:
                self.subscription_plan = []
            self.subscription_plan.append(plan_name)
            return f"Subscribed to {plan_name}"
 
    def watch(self, content_name):
        if self.subscription_plan is None:
            return "You don't have access to this content"
        else:
            return f"Watching {content_name}"
 
    def get_watch_history(self):
        return self.watched_content