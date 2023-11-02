import logging

import cql

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    cqllexer = cql.CQLLexer()
    cqllexer.build(debug=True, debuglog=logging.getLogger("CQLLexer"))

    cqlparser = cql.CQLParser12()
    cqlparser.build(cqllexer)  # , debug=True, debuglog=logging.getLogger("CQLParser"))

    content = "stuff AND cat OR ( v = 1 )"
    content = "stuff AND cat"
    content = "stuff AND"
    content = "( a )"
    content = "a /mod"

    content = "dC.tiTlE any fish"
    content = "dc.TitlE Any/rEl.algOriThm=cori fish"
    content = """> dc = "http://deepcustard.org/" dc.custardDepth > 10"""
    content = """> "http://deepcustard.org/" custardDepth > 10"""
    # content = 'prox/xyz.unit="street"'
    content = "dc.title any fish or/rel.combine=sum dc.creator any sanderson"

    content = "a and b"

    content = "dc.TitlE Any/rEl.algOriThm=cori fish soRtbY Dc.TitlE"
    content = "( dc.TitlE Any/rEl.algOriThm=cori fish"

    content = "author=(bar or baz)"
    content = "(bar or baz)"

    content = (
        '>ns1="http://uri1" >ns2="http://uri2" whatever sortby ns1.key/a/b/c=1 ns2.key2'
    )

    content = '>dc="http://deepcustard.org" (>dc="http://dublincore.org" dc.title=jaws) sortby dc.custardDepth'

    content = ">a=1 (>c=2 x)"
    content = ">a=1 >c=2 x"

    content = "any or all:stem and all contains any prox proxfuzzy"
    content = r'"te\rm\*\?\^"'
    content = '>dc="http://deepcustard.org" (fish or >dc="http://dublincore.org" dc.title=jaws) sortby dc.custardDepth'

    content = '"^cat says \\"fish\\""'
    content = '"dinosaur" sortBy dc.date/sort.descending dc.title/sort.ascending'
    content = '(("^cat*fishdog\\"horse?"))'  #  --> &quot; / "

    content = "author=(bar or baz)"
    content = "bar or baz)"
    content = "baz=1) and (a or b)"

    content = "b=(>dc=x c) sortby d"
    content = '>dc="http://deepcustard.org" (fish or (>dc="http://dublincore.org" dc.title=jaws)) sortby dc.custardDepth'

    print(list(cqllexer.run(content)))

    parsed = cqlparser.parse(content, tracking=True)  # tracking=True  # debug=True
    # parsed.setServerDefaults()
    print(content)
    if parsed:
        print(parsed.toCQL())
        print(parsed.toXCQLString(pretty=True))
    else:
        print("--> no result!")
