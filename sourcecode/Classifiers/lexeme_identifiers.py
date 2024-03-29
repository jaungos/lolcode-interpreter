"""
    This file is used to pattern match the lexemes and identify the lexeme type.
"""

def get_all_lexeme_regex_patterns():
    lexeme_regex_patterns = {
        "HAI": r'HAI',
        "KTHXBYE":r'KTHXBYE',
        "WAZZUP": r'WAZZUP',
        "BUHBYE": r'BUHBYE',
        "BTW": r'BTW',
        "OBTW": r'OBTW',
        "TLDR": r'TLDR',
        "I HAS A": r'I\sHAS\sA',
        "ITZ": r'ITZ',
        "R": r'R',
        "SUM OF": r'SUM\sOF',
        "DIFF OF": r'DIFF\sOF',
        "PRODUKT OF": r'PRODUKT\sOF',
        "QUOSHUNT OF": r'QUOSHUNT\sOF',
        "MOD OF": r'MOD\sOF',
        "BIGGR OF": r'BIGGR\sOF',
        "SMALLR OF": r'SMALLR\sOF',
        "BOTH OF": r'BOTH\sOF',
        "EITHER OF": r'EITHER\sOF',
        "WON OF": r'WON\sOF',
        "NOT": r'NOT',
        "ANY OF": r'ANY\sOF',
        "ALL OF": r'ALL\sOF',
        "BOTH SAEM": r'BOTH\sSAEM',
        "DIFFRINT": r'DIFFRINT',
        "SMOOSH": r'SMOOSH',
        "MAEK": r'MAEK',
        "AN": r'AN',
        "A": r'A',
        "IS NOW A": r'IS\sNOW\sA',
        "VISIBLE": r'VISIBLE',
        "GIMMEH": r'GIMMEH',
        "O RLY?": r'O\sRLY\?',
        "YA RLY": r'YA\sRLY',
        "MEBBE": r'MEBBE',
        "NO WAI": r'NO\sWAI',
        "OIC": r'OIC',
        "WTF?": r'WTF\?',
        "OMGWTF": r'OMGWTF',
        "OMG": r'OMG',
        "IM IN YR": r'IM\sIN\sYR',
        "UPPIN": r'UPPIN',
        "NERFIN": r'NERFIN',
        "YR": r'YR',
        "TIL": r'TIL',
        "WILE": r'WILE',
        "IM OUTTA YR": r'IM\sOUTTA\sYR',
        "HOW IZ I": r'HOW\sIZ\sI',
        "IF U SAY SO": r'IF\sU\sSAY\sSO',
        "GTFO": r'GTFO',
        "FOUND YR": r'FOUND\sYR',
        "I IZ": r'I\sIZ',
        "MKAY": r'MKAY',
        "NUMBAR_LITERAL": r'\-?(\d)+\.(\d)+',
        "NUMBR_LITERAL": r'(\-?[1-9](\d)*)|(0)',
        "YARN": r'\"[^"]*\"',                            
        "WIN": r'WIN',
        "FAIL": r'FAIL',
        "TYPE": r'(NOOB|TROOF|NUMBAR|NUMBR|YARN)',
        "+": r'\+',
        "NEWLINE": r'\n',
        "SUPPRESS_NEWLINE": r'!',
        "IDENTIFIER": r'[a-zA-Z][a-zA-Z0-9_]*',
    }
    
    return lexeme_regex_patterns # Return the dictionary of regex patterns for the lexemes
