class User:
    def __init__(self, record: (int, int, str, str, str, str, int)):
        self.group_id = record[0]
        self.qq_id = record[1]
        self.qq_name = record[2]
        self.role = record[3]
        self.password = record[4]
        self.player_name = record[5]
        self.id = record[6]
