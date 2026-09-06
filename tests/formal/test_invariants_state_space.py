import itertools

CLASSES=["L0","L1","L2","L3","L4"]
AUTONOMY=["A0","A1","A2","A3","A4","A5"]

def reference_authorize(*, registered, revoked, klass, autonomy, capability, depth, max_depth, offline, critical):
    return all([
        registered,
        not revoked,
        not (klass=="L4" and autonomy=="A5"),
        capability,
        depth <= max_depth,
        not (offline and critical),
    ])

def test_small_state_space_preserves_core_invariants():
    for registered,revoked,klass,autonomy,capability,offline,critical in itertools.product(
        [False,True],[False,True],CLASSES,AUTONOMY,[False,True],[False,True],[False,True]
    ):
        for depth,max_depth in itertools.product(range(3),range(3)):
            allow=reference_authorize(registered=registered,revoked=revoked,klass=klass,autonomy=autonomy,
                capability=capability,depth=depth,max_depth=max_depth,offline=offline,critical=critical)
            if allow:
                assert registered
                assert not revoked
                assert capability
                assert not (klass=="L4" and autonomy=="A5")
                assert depth <= max_depth
                assert not (offline and critical)

def test_delegated_capabilities_are_subset_of_parent():
    universe={"read","write","pay","egress"}
    for parent_bits in itertools.product([0,1], repeat=len(universe)):
        parent={c for c,b in zip(sorted(universe),parent_bits) if b}
        for child_bits in itertools.product([0,1], repeat=len(universe)):
            requested={c for c,b in zip(sorted(universe),child_bits) if b}
            allowed=requested.issubset(parent)
            if allowed:
                assert not (requested-parent)
