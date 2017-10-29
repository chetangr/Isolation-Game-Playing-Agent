# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:30:28 2017

@author: chetan
"""
"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(my_moves - 5 * opp_moves)#-2


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(my_moves - 4 * opp_moves)#-3

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)
    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    return float(3 * my_moves - opp_moves)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.
    ********************  DO NOT MODIFY THIS CLASS  ********************
    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)
    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.
    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

#MINI-MAX IMPLEMENTATION
class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************
        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initializing so that this function returns something if at all the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will catch the exception
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        return best_move

    def max_values(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0 ):
           return game.utility(self)
        
        if depth <= 0:
            return self.score(game, self)
                 
        v = float("-inf")

        for a in legal_moves:
            v = max(v, self.min_values(game.forecast_move(a), depth - 1))
        return v

    def min_values(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0):
           return game.utility(self) 
        
        if depth <= 0:
            return self.score(game, self)
            
        
        v = float("inf")
        
        for a in legal_moves:
            v = min(v, self.max_values(game.forecast_move(a), depth - 1))
        return v
                
    def minimax(self, game, depth):
       
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0):
            return self.score(game, self)
        
        if depth <= 0:
            return game.utility(self)
        
        max_value = float("-inf") 
        best_move = None
        for a in legal_moves:
            new_value = self.min_values(game.forecast_move(a), depth-1)
            if(new_value > max_value):
                max_value = new_value
                best_move = a
        return best_move


#ALPHA-BETA IMPEMENTATION AIMA METHOD
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.
        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.
        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.
        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initializing so that this function returns something if at all the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will catch the exception
            for i in range(1,101):
                best_move = self.alphabeta(game, i)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        return best_move
        
    def max_values(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0 ):
           return game.utility(self)
        
        if depth <= 0:
            return self.score(game, self)
                    
        v = float("-inf")
       
        for a in legal_moves:
            v = max(v, self.min_values(game.forecast_move(a), depth - 1, alpha, beta))
            if (v >= beta):
                return v
            alpha = max(alpha, v)
        return v
    
    def min_values(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0):
           return game.utility(self) 
        
        if depth <= 0:
            return self.score(game, self)
                    
        v = float("inf")
        for a in legal_moves:
            v = min(v, self.max_values(game.forecast_move(a), depth -  1, alpha, beta))
            if (v <= alpha):
                return v
            beta = min(v, beta)
        return v
            
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
 
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        legal_moves = game.get_legal_moves()
        
        if(len(legal_moves) == 0):
            return self.score(game, self)
        
        if depth <= 0:
            return game.utility(self)
        
        max_value = float("-inf") 
        best_move = None
        for a in legal_moves:
            new_value = self.min_values(game.forecast_move(a), depth-1, alpha, beta )
            
            if(new_value > max_value):
                max_value = new_value
                best_move = a
            
            if (new_value >= beta):
                return best_move
            alpha = max(alpha, new_value)
            
        return best_move