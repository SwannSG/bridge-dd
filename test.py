import json
def bid_to_json(obj:'Bid', properties = ['bid', 'alert', 'comment']):
    r = {}
    for each in properties:
        r[each] = obj.each
    return json.dumps(r)