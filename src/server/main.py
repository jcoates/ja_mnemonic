from typing import List, Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel

from mnemonic.conversion import Converter

app = FastAPI()

class MnemonicSuggestions(BaseModel):
    words: List[str] | None
    given_names: List[str] | None
    surnames: List[str] | None
    full_names: List[str] | None

converter = Converter.build_default()

@app.get("/ja_mnemonic")
def produce_word(query: Annotated[str, Query(pattern="\\d+", max_length=45)]) -> MnemonicSuggestions:
    """Given a query string with a number in it, produces some options for japanese words.

    The query has to be digits only. We're allowing 45 currently since that's the longest
    possible string in the data set, but the data is very very sparse between like 8 and 45
    digits long.
    """
    r = converter.find_all_options(query)
    resp = MnemonicSuggestions(
        words=r.words if r.words else None,
        given_names=r.given_names if r.given_names else None,
        surnames=r.surnames if r.surnames else None,
        full_names=r.full_names if r.full_names else None
    )
    return resp