class KillSwitch:
    def __init__(self):
        self._revoked: set[str] = set()

    def revoke(self, agent_id: str) -> None:
        self._revoked.add(agent_id)

    def restore(self, agent_id: str) -> None:
        self._revoked.discard(agent_id)

    def is_revoked(self, agent_id: str) -> bool:
        return agent_id in self._revoked
