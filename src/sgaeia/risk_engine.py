from .models import Agent, RiskContext, AUTONOMY_LEVEL

class RiskEngine:
    # weights sum to 20; each dimension 0..5 => max raw 100
    weights = {
        "autonomy": 3,
        "privilege": 3,
        "data_sensitivity": 2,
        "tool_power": 3,
        "network_reach": 2,
        "delegation": 2,
        "impact": 4,
        "behavior_anomaly": 1,
    }

    def score(self, agent: Agent, ctx: RiskContext) -> int:
        vals = {
            "autonomy": AUTONOMY_LEVEL[agent.autonomy],
            "privilege": ctx.privilege,
            "data_sensitivity": ctx.data_sensitivity,
            "tool_power": ctx.tool_power,
            "network_reach": ctx.network_reach,
            "delegation": ctx.delegation,
            "impact": ctx.impact,
            "behavior_anomaly": ctx.behavior_anomaly,
        }
        for k,v in vals.items():
            if not 0 <= v <= 5:
                raise ValueError(f"risk dimension {k} must be 0..5")
        raw = sum(vals[k]*self.weights[k] for k in self.weights) # max 100
        return min(100, max(0, round(raw)))

    @staticmethod
    def disposition(score: int) -> str:
        if score <= 20: return "ALLOW"
        if score <= 40: return "ALLOW_MONITORED"
        if score <= 60: return "RESTRICT"
        if score <= 80: return "REQUIRE_APPROVAL"
        if score <= 90: return "QUARANTINE"
        return "DENY_REVOKE"
