from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, DataTable, Static, Label, Tabs, Tab
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.message import Message

from GameEngine import GameEngine
from GameState import GameState, GameView
from actions.Action import Action
from player.ManualPlayer import ManualPlayer
from events.Event import EventView
import asyncio

class WerewolfApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }

    #game_view {
        height: 1fr;
        padding: 1;
    }

    .phase-header {
        text-align: center;
        background: $primary;
        color: white;
        padding: 1;
        margin-bottom: 1;
        text-style: bold;
    }

    .main-content {
        height: 1fr;
    }

    #player_table {
        width: 60%;
        height: 100%;
        border: solid green;
    }

    #log_container {
        width: 40%;
        height: 100%;
        border: solid blue;
        margin-left: 1;
    }

    .section-header {
        background: $accent;
        color: black;
        padding: 0 1;
    }

    #event_log {
        height: 1fr;
        background: $surface;
    }

    #action_bar {
        height: auto;
        min-height: 5;
        border-top: solid red;
        margin-top: 1;
        align: center middle;
        overflow-x: scroll;
        padding: 1;
    }

    Button {
        margin: 1;
    }
    """

    current_player_id = reactive("")

    def __init__(self, game_engine: GameEngine, players: list[ManualPlayer]):
        super().__init__()
        self.game_engine = game_engine
        self.players = {p.id: p for p in players}
        # default to first player
        if players:
            self.current_player_id = players[0].id

    def compose(self) -> ComposeResult:
        yield Header()

        # Tabs for switching players
        yield Tabs(
            *[Tab(p.name, id=f"tab_{p.id}") for p in self.players.values()]
        )

        with Vertical(id="game_view"):
            yield Label("Phase: [Loading...]", id="phase_info", classes="phase-header")

            with Horizontal(classes="main-content"):
                 yield DataTable(id="player_table")

                 with Vertical(id="log_container"):
                     yield Label("Event Log", classes="section-header")
                     yield VerticalScroll(id="event_log")

            yield Label("Actions", classes="section-header")
            with Horizontal(id="action_bar"):
                 pass # Buttons added dynamically

        yield Footer()

    async def on_mount(self) -> None:
        # Start the game loop in the background
        asyncio.create_task(self.game_engine.game_loop())

        # Setup DataTable columns
        table = self.query_one("#player_table", DataTable)
        table.add_columns("Name", "Role", "Faction", "State")
        table.cursor_type = "row"

        # Wire up player updates to UI
        for player in self.players.values():
            player.on_update = self.on_player_update

    def on_player_update(self):
        # Schedule the async update_ui on the event loop
        asyncio.create_task(self.update_ui())

    async def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        # Update current player when tab changes
        if event.tab and event.tab.id:
            pid = event.tab.id.replace("tab_", "")
            self.current_player_id = pid
            await self.update_ui()

    async def update_ui(self) -> None:
        if not self.current_player_id:
            return

        player = self.players.get(self.current_player_id)
        if not player:
            self.notify(f"Player {self.current_player_id} not found!", severity="error")
            return
        if not player.current_game_view:
            return

        view = player.current_game_view

        # 1. Update Phase Info
        phase_label = self.query_one("#phase_info", Label)
        phase_text = f"Phase: {view.phase.type} | Time: {view.phase.time}"
        if view.phase.type == "game_over":
             # TODO: add winners logic if available in view, but mostly it's in events
             pass
        phase_label.update(phase_text)

        # 2. Update Player Table
        table = self.query_one("#player_table", DataTable)
        table.clear()

        # We need to sort or consistent order?
        # view.characters order might change? Let's assume consistent for now or sort by name.
        sorted_chars = sorted(view.characters, key=lambda c: c.name)

        for char in sorted_chars:
            # Determine row style based on state
            style = ""
            if char.state == "dead":
                style = "dim"
            elif char.role.faction == "werewolves":
                 # Only if visible! logic is handled by get_view
                 # But we can style it if we know.
                 # Actually RoleView.faction tells us what THIS player knows.
                 if char.role.faction == "werewolves":
                     style = "bold red"

            table.add_row(
                char.name,
                char.role.name,
                char.role.faction.title(),
                char.state.title(),
                label=char.name # key for updates if needed, but we clear/rewrite
            )

        # 3. Update Event Log
        log_view = self.query_one("#event_log", VerticalScroll)
        await log_view.remove_children()

        for event in view.events:
             log_view.mount(Label(f"> {event.description}"))

        # Scroll to bottom? Textual might auto-scroll or need manual helper.
        # log_view.scroll_end() # verify if this works

        # 4. Update Actions
        action_bar = self.query_one("#action_bar", Horizontal)
        await action_bar.remove_children()

        seen_ids = set()
        for action in player.possible_actions:
            key = self.actions_map_key(action)
            # Ensure uniqueness even if duplicate actions exist
            if key in seen_ids:
                continue
            seen_ids.add(key)

            btn = Button(action.name, id=f"action_{key}")
            btn.action_target = action # Monkey-patch action

            # Contextual styling?
            if "Kill" in action.name or "Hunt" in action.name:
                btn.variant = "error"
            elif "Protect" in action.name:
                btn.variant = "success"

            action_bar.mount(btn)

    def actions_map_key(self, action: Action) -> str:
        # create a semi-unique string for the key
        return f"{action.actorId}_{action.name.replace(' ', '_')}"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if hasattr(event.button, "action_target"):
            action = getattr(event.button, "action_target")
            await self.apply_player_action(action)

    async def apply_player_action(self, action: Action):
        try:
            await self.game_engine.handle_action(action)
            # Force a re-render/update so the player sees the result immediately
            self.notify(f"Action executed: {action.name}")

        except Exception as e:
            self.notify(f"Error executing action: {e}", severity="error")
