class Animal(object):

    def __init__(self, health=10, skill=10, weapon=None):
        self.health = health
        self.skill = skill
        self.is_alive = True
        self.weapon = weapon

    def attack(self, target):
        if self.weapon is not None:
            self.weapon.attack(target, skill=self.skill)

    def receive_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.health = 0
        self.is_alive = False


class Died(Exception):
    pass


class Shark(Animal):

    def eat(self, target):
        target.receive_hit(damage=5)

    def attack(self, target):
        super(Shark, self).attack(target)
        self.eat(target)


class Weapon(object):
    pass


class Laser(Weapon):

    def calculate_damage(self, skill):
        # Expects to be mixed in to a class with `skill`
        skill_modifier = 1 + (0.1 * skill)
        return 5 * skill_modifier

    def attack(self, target, skill=0):
        damage = self.calculate_damage(skill)
        target.receive_hit(damage)


class Orca(Animal):

    def eat(self, target):
        target.receive_hit(damage=10)

    def attack(self, target):
        super(Orca, self).attack(target)
        self.eat(target)


class Nunchuck(Weapon):

    def attack(self, target, skill):
        target.receive_hit(damage=2)


class SharkWithNunchucks(Nunchuck, Shark):

    # Another approach to refactoring:
    # Haven't rewritten Nunchucks yet, instead override attack().

    def attack(self, target):
        Nunchuck().attack(target, self.skill)
        Shark.attack(self, target)


def OrcaWithLasers(*args, **kwargs):
    orca = Orca(*args, **kwargs)
    orca.weapon = Laser()


class ArmorProxy(object):

    armor_health = 10

    def __init__(self, wearer):
        self.wearer = wearer

    def receive_hit(self, damage):
        """
        Absorb some damage before passing any on to self.health.
        """
        self.armor_health -= damage
        if self.armor_health < 0:
            self.wearer.receive_hit(-self.armor_health)
            self.armor_health = 0

    def __getattr__(self, name):
        return getattr(self.wearer, name)
