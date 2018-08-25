import random


def n_dead_members(snapinfo):
    n = 0
    for m in snapinfo:
        if not snapinfo[m]["alive"]:
            n += 1
    return n


def infinitysnap(members):
    user_ids = []
    snapture_info = {}
    base_status = {
        "alive":True,
        "member_obj":None
    }
    total_users = 0
    for m in members:
        if m.id != "480817419963858944":
            user_ids.append(m.id)
            snapture_info[m.id] = base_status.copy()
            snapture_info[m.id]["member_obj"] = m
            total_users += 1
    random.shuffle(user_ids)
    for m in user_ids:
        if n_dead_members(snapture_info) < total_users/2:
            snapture_info[m]["alive"] = False
    if random.random() > 0.5 and len(user_ids)%2 != 0:
        snapture_info[user_ids[0]]["alive"] = not snapture_info[user_ids[0]]["alive"]
    return snapture_info


def snapstring(userinfo):
    response = []
    deaths = 0
    total_users = len(userinfo)
    for m in userinfo:
        if not userinfo[m]["alive"]:
            response.append(userinfo[m]["member_obj"].display_name + " was killed.")
            deaths += 1
        else:
            response.append(userinfo[m]["member_obj"].display_name + " was spared.")
    response.append(str(deaths) + "/" + str(total_users) + " users were killed. The server is now balanced, as all things should be.")
    return response


def infinitysnaptest(usernames):
    response = "```"
    for u in usernames:
        if random.random() > 0.5:
            response += usernames[u] + " was killed.\n"
        else:
            response += usernames[u] + " was spared.\n"
    response += "```"
    return response