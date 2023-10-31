class SortOrder:
    Ascending = 0
    Descending = 1


class SearchType:
    Aprox = 0
    Exact = 1


class NotFoundBehavior:
    RaiseError = 0
    ReturnNone = 1


def bin_search(l, v, order=SortOrder.Ascending, search_type=SearchType.Aprox, key=None, not_found_behavior=NotFoundBehavior.RaiseError):
    lo = 0
    hi = len(l) - 1
    mi = int((hi + lo) / 2)
    if order == SortOrder.Ascending:
        if key is None:
            while hi != lo and l[mi] != v:
                if v > l[mi]:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
            if l[mi] == v:
                return mi
        else:
            cv = key(l[mi])
            while hi != lo and cv != v:
                if v > cv:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
                cv = key(l[mi])
            if cv == v:
                return mi
    else:
        if key is None:
            while hi != lo and l[mi] != v:
                if v < l[mi]:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
            if l[mi] == v:
                return mi
        else:
            cv = key(l[mi])
            while hi != lo and cv != v:
                if v < cv:
                    lo = mi + 1
                else:
                    hi = mi
                mi = (hi + lo) // 2
                cv = key(l[mi])
            if cv == v:
                return mi

    if search_type == SearchType.Aprox:
        return mi
    else:
        if not_found_behavior == NotFoundBehavior.RaiseError:
            raise RuntimeError("Value not found")
        else:
            return None
