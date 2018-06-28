from sample_players import BasePlayer


class CustomPlayer(BasePlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def __init__(self, player_id):
        super().__init__(player_id)

        self.quadrant = dict()
        # 第4象限元素
        a = [0, 1, 2, 3, 4, 5]
        b = [i + 13 for i in a]
        c = [i + 13 for i in b]
        d = [i + 13 for i in c]
        e = [i + 13 for i in d]
        # print("第4象限元素:", a, b, c, d, e)
        self.quadrant['IV'] = [a, b, c, d, e]
        # 第1象限元素
        f = [i + 13 for i in e]
        g = [i + 13 for i in f]
        h = [i + 13 for i in g]
        i = [i + 13 for i in h]
        # print("第1象限元素:", f, g, h, i)
        self.quadrant['I'] = [f, g, h, i]

        # 第3象限元素
        a = [6, 7, 8, 9, 10]
        b = [i + 13 for i in a]
        c = [i + 13 for i in b]
        d = [i + 13 for i in c]
        e = [i + 13 for i in d]
        # print("第3象限元素:", a, b, c, d, e)
        self.quadrant['III'] = [a, b, c, d, e]

        # 第2象限元素
        f = [i + 13 for i in e]
        g = [i + 13 for i in f]
        h = [i + 13 for i in g]
        i = [i + 13 for i in h]
        # print("第2象限元素:", f, g, h, i)
        self.quadrant['II'] = [f, g, h, i]

        self.relative_loc = dict()
        self.relative_loc['I'] = [25, 11]
        self.relative_loc['II'] = [27, 15]
        self.relative_loc['III'] = [-11, -25]
        self.relative_loc['IV'] = [-27, -15]

    def score(self, state):
        own_loc = state.locs[self.player_id]
        own_relatives = list()
        own_liberties = state.liberties(own_loc)
        opp_loc = state.locs[1 - self.player_id]
        opp_liberties = state.liberties(opp_loc)
        opp_relatives = list()

        if len(own_liberties) >= 2:
            for opp in opp_liberties:
                opp_relatives.append(opp - opp_loc)
            for own in own_liberties:
                own_relatives.append(own - opp_loc)
            if set(opp_relatives).intersection(own_liberties) in None:  # 有交集表示在同一个方向
                return own_liberties
            else:
                return set(own_liberties).intersection(set(opp_liberties))

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        # import random
        # self.queue.put(random.choice(state.actions()))

        if state.ply_count == 0:  # I am the first player
            self.queue.put(57)
        elif state.ply_count == 1:  # I am the second player
            opp_loc = state.locs[1 - self.player_id]
            opp_liberties = state.liberties(opp_loc)
            self.queue.put(max(opp_liberties, key=lambda x: len(state.result(x))))
        else:  # other common moves
            # self.queue.put(max(state.actions(), key=lambda x: self.score(state.result(x))))
            self.queue.put(self.score(state))
