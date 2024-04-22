from utils.database import DataBase, UserType

database = DataBase()
database.open()

data = database.find_user_by_id(7079382841)
print(data.game)

database.execute("""UPDATE users SET game = 'football' WHERE user_id = 7079382841""")
database.commit()


# print(
#     database.find_user_by_id(7079382841)[DataBaseType.username]
# )
# database.register_user(
#     1, None, "😌", 0
# )

database.close()