

from GameState import GameState
from events.Event import Event
from player.Player import Player
from actions.Action import Action


class GameEngine:
   players: list[Player]
   game_state: GameState

   def __init__(self, players: list[Player], game_state: GameState):
      self.players = players
      self.game_state=game_state
      self.game_state.subscribe(self.on_update)

   async def game_loop(self):
      game_state = self.game_state


      try:
         while True:
            self.alert_all_players(game_state, None)
            current_phase = game_state.phase

            await current_phase.run(state = game_state)

            next_phase = await current_phase.next(game_state)
            if next_phase is None:
               break

            game_state.phase = next_phase
      except Exception as e:
         import traceback
         traceback.print_exc()
         # Also try to alert players of crash?
         print(f"GAME ENGINE CRASH: {e}")


   def on_update(self, game_state: GameState, latest_event: Event | None):
      self.alert_all_players(
         game_state=game_state,
         event=latest_event
      )

   def alert_player(self, game_state: GameState, player: Player, event: None | Event):
      character = game_state.get_character(player.character_id)
      player.receive_update(
         game_view=game_state.get_view(character),
         actions=game_state.phase.get_possible_actions( state=game_state, actor=character),
         latest_event=event.get_view(state=self.game_state, observer=character) if event else None
      )

   def alert_all_players(self, game_state: GameState, event: None | Event):
      for p in self.players:
         self.alert_player(game_state, p, event)

   async def handle_action(self, action: Action):
      # Resolve the action to an event
      event = action.resolve(self.game_state)

      # Apply the event to the state
      self.game_state.apply_event(event)