import random
import copy

def n_dead_members(snapinfo):
    n = 0
    for m in snapinfo:
        if not snapinfo[m]["alive"]:
            n += 1
    return n

def infinitysnap(members):
    users = []
    snapture_info = {}
    base_status = {
        "alive":True,
        "member_obj":None
    }
    total_users = 0
    for m in members:
        if not m.bot:
            users.append(m)
            snapture_info[m.id] = copy.copy(base_status)
            snapture_info[m.id]["member_obj"] = m
            total_users += 1
    random.shuffle(users)
    deaths = 0
    n = 0
    for m in users:
        if n_dead_members(snapture_info) < total_users/2:
            snapture_info[m.id]["alive"] = False
    if total_users%2 != 0:
        print("odd correction")
        snapture_info[random.choice(users).id]["alive"] = True
    response = []
    random.shuffle(users)
    for m in users:
        if not snapture_info[m.id]["alive"]:
            response.append(m.display_name + " was killed.")
            deaths += 1
        else:
            response.append(m.display_name + " was spared.")
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

if __name__ == "__main__":
    all_users = {
        "160481323746590731": "chloe",
        "190065758267637760": "zoey",
        "125424672765509632": "tenttle",
        "196422115212132353": "rory",
        "166068876008882176": "chris",
        "208122604161204224": "autumn",
        "140324228745396225": "bard",
        "262794787248144385": "shannon",
        "204439791675113473": "tosh",
        "195339166769217536": "kit"
    }

    print(infinitysnaptest(all_users))