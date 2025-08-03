from collections import defaultdict, deque

class LoginMonitor:
    def __init__(self):
        self.user_map = defaultdict(deque)
        self.window_seconds = 60

    def add_login(self, timestamp: int, user_id: str, city: str) -> None:
        """Records a login attempt for the user."""
        while self.user_map[user_id] and timestamp - self.user_map[user_id][0][0] > self.window_seconds:
            self.user_map[user_id].popleft()
        self.user_map[user_id].append((timestamp, city))


    def is_suspicious(self, user_id: str) -> bool:
        """Returns True if the user's recent login activity is suspicious."""
        user = self.user_map[user_id]
        cities = set()
        for t, c in user:
            if c in cities:
                return False
            cities.add(c)
        return True




# Example usage
if __name__ == "__main__":
    monitor = LoginMonitor()
    monitor.add_login(100, "user1", "Toronto")
    monitor.add_login(120, "user1", "Toronto")
    print(monitor.is_suspicious("user1"))  # ➞ False

    monitor.add_login(150, "user1", "Vancouver")
    print(monitor.is_suspicious("user1"))  # ➞ True (Toronto ➞ Vancouver within 60s)

