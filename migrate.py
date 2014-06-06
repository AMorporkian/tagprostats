from db import *
with db_session:
    with open('ids.txt', 'w') as f:
        f.write('\n'.join(select(x.profile_string for x in Player)))
