BNF = """TextParser = { (NamedString | UnnamedString) } ;

(* Unnamed strings *)

UnnamedString = UnnamedString1
              | UnnamedString2
              | UnnamedString3
              | UnnamedString4
              | EmptyUnnamedString1
              | UnnamedString5
              | UnnamedString6
              | EmptyUnnamedString2
              ;

UnnamedString1 = LBRACE, VALUE, [COLON], RBRACE ;
UnnamedString2 = LBRACE, BACKTICK, VALUE, BACKTICK, COLON, RBRACE ;
UnnamedString3 = LBRACE, BACKTICK, VALUE, BACKTICK, RBRACE ;
UnnamedString4 = LBRACE, BACKTICK, VALUE, BACKTICK, COLON, RBRACE ;
UnnamedString5 = VALUE ;
UnnamedString6 = BACKTICK, VALUE, BACKTICK ;
EmptyUnnamedString1 = LBRACE, RBRACE ;
EmptyUnnamedString2 = BACKTICK, BACKTICK ;

(* Named strings *)

NamedString = NamedString1
            | NamedString2
            | NamedString3
            | NamedString4
            | NamedString5
            | EmptyNamedString
            | BacktickedEmptyKey
            ;

NamedString1 = VALUE, LBRACE, COLON, VALUE, RBRACE ;
NamedString2 = BACKTICK, VALUE, BACKTICK, LBRACE, COLON, VALUE, RBRACE ;
NamedString3 = LBRACE, VALUE, COLON, VALUE, RBRACE ;
NamedString4 = LBRACE, BACKTICK, VALUE, BACKTICK, COLON, VALUE, RBRACE ;
NamedString5 = VALUE, LBRACE, BACKTICK, BACKTICK, COLON, RBRACE ;
EmptyNamedString = LBRACE, COLON, RBRACE ;
BacktickedEmptyKey = LBRACE, BACKTICK, BACKTICK, COLON, VALUE, RBRACE ;
"""