class Spaceship:
    def __init__(self, spaceship_id, name, ship_type, status="available"):
        self.spaceship_id = spaceship_id
        self.name = name
        self.ship_type = ship_type  # "research" или "combat"
        self.status = status  # "available", "on_mission", "under_repair"

    def update_status(self, new_status):
        valid_statuses = ["available", "on_mission", "under_repair"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.status = new_status

    def to_dict(self):
        return {
            "spaceship_id": self.spaceship_id,
            "name": self.name,
            "type": self.ship_type,
            "status": self.status
        }


class Mission:
    def __init__(self, mission_id, name, goal, status="planned"):
        self.mission_id = mission_id
        self.name = name
        self.goal = goal  # "research" или "defense"
        self.status = status  # "planned", "in_progress", "completed"
        self.spaceships = []

    def add_spaceship(self, spaceship):
        if spaceship.status != "available":
            raise ValueError("Spaceship is not available")
        self.spaceships.append(spaceship)
        spaceship.update_status("on_mission")

    def complete_mission(self):
        self.status = "completed"
        for ship in self.spaceships:
            ship.update_status("available")
        self.spaceships = []

    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "name": self.name,
            "goal": self.goal,
            "status": self.status,
            "spaceships": [s.to_dict() for s in self.spaceships]
        }


class CrewMember:
    ROLES = ["captain", "engineer", "pilot", "scientist"]

    def __init__(self, member_id, name, role):
        self.member_id = member_id
        self.name = name
        if role not in self.ROLES:
            raise ValueError(f"Invalid role. Must be one of: {self.ROLES}")
        self.role = role

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "role": self.role
        }
