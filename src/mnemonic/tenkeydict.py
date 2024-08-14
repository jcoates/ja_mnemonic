"""TenKeyDict is a dictionary format used for ja_mnemonic to store maps of digit strings to kana words."""

from typing import Dict, List


class TenKeyDict(dict[str, list[str]]):
    """TenKeyDicts are a convenience for naming the kind of dict used for all these methods.

    It also includes a merge method. It should be Dict[str, List[str]] currently.

    """

    def merge(self, other):
        if not isinstance(other, dict):
            raise ValueError("Can only merge dicts with TenKeyDict")
        empty = []
        for k in set(self.keys()).union(other.keys()):
            self[k] = self.get(k, empty) + other.get(self, empty)


    @classmethod
    def merge_dicts(cls, *dicts: Dict[str, List[str]]):
        shared = set()
        for d in dicts:
            shared = shared.union(d.keys())
        r = {}
        empty = []
        for k in shared:
            l = []
            for d in dicts:
                fetched = d.get(k, empty)
                l += [f if isinstance(f, str) else f[0] for f in fetched]
            r[k] = l
        return cls(r)