class UserRepository:

    def get_by_id(
        self,
        user_id: int
    ):

        users = {
            1: {
                "id": 1,
                "email": "adamya@example.com"
            }
        }

        return users.get(user_id)