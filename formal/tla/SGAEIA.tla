------------------------------ MODULE SGAEIA ------------------------------
EXTENDS Naturals, FiniteSets

CONSTANTS Agents, Operations

VARIABLES registered, revoked, klass, autonomy, capabilities, maxDepth,
          requestedOp, delegationDepth, offline, critical, authorized

vars == <<registered, revoked, klass, autonomy, capabilities, maxDepth,
          requestedOp, delegationDepth, offline, critical, authorized>>

Init ==
  /\ registered \in [Agents -> BOOLEAN]
  /\ revoked \in [Agents -> BOOLEAN]
  /\ klass \in [Agents -> {"L0","L1","L2","L3","L4"}]
  /\ autonomy \in [Agents -> {"A0","A1","A2","A3","A4","A5"}]
  /\ capabilities \in [Agents -> SUBSET Operations]
  /\ maxDepth \in [Agents -> Nat]
  /\ requestedOp \in [Agents -> Operations]
  /\ delegationDepth \in [Agents -> Nat]
  /\ offline \in [Agents -> BOOLEAN]
  /\ critical \in [Agents -> BOOLEAN]
  /\ authorized = [a \in Agents |-> FALSE]

CanAuthorize(a) ==
  /\ registered[a]
  /\ ~revoked[a]
  /\ ~(klass[a] = "L4" /\ autonomy[a] = "A5")
  /\ requestedOp[a] \in capabilities[a]
  /\ delegationDepth[a] <= maxDepth[a]
  /\ ~(offline[a] /\ critical[a])

Authorize(a) ==
  /\ authorized' = [authorized EXCEPT ![a] = CanAuthorize(a)]
  /\ UNCHANGED <<registered, revoked, klass, autonomy, capabilities, maxDepth,
                 requestedOp, delegationDepth, offline, critical>>

Revoke(a) ==
  /\ revoked' = [revoked EXCEPT ![a] = TRUE]
  /\ authorized' = [authorized EXCEPT ![a] = FALSE]
  /\ UNCHANGED <<registered, klass, autonomy, capabilities, maxDepth,
                 requestedOp, delegationDepth, offline, critical>>

Next == \E a \in Agents : Authorize(a) \/ Revoke(a)

Spec == Init /\ [][Next]_vars

NoUnknownExecution == \A a \in Agents : authorized[a] => registered[a]
NoRevokedExecution == \A a \in Agents : revoked[a] => ~authorized[a]
NoL4A5 == \A a \in Agents : (klass[a] = "L4" /\ autonomy[a] = "A5") => ~authorized[a]
NoExcessDelegation == \A a \in Agents : delegationDepth[a] > maxDepth[a] => ~authorized[a]
OfflineCriticalDenied == \A a \in Agents : (offline[a] /\ critical[a]) => ~authorized[a]
=============================================================================
