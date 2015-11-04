import overpass
api = overpass.API()
map_query = overpass.MapQuery(174.0591, -37.1384,  175.4653, -36.5758)
response = api.Get(map_query)



import overpy

api = overpy.Overpass()

# fetch all ways and nodes
result = api.query("""
    way(50.746,7.154,50.748,7.157) ["highway"];
    (._;>;);
    out body;
    """)

result = api.query("""
    way(-37.1384, 174.0591, -36.5758, 175.4653) ["highway"];
    (._;>;);
    out body;
    """)

for way in result.ways:
    print("Name: %s" % way.tags.get("name", "n/a"))
    print("  Highway: %s" % way.tags.get("highway", "n/a"))
    print("  Nodes:")
    for node in way.nodes:
        print("    Lat: %f, Lon: %f" % (node.lat, node.lon))

