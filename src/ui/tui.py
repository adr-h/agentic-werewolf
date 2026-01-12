import asyncio
from typing import List, Optional, Any
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Grid, Container
from textual.widgets import Header, Footer, Static, Button, Label, ListView, ListItem, Collapsible
from textual.reactive import reactive
from textual.binding import Binding
from rich.markup import escape

from domain.GameState import GameState
from engine.GameEngine import GameEngine
from engine.projections import project_game_view
from player.agentic_player.AgenticPlayer import AgenticPlayer

class PlayerSwitch(Static):
    """A row of buttons to switch between players."""
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Switch: ", id="switch_label")
            # Using cast to avoid lint error
            from typing import cast
            players = cast(Any, self.app).players
            for i, p in enumerate(players):
                if i > 0:
                    yield Label("|", classes="divider")
                model_suffix = f" <{p.model_id.split('/')[-1]}>" if hasattr(p, 'model_id') else ""
                label = f"{p.character_name} ({p.character_id}){model_suffix}"
                yield Button(label, id=f"btn_{p.character_id}", variant="default")

class InfoPanel(Static):
    """Displays Subject, Status, Role, Phase, and Winners."""
    subject = reactive("Unknown")
    status = reactive("Unknown")
    role = reactive("Unknown")
    phase = reactive("Unknown")
    winners = reactive("None Yet")

    def render(self) -> str:
        return (
            f"Subject: [bold]{escape(self.subject)}[/bold]\n"
            f"Status: [bold]{escape(self.status)}[/bold]\n"
            f"Character Role: [bold cyan]{escape(self.role)}[/bold cyan]\n"
            f"Current Phase: [bold yellow]{escape(self.phase)}[/bold yellow]\n"
            f"Winners: [bold green]{escape(self.winners)}[/bold green]"
        )
class HistoryList(ListView):
    """A ListView for history events."""
    pass

class WerewolfTUI(App):
    CSS = """
    Screen {
        overflow-y: scroll;
    }
    #top_bar {
        height: 3;
        background: $boost;
        border-bottom: solid $primary;
        padding: 0 1;
        align: left middle;
    }
    #switch_label {
        padding: 0 1;
        content-align: center middle;
    }
    #top_bar Button {
        margin: 0 1;
        min-width: 10;
    }
    .divider {
        padding-top: 1;
        color: $primary;
    }
    #info_panel {
        height: 7;
        padding: 1 2;
        background: $panel;
        border-bottom: double $primary;
    }
    .history_container {
        padding: 1;
        border-bottom: solid $primary;
    }
    .history_title {
        text-align: center;
        text-style: bold;
        background: $accent;
        margin-bottom: 0;
    }
    ListView {
        height: 11; /* Approx 10 lines + header or just enough for 10 items */
        border: round $accent;
    }
    ListView ListItem {
        height: auto;
        padding: 0 1;
    }
    ListView ListItem Static, ListView ListItem Label {
        height: auto;
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    selected_player_id = reactive("")

    def __init__(self, engine: GameEngine, players: List[AgenticPlayer]):
        super().__init__()
        self.engine = engine
        self.players = players
        if players:
            self.selected_player_id = players[0].character_id

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="top_bar"):
            yield Label("Switch: ", id="switch_label")
            for i, p in enumerate(self.players):
                if i > 0:
                    yield Label("|", classes="divider")
                model_suffix = f" <{p.model_id.split('/')[-1]}>" if hasattr(p, 'model_id') else ""
                label = f"{p.character_name} ({p.character_id}){model_suffix}"
                yield Button(label, id=f"btn_{p.character_id}", variant="default")

        yield InfoPanel(id="info_panel")

        with Vertical(id="histories"):
            with Vertical(classes="history_container"):
                yield Label("Event History", classes="history_title")
                yield HistoryList(id="event_history")
            with Vertical(classes="history_container"):
                yield Label("Command History", classes="history_title")
                yield HistoryList(id="command_history")

        yield Footer()

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1.0, self.update_state)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("btn_"):
            player_id = event.button.id[4:]
            self.selected_player_id = player_id

    def watch_selected_player_id(self, new_id: str) -> None:
        self.update_state()

    def update_state(self) -> None:
        if not self.is_running:
            return

        state = self.engine.state
        if not state:
            return

        selected_player = next((p for p in self.players if p.character_id == self.selected_player_id), None)
        if not selected_player:
            return

        # Use query to avoid ScreenStackError if widgets aren't ready
        try:
            info_panel = self.query_one("#info_panel", InfoPanel)
        except Exception:
            return

        # Determine role and status
        char = next((c for c in state.characters if c.id == self.selected_player_id), None)
        model_suffix = f" <{selected_player.model_id.split('/')[-1]}>" if hasattr(selected_player, 'model_id') else ""
        info_panel.subject = f"{selected_player.character_name} ({selected_player.character_id}){model_suffix}"
        info_panel.status = char.status.capitalize() if char else "Unknown"
        info_panel.role = char.role.__class__.__name__.replace("Role", "") if char else "Unknown"
        info_panel.phase = state.phase.__class__.__name__.replace("Phase", "")

        # Check for winners
        from domain.Phase import GameOverPhase
        if isinstance(state.phase, GameOverPhase):
            info_panel.winners = state.phase.winner
        else:
            info_panel.winners = "None Yet"

        # Update Event History
        event_list = self.query_one("#event_history", HistoryList)
        event_list.clear()

        # Projection: Events filtered for this player
        # In a real scenario, we might have a specific projection for this.
        # For now, let's just show events that mention them or are public.
        # Actually the prompt says "Event History are views of events from their eyes"
        # Since I don't have a formal "eye" projection, I'll just show the last N events for simplicity,
        # but in a real game we should use `get_agent_view`.
        # However, `get_agent_view` returns a string.
        # Let's just use the state events and filter (if possible).

        # Projection: Events filtered for this player
        view = project_game_view(state, self.selected_player_id)

        for e_str, ts in reversed(view.recent_events[-20:]): # Last 20 narrated events
            timestamp = ts.strftime("%I:%M:%S%p").lower()
            event_text = f"> [[{escape(timestamp)}] {escape(e_str)}"
            event_list.append(ListItem(Label(event_text)))

        # Update Command History
        cmd_list = self.query_one("#command_history", HistoryList)
        cmd_list.clear()

        for cmd in reversed(selected_player.command_history[-20:]):
            timestamp = cmd.timestamp.strftime("%I:%M:%S%p").lower()
            cmd_name = cmd.__class__.__name__.replace("Command", "")
            rationale = cmd.rationale if hasattr(cmd, 'rationale') and cmd.rationale else "No thought"

            # Formatting as requested: [ CommandName (params)]. [Thought: ...]
            # We'd need to extract params.
            params = {k: v for k, v in cmd.__dict__.items() if k not in ['actor_id', 'rationale', 'timestamp']}
            params_str = ", ".join(f"{k}={v}" for k, v in params.items())

            item_text = f"> [[{escape(timestamp)}] [bold]{escape(cmd_name)}[/bold] ({escape(params_str)}). [[Thought: {escape(rationale)}]"
            cmd_list.append(ListItem(Static(item_text)))

def run_tui(engine: GameEngine, players: List[AgenticPlayer]):
    app = WerewolfTUI(engine, players)
    app.run()
