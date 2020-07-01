import random


class Player(object):
    def __init__(self, name):
        self.points_won = 0
        self.games_won = 0
        self.sets_won = 0
        self.score = (
            str(self.sets_won)
            + " sets "
            + str(self.games_won)
            + " games "
            + str(self.points_won)
            + " points "
        )
        self.name = name

    def __repr__(self):
        return self.name + " " + self.score

    def set_score(self, score):
        self.score = (
            str(self.sets_won)
            + " sets "
            + str(self.games_won)
            + " games "
            + str(self.points_won)
            + " points "
        )

    def add_point(self):

        if self.points_won == 0 or self.points_won == 15:
            self.points_won += 15
        elif self.points_won == 30:
            self.points_won += 10
        elif self.points_won == 40:
            self.points_won = "Adv"
        elif self.points_won == "Adv":
            self.points_won = 0
            self.games_won += 1
            if self.games_won >= 6:
                self.sets_won += 1
                self.games_won = 0
                self.points_won = 0
        self.set_score(self.score)


class Match(object):
    def __init__(self, player1, player2):
        self.player1 = Player(player1)
        self.player2 = Player(player2)
        self.sets_played = 0
        self.points_played = 0
        self.winner = None

    def __repr__(self):
        if self.winner != None:
            return str(self.winner) + " won! "

    def simulate_match(self):
        while self.sets_played <= 3:
            self.points_played += 1
            self.sets_played = self.player1.sets_won + self.player2.sets_won
            if self.player1.sets_won == 2 or self.player2.sets_won == 2:
                break
            self.win_point()

    def win_point(self):
        decider = random.randint(1, 2)
        if decider == 1:
            self.player1.add_point()
            return self.player1.name
        if decider == 2:
            self.player2.add_point()
            return self.player2.name

    def who_won(self):
        if self.player1.sets_won > self.player2.sets_won:
            self.winner = self.player1
        else:
            self.winner = self.player2

        return self.winner


# trial

x = Match("Nadal", "Federer")
x.simulate_match()
x.who_won()
print(x.who_won())
