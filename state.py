import typing as t
from dataclasses import dataclass, field

class StateHolder(t.Protocol):
    def set(self, key, value) -> None:
        ...
    
    def get(self, key) -> t.Union[t.Union[str, int], None]:
        ...



@dataclass
class InMemoryState(StateHolder):
    state: t.Dict[str, t.Dict['str', t.Union[str, int]]] = field(default_factory=dict)

    def set(self, key, value) -> None:
        v = self.state.get(key, None)
        if v:
            self.state[key]['v'] = value
            if self.state[key]['v'] != value:
                self.state[key]['dirty'] = True
        else:
            self.state[key] = {'v': value, 'dirty': False}

    def get(self, key) -> t.Union[t.Union[str, int], None]:
        if stored_state := self.state.get(key, None):
            return stored_state['v']
            
        return None