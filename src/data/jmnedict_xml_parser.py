"""This file is for parsing the jmnedict xml export into names and words.

The JMNEDict is a named entity dataset, but the named entities aren't all people names,
they include locations, companies, organizations, etc.

Those might be useful in the words dictionary, but need to parsed separately from
the given names and surnames, since those are handled differently.
"""

import copy
import io
from pathlib import Path
from typing import List, Tuple
import xml.etree.ElementTree as ET

DATA_DIR = Path(__file__).parent.parent.parent / "data"

JMNEDICT_XML_FILE = DATA_DIR / 'JMnedict.xml'

SURNAMES_OUT_FILE = DATA_DIR / 'jmnedict_surnames.csv'
GIVEN_NAMES_OUT_FILE = DATA_DIR / 'jmnedict_given_names.csv'
OTHER_NAMES_OUT_FILE = DATA_DIR / 'jmnedict_other_names.csv'

# `surname`, `masc`, `fem`, and `given`
SURNAME_TYPE = 'surname'
MASC_TYPE = 'masc'
FEM_TYPE = 'fem'
GIVEN_TYPE = 'given'
GIVEN_TYPES = [MASC_TYPE, FEM_TYPE, GIVEN_TYPE]

def parse_jmnedict_xml():
    """This method parses the JMNEdict xml dump file into the relevant parts.

    Produces 3 Files
    File 1 - Non-person names
    File 2 - Surnames
    File 3 - Given Names

    Example Element:
    ```
    <JMnedict>
    <...>
        <entry>
            <ent_seq>5532809</ent_seq>
            <k_ele>
                <keb>追河</keb>
            </k_ele>
            <r_ele>
                <reb>おいかわ</reb>
            </r_ele>
            <trans>
                <name_type>&surname;</name_type>
                <trans_det>Oikawa</trans_det>
            </trans>
        </entry>
    <...>
    </JMnedict>
    ```

    the name_types we're interested in are `surname`, `masc`, `fem`, and `given`.
    """

    print("Parsing Tree")
    tree = ET.parse(JMNEDICT_XML_FILE)
    print("Tree Parse")

    surnames = []
    given_names = []
    other_names = []
    root = tree.getroot() # This should be JMnedict
    print("Processing elements:")
    for child in root:
        trans = child.findall('trans')
        # currently this is unused so not important
        kanji = ""
        k_ele = child.find('k_ele')
        if k_ele:
            kanji = k_ele.find('keb').text # type: ignore (ignoring a none check as in our data this is always present)
        if not kanji:
            kanji = ""
        readings = [r.find('reb').text for r in child.findall('r_ele')] # type: ignore (see above)
        for t in trans:
            # There was one record with no name type, so leaving this here for safety
            if t.find('name_type') is None:
                print(ET.tostring(t, encoding="unicode"))
                continue
            name_type = t.find('name_type').text # type: ignore (see above)
            translation = t.find('trans_det').text.replace(',', ';').replace('"', "'") # type: ignore (see above)
            if name_type == SURNAME_TYPE:
                for r in readings:
                    surnames.append((r, kanji, translation))
            elif name_type in GIVEN_TYPES:
                for r in readings:
                    given_names.append((r, kanji, translation))
            else:
                for r in readings:
                    other_names.append((r, kanji, translation))

    print("Writing Files")
    with open(GIVEN_NAMES_OUT_FILE, 'w') as f:
        for g in given_names:
            f.write(','.join(g) + '\n')
    with open(SURNAMES_OUT_FILE, 'w') as f:
        for s in surnames:
            f.write(','.join(s) + '\n')
    with open(OTHER_NAMES_OUT_FILE, 'w') as f:
        for o in other_names:
            f.write(','.join(o) + '\n')


def main():
    parse_jmnedict_xml()

if __name__ == '__main__':
    main()
